"""Integration tests that validates the BYOML story.

See https://github.com/waylayio/waylay-py/issues/3
"""
from ensurepip import version
from typing import Any, Tuple
import time
import tempfile
import os
import logging
import sys

import numpy as np
import pandas as pd

from http import HTTPStatus
from waylay import (
    WaylayClient,
    RestResponseError
)

from waylay.service.byoml import ByomlActionError, ModelNotReadyError

from fixtures import (
    sklearn_model_and_test_data,
    tensorflow_model_and_test_data,
    pytorch_model_and_test_data,
    pytorch_custom_model_and_test_data,
    xgboost_model_and_test_data,
    custom_sarima_model_and_data,
    generate_dataset,
    generate_labels,
    integration_test_prefix,
    integration_test_id,
    integration_test_session_id
)
import pytest


LOG = logging.getLogger(__name__)


class ModelUpload():
    """Object to upload a trained model for any supported framework."""

    def __init__(
        self,
        client,
        model,
        framework,
        model_name,
        input_data,
        predictions,
        work_dir=None,
    ):
        """Create the ModelUpload object."""
        self.client = client
        self.model = model
        self.framework = framework
        self.model_name = model_name
        self.input_data = input_data
        self.predictions = predictions
        self.work_dir = work_dir

    def upload_test_model(self, **kwargs) -> Any:
        """Delete any test model before uploading a new one."""
        try:
            self.client.byoml.model.remove(self.model_name)
            # removed, await (see )
            time.sleep(10)
        except RestResponseError as exc:
            # not found, OK
            pass

        try:
            return self.client.byoml.model.upload(
                self.model_name, self.model, framework=self.framework,
                description=f"integration test {__name__}.test_byoml_create_{self.framework}_model",
                work_dir=self.work_dir,
                **kwargs
            )
        except ByomlActionError as e:
            if e.response.status_code == HTTPStatus.BAD_GATEWAY:
                LOG.warn('ignoring a BAD_GATEWAY error upon model deployment')
                return None
            raise

    def validate_uploaded_model(self, **kwargs):
        """Validate if the model has been uploaded correctly."""
        model_repr = self.client.byoml.model.get(self.model_name, **kwargs)
        assert 'name' in model_repr
        assert f'integration test {__name__}' in model_repr['description']
        return model_repr

    def validate_updated_model(self):
        """Validate if the model has been correctly updated."""
        model_repr = self.client.byoml.model.get(self.model_name)
        assert 'updated' in model_repr['description']

    def predict_model(self, **kwargs):
        """Create a prediction with a model."""
        # test model on byoml, wait until ready
        predictions = self.client.byoml.model.predict(
            self.model_name, self.input_data,
            response_constructor=np.array,
            **kwargs
        )

        assert predictions is not None
        assert predictions.shape == self.predictions.shape

        # Floating points can be imprecise, don't assert equality
        np.testing.assert_allclose(self.predictions, predictions, atol=1e-05)

    def replace_test_model(self):
        """Replace the current model."""
        self.client.byoml.model.replace(
            self.model_name, self.model, framework=self.framework,
            description=f"updated integration test {__name__}.test_byoml_create_{self.framework}_model"
        )

    def remove_test_model(self):
        """Remove the model used in the test case."""
        self.client.byoml.model.remove(self.model_name)

    def execute_model_upload(self):
        """
        Upload a model using the following steps.

        Upload model, validate the upload, create a prediction,
        replace the test model and validate the replacement.
        Finally remove the test model.
        """
        self.upload_test_model()
        self.validate_uploaded_model()
        self.predict_model()
        self.replace_test_model()
        self.validate_updated_model()


