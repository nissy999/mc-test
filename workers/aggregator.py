import datetime
from typing import Optional, Union

from bson import ObjectId

from common.consts import MONGODB_ID
from common.structs.results import TResultDict


def calc_pair_rank(pair: Union[TResultDict, ObjectId, str],
                   exchange: Optional[TResultDict, ObjectId, str],
                   start_time: Optional[datetime.datetime] = None,
                   end_time: Optional[datetime.datetime] = None) -> float:
    if not end_time:
        end_time = datetime.datetime.utcnow()
    if not start_time:
        start_time = end_time - datetime.timedelta(days=1)





