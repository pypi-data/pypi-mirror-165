from jinja2 import Template
from continual.python.sdk.query import Query
import logging
from continual.rpc.management.v1 import management_types_pb2
from google.protobuf.json_format import MessageToDict
from continual.python.utils.utils import (
    split_name,
)

TypemapString = {
    "NUMBER": "float",
    "FIXED": "float",
    "REAL": "float",
    "TEXT": "text",
    "BOOLEAN": "boolean",
    "CATEGORICAL": "text",
    "NUMBER_LIST": "[] float",
    "TEXT_LIST": "[] text",
    "TIMESTAMP": "timestamptz",
}

"""
    left_id, left_ts - right_id, right_ts - Condition
    1    ✅      ✅        ✅         ❌         id join
        
    2    ⭐️      ⭐️        ❌         ❌         Invalid
        
    3    ✅      ✅        ❌         ✅         ts join
        
    4    ✅      ✅        ✅         ✅         id and ts join
        
    5    ✅      ❌        ❌         ✅         Invalid
        
    6    ✅      ❌        ✅         ✅         id join
        
    7    ❌      ✅        ✅         ❌         Invalid
        
    8    ❌      ✅        ❌         ✅         ts join
        
    9    ❌      ✅        ✅         ✅         Invalid
        
    10   ❌      ❌        ⭐️         ⭐️         Invalid

    11   ✅      ❌        ✅         ❌         id join
"""
join_decision_dict = {
    (True, True, True, False): "ID",  # 1
    (True, True, False, True): "TS",  # 3
    (True, True, True, True): "IDTS",  # 5
    (True, False, True, True): "ID",  # 6
    (False, True, False, True): "TS",  # 8
    (True, False, True, False): "ID",  # 11
}

# NOTE: changed "<=" tp "=" for opalai temporary workaround
qtemplate = Template(
    """
    {% if params.SubEntity %} LEFT JOIN {% endif %}
    (SELECT {% for fname in params.FeatureNames %} {% if loop.index > 1 %},{% endif %}{{ fname }} as "{{ params.FeatureNames[fname]['qualified'] }}" {% endfor %}
            , {% if params.Latest and params.TsName and params.PkName %} rank() over (partition by  {{params.PkName}} ORDER BY {{params.TsName}} DESC) as "{{params.TableAlias}}.timerank" 
            {% else %}
             1 as "{{params.TableAlias}}.timerank"
            {% endif %}
        FROM {{ params.EntityTable}}
                {% if params.FilterList %} WHERE {% for filter in params.FilterList %} {% if filter != params.FilterList[loop.index0] %} AND {% endif %} {{ filter}} {% endfor %} {% endif %}
        {% if params.OrderByClause %} ORDER BY {{ params.OrderByClause }} {% endif %}) AS "{{ params.TableAlias }}"
        {% if params.SubEntity %} ON {% if params.IDJoin %} "{{ params.IDJoin[0] }}" = "{{ params.IDJoin[1] }}" {% endif %} {% if params.TSJoin %} {% if params.IDJoin %} AND {% endif %}"{{ params.TSJoin[0] }}" = ({{ params.TSJoin[1] }} {% endif %} ){% endif %} 
        """
)

qtemplate_no_ranking = Template(
    """
    {% if params.SubEntity %} LEFT JOIN {% endif %}
    (SELECT {% for fname in params.FeatureNames %} {% if loop.index > 1 %},{% endif %}{{ fname }} as "{{ params.FeatureNames[fname]['qualified'] }}" {% endfor %}
        FROM {{ params.EntityTable}}
                {% if params.FilterList %} WHERE {% for filter in params.FilterList %} {% if filter != params.FilterList[loop.index0] %} AND {% endif %} {{ filter}} {% endfor %} {% endif %}
        {% if params.OrderByClause %} ORDER BY {{ params.OrderByClause }} {% endif %}) AS "{{ params.TableAlias }}"
        {% if params.SubEntity %} ON {% if params.IDJoin %} "{{ params.IDJoin[0] }}" = "{{ params.IDJoin[1] }}" {% endif %} {% endif %} 
        """
)

