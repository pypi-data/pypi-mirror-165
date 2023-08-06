from jinja2 import Template


model_prediction_classification_template = Template(
    """
        CREATE OR REPLACE VIEW {{params.DbSchema}}.{{params.ModelView}} AS
        SELECT entity_table.*, C.{{ params.TargetName}}_prediction, C.{{ params.TargetName}}_prediction_score, C.{{ params.TargetName}}_prediction_details from {{ params.ModelDataView}} AS entity_table
        LEFT JOIN
        (SELECT B.{{params.IndexColumn}}, {% if params.TimestampColumn %} B.{{params.TimestampColumn}}, {% endif %} B.{{ params.TargetName}}_prediction, B.{{ params.TargetName}}_prediction_score, B.{{ params.TargetName}}_prediction_details 
            FROM 
                (SELECT {{params.IndexColumn}}, {% if params.TimestampColumn %} {{params.TimestampColumn}}, {% endif %} max(prediction_time) AS p_time
                FROM {{params.DbSchema}}.{{params.ModelPredictionTable}}
                GROUP BY {{params.IndexColumn}} 
                {% if params.TimestampColumn %}, {{params.TimestampColumn}} {% endif %}) AS A
            LEFT JOIN 
                (SELECT {{params.IndexColumn}}, {% if params.TimestampColumn %} {{params.TimestampColumn}}, {% endif %} {{ params.TargetName}}_prediction, {{ params.TargetName}}_prediction_score, {{ params.TargetName}}_prediction_details, prediction_time 
                FROM  {{params.DbSchema}}.{{params.ModelPredictionTable}}) AS B
            ON A.{{params.IndexColumn}} = B.{{params.IndexColumn}} 
            {% if params.TimestampColumn %} AND A.{{params.TimestampColumn}}  = B.{{params.TimestampColumn}} {% endif %}
            AND A.p_time = B.prediction_time) AS C
        ON entity_table.{{params.IndexMatchName}} = C.{{params.IndexColumn}}  {% if params.TimestampColumn %}  AND entity_table.{{params.TSMatchName}} = C.{{params.TimestampColumn}}  {% endif %}
"""
)

model_prediction_regression_template = Template(
    """
        CREATE OR REPLACE VIEW {{params.DbSchema}}.{{params.ModelView}} AS
        SELECT entity_table.*, C.{{ params.TargetName}}_prediction from {{ params.ModelDataView}} AS entity_table
        LEFT JOIN
        (SELECT B.{{params.IndexColumn}}, {% if params.TimestampColumn %} B.{{params.TimestampColumn}}, {% endif %} B.{{ params.TargetName}}_prediction 
            FROM 
                (SELECT {{params.IndexColumn}}, {% if params.TimestampColumn %} {{params.TimestampColumn}}, {% endif %} max(prediction_time) AS p_time
                FROM {{params.DbSchema}}.{{params.ModelPredictionTable}}
                GROUP BY {{params.IndexColumn}} 
                {% if params.TimestampColumn %}, {{params.TimestampColumn}} {% endif %}) AS A
            LEFT JOIN 
                (SELECT {{params.IndexColumn}}, {% if params.TimestampColumn %} {{params.TimestampColumn}}, {% endif %} {{ params.TargetName}}_prediction, prediction_time 
                FROM  {{params.DbSchema}}.{{params.ModelPredictionTable}}) AS B
            ON A.{{params.IndexColumn}} = B.{{params.IndexColumn}} 
            {% if params.TimestampColumn %} AND A.{{params.TimestampColumn}}  = B.{{params.TimestampColumn}} {% endif %}
            AND A.p_time = B.prediction_time) AS C
        ON entity_table.{{params.IndexMatchName}} = C.{{params.IndexColumn}}  {% if params.TimestampColumn %}  AND entity_table.{{params.TSMatchName}} = C.{{params.TimestampColumn}}  {% endif %}
"""
)

model_prediction_binary_template = Template(
    """
        CREATE OR REPLACE VIEW {{params.DbSchema}}.{{params.ModelView}} AS
        SELECT entity_table.*, C.{{ params.TargetName}}_prediction, C.{{ params.TargetName}}_true_prediction_score from {{ params.ModelDataView}} AS entity_table
        LEFT JOIN
        (SELECT B.{{params.IndexColumn}}, {% if params.TimestampColumn %} B.{{params.TimestampColumn}}, {% endif %} B.{{ params.TargetName}}_prediction, B.{{ params.TargetName}}_true_prediction_score 
            FROM 
                (SELECT {{params.IndexColumn}}, {% if params.TimestampColumn %} {{params.TimestampColumn}}, {% endif %} max(prediction_time) AS p_time
                FROM {{params.DbSchema}}.{{params.ModelPredictionTable}}
                GROUP BY {{params.IndexColumn}} 
                {% if params.TimestampColumn %}, {{params.TimestampColumn}} {% endif %}) AS A
            LEFT JOIN 
                (SELECT {{params.IndexColumn}}, {% if params.TimestampColumn %} {{params.TimestampColumn}}, {% endif %} {{ params.TargetName}}_prediction, {{ params.TargetName}}_true_prediction_score, prediction_time 
                FROM  {{params.DbSchema}}.{{params.ModelPredictionTable}}) AS B
            ON A.{{params.IndexColumn}} = B.{{params.IndexColumn}} 
            {% if params.TimestampColumn %} AND A.{{params.TimestampColumn}}  = B.{{params.TimestampColumn}} {% endif %}
            AND A.p_time = B.prediction_time) AS C
        ON entity_table.{{params.IndexMatchName}} = C.{{params.IndexColumn}}  {% if params.TimestampColumn %}  AND entity_table.{{params.TSMatchName}} = C.{{params.TimestampColumn}}  {% endif %}
"""
)


def create_model_view_query(
    model_data_view,
    index_column,
    ts_column,
    index_match_name,
    ts_match_name,
    model_prediction_table,
    project,
    model_view_name,
    target_name,
    db_schema,
    problem_type,
):
    params = {
        "ModelDataView": model_data_view,
        "IndexColumn": index_column,
        "TimestampColumn": ts_column,
        "IndexMatchName": index_match_name,
        "TSMatchName": ts_match_name,
        "ModelPredictionTable": model_prediction_table,
        "ProjectName": project,
        "ModelView": model_view_name,
        "TargetName": target_name,
        "DbSchema": db_schema,
    }
    if problem_type == "regression" or problem_type == "forecasting":
        return model_prediction_regression_template.render(params=params)
    if problem_type == "multiclass_classification":
        return model_prediction_classification_template.render(params=params)
    if problem_type == "binary_classification":
        return model_prediction_binary_template.render(params=params)

    raise ValueError("Unable to handle problem type [{}]".format(problem_type))
