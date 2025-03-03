from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes.modeling.modeling import split_data, train_model, evaluate_model


def create_pipeline(**kwargs) -> Pipeline:


    modeling_pipeline = pipeline(
        [
            node(
                func=split_data,
                inputs=["model_input", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=train_model,
                inputs=["X_train", "y_train"],
                outputs="regressor",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["regressor", "X_test", "y_test"],
                outputs=None,
                name="evaluate_model_node",
            ),
        ]
    )

    return pipeline(
        pipe=modeling_pipeline,
        namespace="data_science",
        inputs=["model_input"],
        outputs=["regressor"],
    )