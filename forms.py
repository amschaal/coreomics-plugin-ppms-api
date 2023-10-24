from plugins import RESTRICT_TO_LAB, RESTRICT_TO_INSTITUTION

form = {
    'private': {
        "order": [
          "pumapi_token",
          "api2_token",
          "core_id",
          "user_info_report_id",
          "order_search_report_id"
        ],
        "required": [
          "pumapi_token",
          "api2_token",
          "core_id"
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
          "user_info_report_id": {
            "type": "string",
            "title": "Report ID of custom user info API2 call",
            "description": "I.E. Report1234"
            # "restrict_to": [RESTRICT_TO_INSTITUTION]
          },
          "order_search_report_id": {
            "type": "string",
            "title": "Report ID of custom order search API2 call",
            "description": "I.E. Report1234"
            # "restrict_to": [RESTRICT_TO_INSTITUTION]
          },
          "core_id": {
            "type": "number",
            "title": "Core ID",
            "description": "ID number of Core in PPMS",
            "restrict_to": [RESTRICT_TO_LAB]
          }
        }
        },
    'public': {
        "order": [
          "ppms_url",
        ],
        "required": [
          "ppms_url"
        ],
        "layout": {},
        "properties": {
          "ppms_url": {
            "type": "string",
            "title": "PPMS Base URL",
            "description": "I.E. https://ppms.us/yourorg/",
            "pattern": "^https://.+$",
          }
        }
      }
    }