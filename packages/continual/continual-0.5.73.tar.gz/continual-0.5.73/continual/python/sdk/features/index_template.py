from jinja2 import Template
from continual.python.sdk.query import Query
from continual.rpc.management.v1 import management_types_pb2
from google.protobuf.json_format import MessageToDict
import logging

time_index_template = Template(
    """(select {% if params.time_index %} max({{ params.time_index }}) from {{ params.table_name }} as {{ params.table_alias }} 
                      where {{ params.table_alias }}.{{ params.index }} = {{ params.model_alias }}.{{ params.match_index}}
                          {% if params.match_time_index %} and {{ params.table_alias }}.{{params.time_index}} <= {{ params.model_alias }}.{{params.match_time_index}} {% endif %} {% else %} {{params.match_time_index}} {% endif %}
                      ) as {{ params.qualified_time_index }} """
)

databricks_time_index_max_template = Template(
    """{% if params.time_index %} max({{ params.table_alias }}.{{params.match_time_index}}) as {{ params.qualified_time_index }} {% endif %}
    """
)
databricks_time_index_template = Template(
    """{% if params.time_index %} left join {{ params.table_name }} as {{ params.table_alias }} 
                on {{ params.table_alias }}.{{ params.match_index }} = {{ params.model_alias }}.{{ params.index }}
                and {{ params.table_alias }}.{{ params.match_time_index }} <= {{ params.model_alias }}.{{ params.time_index }}  {% endif %}
            """
)

train_template = Template(
    """
    {{ params.index_query }} SELECT time_index.* {% for fname in params.select_list %},{{ fname }} as {{params.select_list[fname]}} {% endfor %}
    FROM  time_index {% for fname in params.join_list %} LEFT JOIN {{fname}} AS {{params.join_list[fname][0]}} ON {{params.join_list[fname][1]}} {% endfor %}
    {% if params.filter_list %} WHERE {% for filter in params.filter_list %} {% if filter != params.filter_list[loop.index0] %} AND {% endif %} {{ filter}} {% endfor %} {% endif %}
    """
)

non_time_train_template = Template(
    """
    SELECT {% for fname in params.select_list %} {% if loop.index > 1 %},{% endif %} {{ fname }} as {{params.select_list[fname]}} {% endfor %}
    FROM   {% for fname in params.join_list %} {% if loop.index > 1 %} LEFT JOIN {% endif %}  {{fname}} AS {{params.join_list[fname][0]}} {% endfor %}
    {% if params.filter_list %} WHERE {% for filter in params.filter_list %} {% if filter != params.filter_list[loop.index0] %} AND {% endif %} {{ filter}} {% endfor %} {% endif %}
    """
)


def get_index(qdict):
    for field in qdict["fields"]:
        if ("type" in field and field["type"] == "INDEX") or (
            "index" in field and field["index"]
        ):
            return field["name"], field["qualified_name"]
    return None, None


def get_time_index_field(qdict):
    for field in qdict["fields"]:
        if ("type" in field and field["type"] == "TIME_INDEX") or (
            "time_index" in field and field["time_index"]
        ):
            return field["name"], field["qualified_name"]
    return None, None


def render_index_query(
    qdict,
    match_index,
    match_time_index,
    feature_store,
    table_alias="t1",
    column_alias_map=None,
    model_name=None,
    model_alias="t",
):
    project_id, table_name = feature_store.get_data_table_name(qdict["name"])
    full_name = qdict.get("table_name", None)
    if full_name is None:
        full_name = feature_store.db_schema + "." + table_name

    rel_index, rel_qualified_index = get_index(qdict)
    rel_time_index, rel_qualified_time_index = get_time_index_field(qdict)
    if rel_qualified_time_index is not None:
        ts_alias_name = rel_qualified_time_index.replace(":", "_")
        ts_alias_name = ts_alias_name.replace("$", "_")

    else:
        ts_alias_name = rel_qualified_time_index
    column_alias_map[ts_alias_name] = rel_qualified_time_index

    params = {
        "db_schema": feature_store.db_schema,
        "table_name": full_name,
        "index": rel_index,
        "time_index": rel_time_index,
        "match_index": match_index,
        "qualified_time_index": ts_alias_name,
        "match_time_index": match_time_index,
        "table_alias": table_alias,
        "model_alias": model_alias,
    }

    if feature_store.get_type() == "databricks":
        params["model_name"] = model_name or ""
        return (
            databricks_time_index_template.render(params=params),
            databricks_time_index_max_template.render(params=params),
        )
    else:
        return time_index_template.render(params=params), ""


