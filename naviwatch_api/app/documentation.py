from configparser import RawConfigParser
import re
from app import app


swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "ThingAPI",
        "description": "Superloop Thing API",
        "contact": {
            "responsibleOrganization": "Superloop",
            "responsibleDeveloper": "some person",
            "email": "someemail@superloop.com",
            "url": "www.superloop.com",
        },
        "termsOfService": "http://www.superloop.com/",
        "version": "0.0.1"
    },
    "host": app.config.get('SWAGGER_HOST'),
    "basePath": "/",
    "schemes": [
        "http"
    ],
    "definitions": {
        "Thing": {
            "properties": {
                "name": {
                    "description": "Name of thing",
                    "type": "string"
                },
                "description": {
                    "description": "Description of thing",
                    "type": "string"
                }
            },
            "required": [
                "name"
            ],
            "type": "object"
        },
        "Things": {
                    "description": "List ofThings",
                    "items": {
                        "$ref": "#/definitions/Thing"
                    },
                    "minItems": "0",
                    "type": "array"
                },
        "Errors": {
            "description": "One or more field errors",
            "properties": {
                "error": {
                    "description": "List of errors"
                },
                "data": {
                    "description": "data result",
                    "type": None
                }
            }
        },
        "Message": {
            "description": "asdf",
            "properties": {
                "message": {
                    "description": "completion message"
                },
                "data": {
                    "description": "data result",
                    "type": None
                }
            }
        }
    }
}

thing_get_xid = {
    "summary": "Retrieve a specific Thing",
    "description": "If XID is specified retrieve the specific Thing by XID",
    "operationId": "thing_get_xid",
    "tags": ["thing"],
    "produces": "application/json",
    "parameters": [{"description": "Thing ID",
                    "in": "path",
                    "name": "xid",
                    "required": True,
                    "type": "integer"}],
    "responses": {"200": {"schema": {"$ref": "#/definitions/Thing"}},
                  "404": {"schema": None}}
}
thing_get_all = {
    "summary": "Retrieve all Things",
    "description": "Fetch all the Things!",
    "operationId": "thing_get_all",
    "tags": ["thing"],
    "produces": "application/json",
    "responses": {"200": {"schema": {"$ref": "#/definitions/Things"}},
                  "404": {"schema": None}}
}
thing_post = {
    "summary": "Create a new Thing",
    "description": "Creates a new thing with the specified name and optional description",
    "operationId": "thing_post",
    "tags": ["thing"],
    "consumes": "application/json",
    "produces": "application/json",
    "parameters": [{"in": "body",
                    "name": "body",
                    "required": True,
                    "schema": {"$ref": "#/definitions/Thing"}}],
    "responses": {"200": {"schema": {"$ref": "#/definitions/Thing"}},
                  "422": {"schema": {"$ref": "#/definitions/Errors"}}}
}
thing_put = {
    "summary": "Updates an existing Thing",
    "description": "Attempts to update the Thing identified by the specified XID",
    "operationId": "thing_post",
    "tags": ["thing"],
    "consumes": "application/json",
    "produces": "application/json",
    "parameters": [{"in": "body",
                    "name": "body",
                    "required": True,
                    "schema": {"$ref": "#/definitions/Thing"}},
                   {"description": "Thing ID",
                    "in": "path",
                    "name": "xid",
                    "required": True,
                    "type": "integer"}
                   ],
    "responses": {"200": {"schema": {"$ref": "#/definitions/Thing"}},
                  "422": {"schema": {"$ref": "#/definitions/Errors"}},
                  "404": {"schema": None}}
}
thing_delete = {
    "summary": "Delete a Thing",
    "description": "Delete a Thing with the specified XID",
    "operationId": "thing_delete",
    "tags": ["thing"],
    "produces": "application/json",
    "parameters": [{"description": "Thing ID",
                    "in": "path",
                    "name": "xid",
                    "required": True,
                    "type": "string"}],
    "responses": {"200": {"schema": {"$ref": "#/definitions/Message"}},
                  "404": {"schema": None}}
}