"""
location of base models
"""
from http import HTTPStatus
from typing import Union

from pydantic import BaseModel, Field


class BaseOutput(BaseModel):
    """
    https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format

    {
        "isBase64Encoded": true | false,
        "statusCode": httpStatusCode,
        "headers": {"headerName": "headerValue", ...},
        "multiValueHeaders": {
            "headerName": ["headerValue", "headerValue2", ...],
            ...
        },
        "body": "..."
    }
    """

    isBase64Encoded: bool = Field(False, alias="is_base_64_encoded")
    statusCode: Union[HTTPStatus, int] = Field(..., alias="status_code")
    headers: dict[str, str] = Field(default_factory=dict, description='{"headerName": "headerValue", ...}')
    multiValueHeaders: dict[str, Union[str, list[str]]] = Field(
        default_factory=dict,
        description='{"headerName": ["headerValue", "headerValue2", ...], ...}',
        alias="multi_value_headers",
    )
    body: Union[dict, list, str, int]
