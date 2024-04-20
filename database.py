from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://drak:Thispassword!!@drakahari.mysql.database.azure.com/drakaharicareers?charset=utf8mb3"


engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/var/www/html/DigiCertGlobalRootCA.crt.pem"
    }
  })

##old code being left as it helps me understand transfer from database to app.py and then back
  ##print("type(result):", type(result))
  ##result_all = result.all()
  ##print("type(result.all()):" , type(result_all))
  ###print("result.all():" , result_all)
  ##first_result = result_all[0]
  ##print(type(result_all[0]))
  ##print("type(first_result):" , type(first_result))
  ##first_result_dict = dict(result_all[0]) does not work need alternate method
  ##first_result_dict = result_all[0]._asdict()
  ##print("type(first_result_dict):" , type(first_result_dict))
  ##print(first_result_dict)

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      jobs.append(row._asdict())
    return jobs
  ##result_dicts.append(row._mapping)



##print(result_dicts)