qtemplate_mssql = Template(
    """
    {% if params.SubEntity %} LEFT JOIN {% endif %}
    (SELECT {% for fname in params.FeatureNames %} {% if loop.index > 1 %},{% endif %} [{{ params.FeatureNames[fname]['column_name'] }}] as "{{ params.FeatureNames[fname]['qualified'] }}" {% endfor %}
            , {% if params.Latest and params.TsName %}rank() over (partition by  {{params.PkName}} ORDER BY {{params.TsName}} DESC) as "{{params.Entity}}.timerank" 
            {% else %}
             1 as "{{params.Entity}}.timerank"
            {% endif %}
        FROM {{ params.EntityTable}}
                {% if params.FilterList %} WHERE {% for filter in params.FilterList %} {% if filter != params.FilterList[loop.index0] %} AND {% endif %} {{ filter}} {% endfor %} {% endif %}
        ) AS {{ params.TableAlias }}
        {% if params.SubEntity %} ON [{{params.MatchId}}] = [{{params.MatchRHS}}] {% if params.RootVisibilityTime and params.TsName %} AND [{{params.QualifiedTs}}] <= [{{params.RootVisibilityTime}}] {% endif %} {% endif %} 
        """
)

qtemplate_mssql_no_ranking = Template(
    """
    {% if params.SubEntity %} LEFT JOIN {% endif %}
    (SELECT {% for fname in params.FeatureNames %} {% if loop.index > 1 %},{% endif %} [{{ params.FeatureNames[fname]['column_name'] }}] as "{{ params.FeatureNames[fname]['qualified'] }}" {% endfor %}
        FROM {{ params.EntityTable}}
                {% if params.FilterList %} WHERE {% for filter in params.FilterList %} {% if filter != params.FilterList[loop.index0] %} AND {% endif %} {{ filter}} {% endfor %} {% endif %}
        ) AS {{ params.TableAlias }}
        {% if params.SubEntity %} ON [{{params.MatchId}}] = [{{params.MatchRHS}}] {% endif %} 
        """
)

ranktemplate = Template(
    """
    SELECT *
    FROM (SELECT *,
          rank() over (partition by "{{params.PkName}}" {% if not params.Latest and params.TsName %} , "{{params.TsName}}" {% endif %} ORDER BY "{{params.TableAlias}}.timerank" ASC
            {% for subentity in params.SubEntities %} , "{{subentity}}.timerank" ASC {% endfor %}) AS finalrank
          FROM {{params.EntityQuery}}) AS final
    WHERE finalrank = 1
    ORDER BY "{{params.PkName}}" ASC
    {% if params.Limit %} LIMIT {{params.Limit}} {% endif %}
    """
)

ranktemplate_norank = Template(
    """
    SELECT * FROM {{params.EntityQuery}}
    ORDER BY "{{params.PkName}}" ASC
    {% if params.Limit %} LIMIT {{params.Limit}} {% endif %}
    """
)

ranktemplate_mssql = Template(
    """
    SELECT *
    FROM (SELECT *,
          rank() over (partition by [{{params.PkName}}] {% if not params.Latest and params.TsName %} , [{{params.Entity}}:{{params.TsName}}] {% endif %} ORDER BY [{{params.TableAlias}}.timerank] ASC
            {% for subentity in params.SubEntities %} , [{{subentity}}.timerank] ASC {% endfor %}) AS finalrank
          FROM {{params.EntityQuery}}) AS final
    WHERE finalrank = 1
    {% if params.Limit %} LIMIT {{params.Limit}} {% endif %}
    """
)

ranktemplate_mssql_norank = Template(
    """
    SELECT * FROM {{params.EntityQuery}}
    {% if params.Limit %} LIMIT {{params.Limit}} {% endif %}
    """
)

timestamp_template = Template(
    """
    SELECT max({{params.EntityTable}}.{{params.TsName}}) 
    FROM {{params.EntityTable}}
    WHERE {{params.EntityTable}}.{{params.PkName}}="{{params.RootEntityID}}" and {{params.EntityTable}}.{{params.TsName}}<= "{{params.RootVisibilityTime}}"
"""
)

