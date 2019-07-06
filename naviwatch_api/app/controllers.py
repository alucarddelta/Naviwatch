from flask import jsonify, request, abort
from app import app, models, schema, db, documentation
from flask_cors import CORS
from flask_accept import accept
from sqlalchemy import and_, exists
from marshmallow import ValidationError
import re
from typing import List, Dict, Tuple, Optional, Union, Type, Any
from flasgger import Swagger, swag_from


"""
allow cross origin resource sharing
"""
CORS(app)

"""
Swagger
"""
# set up swagger
app.config["SWAGGER"] = {"uiversion": 3}
swagger = Swagger(app, template=documentation.swagger_template)


def format_search(model: Type[models.Base]) -> List[Any]:
    """
    Returns a list of SQL Alchemy filter terms based on request arguments. If the request argument key is a valid model column name an
    SQL Alchemy "like" filter will be generated and appended to filters for return.

    Args:
        model: <Sqlalchemy model>
    
    Returns:
        list: [<Sqlalchemy model>.<request.arg.key>.like(<request.arg.value>) if <request.arg.key> in <model.columns>]

    """
    filters = list()
    if request.args:
        for k, v in request.args.items():
            if k.lower() in model.__table__.columns.keys():
                if str(model.__table__.columns[k.lower()].type) == "INTEGER":
                    try:
                        filters.append(getattr(model, k.lower()) == int(re.sub("[^0-9]", "", v)))
                    except ValueError as e:
                        print(e)
                else:
                    filters.append(getattr(model, k.lower()).like(v.replace("*", "%")))
    return filters


def return_result(result: Union[Dict, None]) -> Tuple[Union[str, None], int]:
    """
    Helper function to reduce code repetition in routes

    Args:
        result: Dict on which to perform an existence check

    Returns:
        tuple (json, 200): if o is not None
        404: if o is of type dict
    """
    if result:
        return jsonify({"__args": request.args, "data": result}), 200
    else:
        abort(404)


@app.route('/')
def route_default() -> Tuple[str, int]:
    return jsonify({"message": "peruse controllers.py for valid enpoints/methods",
                    "data": None}), 200

######################################################################################################
############################### PERSON ###############################################################
######################################################################################################

@app.route('/person/<int:xid>', methods=['DELETE'])
def route_person_delete(xid: int) -> Tuple[str, int]:

    person = db.session.query(models.Person).get(int(xid))
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "Deleted Person '{}'".format(person.name),
                        "data": None}), 200
    else:
        abort(404)


@app.route('/person/', methods=['GET'], endpoint='person_get_all')
@app.route('/person/<int:xid>', methods=['GET'], endpoint='person_get_xid')
def route_person_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:

    if xid:
        return return_result(schema.PersonSchema().dump(db.session.query(models.Person).get(int(xid))))
    else:
        return return_result(schema.PersonSchema(many=True).dump(db.session.query(models.Person).filter(and_(*format_search(models.Person))).all()))


@app.route('/person/', methods=['POST'])
@accept('application/json')
def route_person_post() -> Tuple[str, int]:

    if request.get_json():
        try:
            person = schema.PersonSchema().load(request.get_json())
            db.session.add(person)
            db.session.commit()
            return return_result(schema.PersonSchema().dump(person))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422


@app.route('/person/<int:xid>', methods=['PUT'])
@accept('application/json')
def route_person_put(xid: int) -> Tuple[str, int]:

    if request.json:
        person = db.session.query(models.Person).get(int(xid))
        if person:
            try:
                person = schema.PersonSchema().load(request.json,
                                                  instance=person)
                db.session.add(person)
                db.session.commit()
            except ValidationError as err:
                return jsonify({"error": err.messages,
                                "data": None}), 409 if "name" in err.messages.keys() else 422

        return return_result(schema.PersonSchema().dump(person))

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

######################################################################################################
################################## PET ###############################################################
######################################################################################################