@pytest.mark.sklearn
@pytest.mark.byoml_integration
def test_byoml_create_model(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f'{integration_test_prefix}-sk'

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.sklearn
@pytest.mark.byoml_integration
def test_byoml_create_model_in_local_dir(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f'{integration_test_prefix}-skl'

    with tempfile.TemporaryDirectory() as work_dir:

        model_upload = ModelUpload(
            client=waylay_test_client,
            model=model,
            framework=framework,
            model_name=model_name,
            input_data=df_validate,
            predictions=predictions,
            work_dir=work_dir
        )

        model_upload.execute_model_upload()

        assert os.path.exists(os.path.join(work_dir, 'model.joblib'))


@pytest.mark.sklearn
@pytest.mark.byoml_integration
def test_byoml_create_model_in_unexisting_local_dir(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f'{integration_test_prefix}-sknd'

    dir_name = "dir_does_not_exist"

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions,
        work_dir=dir_name
    )

    with pytest.raises(FileNotFoundError) as exc_info:
        model_upload.execute_model_upload()

    assert 'No such file or directory' in format(exc_info)


@pytest.mark.sklearn
@pytest.mark.byoml_integration
def test_byoml_get_model_without_retry(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f'{integration_test_prefix}-sknr'

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions
    )

    model_upload.upload_test_model()
    with pytest.raises(ByomlActionError):
        model_upload.predict_model(retry_attempts=-1)


@pytest.mark.sklearn
@pytest.mark.byoml_integration
def test_byoml_create_dill_model(
    sklearn_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a model."""
    model, df_validate, predictions = sklearn_model_and_test_data

    framework = "sklearn"
    model_name = f'{integration_test_prefix}-skdi'

    import dill  # pylint: disable=import-error

    with tempfile.TemporaryDirectory() as tmp_dir:
        model_file = f'{tmp_dir}/model.joblib'

        with open(model_file, 'wb') as f:
            dill.settings['recurse'] = True
            dill.dump(model, f)

        model_upload = ModelUpload(
            client=waylay_test_client,
            model=model_file,
            framework=framework,
            model_name=model_name,
            input_data=df_validate,
            predictions=predictions
        )

        model_upload.execute_model_upload()


@pytest.mark.tensorflow
@pytest.mark.byoml_integration
def test_byoml_create_tf_model(
    tensorflow_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a tensorflow model."""
    model, df_validate, predictions = tensorflow_model_and_test_data

    framework = "tensorflow"
    model_name = f'{integration_test_prefix}-tf'

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.pytorch
@pytest.mark.byoml_integration
def test_byoml_create_pytorch_model(
    pytorch_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a pytorch model."""
    model, validation_tensor, predictions = pytorch_model_and_test_data

    framework = "pytorch"
    model_name = f'{integration_test_prefix}-pt'

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=validation_tensor.float(),
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.pytorch
@pytest.mark.byoml_integration
def test_byoml_create_pytorch_script(
    pytorch_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a pytorch script."""
    model, validation_tensor, predictions = pytorch_model_and_test_data

    framework = "pytorch"
    model_name = f'{integration_test_prefix}-pts'

    import torch  # pylint: disable=import-error
    model_script = torch.jit.script(model)
    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model_script,
        framework=framework,
        model_name=model_name,
        input_data=validation_tensor.float(),
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.pytorch
@pytest.mark.byoml_integration
def test_byoml_create_pytorch_trace(
    pytorch_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a pytorch trace."""
    model, validation_tensor, predictions = pytorch_model_and_test_data

    framework = "pytorch"
    model_name = f'{integration_test_prefix}-ptt'

    import torch  # pylint: disable=import-error
    model_trace = torch.jit.trace(model, torch.randn(5, 1))  # pylint: disable=no-member
    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model_trace,
        framework=framework,
        model_name=model_name,
        input_data=validation_tensor.float(),
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.skip(reason="PyTorch 1.5 does not support this")
@pytest.mark.pytorch
@pytest.mark.byoml_integration
def test_byoml_create_pytorch_custom(
    pytorch_custom_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a custom pytorch function."""
    model, validation_tensor, predictions = pytorch_custom_model_and_test_data

    framework = "pytorch"
    model_name = f'{integration_test_prefix}-ptc'

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=validation_tensor.float(),
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.xgboost
@pytest.mark.byoml_integration
def test_byoml_create_xgboost_model(
    xgboost_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test an xgboost model."""
    model, df_validate, predictions = xgboost_model_and_test_data

    framework = "xgboost"
    model_name = f'{integration_test_prefix}-xgb'

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions
    )

    model_upload.execute_model_upload()


@pytest.mark.xgboost
@pytest.mark.byoml_integration
def test_byoml_create_xgboost_model_retry_get_until_ready_raise(
    xgboost_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and test a failing get call to an xgboost model."""
    model, df_validate, predictions = xgboost_model_and_test_data

    framework = "xgboost"
    model_name = f'{integration_test_prefix}-xgb-retry-until-rdy'

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions,
    )

    model_upload.upload_test_model()
    with pytest.raises(ModelNotReadyError):
        model_upload.validate_uploaded_model(retry_until_ready=True, retry_attempts=-1)


@pytest.mark.xgboost
@pytest.mark.byoml_integration
def test_byoml_create_xgboost_model_retry_get_until_ready(
    xgboost_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Create, upload, and retry a get call to an xgboost model."""
    model, df_validate, predictions = xgboost_model_and_test_data

    framework = "xgboost"
    model_name = f'{integration_test_prefix}-xgb-retry-until-rdy'

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions,
    )

    model_upload.upload_test_model()
    upload_result = model_upload.validate_uploaded_model(retry_until_ready=True, retry_attempts=50)
    assert upload_result['ready'] is True


@pytest.mark.xgboost
@pytest.mark.byoml_integration
def test_byoml_create_xgboost_model_retry_predict_until_ready(
    xgboost_model_and_test_data: Tuple[Any, pd.DataFrame, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """
    Create, upload, and test an xgboost model after deleting a model with the same name.

    Should raise ByomlActionError.
    """
    model, df_validate, predictions = xgboost_model_and_test_data

    framework = "xgboost"

    model_name = f'{integration_test_prefix}-xgb-retry-raise'

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=predictions,
    )

    model_upload.upload_test_model(framework_version="1.0")
    model_upload.remove_test_model()
    try:
        model_upload.upload_test_model(retry_max_delay=0, timeout=120)
        pytest.skip("Could have thrown a 409: CONFLICT due to recent deletion, but didn't.")
    except ByomlActionError as exc:
        assert exc.response.status_code == 409, 'expected a 409: CONFLICT due to recent deletion.'


@pytest.mark.skip('See https://github.com/waylayio/plug-registry/issues/812')
@pytest.mark.custom
@pytest.mark.byoml_integration
def test_byoml_custom_sarima_model(
    custom_sarima_model_and_data: Tuple[Any, np.ndarray, np.ndarray],
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Test the upload of a custom sarima model."""
    model, input_data, predictions = custom_sarima_model_and_data

    model_name = f'{integration_test_prefix}-custom-sarima'

    # validate local model inference and input/output conversion
    json_request = {'instances': input_data.tolist()}
    result = model.predict(model.map_input(json_request))
    json_result = model.map_output(json_request, result)
    assert json_result == {'predictions': predictions.tolist()}

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=model,
        framework='custom',
        model_name=model_name,
        input_data=input_data,
        predictions=predictions
    )

    model_upload.upload_test_model(
        framework_version='1.0',
        lib='test/lib',
        requirements='lib/sarima_byoml_wrapper'
    )
    model_upload.validate_uploaded_model()
    model_upload.predict_model()

    # TODO see https://github.com/waylayio/byoml/issues/221
    # model_upload.replace_test_model(
    #     framework_version='1.0',
    #     lib='test/lib',
    #     requirements='lib/sarima_byoml_wrapper'
    # )
    # model_upload.validate_updated_model()


@pytest.mark.skipif(sys.version_info >= (3, 8), reason='Only works for Python 3.7')
@pytest.mark.custom
@pytest.mark.byoml_integration
def test_byoml_custom_model(
    waylay_test_client: WaylayClient,
    integration_test_prefix: str
):
    """Test the upload of a custom model."""
    class Doubler:
        def __init__(self):
            self.keys = ['foo', 'bar', 'baz', 'something', 'else']

        def predict(self, data):
            return data * 2

        def map_output(self, request, predictions):
            mapped_predictions = [
                {
                    self.keys[idx]: value
                    for idx, value in enumerate(pred)
                }
                for pred in predictions.tolist()
            ]
            mapped_predictions2 = [
                {
                    value: self.keys[idx]
                    for idx, value in enumerate(pred)
                }
                for pred in predictions.tolist()
            ]
            return {'predictions': mapped_predictions, 'predictions_2': mapped_predictions2}

    Doubler.__module__ = '__main__'
    custom_model = Doubler()
    model_name = f'{integration_test_prefix}-custom-model'
    df_validate = [[1, 2, 3], [10, 20, 30]]
    framework = "custom"

    model_upload = ModelUpload(
        client=waylay_test_client,
        model=custom_model,
        framework=framework,
        model_name=model_name,
        input_data=df_validate,
        predictions=df_validate
    )

    model_upload.upload_test_model()
    upload_result = model_upload.validate_uploaded_model(retry_until_ready=True, retry_attempts=50)
    assert upload_result['ready'] is True

    predictions = waylay_test_client.byoml.model.predict(model_name, df_validate)
    assert list(predictions[0].keys()) == ['foo', 'bar', 'baz']
    assert list(predictions[0].values()) == [2, 4, 6]