stats_template_snowflake = Template(
    """
 {% for elem in params.AllFeatures %} {% if loop.index > 1 %} UNION {% endif %}
	SELECT {% if elem.Alias %} '{{elem.Alias}}' {% else %} '{{elem.name}}' {% endif %}as "column_name",
{% if (elem.type == "NUMBER" or elem.type == "REAL" or elem.type == "FIXED") %}
	COALESCE(max(allentities.{{elem.name}}), 0.0) as "max", COALESCE(min(allentities.{{elem.name}}), 0.0) as "min",
	COALESCE(avg(allentities.{{elem.name}}), 0.0) as "mean", COALESCE(stddev_pop(TO_DOUBLE(allentities.{{elem.name}})), 0.0) as "sd",
	0 as "min_length", 0 as "max_length", 0 as "distinct_values", NULL::timestamp  as "latest", NULL::timestamp  as "earliest",
{% elif (elem.type == "TIMESTAMP" or elem.type == "TIMESTAMP_LTZ" or elem.type == "TIMESTAMP_TZ" or elem.type == "TIMESTAMP_NTZ" or elem.type == "DATE") %}
	0.0 as "max", 0.0 as "min", 0.0 as "mean", 0.0 as "sd", 0 as "min_length", 0 as "max_length", 0 as "distinct_values", 
    max(allentities.{{elem.name}})::timestamp as "latest", min(allentities.{{elem.name}})::timestamp as "earliest",
{% elif elem.type == "TEXT" %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd", COALESCE(min(length(allentities.{{elem.name}})), 0) as "min_length",
	COALESCE(max(length(allentities.{{elem.name}})), 0) as "max_length", COALESCE(count(distinct(allentities.{{elem.name}})), 0) as "distinct_values",
	NULL::timestamp  as "latest", NULL::timestamp  as "earliest",
{% elif elem.type == "CATEGORICAL" %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd",
	COALESCE(min(length(allentities.{{elem.name}})), 0) as "min_length", COALESCE(max(length(allentities.{{elem.name}})), 0) as "max_length",
	COALESCE(count(distinct(allentities.{{elem.name}})), 0) as "distinct_values", NULL::timestamp  as "latest",
	NULL::timestamp  as "earliest",
{% elif elem.type == "BOOLEAN" %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd", 0 as "min_length", 0 as "max_length",
	COALESCE(count(distinct(allentities.{{elem.name}})), 0) as "distinct_values", NULL::timestamp  as "latest", NULL::timestamp  as "earliest",
{% else %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd", 0 as "min_length", 0 as "max_length", 0 as "distinct_values",
	NULL::timestamp  as "latest", NULL::timestamp  as "earliest",{% endif %}
	count(*) - count(allentities.{{elem.name}})  as "null_count",
	count(allentities.{{elem.name}}) as "count",
	CURRENT_TIMESTAMP as "computed_at", '{{elem.ctype}}' as "type"
    FROM  {{params.FullName}} as allentities
	{% endfor %}
    """
)

stats_template = Template(
    """
 {% for elem in params.AllFeatures %} {% if loop.index > 1 %} UNION {% endif %}
	SELECT {% if elem.Alias %} '{{elem.Alias}}' {% else %} '{{elem.name}}' {% endif %}as "column_name",
{% if elem.type == "NUMBER" %}
	COALESCE(max(allentities.{{elem.name}}), 0.0) as "max", COALESCE(min(allentities.{{elem.name}}), 0.0) as "min",
	COALESCE(avg(allentities.{{elem.name}}), 0.0) as "mean", COALESCE(stddev_pop(allentities.{{elem.name}}), 0.0) as "sd",
	0 as "min_length", 0 as "max_length", 0 as "distinct_values", NULL::timestamp  as "latest", NULL::timestamp  as "earliest",
{% elif elem.type == "TIMESTAMP" %}
	0.0 as "max", 0.0 as "min", 0.0 as "mean", 0.0 as "sd", 0 as "min_length", 0 as "max_length", 0 as "distinct_values", 
    max(allentities.{{elem.name}})::timestamp as "latest", min(allentities.{{elem.name}})::timestamp as "earliest",
{% elif elem.type == "TEXT" %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd", COALESCE(min(length(allentities.{{elem.name}})), 0) as "min_length",
	COALESCE(max(length(allentities.{{elem.name}})), 0) as "max_length", COALESCE(count(distinct(allentities.{{elem.name}})), 0) as "distinct_values",
	NULL::timestamp  as "latest", NULL::timestamp  as "earliest",
{% elif elem.type == "CATEGORICAL" %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd",
	COALESCE(min(length(allentities.{{elem.name}})), 0) as "min_length", COALESCE(max(length(allentities.{{elem.name}})), 0) as "max_length",
	COALESCE(count(distinct(allentities.{{elem.name}})), 0) as "distinct_values", NULL::timestamp  as "latest",
	NULL::timestamp  as "earliest",
{% elif elem.type == "BOOLEAN" %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd", 0 as "min_length", 0 as "max_length",
	COALESCE(count(distinct(allentities.{{elem.name}})), 0) as "distinct_values", NULL::timestamp  as "latest", NULL::timestamp  as "earliest",
{% else %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd", 0 as "min_length", 0 as "max_length", 0 as "distinct_values",
	NULL::timestamp  as "latest", NULL::timestamp  as "earliest",{% endif %}
	count(*) - count(allentities.{{elem.name}})  as "null_count",
	count(allentities.{{elem.name}}) as "count",
	CURRENT_TIMESTAMP as "computed_at", '{{elem.ctype}}' as "type"
    FROM  {{params.FullName}} as allentities
	{% endfor %}
    """
)