@app.route('/pet/<int:xid>', methods=['DELETE'])
def route_pet_delete(xid: int) -> Tuple[str, int]:

    pet = db.session.query(models.Pet).get(int(xid))
    if pet:
        db.session.delete(pet)
        db.session.commit()
        return jsonify({"message": "Deleted Pet '{}'".format(pet.name),
                        "data": None}), 200
    else:
        abort(404)


@app.route('/pet/', methods=['GET'], endpoint='pet_get_all')
def route_pet_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:


    if xid:
        return return_result(schema.PetSchema().dump(db.session.query(models.Pet).get(int(xid))))
    else:
        return return_result(schema.PetSchema(many=True).dump(db.session.query(models.Pet).filter(and_(*format_search(models.Pet))).all()))


@app.route('/pet/', methods=['POST'])
@accept('application/json')
def route_pet_post() -> Tuple[str, int]:

    if request.get_json():
        try:
            pet = schema.PetSchema().load(request.get_json())
            db.session.add(pet)
            db.session.commit()
            return return_result(schema.PetSchema().dump(pet))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422


@app.route('/pet/<int:xid>', methods=['PUT'])
@accept('application/json')
def route_pet_put(xid: int) -> Tuple[str, int]:

    if request.json:
        pet = db.session.query(models.Pet).get(int(xid))
        if pet:
            try:
                pet = schema.PetSchema().load(request.json,
                                                  instance=pet)
                db.session.add(pet)
                db.session.commit()
            except ValidationError as err:
                return jsonify({"error": err.messages,
                                "data": None}), 409 if "name" in err.messages.keys() else 422

        return return_result(schema.PetSchema().dump(pet))

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

######################################################################################################
################################# FOOD ###############################################################
######################################################################################################

@app.route('/food/<int:xid>', methods=['DELETE'])
def route_food_delete(xid: int) -> Tuple[str, int]:

    food = db.session.query(models.Food).get(int(xid))
    if food:
        db.session.delete(food)
        db.session.commit()
        return jsonify({"message": "Deleted Food '{}'".format(food.name),
                        "data": None}), 200
    else:
        abort(404)


@app.route('/food/', methods=['GET'], endpoint='food_get_all')
def route_food_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:


    if xid:
        return return_result(schema.FoodSchema().dump(db.session.query(models.Food).get(int(xid))))
    else:
        return return_result(schema.FoodSchema(many=True).dump(db.session.query(models.Food).filter(and_(*format_search(models.Food))).all()))


@app.route('/food/', methods=['POST'])
@accept('application/json')
def route_food_post() -> Tuple[str, int]:

    if request.get_json():
        try:
            food = schema.FoodSchema().load(request.get_json())
            db.session.add(food)
            db.session.commit()
            return return_result(schema.FoodSchema().dump(food))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422


@app.route('/food/<int:xid>', methods=['PUT'])
@accept('application/json')
def route_food_put(xid: int) -> Tuple[str, int]:

    if request.json:
        food = db.session.query(models.Food).get(int(xid))
        if food:
            try:
                food = schema.FoodSchema().load(request.json,
                                                  instance=food)
                db.session.add(food)
                db.session.commit()
            except ValidationError as err:
                return jsonify({"error": err.messages,
                                "data": None}), 409 if "name" in err.messages.keys() else 422

        return return_result(schema.FoodSchema().dump(food))

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

######################################################################################################
################################ WATER ###############################################################
######################################################################################################

@app.route('/water/<int:xid>', methods=['DELETE'])
def route_water_delete(xid: int) -> Tuple[str, int]:

    water = db.session.query(models.Water).get(int(xid))
    if water:
        db.session.delete(water)
        db.session.commit()
        return jsonify({"message": "Deleted Water '{}'".format(water.name),
                        "data": None}), 200
    else:
        abort(404)


@app.route('/water/', methods=['GET'], endpoint='water_get_all')
def route_water_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:


    if xid:
        return return_result(schema.WaterSchema().dump(db.session.query(models.Water).get(int(xid))))
    else:
        return return_result(schema.WaterSchema(many=True).dump(db.session.query(models.Water).filter(and_(*format_search(models.Water))).all()))


