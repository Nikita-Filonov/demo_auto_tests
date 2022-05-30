from typing import Optional

from models_manager import Field, Model


class SortModel(Model):
    """
    This model used to get schema for sorting response.
    Keep in mind that this model does not exists in database.
    """
    data = Field(default=list, json='data', category=list)
    total_count = Field(default=10, json='totalCount', category=int)
    group_count = Field(default=-1, json='groupCount', category=int)
    summary = Field(json='summary', category=Optional[str], null=True)
