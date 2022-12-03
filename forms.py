form = {
    'private': {
        "order": [
          "pumapi_url",
          "pumapi_token"
        ],
        "required": [
          "pumapi_url",
          "pumapi_token"
        ],
        "layout": {},
        "properties": {
          "pumapi_token": {
            "type": "string",
            "title": "PPMS PUMAPI Token",
            "description": "Calls to the PPMS PUMAPI will be made using the token.  It should have the necessary permissions to perform API calls on behalf of the core",
            "pattern": "^.+$"
          },
          "pumapi_url": {
            "type": "string",
            "title": "PPMS PUMAPI URL",
            "description": "I.E. https://ppms.us/yourorg/pumapi/",
            "pattern": "^https://.+$"
          }
        }
        },
    'public': {
        "order": [
          "message",
        ],
        "required": [
        ],
        "layout": {},
        "properties": {
          "message": {
            "type": "string",
            "title": "Message",
            "validators": [],
            "description": "You may enter an optional message to your staff and clients regarding usage of PPMS."
          }
        }
      }
    }