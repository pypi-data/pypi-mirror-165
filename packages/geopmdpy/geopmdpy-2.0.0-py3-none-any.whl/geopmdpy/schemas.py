#
#  Copyright (c) 2015 - 2022, Intel Corporation
#  SPDX-License-Identifier: BSD-3-Clause
#

"""Json schemas used by geopmdpy

GEOPM_ACTIVE_SESSIONS_SCHEMA:

.. code-block:: json

    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "id": "https://geopm.github.io/active_sessions.schema.json",
        "title": "ActiveSession",
        "type": "object",
        "properties": {
          "client_pid": {
            "type": "integer"
          },
          "reference_count": {
            "type": "integer",
            "minimum": 0
          },
          "signals": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "controls": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "watch_id": {
            "type": "integer"
          },
          "batch_server": {
            "type": "integer"
          }
        },
        "required": ["client_pid", "signals", "controls"],
        "additionalProperties": false
    }


"""

GEOPM_ACTIVE_SESSIONS_SCHEMA = """
    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "id": "https://geopm.github.io/active_sessions.schema.json",
        "title": "ActiveSession",
        "type": "object",
        "properties": {
          "client_pid": {
            "type": "integer"
          },
          "reference_count": {
            "type": "integer",
            "minimum": 0
          },
          "signals": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "controls": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "watch_id": {
            "type": "integer"
          },
          "batch_server": {
            "type": "integer"
          }
        },
        "required": ["client_pid", "signals", "controls"],
        "additionalProperties": false
    }
"""