@app.route('/water/', methods=['POST'])
@accept('application/json')
def route_water_post() -> Tuple[str, int]:

    if request.get_json():
        try:
            water = schema.WaterSchema().load(request.get_json())
            db.session.add(water)
            db.session.commit()
            return return_result(schema.WaterSchema().dump(water))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422


@app.route('/water/<int:xid>', methods=['PUT'])
@accept('application/json')
def route_water_put(xid: int) -> Tuple[str, int]:

    if request.json:
        water = db.session.query(models.Water).get(int(xid))
        if water:
            try:
                water = schema.WaterSchema().load(request.json,
                                                  instance=water)
                db.session.add(water)
                db.session.commit()
            except ValidationError as err:
                return jsonify({"error": err.messages,
                                "data": None}), 409 if "name" in err.messages.keys() else 422

        return return_result(schema.WaterSchema().dump(water))

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

######################################################################################################
############################### ACTIVITIES ###########################################################
######################################################################################################

@app.route('/activities/<int:xid>', methods=['DELETE'])
def route_activities_delete(xid: int) -> Tuple[str, int]:

    activities = db.session.query(models.Activities).get(int(xid))
    if activities:
        db.session.delete(activities)
        db.session.commit()
        return jsonify({"message": "Deleted Activities '{}'".format(activities.name),
                        "data": None}), 200
    else:
        abort(404)


@app.route('/activities/', methods=['GET'], endpoint='activities_get_all')
def route_activities_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:


    if xid:
        return return_result(schema.ActivitiesSchema().dump(db.session.query(models.Activities).get(int(xid))))
    else:
        return return_result(schema.ActivitiesSchema(many=True).dump(db.session.query(models.Activities).filter(and_(*format_search(models.Activities))).all()))


@app.route('/activities/', methods=['POST'])
@accept('application/json')
def route_activities_post() -> Tuple[str, int]:

    if request.get_json():
        try:
            activities = schema.ActivitiesSchema().load(request.get_json())
            db.session.add(activities)
            db.session.commit()
            return return_result(schema.ActivitiesSchema().dump(activities))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422


@app.route('/activities/<int:xid>', methods=['PUT'])
@accept('application/json')
def route_activities_put(xid: int) -> Tuple[str, int]:

    if request.json:
        activities = db.session.query(models.Activities).get(int(xid))
        if activities:
            try:
                activities = schema.ActivitiesSchema().load(request.json,
                                                  instance=activities)
                db.session.add(activities)
                db.session.commit()
            except ValidationError as err:
                return jsonify({"error": err.messages,
                                "data": None}), 409 if "name" in err.messages.keys() else 422

        return return_result(schema.ActivitiesSchema().dump(activities))

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

######################################################################################################
############################### TOILET ###############################################################
######################################################################################################

@app.route('/toilet/<int:xid>', methods=['DELETE'])
def route_toilet_delete(xid: int) -> Tuple[str, int]:

    toilet = db.session.query(models.Toilet).get(int(xid))
    if toilet:
        db.session.delete(toilet)
        db.session.commit()
        return jsonify({"message": "Deleted Toilet '{}'".format(toilet.name),
                        "data": None}), 200
    else:
        abort(404)


@app.route('/toilet/', methods=['GET'], endpoint='toilet_get_all')
def route_toilet_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:


    if xid:
        return return_result(schema.ToiletSchema().dump(db.session.query(models.Toilet).get(int(xid))))
    else:
        return return_result(schema.ToiletSchema(many=True).dump(db.session.query(models.Toilet).filter(and_(*format_search(models.Toilet))).all()))


@app.route('/toilet/', methods=['POST'])
@accept('application/json')
def route_toilet_post() -> Tuple[str, int]:

    if request.get_json():
        try:
            toilet = schema.ToiletSchema().load(request.get_json())
            db.session.add(toilet)
            db.session.commit()
            return return_result(schema.ToiletSchema().dump(toilet))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422


