from dataclasses import dataclass
from enum import Enum
from typing import List, Union

import pandas as pd

### Abstractions to represent (a list of) either meteringpoints or substations


class ModelTargetLevel(Enum):

    METERING_POINT = 1
    SUBSTATION = 2


@dataclass
class ModelTargetList:

    level: ModelTargetLevel
    identifiers: Union[List[str], List[int]]


@dataclass
class MeteringPointList(ModelTargetList):

    level = ModelTargetLevel.METERING_POINT
    identifiers: List[int]


@dataclass
class SubstationList(ModelTargetList):

    level = ModelTargetLevel.SUBSTATION
    identifiers: List[str]


### Dataframe groupings


@dataclass
class IngestedDataframes:
    """
    Dataframes ready for use in the enrichment stage
    """
    weekly_average: pd.DataFrame
    school_holidays: pd.DataFrame
    national_holidays: pd.DataFrame
    prices: pd.DataFrame


@dataclass
class Dataframes:
    """
    This class is a convenient encapsulation of diverse dataframes
    """
    hourly_consumption: pd.DataFrame
    ingested: IngestedDataframes
