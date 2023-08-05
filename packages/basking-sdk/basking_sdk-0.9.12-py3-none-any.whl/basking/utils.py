import logging
from datetime import datetime

import pytz


class Utils:
    def __init__(self, basking_obj):
        self.basking = basking_obj
        self.log = logging.getLogger(self.__class__.__name__)
        basking_log_level = logging.getLogger(self.basking.__class__.__name__).level
        self.log.setLevel(basking_log_level)

    def convert_timestamp_to_building_timezone(self, building_id: str, timestamp: datetime) -> datetime:
        """
        :param building_id: the building to get the timezone from
        :param timestamp: no timezone
        # :return: UTC representation of the timestamp in the building's timezone
        """
        building = self.basking.location.get_building(building_id=building_id)
        timezoned_timestamp = pytz.timezone(building['data']['getBuilding']['timeZone']).localize(timestamp)
        return datetime.utcfromtimestamp(timezoned_timestamp.timestamp())
