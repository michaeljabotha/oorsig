from celery import shared_task
import requests
from ping3 import ping

from .models import Monitor, Result

@shared_task()
def check_monitor(monitor_id):
    monitor = Monitor.objects.get(id=monitor_id)
    if monitor.type == "http":
        check_http_monitor.delay(monitor_id)
    elif monitor.type == "ping":
        check_ping_monitor.delay(monitor_id)

@shared_task()
def check_http_monitor(monitor_id):
    monitor = Monitor.objects.get(id=monitor_id)
    r = requests.get(monitor.url, timeout=monitor.timeout, allow_redirects=True)
    result = Result()
    result.monitor = monitor
    r.elapsed
    if r.status_code in monitor.options["allowed_status_codes"]:
        result.rtt = r.elapsed.total_seconds()*1000
        result.result["status_code"] = r.status_code
        result.set_pass()
    else:
        result.result["status_code"] = r.status_code
        result.set_fail()
    
    result.save()

@shared_task()
def check_ping_monitor(monitor_id):
    monitor = Monitor.objects.get(id=monitor_id)
    r = ping(monitor.hostname, unit='ms')
    result = Result()
    result.monitor = monitor
    if r:
        result.rtt = r
        result.set_pass()
    elif r == False:
        result.result["status"] = "Host Unknown (cannot resolve)"
    elif r is None:
        result.result["status"] = "Timed Out (no reply)"
    else:
        result.result["status"] = f"{r}"
    
    result.save()

@shared_task()
def checkit():
    print("hello")