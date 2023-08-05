from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from model.config.core import config


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    relevant_data = input_data[config.model_config.features].copy()
    validated_data = relevant_data
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleMortgageDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class MortgageDataInputSchema(BaseModel):
    AP001: Optional[int]
    AP002: Optional[int]
    AP003: Optional[int]
    AP004: Optional[int]
    AP005: Optional[str]
    AP006: Optional[str]
    AP007: Optional[int]
    AP008: Optional[int]
    AP009: Optional[int]
    TD001: Optional[int]
    TD002: Optional[int]
    TD005: Optional[int]
    TD006: Optional[int]
    TD009: Optional[int]
    TD010: Optional[int]
    TD013: Optional[int]
    TD014: Optional[int]
    TD015: Optional[int]
    TD022: Optional[float]
    TD023: Optional[float]
    TD024: Optional[float]
    TD025: Optional[float]
    TD026: Optional[float]
    TD027: Optional[float]
    TD028: Optional[float]
    TD029: Optional[float]
    TD055: Optional[float]
    CR004: Optional[int]
    CR005: Optional[int]
    CR009: Optional[int]
    CR012: Optional[int]
    CR015: Optional[int]
    CR017: Optional[int]
    CR018: Optional[int]
    CR019: Optional[int]
    PA022: Optional[str]
    PA023: Optional[float]
    PA028: Optional[float]
    PA029: Optional[float]
    PA030: Optional[float]
    PA031: Optional[float]
    CD008: Optional[float]
    CD018: Optional[float]
    CD071: Optional[float]
    CD072: Optional[float]
    CD088: Optional[float]
    CD100: Optional[float]
    CD101: Optional[float]
    CD106: Optional[float]
    CD107: Optional[float]
    CD108: Optional[float]
    CD113: Optional[float]
    CD114: Optional[float]
    CD115: Optional[float]
    CD117: Optional[float]
    CD118: Optional[float]
    CD120: Optional[float]
    CD121: Optional[float]
    CD123: Optional[float]
    CD130: Optional[float]
    CD131: Optional[float]
    CD132: Optional[float]
    CD133: Optional[float]
    CD135: Optional[float]
    CD136: Optional[float]
    CD137: Optional[float]
    CD152: Optional[float]
    CD153: Optional[float]
    CD160: Optional[float]
    CD162: Optional[float]
    CD164: Optional[float]
    CD166: Optional[float]
    CD167: Optional[float]
    CD169: Optional[float]
    CD170: Optional[float]
    CD172: Optional[float]
    CD173: Optional[float]
    MB005: Optional[float]
    MB007: Optional[str]


class MultipleMortgageDataInputs(BaseModel):
    inputs: List[MortgageDataInputSchema]
