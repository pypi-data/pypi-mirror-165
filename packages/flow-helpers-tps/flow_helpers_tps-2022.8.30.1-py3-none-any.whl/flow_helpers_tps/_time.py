import pendulum

def get_dates(start_date=None, end_date='yesterday', lookback=7, partition_type='days', partition_gap=1,
              format='YYYY-MM-DD HH:mm:ss'):
    """
    :param start_date: special word (today, yesterday, tomorrow) or ISO 8601 string representation of date
    :param end_date: special word (today, yesterday, tomorrow) or ISO 8601 string representation of date
    :param lookback: force construct start_date using end_date-lookback
    :param partition: how to partition period between start_date and end_date (None, days, months)
    :param format: return format for date string
    :return: list of tuple date strings
    """

    if end_date == 'today':
        end_date = pendulum.today()
    elif end_date == 'yesterday':
        end_date = pendulum.yesterday()
    elif end_date == 'tomorrow':
        end_date = pendulum.tomorrow()
    else:
        end_date = pendulum.parse(end_date)

    if start_date is None:
        start_date = end_date.add(days=-lookback)
    elif start_date == 'today':
        start_date = pendulum.today()
    elif start_date == 'yesterday':
        start_date = pendulum.yesterday()
    elif start_date == 'tomorrow':
        start_date = pendulum.tomorrow()
    else:
        start_date = pendulum.parse(start_date)

    if partition_type is None:
        return [(start_date.format(format), end_date.format(format))]
    else:
        period = pendulum.period(start_date, end_date)
        if partition_type == 'days':
            return [(dt.format(format), dt.add(days=partition_gap).format(format)) for dt in
                    period.range(partition_type)]
        elif partition_type == 'weeks':
            return [(dt.format(format), dt.add(days=partition_gap * 7).format(format)) for dt in
                    period.range(partition_type)]
        elif partition_type == 'months':
            return [(dt.format(format), dt.add(months=partition_gap).format(format)) for dt in
                    period.range(partition_type)]
        elif partition_type == 'years':
            return [(dt.format(format), dt.add(years=partition_gap).format(format)) for dt in
                    period.range(partition_type)]
        else:
            print(f'Not able to partition using {partition_type}')