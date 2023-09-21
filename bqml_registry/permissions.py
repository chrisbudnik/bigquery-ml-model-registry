from enum import Enum


class RequiredPermissions(Enum):
    ALL = [
        "bigquery.datasets.create",
        "bigquery.datasets.get",
        "bigquery.tables.create",
        "bigquery.tables.updateData"
    ]