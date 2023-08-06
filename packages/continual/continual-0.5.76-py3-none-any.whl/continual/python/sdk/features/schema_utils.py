from continual.rpc.management.v1 import management_types_pb2
import yaml


def get_type_enum(typename):
    if typename is None:
        return None

    return management_types_pb2._FIELDTYPE.values_by_name[typename.upper()].number


def load_schemas(file_name):

    sc = None
    schema_text = None
    with open(file_name, "r") as inp_file:
        schema_text = inp_file.read()

    with open(file_name, "r") as inp_file:
        sc = yaml.load(inp_file, Loader=yaml.FullLoader)
        # full_name = "projects/" + project + '/featureSets/' + sc['name'] + "@1"

    if sc is None or "type" not in sc:
        return None

    if sc["type"] == "FeatureSet":
        schema = management_types_pb2.FeatureSetSchema(
            type=sc["type"],
            name=sc["name"],
            entity=sc["entity"],
            table=sc.get("table", None),
            description=sc.get("description", None),
            url=sc.get("url", None),
            owners=sc.get("owners", None),
            documentation=sc.get("documentation", None),
            query=sc.get("query", None),
            exclude_columns=sc.get("exclude_columns", None),
            columns=[],
        )
    elif sc["type"] == "Model":
        schema = management_types_pb2.ModelSchema(
            type=sc["type"],
            name=sc["name"],
            table=sc.get("table", None),
            description=sc.get("description", None),
            url=sc.get("url", None),
            owners=sc.get("owners", None),
            documentation=sc.get("documentation", None),
            query=sc.get("query", None),
            exclude_columns=sc.get("exclude_columns", None),
            columns=[],
            target=sc.get("target", None),
        )

        if "train" in sc:
            if "schedule" in sc["train"]:
                schema.train.schedule = sc["train"]["schedule"]
            if "metric" in sc["train"]:
                schema.train.metric = sc["train"]["metric"]
            if "optimization" in sc["train"]:
                schema.train.optimization = sc["train"]["optimization"]
            if "advanced" in sc["train"]:
                schema.train.advanced = sc["train"]["advanced"]

        if "promote" in sc and "policy" in sc["promote"]:
            schema.promote.policy = sc["promote"]["policy"]

        if "predict" in sc:
            if "schedule" in sc["predict"]:
                schema.predict.schedule = sc["predict"]["schedule"]
            if "incremental" in sc["predict"]:
                schema.predict.incrememtal = sc["predict"]["incremental"]

    else:
        raise Exception("Unknow schema type " + sc["type"])

    if "columns" in sc:
        column_configs = []
        columns = sc["columns"]
        for entry in columns:
            mc = management_types_pb2.ColumnConfig(
                name=entry["name"].lower(),
                description=entry.get("description", None),
                type=get_type_enum(entry.get("type", None)),
                entity=entry.get("entity", None),
            )
            column_configs.append(mc)
        schema.columns.extend(column_configs)

    return schema, schema_text
