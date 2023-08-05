# coding: utf8
from typing import Optional

from .....content._types import Strings
from ._enums import ExerciseScheduleType
from ..._object_definition import ObjectDefinition


class BermudanSwaptionDefinition(ObjectDefinition):
    def __init__(
        self,
        exercise_schedule: Optional[Strings] = None,
        exercise_schedule_type: Optional[ExerciseScheduleType] = None,
        notification_days: Optional[int] = None,
    ):
        super().__init__()
        self.exercise_schedule = exercise_schedule
        self.exercise_schedule_type = exercise_schedule_type
        self.notification_days = notification_days

    @property
    def exercise_schedule(self):
        """
        Overridable exercise schedule
        :return: list string
        """
        return self._get_list_parameter(str, "exerciseSchedule")

    @exercise_schedule.setter
    def exercise_schedule(self, value):
        self._set_list_parameter(str, "exerciseSchedule", value)

    @property
    def exercise_schedule_type(self):
        """
        :return: enum ExerciseScheduleType
        """
        return self._get_enum_parameter(ExerciseScheduleType, "exerciseScheduleType")

    @exercise_schedule_type.setter
    def exercise_schedule_type(self, value):
        self._set_enum_parameter(ExerciseScheduleType, "exerciseScheduleType", value)

    @property
    def notification_days(self):
        """
        :return: int
        """
        return self._get_parameter("notificationDays")

    @notification_days.setter
    def notification_days(self, value):
        self._set_parameter("notificationDays", value)
