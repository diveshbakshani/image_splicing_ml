import os
from datetime import datetime
from flask import Flask, render_template, redirect, request, flash, g
from werkzeug.utils import secure_filename

import sqlite3

from predict import predict

project_dir = os.path.dirname(os.path.abspath(__file__))


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_request
def before_request():
    con = sqlite3.connect('database.db', check_same_thread=False)
    print("Opened database successfully")
    g.db = con

@app.route("/", methods=["GET", "POST"])

def home():
    cur = g.db.cursor()
    results = []
    predict_result="None"
    if request.form:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        # TODO: handle same named files
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # prediction code here
        # authentic = 0/True
        # spliced = 1/False

        #Extract results here
        filepath = os.path.join(os.path.expanduser('~'), 'PycharmProjects', 'image_splicing_ml', 'uploads', filename)
        boolarray = predict(filepath)
        casia_r = boolarray[0]
        columbia_r = boolarray[1]
        columbiauc_r = boolarray[2]

        #TODO: check logical correctness
        if ((casia_r and columbia_r) == True) or ((casia_r and columbiauc_r) == True) or ((columbia_r and columbiauc_r)):
            predict_result = "Authentic"
        else:
            predict_result = "Spliced"

        print(predict_result)

        results.append(casia_r)
        results.append(columbia_r)
        results.append(columbiauc_r)

        # insert into sqlite3 database.db
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        cur.execute("INSERT INTO PREDICTIONS (NAME,FILE,DATE,RESULT) VALUES (?,?,?,?)",(request.form.get('user'), filename, date_time, predict_result))
        print("Inserted values:",(request.form.get('user'), filename, date_time, predict_result))

        g.db.commit()
    return render_template("index.html", result=predict_result, results=results)

@app.route('/admin',methods = ["GET","POST"])
def login():
    cur = g.db.cursor()
    error = None;
    data=[]
    delete = False
    if request.method == "POST":
        if request.form.get('pass') != 'login':
            error = "invalid password"
        else:
            cur.execute("SELECT * FROM PREDICTIONS ORDER BY ID DESC")
            data = cur.fetchall()
            g.db.commit()
            delete = True

    return render_template('admin.html',error=error, data=data, delete=delete)


@app.route("/delete")
def delete():
    cur = g.db.cursor()
    cur.execute("DELETE FROM PREDICTIONS")
    g.db.commit()
    message = "Database cleared"
    print(message)
    return render_template('admin.html', message=message)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/models")
def models():
    return render_template('models.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.after_request
def after_request(response):
    if g.db is not None:
        print('closing database connection')
        g.db.close()
    return response

  
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)