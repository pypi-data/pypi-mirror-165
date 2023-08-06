"""
Base classes with custom attributes for updating, serializing and deserializing data classes and enums.
"""
import base64
import json
from abc import ABC
from datetime import date, datetime, tzinfo

from pydantic import BaseModel, create_model

from algora.common.date import date_to_timestamp, datetime_to_timestamp


class Base(ABC, BaseModel):
    """
    Base class used for all data classes.
    """

    class Config:
        # use enum values when using .dict() on object
        use_enum_values = True

        json_encoders = {
            date: date_to_timestamp,
            datetime: datetime_to_timestamp,
            tzinfo: str
        }

    @classmethod
    def cls_name(cls) -> str:
        """
        Get class name.

        Returns:
            str: Class name
        """
        return cls.__name__

    @classmethod
    def new_fields(cls, *args, **kwargs):
        """
        The only fields that need to be returned are fields using the custom algora Annotation class or class that
        contain the custom algora Annotation class

        Cases:
            - Annotated Field:
                class Container:
                    foo: AnnotatedClass.annotation()

                    @classmethod
                    def new_fields(cls):
                        return {'foo': (AnnotatedClass.annotation(), None)}

            - Internal field with a class type that contains an annotated field
                class ContainerSquared(Base):
                    container: Container

                    @classmethod
                    def new_fields(cls, updated_container_cls):
                        return {'container': (updated_container_cls, None)}

        Args:
            *args:
            **kwargs:

        Returns:
            A mapping of the updated fields and types
        """
        return {}

    @classmethod
    def update(cls, *args, **kwargs):
        """
        This method creates a new class instance that can be used for serialization

        Note: the returned class must be used for serialization and object creation for you to see the updated effects

        Example:
            AnnotatedClass.add_types(Fizz)
            c = Container.update()
            c_squared = ContainerSquared.update(c)

            container = c(foo=self.foo)
            container_squared = c_squared(container=container)

        Args:
            *args:
            **kwargs:

        Returns:
            The updated class
        """
        new_fields = cls.new_fields(*args, **kwargs)
        return create_model(cls.__name__, __base__=cls, **new_fields)

    def request_dict(self) -> dict:
        """
        Convert data class to dict. Used instead of `.dict()` to serialize dates as timestamps.

        Returns:
            dict: Serialized data class as dict
        """
        return json.loads(self.json())

    def base64_encoded(self, exclude=None) -> bytes:
        """
        Base-64 encode data class.

        Returns:
            bytes: Base-64 encoded data class as bytes
        """
        json_str = json.dumps(self.json(exclude=exclude), sort_keys=True)
        bytes_rep = bytes(json_str, 'utf-8')
        return base64.b64encode(bytes_rep)
