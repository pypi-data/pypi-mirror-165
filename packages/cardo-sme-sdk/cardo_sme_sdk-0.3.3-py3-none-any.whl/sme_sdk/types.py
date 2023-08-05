from typing import TypedDict


class BatchResultType(TypedDict):
    failed_data_points: list[str]
    missing_data_points: list[str]
    companies: list[dict]
