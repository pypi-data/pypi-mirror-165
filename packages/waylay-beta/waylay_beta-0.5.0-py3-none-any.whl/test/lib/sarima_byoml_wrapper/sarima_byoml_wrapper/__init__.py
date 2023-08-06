"""BYOML Model wrappers for Sarima models"""
import numpy as np
import pandas as pd
import statsmodels.api as sm


def convert_to_pandas(data):
    # to make the model behave the same when fitting and when deployed
    if isinstance(data, list):
        data = np.array(data)
    if isinstance(data, np.ndarray):
        (instance_count, row_count) = data.shape
        if row_count == 2:
            timestamps, values = data.transpose()
        elif instance_count == 2:
            timestamps, values = data
        else:
            raise ValueError('This model requires a timestamp and value row as input')

        if len(timestamps) and isinstance(timestamps[0], np.number):
            # millisecond epoch is standard for waylay
            data = pd.DataFrame(values, index=pd.to_datetime(timestamps, unit='ms'))
        else:
            data = pd.DataFrame(values, index=pd.to_datetime(timestamps))

    if not isinstance(data, pd.DataFrame):
        raise ValueError('This model requires an input that can be converted to a dataframe.')

    return data


def convert_to_numpy(series_or_df):
    # convert dataframe to an array of (timestamp_millis, value) tuples
    timestamps = series_or_df.index.map(lambda _: _.timestamp() * 1000).values
    if isinstance(series_or_df, pd.DataFrame):
        df = series_or_df
        series = [df[c].values for c in df.columns]
        return np.array([timestamps, *series]).transpose()
    else:
        series = series_or_df.values
        return np.array([timestamps, series]).transpose()

DEFAULT_MODEL_ARGS = dict(
    order=(1, 1, 1),
    enforce_stationarity=False
)

class SARIMAXForecaster:
    def __init__(self, model_args=DEFAULT_MODEL_ARGS, default_window=24):
        self.model_args = model_args
        self.default_window = default_window
        self.fitted_params = None

    def map_input(self, request):
        instances = convert_to_pandas(request['instances'])
        window = request.get('window', self.default_window)
        return (instances, window)

    def map_output(self, request, result):
        """Convert the output of `predict` to a json-data response payload."""
        return {'predictions': convert_to_numpy(result).tolist()}

    def create_model(self, data):
        return sm.tsa.SARIMAX(
            data,
            **self.model_args
        )

    def fit(self, data, **fit_args):
        fitted_model = self.create_model(data).fit(**fit_args)
        self.fitted_params = fitted_model.params
        return fitted_model

    def get_fitted_model(self, data):
        model = self.create_model(data)
        if self.fitted_params is None:
            raise ValueError('Model has not been fitted')
        return model.smooth(self.fitted_params)

    def predict(self, data_and_window):
        data, window = data_and_window
        fitted_model = self.get_fitted_model(data)
        return fitted_model.forecast(steps=window)


class SARIMAXConfidenceForecaster(SARIMAXForecaster):
    def __init__(self, model_args=DEFAULT_MODEL_ARGS, default_window=24, default_alpha=0.05):
        super().__init__(model_args, default_window)
        self.default_alpha = default_alpha

    def map_input(self, request):
        instances = convert_to_pandas(request['instances'])
        alpha = request.get('alpha', self.default_alpha)
        window = request.get('window', self.default_window)
        return (instances, window, alpha)

    def predict(self, data_window_and_alpha):
        data, window, alpha = data_window_and_alpha
        fitted_model = self.get_fitted_model(data)
        forecast = fitted_model.get_forecast(steps=window)
        return forecast.conf_int(alpha=alpha)

        

