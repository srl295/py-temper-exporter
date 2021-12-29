import time
from prometheus_client import start_http_server, Gauge, Enum
from temper import Temper

def main():
    port = 9204
    t = Temper()
    label_names = ['vendorid','productid','busnum','devnum']
    temp_c = Gauge('temper_internal_temperature_celsius', 'Temperature in °C', label_names)
    humid = Gauge('temper_internal_humidity_percent', 'Humidity in percent', label_names)
    report_time = Gauge('temper_time', 'Time of report', label_names)
    print('Listening on port %d' % port)
    start_http_server(port)
    while True:
        data = t.read()
        # print(data)
        for d in data:
            l = []
            for label in label_names:
                l.append(str(d[label]))
            # print(l)
            temp_c.labels(*l).set(d['internal temperature'])
            humid.labels(*l).set(d['internal humidity'])
            report_time.labels(*l).set_to_current_time()
        time.sleep(500)
