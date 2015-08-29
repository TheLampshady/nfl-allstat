from datetime import timedelta

MONITOR_QUEUE = {
    'name': 'monitor-lead-activities',
    'time_delta': dict(crime=timedelta(hours=10)),
}