curl -X POST "https://telex-uo3s.onrender.com/format_message" \
     -H "Content-Type: application/json" \
     -d '{
       "channel_id": "01950e4c-1362-74a3-9ce1-5d7cf1b5ab76",
       "return_url": "https://ping.telex.im/v1/webhooks/01950e4c-1362-74a3-9ce1-5d7cf1b5ab76",
       "settings": [
         {"label": "maxMessageLength", "type": "number", "default": 300, "required": true},
         {"label": "repeatWords", "type": "multi-select", "default": "world, happy", "required": true},
         {"label": "noOfRepetitions", "type": "number", "default": 2, "required": true}
       ],
       "message": "Hello, world. I hope you are happy today"
     }'