stats_template_databricks = Template(
    """
 {% for elem in params.AllFeatures %} {% if loop.index > 1 %} UNION {% endif %}
	SELECT {% if elem.Alias %} '{{elem.Alias}}' {% else %} '{{elem.name}}' {% endif %}as column_name,
{% if elem.type == "NUMBER" %}
	COALESCE(max(allentities.{{elem.name}}), 0.0) as max, COALESCE(min(allentities.{{elem.name}}), 0.0) as min,
	COALESCE(avg(allentities.{{elem.name}}), 0.0) as mean, COALESCE(stddev_pop(allentities.{{elem.name}}), 0.0) as sd,
	0 as min_length, 0 as max_length, 0 as distinct_values, NULL::timestamp  as latest, NULL::timestamp  as earliest,
{% elif elem.type == "TIMESTAMP" %}
	0.0 as max, 0.0 as min, 0.0 as mean, 0.0 as sd, 0 as min_length, 0 as max_length, 0 as distinct_values, 
    max(allentities.{{elem.name}})::timestamp as latest, min(allentities.{{elem.name}})::timestamp as earliest,
{% elif elem.type == "TEXT" %}
	0 as max, 0 as min, 0.0 as mean, 0.0 as sd, COALESCE(min(length(allentities.{{elem.name}})), 0) as min_length,
	COALESCE(max(length(allentities.{{elem.name}})), 0) as max_length, COALESCE(count(distinct(allentities.{{elem.name}})), 0) as distinct_values,
	NULL::timestamp  as latest, NULL::timestamp  as earliest,
{% elif elem.type == "CATEGORICAL" %}
	0 as max, 0 as min, 0.0 as mean, 0.0 as sd,
	COALESCE(min(length(allentities.{{elem.name}})), 0) as min_length, COALESCE(max(length(allentities.{{elem.name}})), 0) as max_length,
	COALESCE(count(distinct(allentities.{{elem.name}})), 0) as distinct_values, NULL::timestamp  as latest,
	NULL::timestamp  as earliest,
{% elif elem.type == "BOOLEAN" %}
	0 as max, 0 as min, 0.0 as mean, 0.0 as sd, 0 as min_length, 0 as max_length,
	COALESCE(count(distinct(allentities.{{elem.name}})), 0) as distinct_values, NULL::timestamp  as latest, NULL::timestamp  as earliest,
{% else %}
	0 as max, 0 as min, 0.0 as mean, 0.0 as sd, 0 as min_length, 0 as max_length, 0 as distinct_values,
	NULL::timestamp  as latest, NULL::timestamp  as earliest,{% endif %}
	count(*) - count(allentities.{{elem.name}})  as null_count,
	count(allentities.{{elem.name}}) as count,
	CURRENT_TIMESTAMP as computed_at, '{{elem.ctype}}' as type
    FROM  {{params.FullName}} as allentities
	{% endfor %}
    """
)

stats_template_mssql = Template(
    """
 {% for elem in params.AllFeatures %} {% if loop.index > 1 %} UNION {% endif %}
	SELECT {% if elem.Alias %} '{{elem.Alias}}' {% else %} '{{elem.name}}' {% endif %}as "column_name",
{% if elem.type == "NUMBER" %}
	COALESCE(max([{{elem.name}}]), 0.0) as "max", COALESCE(min([{{elem.name}}]), 0.0) as "min",
	COALESCE(avg([{{elem.name}}]), 0.0) as "mean", COALESCE(stddev_pop([{{elem.name}}]), 0.0) as "sd",
	0 as "min_length", 0 as "max_length", 0 as "distinct_values", CAST(NULL as datetime)  as "latest", CAST(NULL as datetime)  as "earliest",
{% elif elem.type == "TIMESTAMP" %}
	0.0 as "max", 0.0 as "min", 0.0 as "mean", 0.0 as "sd", 0 as "min_length", 0 as "max_length", 0 as "distinct_values", 
    max([{{elem.name}}])::timestamp as "latest", min([{{elem.name}}])::timestamp as "earliest",
{% elif elem.type == "TEXT" %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd", COALESCE(min(length([{{elem.name}}])), 0) as "min_length",
	COALESCE(max(length([{{elem.name}}])), 0) as "max_length", COALESCE(count(distinct([{{elem.name}}])), 0) as "distinct_values",
	CAST(NULL as datetime)  as "latest", CAST(NULL as datetime)  as "earliest",
{% elif elem.type == "CATEGORICAL" %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd",
	COALESCE(min(length([{{elem.name}}])), 0) as "min_length", COALESCE(max(length([{{elem.name}}])), 0) as "max_length",
	COALESCE(count(distinct([{{elem.name}}])), 0) as "distinct_values", CAST(NULL as datetime)  as "latest",
	CAST(NULL as datetime)  as "earliest",
{% elif elem.type == "BOOLEAN" %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd", 0 as "min_length", 0 as "max_length",
	COALESCE(count(distinct([{{elem.name}}])), 0) as "distinct_values", CAST(NULL as datetime)  as "latest", CAST(NULL as datetime)  as "earliest",
{% else %}
	0 as "max", 0 as "min", 0.0 as "mean", 0.0 as "sd", 0 as "min_length", 0 as "max_length", 0 as "distinct_values",
	CAST(NULL as datetime)  as "latest",CAST(NULL as datetime)  as "earliest",{% endif %}
	count(*) - count([{{elem.name}}])  as "null_count",
	count([{{elem.name}}]) as "count",
	CURRENT_TIMESTAMP as "computed_at", '{{elem.ctype}}' as "type"
    FROM  {{params.FullName}} as allentities
	{% endfor %}
    """
)

