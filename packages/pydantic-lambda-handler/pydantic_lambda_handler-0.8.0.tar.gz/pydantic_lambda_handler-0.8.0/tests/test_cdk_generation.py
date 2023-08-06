from pydantic_lambda_handler.hooks.cdk_conf_hook import add_resource_v2


def test_generate_cdk_config(cdk_config):
    hello_resource = next(i for i in cdk_config[0]["resources"] if i.get("name") == "hello")
    assert hello_resource["name"] == "hello", cdk_config["resources"]
    assert hello_resource["methods"] == [
        {
            "function_name": "HelloHandler",
            "handler": "hello_handler",
            "index": "demo_app_handlers.py",
            "method": "GET",
            "reference": "demo_app_handlers.hello_handler",
            "status_code": "200",
        },
        {
            "function_name": "CreateHandler",
            "handler": "create_handler",
            "index": "demo_app_handlers.py",
            "method": "POST",
            "reference": "demo_app_handlers.create_handler",
            "status_code": "201",
        },
    ]


def test_generate_cdk_config_status_code(cdk_config):
    hello_resource = next(i for i in cdk_config[0]["resources"] if i.get("name") == "hello")
    assert hello_resource["methods"][0]["status_code"] == "200"


def test_generate_cdk_config_nested_resources(cdk_config):
    hello_resource = next(i for i in cdk_config[0]["resources"] if i.get("name") == "items")
    assert hello_resource["resources"] == [
        {
            "methods": [
                {
                    "function_name": "HandlerWithTypeHint",
                    "handler": "handler_with_type_hint",
                    "index": "subfolder/path_parameters_handlers.py",
                    "method": "GET",
                    "reference": "subfolder.path_parameters_handlers.handler_with_type_hint",
                    "status_code": "200",
                }
            ],
            "name": "{item_id}",
        }
    ]


conf = [
    (
        "/hello",
        {
            "POST": {
                "function_name": "CreateHandler",
                "status_code": "201",
                "index": "demo_app_handlers.py",
                "handler": "create_handler",
                "reference": "demo_app_handlers.create_handler",
            },
            "GET": {
                "function_name": "HelloHandler",
                "status_code": "200",
                "index": "demo_app_handlers.py",
                "handler": "hello_handler",
                "reference": "demo_app_handlers.hello_handler",
            },
        },
    ),
    (
        "/",
        {
            "POST": {
                "function_name": "IndexHandler",
                "status_code": "201",
                "index": "demo_app_handlers.py",
                "handler": "index_handler",
                "reference": "demo_app_handlers.index_handler",
            }
        },
    ),
    (
        "/query",
        {
            "GET": {
                "function_name": "QuerySkip",
                "status_code": "200",
                "index": "subfolder/query_parameters_handlers.py",
                "handler": "query_skip",
                "reference": "subfolder.query_parameters_handlers.query_skip",
            }
        },
    ),
    (
        "/query_required",
        {
            "GET": {
                "function_name": "QueryRequired",
                "status_code": "200",
                "index": "subfolder/query_parameters_handlers.py",
                "handler": "query_required",
                "reference": "subfolder.query_parameters_handlers.query_required",
            }
        },
    ),
    (
        "/teapot",
        {
            "GET": {
                "function_name": "HelloTeapot",
                "status_code": "418",
                "index": "subfolder/path_parameters_handlers.py",
                "handler": "hello_teapot",
                "reference": "subfolder.path_parameters_handlers.hello_teapot",
            }
        },
    ),
    (
        "/pets/{petId}",
        {
            "GET": {
                "function_name": "PetsHandler",
                "status_code": "200",
                "index": "subfolder/path_parameters_handlers.py",
                "handler": "pets_handler",
                "reference": "subfolder.path_parameters_handlers.pets_handler",
            }
        },
    ),
    (
        "/items/{item_id}",
        {
            "GET": {
                "function_name": "HandlerWithTypeHint",
                "status_code": "200",
                "index": "subfolder/path_parameters_handlers.py",
                "handler": "handler_with_type_hint",
                "reference": "subfolder.path_parameters_handlers.handler_with_type_hint",
            }
        },
    ),
    (
        "/item_enum/{item_id}",
        {
            "GET": {
                "function_name": "HandlerWithEnumTypeHint",
                "status_code": "200",
                "index": "subfolder/path_parameters_handlers.py",
                "handler": "handler_with_enum_type_hint",
                "reference": "subfolder.path_parameters_handlers.handler_with_enum_type_hint",
            }
        },
    ),
    (
        "/context",
        {
            "GET": {
                "function_name": "WithContext",
                "status_code": "200",
                "index": "subfolder/additional_args_handlers.py",
                "handler": "with_context",
                "reference": "subfolder.additional_args_handlers.with_context",
            }
        },
    ),
    (
        "/response_model",
        {
            "GET": {
                "function_name": "ResponseModel",
                "status_code": "200",
                "index": "subfolder/response_model_handlers.py",
                "handler": "response_model",
                "reference": "subfolder.response_model_handlers.response_model",
            }
        },
    ),
]


