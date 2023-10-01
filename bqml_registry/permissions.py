from enum import Enum


class RequiredPermissions(Enum):
    ALL = [
        "bigquery.datasets.create"
        "bigquery.datasets.get"
        "bigquery.datasets.getIamPolicy"
        "bigquery.models.getData"
        "bigquery.models.getMetadata"
        "bigquery.tables.create"
        "bigquery.tables.get"
        "bigquery.tables.updateData"
        "bigquery.jobs.create"
        "bigquery.readsessions.create"
        "bigquery.readsessions.getData"
        "bigquery.jobs.listAll"
    ]