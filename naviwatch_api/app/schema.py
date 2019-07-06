from sqlalchemy.inspection import inspect
from marshmallow import post_dump, validates_schema, ValidationError, fields
from app import models, ma, db
from typing import List, Dict, Optional, Union


def _includeprops(model: object,
                  exclude: Optional[List[str]] = None,
                  include: Optional[List[str]] = None,
                  excludeids: bool = True) -> List[str]:
    """
    returns a string list of sqlalchemy model property names to be included in marshmallow output

    Args:
        model (:obj:): SqlAlchemy Model instance
        exclude (:obj:`list` of :obj:`str`, optional): specifically exclude these property names
        include (:obj:`list` of :obj:`str`, optional): specifically include these property names - overrides excludeids
        excludeids (bool): exclude properties whose name ends in '_xid'

    Returns:
        List[str]: List of property names to be included in schema view

    """

    i = list()
    e = list()
    if isinstance(exclude, list):
        e.extend(exclude)
    if isinstance(include, list):
        i.extend(include)
    for prop in inspect(model)._props.keys():
        if prop[0] != "_" and prop not in e:
            if excludeids and prop[-4:] == "_xid" and prop not in i:
                continue
            i.append(prop)
    return i


class BaseSchema(ma.ModelSchema):
    """
    Base Marshmallow Schema inherited from Flask-Marshmallow instance. Implements default sqla_session and post dump def
    that ignores first level keys with no value set

    """
    class Meta:
        sqla_session = db.session

    @staticmethod
    def is_not_null(value: Union[str, List, int, Dict, bool, float, None]) -> bool:
        """
        Checks if key value is equivalent or equal to None

        Args:
            value: marshmallow schema value to validate

        Returns:
            bool: True if value is not None, else False

        """
        if isinstance(value, list):
            return True if len(value) > 0 else False
        elif isinstance(value, dict):
            return True if len(value.keys()) > 0 else False
        elif value is not None:
            return True
        else:
            return False

    @post_dump
    def skip_null(self, data: dict) -> dict:
        """
        Post dump removal of keys with values equivalent or equal to None

        Args:
            data (:obj:`dict`): Marshmallow schema output

        Returns:
            dict: Dictionary pruned of keys with values equivalent or equal to None

        """
        return {
            key: value for key, value in data.items()
            if self.is_not_null(value)
        }


class PersonSchema(BaseSchema):
    """

    """
    class Meta:
        model = models.Person
        fields = _includeprops(model=model,
                               excludeids=False)

    stuff = fields.Nested('StuffSchema',
                          many=True)

    @validates_schema
    def _validate_Person(self, data):
        """

        Args:
            data: field validated instance of models.Person

        Returns:
            None

        Raises:
            ValidationError: if a Person with the specified name already exists
        """
        if db.session.query(models.Person).filter(models.Person.name == data["name"]).count() == 1:
            raise ValidationError(
                "Person with Name '{}' already exists".format(data["name"]), 'name')


class PetSchema(BaseSchema):
    """

    """
    class Meta:
        model = models.Pet
        fields = _includeprops(model=model,
                               excludeids=False)

    food = fields.Nested('FoodSchema',
                          many=True)
    watercheck = fields.Nested('WatercheckSchema',
                          many=True)
    activities = fields.Nested('ActivitiesSchema',
                          many=True)
    toilet = fields.Nested('ToiletSchema',
                          many=True)

    @validates_schema
    def _validate_Pet(self, data):
        """

        Args:
            data: field validated instance of models.Pet

        Returns:
            None

        Raises:
            ValidationError: if a Pet with the specified name already exists
        """
        if db.session.query(models.Pet).filter(models.Pet.name == data["name"]).count() == 1:
            raise ValidationError(
                "Pet with Name '{}' already exists".format(data["name"]), 'name')


class FoodSchema(BaseSchema):
    """

    """
    class Meta:
        model = models.Food
        fields = _includeprops(model=model,
                               excludeids=False)


class WatercheckSchema(BaseSchema):
    """

    """
    class Meta:
        model = models.Watercheck
        fields = _includeprops(model=model,
                               excludeids=False)


class ActivitiesSchema(BaseSchema):
    """

    """
    class Meta:
        model = models.Activities
        fields = _includeprops(model=model,
                               excludeids=False)


class ToiletSchema(BaseSchema):
    """

    """
    class Meta:
        model = models.Toilet
        fields = _includeprops(model=model,
                               excludeids=False)


###############################################################################

class ThingSchema(BaseSchema):
    """

    """
    class Meta:
        model = models.Thing
        fields = _includeprops(model=model,
                               include=['stuff'],
                               excludeids=False)

    stuff = fields.Nested('StuffSchema',
                          many=True)

    @validates_schema
    def _validate_thing(self, data):
        """

        Args:
            data: field validated instance of models.Thing

        Returns:
            None

        Raises:
            ValidationError: if a thing with the specified name already exists
        """
        if db.session.query(models.Thing).filter(models.Thing.name == data["name"]).count() == 1:
            raise ValidationError(
                "Thing with Name '{}' already exists".format(data["name"]), 'name')


class StuffSchema(BaseSchema):
    """

    """
    class Meta:
        model = models.Stuff
        fields = _includeprops(model=model,
                               excludeids=False)