def test_add_resource_root_v2():
    child_list = []
    url, conf = (
        "/",
        {
            "POST": {
                "function_name": "IndexHandler",
                "status_code": "201",
                "index": "demo_app_handlers.py",
                "handler": "index_handler",
                "reference": "demo_app_handlers.index_handler",
            }
        },
    )
    add_resource_v2(child_list, url, conf)
    assert child_list == [
        {
            "name": "",
            "methods": [
                {
                    "function_name": "IndexHandler",
                    "handler": "index_handler",
                    "index": "demo_app_handlers.py",
                    "method": "POST",
                    "reference": "demo_app_handlers.index_handler",
                    "status_code": "201",
                }
            ],
        }
    ]


def test_add_resource_query_v2():
    child_list = []
    url, conf = (
        "/query",
        {
            "GET": {
                "function_name": "QuerySkip",
                "status_code": "200",
                "index": "subfolder/query_parameters_handlers.py",
                "handler": "query_skip",
                "reference": "subfolder.query_parameters_handlers.query_skip",
            }
        },
    )
    add_resource_v2(child_list, url, conf)
    assert child_list == [
        {
            "resources": [
                {
                    "name": "query",
                    "methods": [
                        {
                            "function_name": "QuerySkip",
                            "handler": "query_skip",
                            "index": "subfolder/query_parameters_handlers.py",
                            "method": "GET",
                            "reference": "subfolder.query_parameters_handlers.query_skip",
                            "status_code": "200",
                        }
                    ],
                }
            ]
        }
    ]


def test_add_resource_deep_v2():
    child_list = []
    url, conf = (
        "/pets/{petId}",
        {
            "GET": {
                "function_name": "PetsHandler",
                "status_code": "200",
                "index": "subfolder/path_parameters_handlers.py",
                "handler": "pets_handler",
                "reference": "subfolder.path_parameters_handlers.pets_handler",
            }
        },
    )

    add_resource_v2(child_list, url, conf)
    assert child_list == [
        {
            "resources": [
                {
                    "name": "pets",
                    "resources": [
                        {
                            "name": "{petId}",
                            "methods": [
                                {
                                    "function_name": "PetsHandler",
                                    "handler": "pets_handler",
                                    "index": "subfolder/path_parameters_handlers.py",
                                    "method": "GET",
                                    "reference": "subfolder.path_parameters_handlers.pets_handler",
                                    "status_code": "200",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    ]


def test_add_resource_deep_plus2_v2():
    child_list = []
    child_dict = {
        "/pets/{petId}": {
            "GET": {
                "function_name": "PetsHandler",
                "status_code": "200",
                "index": "subfolder/path_parameters_handlers.py",
                "handler": "pets_handler",
                "reference": "subfolder.path_parameters_handlers.pets_handler",
            }
        },
        "/context": {
            "GET": {
                "function_name": "WithContext",
                "status_code": "200",
                "index": "subfolder/additional_args_handlers.py",
                "handler": "with_context",
                "reference": "subfolder.additional_args_handlers.with_context",
            }
        },
    }

    for url, conf in child_dict.items():
        add_resource_v2(child_list, url, conf)
    assert child_list == [
        {
            "resources": [
                {
                    "name": "pets",
                    "resources": [
                        {
                            "name": "{petId}",
                            "methods": [
                                {
                                    "function_name": "PetsHandler",
                                    "handler": "pets_handler",
                                    "index": "subfolder/path_parameters_handlers.py",
                                    "method": "GET",
                                    "reference": "subfolder.path_parameters_handlers.pets_handler",
                                    "status_code": "200",
                                }
                            ],
                        }
                    ],
                },
                {
                    "name": "context",
                    "methods": [
                        {
                            "function_name": "WithContext",
                            "handler": "with_context",
                            "index": "subfolder/additional_args_handlers.py",
                            "method": "GET",
                            "reference": "subfolder.additional_args_handlers.with_context",
                            "status_code": "200",
                        }
                    ],
                },
            ]
        }
    ]
