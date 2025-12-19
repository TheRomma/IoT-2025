from influxdb_client import InfluxDBClient

client = InfluxDBClient(url="127.0.0.1:8086", token="my-super-secret-token", org="my-org", timeout=180_000)
query_api = client.query_api()

query = '''
from(bucket: "mydb")
|> range(start: -1m)
|> filter(fn: (r) => r._measurement == "mqtt_consumer")
|> filter(fn: (r) => r._field == "value" or r._field == "ts_sent")
|> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
|> map(fn: (r) => {
  t_ms = int(v: int(v: time(v: r._time))/1000000)
  s_ms = int(v: r.ts_sent)
  return {_time: r._time, _value: float(v: t_ms - s_ms), _field: "latency_ms", _measurement: "latency"}
})
|> keep(columns: ["_time", "_value", "_field"])
|> aggregateWindow(every: 1s, fn: mean, createEmpty: false)
|> yield(name: "latency_agg")
'''

tables = query_api.query(query)
i = 0
with open("latency.txt", "w", encoding="utf-8") as file:
	for table in tables:
		for record in table.records:
			val = record.get_value()
			print(i, val)
			i += 1
			file.write(f"{val},\n")
