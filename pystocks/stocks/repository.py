import os
from dagster import repository
from .jobs import stocks, basic_schedule


@repository
def stocks_repository():
    return [stocks, basic_schedule]