serving_template_postgres = Template(
    """
    {% if params.SubEntity %} LEFT JOIN {% endif %}
    (SELECT
        {% for fname in params.FeatureNames %} {% if loop.index > 1 %},{% endif %}{{ fname }} as "{{ params.FeatureNames[fname]['qualified'] }}" {% endfor %}
        {% for oride in params.Overrides %} , CAST({{oride["data"]}} as {{oride["type"]}}) as "{{oride["qualified_name"]}}" {% endfor %}
        {% if params.Latest and params.TsName %}, rank() over (partition by {{params.PkName}} ORDER BY {{params.TsName}} DESC) as "{{params.Entity}}.timerank"
        {% else %}
        , 1 as  "{{params.Entity}}.timerank"
        {% endif %}
        FROM {{params.FullName}}
        {% if params.FilterList %} WHERE {% for filter in params.FilterList%} {% if loop.index > 1 %} AND {% endif %} {{filter}} {% endfor %} {% endif %}
        {% if params.OrderByClause %} ORDER BY {{params.OrderByClause}} {% endif %}) AS "{{params.Entity}}"
    {% if params.SubEntity %} ON "{{params.MatchId}}" = "{{params.MatchRHS}}" {% endif %}
"""
)

serving_template_mssql = Template(
    """
    {% if params.SubEntity %} LEFT JOIN {% endif %}
    (SELECT
        {% for fname in params.FeatureNames %} {% if loop.index > 1 %},{% endif %} [{{ params.FeatureNames[fname]['column_name'] }}] as "{{ params.FeatureNames[fname]['qualified'] }}" {% endfor %}
        {% for oride in params.Overrides %} , CAST({{oride["data"]}} as {{oride["type"]}}) as "{{oride["qualified_name"]}}" {% endfor %}
        {% if params.Latest and params.TsName %}, rank() over (partition by {{params.PkName}} ORDER BY {{params.TsName}} DESC) as "{{params.Entity}}.timerank"
        {% else %}
        , 1 as  "{{params.Entity}}.timerank"
        {% endif %}
        FROM {{params.FullName}}
        {% if params.FilterList %} WHERE {% for filter in params.FilterList%} {% if loop.index > 1 %} AND {% endif %} {{filter}} {% endfor %} {% endif %}
        ) AS {{params.Entity}}
    {% if params.SubEntity %} ON [{{params.MatchId}}] = [{{params.MatchRHS}}] {% endif %}
"""
)

serving_template_noid_postgres = Template(
    """
    {% if params.SubEntity %} LEFT JOIN {% endif %}
    (SELECT
    {% for oride in params.Overrides %} CAST({{oride["data"]}} as {{oride["type"]}}) as "{{oride["qualified_name"]}}", {% endfor %}
    1 as "{{params.Entity}}.timerank"
    ) AS "{{params.Entity}}" {% if params.SubEntity %} ON TRUE {% endif %}
"""
)

