#!/bin/bash
curl --location 'http://localhost:8000/tick' \
--header 'Content-Type: application/json' \
--data '{
    "channel_id": "01950895-61a5-757a-b2e9-0d42c05d3218",
    "return_url": "https://ping.telex.im/v1/return/01950895-61a5-757a-b2e9-0d42c05d3218",
    "settings": [
        {
            "label": "site-1",
            "type": "text",
            "required": true,
            "default": "https://google.com"
        },
        {
            "label": "site-2",
            "default": "https://www.somefakewebsitethatisfake.com",
            "type": "text",
            "required": true
        },
        {
            "label": "interval",
            "type": "text",
            "required": true,
            "default": "* * * * *"
        }
    ]
}'