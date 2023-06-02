from plugins import RESTRICT_TO_LAB, RESTRICT_TO_INSTITUTION

form = {
    'private': {
        "order": [
          "ppms_url",
          "pumapi_token",
          "api2_token"
        ],
        "required": [
          "ppms_url",
          "pumapi_token",
          "api2_token"
        ],
        "layout": {},
        "properties": {
          "pumapi_token": {
            "type": "string",
            "title": "PPMS PUMAPI Token",
            "description": "Calls to the PPMS PUMAPI will be made using the token.  It should have the necessary permissions to perform API calls on behalf of the core",
            "pattern": "^.+$"
          },
          "api2_token": {
            "type": "string",
            "title": "PPMS API2 Token",
            "description": "Calls to the PPMS API2 will be made using the token.  It should have the necessary permissions to perform API calls on behalf of the core",
            "pattern": "^.+$"
          },
          "ppms_url": {
            "type": "string",
            "title": "PPMS Base URL",
            "description": "I.E. https://ppms.us/yourorg/",
            "pattern": "^https://.+$",
            # "restrict_to": [RESTRICT_TO_INSTITUTION]
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