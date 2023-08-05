from typing import Optional

from pydantic import BaseModel


class AzureTable(BaseModel):
    table_name: str
    """Name of the azure table"""

    storage_account_name: str
    """Name of the storage account"""


class AzureTableEntry(AzureTable):
    partition_key: str
    """The partition key of the entry"""

    row_key: str
    """The row key of the entry"""

    entry: str
    """A space separate string defining key=value pairs.
    This would be better represented as a dict, but the Azure CLI requests this format"""
