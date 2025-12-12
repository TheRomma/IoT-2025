from influxdb_client import InfluxDBClient

client = InfluxDBClient(url="127.0.0.1:8086", token="my-super-secret-toke", org="my-org")
query_api = client.query_api()

query = f'''
	from(bucket: "mydb")
	|> range(start: -10s)
'''

tables = query_api.query(query)
for table in tables:
	for record in table.records:
		print(record.get_value())