def create_entity_timeindex_query(
    qdict,
    feature_store,
    column_alias_map=None,
):
    all_queries = []
    max_queries = []
    model_alias = "t"
    table_alias_count = 1
    _, table_name = feature_store.get_data_table_name(qdict["name"])
    full_name = qdict.get("table_name", None)
    if full_name is None:
        full_name = feature_store.db_schema + "." + table_name

    index, qualified_index = get_index(qdict)
    time_index, qualified_time_index = get_time_index_field(qdict)

    if time_index is None:
        time_index = "current_timestamp"
        qualified_time_index = "continual__time_index"

    for f in qdict["fields"]:
        if "relation" in f:
            relation = f["relation"]
            rel_time_index, _ = get_time_index_field(relation)
            if rel_time_index is not None:
                table_alias_count += 1
                index_query, max_query = render_index_query(
                    relation,
                    f["qualified_name"],
                    qualified_time_index,
                    feature_store,
                    column_alias_map=column_alias_map,
                    model_name=full_name,
                    table_alias=f"t{table_alias_count}",
                    model_alias=model_alias,
                )
                all_queries.append(index_query)
                if max_query != "":
                    max_queries.append(max_query)

            if "related" in relation:
                for related in relation["related"]:
                    rel_time_index, _ = get_time_index_field(related)
                    if rel_time_index is not None:
                        table_alias_count += 1
                        index_query, max_query = render_index_query(
                            related,
                            f["qualified_name"],
                            qualified_time_index,
                            feature_store,
                            column_alias_map=column_alias_map,
                            model_name=full_name,
                            table_alias=f"t{table_alias_count}",
                            model_alias=model_alias,
                        )
                        all_queries.append(index_query)
                        if max_query != "":
                            max_queries.append(max_query)

    if "related" in qdict:
        for related in qdict["related"]:
            rel_time_index, _ = get_time_index_field(related)
            if rel_time_index is not None:
                table_alias_count += 1
                index_query, max_query = render_index_query(
                    related,
                    qualified_index,
                    qualified_time_index,
                    feature_store,
                    column_alias_map=column_alias_map,
                    model_name=full_name,
                    table_alias=f"t{table_alias_count}",
                    model_alias=model_alias,
                )
                all_queries.append(index_query)
                if max_query != "":
                    max_queries.append(max_query)

    subquery_text = None
    maxquery_text = None
    if len(all_queries) > 0:
        if feature_store.get_type() == "databricks":
            subquery_text = " ".join(all_queries)
        else:
            subquery_text = ",".join(all_queries)

    if len(max_queries) > 0:
        maxquery_text = ",".join(max_queries)

    time_index_query = "WITH time_index AS "

    if feature_store.get_type() == "databricks":
        logging.info("subquery text: {}".format(subquery_text))
        logging.info("maxquery text: {}".format(maxquery_text))
        if subquery_text is not None:
            time_index_query += f"(SELECT {model_alias}.{index} as {qualified_index}, {model_alias}.{time_index} as {qualified_time_index}, {maxquery_text} FROM {full_name} as {model_alias} {subquery_text} group by {model_alias}.{index}, {model_alias}.{time_index})"
        else:
            time_index_query += f"(SELECT {index} as {qualified_index}, {time_index} as {qualified_time_index} FROM {full_name} as {model_alias})"
    else:
        if subquery_text is not None:
            time_index_query += f"(SELECT {index} as {qualified_index}, {time_index} as {qualified_time_index}, {subquery_text} FROM {full_name} as {model_alias})"
        else:
            time_index_query += f"(SELECT {index} as {qualified_index}, {time_index} as {qualified_time_index} FROM {full_name} as {model_alias})"

    return time_index_query


