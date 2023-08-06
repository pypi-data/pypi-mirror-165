"""
Common models.
"""
from datetime import datetime
from typing import Optional

from pydantic import Field as pyField

from algora.common.base import Base
from algora.common.enum import FieldType
from algora.common.type import Datetime


class Field(Base):
    logical_name: str
    type: FieldType


class DataRequest(Base):
    """
    Base data request, inherited by all instrument-specific data request classes.
    """
    as_of_date: Optional[Datetime] = pyField(default=None)
    start_date: Optional[datetime] = pyField(default=None)
    end_date: Optional[datetime] = pyField(default=None)
    as_of: Optional[datetime] = pyField(default=None)
