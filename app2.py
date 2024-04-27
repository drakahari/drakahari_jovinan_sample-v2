# importing from flask module the Flask class, the render_template function, the request function, url_for 
# and redirect function to redirect to index home page after updating the app database
from flask import Flask, render_template, request, url_for, redirect 
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, load_applications_from_db, add_job_to_db
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

uri = os.environ['DB_Mongo_string']
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.flask_database
todos = db.todos

@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == "POST":
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('mongo'))
    all_todos = todos.find()
    return render_template('mongo.html', todos = all_todos)

@app.post("/<id>/delete/")
def delete(id):
    todos.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('mongo'))

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
  return render_template('home.html', jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', job=job)

@app.route("/applications")
def applications():
    applications = load_applications_from_db()
    return render_template('applications.html', applications=applications)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/ack")
def ack():
    return render_template('ack.html')

@app.route("/dir")
def dir():
    return render_template('dir.html')

@app.route("/jira")
def jira():
    return render_template('jira.html')

@app.route("/tools")
def tools():
    return render_template('tools.html')
  
@app.route("/mongo")
def mongo():
    return render_template('mongo.html')

@app.route("/api/job/<id>")
def show_job_json(id):
  job = load_job_from_db(id)
  return jsonify(job)

@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)
  return render_template('application_submitted.html', application=data, job=job)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
