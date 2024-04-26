from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, load_applications_from_db, add_job_to_db
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
auth = HTTPBasicAuth()


users = {
  os.environ['ADMIN_USERNAME']: generate_password_hash(os.environ['ADMIN_PASSWORD'])
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route("/add_job", methods=['GET', 'POST'])
@auth.login_required
def add_job():
    if request.method == 'POST':
        data = request.form
        add_job_to_db(data)
        return 'Job added successfully!'
    return render_template('add_job.html')


@app.route("/")
def hello_world():
  jobs = load_jobs_from_db()
  return render_template('home.html', 
                         jobs=jobs)
                         

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  
  return render_template('jobpage.html', 
                         job=job)

@app.route("/applications")
def applications():
    applications = load_applications_from_db()
    return render_template('applications.html', applications=applications)

@app.route("/about")
def about():
    return render_template('about.html')






@app.route("/api/job/<id>")
def show_job_json(id):
  job = load_job_from_db(id)
  return jsonify(job)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)


  
  # store this data in the database
  # send an email
  #display an acknowledgement
  return render_template('application_submitted.html',
                         application=data, job=job)
  
  ##return jsonify(data)
##return jsonify(job)
      



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)