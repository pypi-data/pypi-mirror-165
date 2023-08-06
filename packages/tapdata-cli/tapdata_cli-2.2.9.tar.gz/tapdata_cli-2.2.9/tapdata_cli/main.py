from tapdata_cli import cli
server = "139.198.127.204:31176"
access_code = "3324cfdf-7d3e-4792-bd32-571638d4562f"
cli.init(server, access_code)
mysql = cli.DataSource("mysql", name="mysql_66ss66")
mysql.host("106.55.169.3:3306").db("INSURANCE").username("TAPDATA").password("Gotapd8!").type("source").props("")
mysql.save()
