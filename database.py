from sqlalchemy import create_engine, text

import os

db_connection_string = os.environ['DB_CONNECTION_STRING']



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
def load_applications_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM applications"))
    applications = [row._asdict() for row in result]
    return applications

def add_job_to_db(data):
  with engine.connect() as conn:
    query = text("INSERT INTO jobs (job_id, job_title, job_description) VALUES (:job_id, :job_title, :job_description)")
    conn.execute(query, {'job_id': data['job_id'],
                         'job_title': data['job_title'],
                         'job_description': data['job_description']})
    conn.commit()








def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      jobs.append(row._asdict())
    return jobs
 
def load_job_from_db(id):
    with engine.connect() as conn:
      result = conn.execute(text("select * from jobs where id = :val"), {"val": id})
      rows = result.all()
      if len(rows) == 0:
        return None
      else:
        return rows[0]._asdict()
        
    
    
def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")

    conn.execute(query, {'job_id': job_id,
                         'full_name': data['full_name'],
                         'email': data['email'],
                         'linkedin_url': data['linkedin_url'],
                         'education': data['education'],
                         'work_experience': data['work_experience'],
                         'resume_url': data['resume_url']})
    conn.commit()
   


  
       
        
        
        ##result_dicts.append(row._mapping)



##print(result_dicts)