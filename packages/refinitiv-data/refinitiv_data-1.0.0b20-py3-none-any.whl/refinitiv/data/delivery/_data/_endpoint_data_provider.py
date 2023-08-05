from ._data_provider import (
    DataProvider,
    ContentValidator,
    ResponseFactory,
    ValidatorContainer,
    RequestFactory,
)
from ._endpoint_data import EndpointData


class EndpointValidator(ContentValidator):
    def validate(self, data, *args, **kwargs):
        return True


class EndpointRequestFactory(RequestFactory):
    def extend_body_parameters(self, body_params, **kwargs):
        return body_params


endpoint_data_provider = DataProvider(
    validator=ValidatorContainer(content_validator=EndpointValidator()),
    response=ResponseFactory(data_class=EndpointData),
    request=EndpointRequestFactory(),
)
