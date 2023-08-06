def tree():
    return {
        "misc": {
            "user_id": '',
            "project_id": '',
            "project_name": 'proj_name',
        },
        "apps": [
            {
                "name": 'app1',
                "base_url": '',
                "endpoints": [
                        {
                            "misc": {
                                "endpoint_id": 'abc',
                                "is_draft": 'isDraft',
                            },
                            "request": {
                                "method": "requestMethod",
                                "host": "requestHost",
                                "uri": "users",
                            },
                            "headers": {
                                "authorization": "authHeaderType",
                                "body": "headers",
                            },
                            "params": "params",
                            "body": {
                                "type": "payloadType",
                                "payload": "payload",
                            },
                            "response": {
                                "code": 200,
                            },
                        },
                ],
                "models": [
                    {
                        "table_name": 'User',
                        "fields": {
                            "Name": {"primary_key": True, "type": "varchar(255)", "null": False, "default": None, "blank": False,},
                            "Status": {"primary_key": False, "type": "id"},
                        },
                    },
                ],
            },
        ],
        "functions": [],
        "integrations": {},
        "settings": {},
    }