@app.route('/toilet/<int:xid>', methods=['PUT'])
@accept('application/json')
def route_toilet_put(xid: int) -> Tuple[str, int]:

    if request.json:
        toilet = db.session.query(models.Toilet).get(int(xid))
        if toilet:
            try:
                toilet = schema.ToiletSchema().load(request.json,
                                                  instance=toilet)
                db.session.add(toilet)
                db.session.commit()
            except ValidationError as err:
                return jsonify({"error": err.messages,
                                "data": None}), 409 if "name" in err.messages.keys() else 422

        return return_result(schema.ToiletSchema().dump(toilet))

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422

######################################################################################################
######################################################################################################
######################################################################################################

@app.route('/thing/<int:xid>', methods=['DELETE'])
@swag_from(documentation.thing_delete, methods=["DELETE"])
def route_thing_delete(xid: int) -> Tuple[str, int]:
    """
    Attempts to delete the thing specified by xid

    Args:
        xid: integer identifier of thing to delete

    Returns:
        Tuple(str, int): JSON string and HTTP status code

    """
    thing = db.session.query(models.Thing).get(int(xid))
    if thing:
        db.session.delete(thing)
        db.session.commit()
        return jsonify({"message": "Deleted Thing '{}'".format(thing.name),
                        "data": None}), 200
    else:
        abort(404)


@app.route('/thing/', methods=['GET'], endpoint='thing_get_all')
@app.route('/thing/<int:xid>', methods=['GET'], endpoint='thing_get_xid')
@swag_from(documentation.thing_get_xid, methods=["GET"], endpoint='thing_get_xid')
@swag_from(documentation.thing_get_all, methods=["GET"], endpoint='thing_get_all')
def route_thing_get(xid: Optional[Union[int, None]] = None) -> Tuple[str, int]:
    """
    Attempts to retrieve thing specified by xid

    Args:
        xid: integer identifier of thing

    Returns:
        Tuple(str, int): JSON string and HTTP status code

    """
    if xid:
        return return_result(schema.ThingSchema().dump(db.session.query(models.Thing).get(int(xid))))
    else:
        return return_result(schema.ThingSchema(many=True).dump(db.session.query(models.Thing).filter(and_(*format_search(models.Thing))).all()))


@app.route('/thing/', methods=['POST'])
@swag_from(documentation.thing_post, methods=["POST"])
@accept('application/json')
def route_device_post() -> Tuple[str, int]:
    """
    Attempts to create a thing from posted JSON (if it exists)

    {
        "name": <str>
        "description": <str>
    }

    Returns:
        Tuple(str, int): JSON string and HTTP status code

    """
    if request.get_json():
        try:
            thing = schema.ThingSchema().load(request.get_json())
            db.session.add(thing)
            db.session.commit()
            return return_result(schema.ThingSchema().dump(thing))
        except ValidationError as err:
            return jsonify({"error": err.messages,
                            "data": None}), 422

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422


@app.route('/thing/<int:xid>', methods=['PUT'])
@swag_from(documentation.thing_put, methods=["PUT"])
@accept('application/json')
def route_device_put(xid: int) -> Tuple[str, int]:
    """
    Attempts to update a thing from posted JSON (if it exists)

    Args:
        xid: integer identifier of thing

    Returns:
        Tuple(str, int): JSON string and HTTP status code

    """
    if request.json:
        thing = db.session.query(models.Thing).get(int(xid))
        if thing:
            try:
                thing = schema.ThingSchema().load(request.json,
                                                  instance=thing)
                db.session.add(thing)
                db.session.commit()
            except ValidationError as err:
                return jsonify({"error": err.messages,
                                "data": None}), 409 if "name" in err.messages.keys() else 422

        return return_result(schema.ThingSchema().dump(thing))

    return jsonify({"error": "No JSON data received",
                    "data": None}), 422