serving_template_noid_mssql = Template(
    """
    {% if params.SubEntity %} LEFT JOIN {% endif %}
    (SELECT
    {% for oride in params.Overrides %} CAST({{oride["data"]}} as {{oride["type"]}}) as "{{oride["qualified_name"]}}", {% endfor %}
    1 as "{{params.Entity}}.timerank"
    ) AS {{params.Entity}} {% if params.SubEntity %} ON 1=1 {% endif %}
"""
)
serving_rank_template_postgres = Template(
    """
    SELECT *
        FROM (SELECT *,
            rank() over (partition by {% if params.IDPresent %} "{{params.PkName}}" {% else %} "{{params.Entity}}.timerank" {% endif %} ORDER BY "{{params.Entity}}.timerank" ASC
                {% for subentity in params.SubEntities %} , "{{subentity}}.timerank" ASC  {% endfor %}) AS finalrank
            FROM {{params.EntityQuery}}) AS final
        WHERE finalrank = 1 {% for idfield in params.IDList %} AND "{{idfield}}" IS NOT NULL {% endfor %}
        {% if params.IDPresent %} ORDER BY "{{params.PkName}}" ASC {% endif %}
"""
)

serving_rank_template_mssql = Template(
    """
    SELECT *
        FROM (SELECT *,
            rank() over (partition by {% if params.IDPresent %} "{{params.PkName}}" {% else %} "{{params.Entity}}.timerank" {% endif %} ORDER BY [{{params.Entity}}.timerank] ASC
                {% for subentity in params.SubEntities %} , "{{subentity}}.timerank" ASC  {% endfor %}) AS finalrank
            FROM {{params.EntityQuery}}) AS final
        WHERE finalrank = 1 {% for idfield in params.IDList %} AND [{{idfield}}] IS NOT NULL {% endfor %}
"""
)

