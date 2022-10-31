import os
from datetime import datetime, timedelta, timezone
import yfinance as yf
from dagster import op, job, repository, schedule, ScheduleDefinition, DefaultScheduleStatus


@op
def get_stock_data_op():
    yesterday = datetime.now()
    yesterday = yesterday.replace(tzinfo=timezone.utc)
    yesterday = yesterday - timedelta(1)

    two_days_ago = yesterday - timedelta(1)

    start_date = datetime.strftime(two_days_ago, '%Y-%m-%d')
    end_date = datetime.strftime(yesterday, '%Y-%m-%d')

    obj = yf.Ticker('goog')
    df = obj.history(start=start_date, end=end_date, tz='UTC')

    return df


@op
def save_stock_data_op(stock_data):
    target_file = '/var/lib/data/google.csv'
    if os.path.exists(target_file):
        stock_data.to_csv(target_file, mode='a', header=False, index=True)
    else:
        stock_data.to_csv(target_file, mode='a', index=True)


@job
def stocks():
    save_stock_data_op(
        get_stock_data_op()
    )


basic_schedule = ScheduleDefinition(
    job=stocks, cron_schedule="* * * * *",
    default_status=DefaultScheduleStatus.RUNNING
)


@repository
def stocks_repository():
    return [stocks, basic_schedule]
