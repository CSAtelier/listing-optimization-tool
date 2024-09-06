from dataclasses import dataclass
from typing import List, Dict


@dataclass
class FeeAmount:
    amount: float
    currency: str


@dataclass
class ComponentFee:
    feeAmount: FeeAmount
    promotionAmount: FeeAmount
    taxAmount: FeeAmount
    total: FeeAmount
    feeNameStringId: str
    timeOfFeesEstimate: float


@dataclass
class PerUnitStorageFee:
    feeAmount: FeeAmount
    promotionAmount: FeeAmount
    taxAmount: FeeAmount
    total: FeeAmount
    id: str
    feeNameStringId: str
    timeOfFeesEstimate: float
    componentFees: List[ComponentFee]


@dataclass
class OtherFeeInfo:
    feeAmount: FeeAmount
    promotionAmount: FeeAmount
    taxAmount: FeeAmount
    total: FeeAmount
    id: str
    feeNameStringId: str
    timeOfFeesEstimate: float


@dataclass
class ProgramFeeResult:
    perUnitPeakStorageFee: PerUnitStorageFee
    perUnitNonPeakStorageFee: PerUnitStorageFee
    otherFeeInfoMap: Dict[str, OtherFeeInfo] 
    futureFeeInfoMap: Dict[str, OtherFeeInfo]


@dataclass
class ProgramFeeResultMap:
    Core: ProgramFeeResult
    MFN: ProgramFeeResult


@dataclass
class FeeDetailsData:
    countryCode: str
    merchantId: str
    programFeeResultMap: ProgramFeeResultMap


@dataclass
class FeeDetailsResponse:
    succeed: bool
    data: FeeDetailsData