incremental_prediction_template = Template(
    """
    SELECT * from (
    SELECT A.*
    FROM ({{params.TrainingQuery}}) as A
    LEFT JOIN
    ( 
        SELECT id, count(*) pred_count
        from {{params.DbSchema}}.model_{{params.Entity}}_{{params.ModelID}}_preds
        GROUP BY id
    ) as B
    ON "{{params.Entity}}:{{params.PkName}}" = B.id
    WHERE pred_count is NULL
    ) as C
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


def create_time_subquery(table_name, pkName, match_id, tsName, root_ts_name):
    params = {
        "EntityTable": table_name,
        "TsName": tsName,
        "PkName": pkName,
        "RootEntityID": match_id,
        "RootVisibilityTime": root_ts_name,
    }
    return timestamp_template.render(params=params)


def create_serving_query(
    query,
    sub_query,
    feature_store,
    match_id=None,
    root_entity_name=None,
    root_ts_name=None,
    start_time=None,
    end_time=None,
    limit=None,
    parent_id_found=False,
):

    """
    Stage 1 for the join queries for all the relations from the spine
    """
    if isinstance(query, Query):
        qdict = query.to_dict()
    elif isinstance(query, management_types_pb2.Query):
        qdict = MessageToDict(query, preserving_proto_field_name=True)
    else:
        qdict = query

    _, table_name = feature_store.get_data_table_name(qdict["name"])

    full_name = qdict.get("table_name", None)
    if full_name is None:
        full_name = feature_store.db_schema + "." + table_name

    entity_name, name_map = split_name(qdict["name"])

    idvalue = None
    id_present = False
    filters = []
    pkName, qualified_pk = get_index(qdict)
    tsName, qualified_ts = get_time_index_field(qdict)

    # If this object is a Model and not a featureset, then
    # the column names are not qualified.
    if "models" in name_map:
        qualified_pk = pkName
        qualified_ts = tsName

    sub_entity_names = []
    id_field_list = []

    params = {
        "Entity": entity_name,
        "EntityTable": full_name,
        "Overrides": [],
        "FeatureNames": {},
        "SubEntity": sub_query,
        "PkName": pkName,
        "TsName": tsName,
        "QualifiedTsName": qualified_ts,
        "FullName": full_name,
    }

    logging.debug(qdict["fields"])
    join_query = ""
    for field in qdict["fields"]:
        if "type" in field and field["type"].upper() == "INDEX":
            id_present = True
            if "value" in field:
                idvalue = field["value"]
                if isinstance(idvalue, str):
                    idvalue = "'{}'".format(idvalue)
                if not sub_query:
                    filters.append("{} = {}".format(pkName, idvalue))
                    field_name = table_name + "." + field["name"]
                    params["FeatureNames"][field_name] = {
                        "qualified": field["qualified_name"],
                        "column_name": field["name"],
                    }
                    continue

        if "value" in field and field["value"] is not None:
            value = field["value"]
            if isinstance(value, str):
                value = "'{}'".format(value)

            type_to_use = field["dtype"]
            if field["dtype"] in TypemapString:
                type_to_use = TypemapString[field["dtype"]]
            params["Overrides"].append(
                {
                    "data": value,
                    "qualified_name": field["qualified_name"],
                    "type": type_to_use,
                }
            )
        else:
            field_name = table_name + "." + field["name"]
            params["FeatureNames"][field_name] = {
                "qualified": field["qualified_name"],
                "column_name": field["name"],
            }

        if "relation" in field:
            # If we filed is found with value then the relations have parent id.
            # else if the current featureset ID is set then the parrent id is set.
            # or if any of the parents have id set, then this set parent_id_found.
            pif = (
                ("value" in field and field["value"] is not None)
                or parent_id_found
                or idvalue != None
            )

            sub_entity_query, sub_entity_n, id_flist = create_serving_query(
                field["relation"],
                True,
                feature_store,
                root_entity_name=entity_name,
                root_ts_name=root_ts_name,
                match_id=field["qualified_name"],
                parent_id_found=pif,
            )
            join_query = join_query + sub_entity_query
            sub_entity_names.extend(sub_entity_n)
            id_field_list.extend(id_flist)

    if not sub_query:
        root_ts_name = qualified_ts
        match_id = qualified_pk
        params["OrderByClause"] = pkName

        if tsName and end_time is not None:
            filters.append("{} <= {}".format(tsName, end_time))

        if tsName and start_time is not None:
            filters.append("{} > {}".format(tsName, start_time))

    else:
        params["MatchId"] = match_id
        params["RootEntityName"] = root_entity_name
        params["RootVisibilityTime"] = root_ts_name
        params["MatchRHS"] = qualified_pk
        qualified_ts = root_ts_name

    if "related" in qdict:
        for sub_qdict in qdict["related"]:
            sub_entity_query, sub_entity_n, id_flist = create_serving_query(
                sub_qdict,
                True,
                feature_store,
                root_entity_name=entity_name,
                root_ts_name=root_ts_name,
                match_id=match_id,
                parent_id_found=(parent_id_found or idvalue != None),
            )
            join_query = join_query + sub_entity_query
            sub_entity_names.extend(sub_entity_n)
            id_field_list.extend(id_flist)

    params["FilterList"] = filters

    # Select template based on dialect.
    template = serving_template_postgres
    if feature_store.data_store.type == "sqlserver":
        template = serving_template_mssql

    if sub_query:
        if not parent_id_found and idvalue is None:
            logging.debug("Using no id template")
            template = serving_template_noid_postgres
            if feature_store.data_store.type == "sqlserver":
                template = serving_template_noid_mssql
    elif idvalue is None:
        logging.debug("Using no id template")
        template = serving_template_noid_postgres
        if feature_store.data_store.type == "sqlserver":
            template = serving_template_noid_mssql
    else:
        logging.debug("Using with id template")
        id_field_list.append(qualified_pk)

    ranktemp = serving_rank_template_postgres
    if feature_store.data_store.type == "sqlserver":
        ranktemp = serving_rank_template_mssql

    entity_query = template.render(params=params)
    entity_query = entity_query.strip() + "\n" + join_query

    """
    Stage 2: Create the rank query if this is the spine.
    """
    if not sub_query:
        params = {
            "IDPresent": (id_present and idvalue is not None),
            "EntityQuery": entity_query,
            "Entity": entity_name,
            "SubEntities": sub_entity_names,
            "PkName": pkName,
            "TsName": tsName,
            "IDList": id_field_list,
        }
        if limit is not None:
            params["Limit"] = limit
        entity_query = ranktemp.render(params=params)

    return entity_query, sub_entity_names, id_field_list


def create_query(
    query,
    sub_query,
    match_id=None,
    root_entity_name=None,
    root_ts_name=None,
    latest=True,
    all_instances=True,
    start_time=None,
    end_time=None,
    limit=None,
    feature_store=None,
    incremental_prediction=False,
    level=0,
):

    """
    Stage 1 for the join queries for all the relations from the spine
    """
    if isinstance(query, Query):
        qdict = query.to_dict()
    elif isinstance(query, management_types_pb2.Query):
        qdict = MessageToDict(query, preserving_proto_field_name=True)
    else:
        qdict = query

    level = level + 1
    _, table_name = feature_store.get_data_table_name(qdict["name"])

    full_name = qdict.get("table_name", None)
    if full_name is None:
        full_name = feature_store.db_schema + "." + table_name

    entity_name, name_map = split_name(qdict["name"])

    query_params = {}
    filters = []
    sub_entity_names = []
    pkName, qualified_pk = get_index(qdict)
    tsName, qualified_ts = get_time_index_field(qdict)

    table_alias = f"{entity_name}_{level}"
    # If this object is a Model and not a featureset, then
    # the column names are not qualified.
    if "models" in name_map:
        qualified_pk = pkName
        qualified_ts = tsName

    params = {
        "Entity": entity_name,
        "TableAlias": table_alias,
        "EntityTable": full_name,
        "FeatureNames": {},
        "SubEntity": sub_query,
        "AllInstances": all_instances,
        "Latest": latest,
        "PkName": pkName,
        "TsName": tsName,
        "QualifiedTsName": qualified_ts,
    }

    join_query = ""

    if not sub_query:
        root_ts_name = qualified_ts
        match_id = qualified_pk
        params["OrderByClause"] = pkName

        if tsName and end_time is not None:
            filters.append("{} <= {}".format(tsName, end_time))
            query_params["visibilitytimeend"] = end_time

        if tsName and start_time is not None:
            filters.append("{} > {}".format(tsName, start_time))
            query_params["visibilitytimestart"] = start_time

    else:
        sub_entity_names.append(table_alias)
        qualified_ts = root_ts_name

        time_sub_query = None
        if tsName and root_ts_name:
            time_sub_query = create_time_subquery(
                full_name, pkName, match_id, tsName, root_ts_name
            )

        des = join_decision_dict.get(
            (
                match_id is not None,
                root_ts_name is not None,
                qualified_pk is not None,
                time_sub_query is not None,
            ),
            "invalid",
        )
        if des == "ID":
            params["IDJoin"] = (match_id, qualified_pk)
        elif des == "TS":
            params["TSJoin"] = (root_ts_name, time_sub_query)
        elif des == "IDTS":
            params["IDJoin"] = (match_id, qualified_pk)
            params["TSJoin"] = (root_ts_name, time_sub_query)
        else:
            raise Exception("Invalid Join")

    if "related" in qdict:
        for sub_qdict in qdict["related"]:

            (sub_entity_query, sub_q_params, sub_entity_n,) = create_query(
                sub_qdict,
                True,
                root_entity_name=entity_name,
                root_ts_name=root_ts_name,
                match_id=match_id,
                latest=latest,
                all_instances=all_instances,
                feature_store=feature_store,
                level=level,
            )
            join_query = join_query + sub_entity_query
            query_params.update(sub_q_params)
            sub_entity_names.extend(sub_entity_n)

    # Set the root_ts_name param so the related featureset query
    # can get them.
    # if not sub_query:
    #    root_ts_name = tsName

    model_id = None
    for field in qdict["fields"]:
        field_name = full_name + "." + field["name"]
        params["FeatureNames"][field_name] = {
            "qualified": field["qualified_name"],
            "column_name": field["name"],
        }
        if "model" in field:
            if not all_instances:
                filters.append(field["name"] + " is NOT NULL")

            model_id = field["name"]

        if "relation" in field:
            (sub_entity_query, sub_q_params, sub_entity_n,) = create_query(
                field["relation"],
                True,
                root_entity_name=entity_name,
                root_ts_name=root_ts_name,
                match_id=field["qualified_name"],
                latest=latest,
                all_instances=all_instances,
                feature_store=feature_store,
                level=level,
            )
            join_query = join_query + sub_entity_query
            query_params.update(sub_q_params)
            sub_entity_names.extend(sub_entity_n)

    params["FilterList"] = filters

    # Select template based on dialect.
    template = None
    ranktemp = None
    if (
        feature_store is not None
        and feature_store.data_store is not None
        and feature_store.data_store.type == "sqlserver"
    ):
        if root_ts_name == None:
            template = qtemplate_mssql_no_ranking
            ranktemp = ranktemplate_mssql_norank
        else:
            template = qtemplate_mssql
            ranktemp = ranktemplate_mssql
    else:
        if root_ts_name == None:
            template = qtemplate_no_ranking
            ranktemp = ranktemplate_norank
        else:
            template = qtemplate
            ranktemp = ranktemplate

    entity_query = template.render(params=params)
    entity_query = entity_query.strip() + "\n" + join_query

    """
	Stage 2: Create the rank query if this is the spine.
	"""
    if not sub_query:
        params = {
            "EntityQuery": entity_query,
            "Entity": entity_name,
            "TableAlias": table_alias,
            "Latest": latest,
            "SubEntities": sub_entity_names,
            "PkName": pkName,
            "TsName": tsName,
        }
        if limit is not None:
            params["Limit"] = limit
            query_params["limit"] = limit
        entity_query = ranktemp.render(params=params)

        if incremental_prediction:
            params = {
                "TrainingQuery": entity_query,
                "ModelID": model_id,
                "Entity": entity_name,
                "PkName": pkName,
                "DbSchema": feature_store.db_schema,
            }
            entity_query = incremental_prediction_template.render(params=params)

    return entity_query, query_params, sub_entity_names