def create_select_list(
    qdict,
    match_index,
    alias_index,
    join_conditions,
    select_list,
    column_alias_map,
    feature_store,
    spine=False,
):
    project_id, table_name = feature_store.get_data_table_name(qdict["name"])
    index, qualified_index = get_index(qdict)
    time_index, qualified_time_index = get_time_index_field(qdict)

    if qualified_time_index is not None:
        qualified_time_index = qualified_time_index.replace(":", "_")
        qualified_time_index = qualified_time_index.replace("$", "_")

    fullname = qdict.get("table_name", None)
    if fullname is None:
        fullname = f"{feature_store.db_schema}.{table_name}"
    table_alias = f"t{alias_index}"

    join_condition = f"{match_index} = {table_alias}.{index}"
    if time_index is not None:

        join_condition += (
            f""" AND time_index.{qualified_time_index} = {table_alias}.{time_index} """
        )

    for f in qdict["fields"]:
        if spine and f["name"] == index:
            continue

        if f["name"] == time_index:
            continue
        col_name = f"t{alias_index}.{f['name']}"
        q_name = f["qualified_name"]
        alias_name = q_name
        if ":" in alias_name:
            alias_name = alias_name.replace(":", "_")
            alias_name = alias_name.replace("$", "_")

        select_list[col_name] = alias_name
        column_alias_map[alias_name] = q_name

    join_conditions[fullname] = (table_alias, join_condition)
    return


def create_training_query(
    query,
    feature_store,
    all_instances=False,
):
    logging.info("In Create training query")
    if isinstance(query, Query):
        qdict = query.to_dict()
    elif isinstance(query, management_types_pb2.Query):
        qdict = MessageToDict(query, preserving_proto_field_name=True)
    else:
        qdict = query

    # Columns are aliased because continual full qualified names are line fs1:feature1$fs2:feature2
    # This is not very database friendly. Hence we replace $ and : with _ and keep a mapping here.
    # This mapping is used to replaced the names in the return data.
    column_alias_map = {}

    join_conditions = {}
    select_list = {}
    filters = []

    time_index_query = create_entity_timeindex_query(
        qdict, feature_store=feature_store, column_alias_map=column_alias_map
    )
    index, _ = get_index(qdict)

    logging.info(f"time_index query: {time_index_query}")
    spine_alias_index = 1
    alias_index = 1

    create_select_list(
        qdict,
        f"time_index.{index}",
        alias_index,
        join_conditions,
        select_list,
        column_alias_map,
        feature_store,
        spine=True,
    )

    if "related" in qdict:
        for related in qdict["related"]:
            alias_index += 1
            create_select_list(
                related,
                f"time_index.{index}",
                alias_index,
                join_conditions,
                select_list,
                column_alias_map,
                feature_store,
                spine=True,
            )

    for f in qdict["fields"]:
        if "model" in f:
            if not all_instances:
                filters.append("t1." + f["name"] + " is NOT NULL")
            continue

        if "relation" not in f:
            continue

        relation = f["relation"]

        match_index = f"t{spine_alias_index}.{f['name']}"

        alias_index += 1
        create_select_list(
            relation,
            match_index,
            alias_index,
            join_conditions,
            select_list,
            column_alias_map,
            feature_store,
        )

        if "related" in relation:
            for related in relation["related"]:
                alias_index += 1
                create_select_list(
                    related,
                    match_index,
                    alias_index,
                    join_conditions,
                    select_list,
                    column_alias_map,
                    feature_store,
                    spine=True,
                )

    params = {
        "index_query": time_index_query,
        "select_list": select_list,
        "join_list": join_conditions,
        "filter_list": filters,
    }

    final_query = ""
    if time_index_query is None:
        final_query = non_time_train_template.render(params=params)
    else:
        final_query = train_template.render(params=params)
    logging.info(final_query)
    return final_query, column_alias_map
