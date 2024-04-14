from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://drak:Thispassword!!@drakahari.mysql.database.azure.com/drakaharicareers?charset=utf8mb3"


engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/var/www/html/DigiCertGlobalRootCA.crt.pem"
    }
  })

with engine.connect() as conn:
  result = conn.execute(text("select * from jobs"))
  print(result.all())