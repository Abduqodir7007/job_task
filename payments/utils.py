from datetime import datetime, timedelta, date
from django.db.models import Q

def parse_dates(start_date_str=None, end_date_str=None):
    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    else:
        start_date = None

    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    else:
        end_date = None

    return start_date, end_date


def build_date_filter(start_date_str=None, end_date_str=None):
    start_date, end_date = parse_dates(start_date_str, end_date_str)
    filter = Q()
    if start_date or end_date:
        if start_date:
            filter &= Q(created_at__date__gte=start_date)
        if end_date:
            filter &= Q(created_at__date__lte=end_date)
    return filter