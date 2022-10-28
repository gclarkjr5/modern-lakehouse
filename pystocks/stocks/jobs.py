import os
from datetime import datetime, timedelta, timezone
import sched
import yfinance as yf
from dagster import job, op, ScheduleDefinition, DefaultScheduleStatus, schedule


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
    if os.path.exists('google.csv'):
        stock_data.to_csv('google.csv', mode='a', header=False, index=True)
    else:
        stock_data.to_csv('google.csv', mode='a', index=True)


@job
def stocks():
    save_stock_data_op(
        get_stock_data_op()
    )


basic_schedule = ScheduleDefinition(
    job=stocks, cron_schedule="* * * * *",
    default_status=DefaultScheduleStatus.RUNNING
)