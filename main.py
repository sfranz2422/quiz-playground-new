from flask import Flask, render_template, send_from_directory, url_for, redirect, render_template, request, flash, send_from_directory, send_file, jsonify, make_response, session
from werkzeug.utils import secure_filename
from csv import DictReader
import uuid
import csv
import json
import os
import random
from pathlib import Path
from replit.object_storage import Client
import io
import pathlib
import hashlib
import requests
import re
import datetime
import stripe
import html
import openai
from flask_sitemapper import Sitemapper
from youtube_transcript_api import YouTubeTranscriptApi


# from flask_mail import Mail, Message
from twilio.rest import Client as TC
# from mailersend import emails

client = Client()
# import psycopg2.pool
# pool = psycopg2.pool.SimpleConnectionPool(0, 80, os.environ['DATABASE_URL'])

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
# DOWNLOAD_FOLDER = 'download'

import psycopg

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['APP_SECRET']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


openai.api_key = os.environ['OPEN_AI_KEY']

# app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

# strip.api_key = os.environ['STRIPE_API_KEY']

sitemapper = Sitemapper()
sitemapper.init_app(app)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilioClient = TC(account_sid, auth_token)

# verification = client.verify \
#                      .v2 \
#                      .services('VAd75f9822ef937c024e4aa6ee06d0433c') \
#                      .verifications \
#                      .create(to='+17249771109', channel='sms')

# print(verification.account_sid)

# Get a connection from the pool
# conn = psycopg2.connect(
#     host=os.environ['PGHOST'],
#     database=os.environ['PGDATABASE'],
#     user=os.environ['PGUSER'],
#     password=os.environ['PGPASSWORD']
# )

# Create a cursor using the connection
# cur = conn.cursor()

# with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD']) as conn:
#     with conn.cursor() as cur:
#         cur.execute("""
#             SELECT * FROM users;
#             """)
#         list = cur.fetchall()

# print(list)

# cur.execute(
#     """
#     CREATE TABLE complete_questions (
#         id SERIAL PRIMARY KEY,
#         quizId VARCHAR(255),
#         questionNumber VARCHAR(255),
#         questionText VARCHAR(255),
#         answer1 VARCHAR(255),
#         answer2 VARCHAR(255),
#         answer3 VARCHAR(255),
#         answer4 VARCHAR(255),
#         correctAnswer VARCHAR(255),
#         questionSetTitle VARCHAR(255),
#         questionSetDescription VARCHAR(255),
#         questionSetPrivate VARCHAR(255),
#         teacherId VARCHAR(255)
#     )
#     """
# )

# cur.execute(
#     """
#     CREATE TABLE results (
#         id SERIAL PRIMARY KEY,
#         questionId INTEGER,
#         correct INTEGER,
#         teacherId INTEGER
#     )
#     """
# )
# conn.commit()
# cur.close()
# conn.close()

# cur.execute(
#     """
#     CREATE TABLE users (
#         teacherId SERIAL PRIMARY KEY,
#         email VARCHAR(100) NOT NULL,
#         password VARCHAR(255) NOT NULL
#     )
#     """
# )

# cur.execute(
# """
# INSERT INTO users (email, password) VALUES ('stephenfranz22@gmail.com', '0ef15de6149819f2d10fc25b8c994b574245f193');
# """
# )

# cur.execute(
#     """
#     CREATE TABLE login_attempts (
#         id SERIAL PRIMARY KEY,
#         ipaddress VARCHAR(100) NOT NULL,
#         date VARCHAR(255) NOT NULL
#     )
#     """
# )

@app.route('/downloadv2')
def download_filev2():
    path = "quiz_playground_template.csv"
    return send_file(path, as_attachment=True)

@app.route('/download')
def download_file():
    # client.download_as_text("quiz_playground_template.csv")
    file_bytes = client.download_as_bytes("quiz_playground_template.csv")
    mem = io.BytesIO()
    mem.write(file_bytes)
    mem.seek(0)
    return send_file(mem,
                     as_attachment=True,
                     download_name="quiz_playground_template.csv")
    # return redirect(url_for('upload'))


def get_random_string():
    keep_going = True


    while(keep_going):
        alpha = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
        num = '23456789'
        code = ''
    
        r = random.randint(0, 23)
        code += alpha[r]
        r = random.randint(0, 7)
        code += num[r]
        code += '-'
        r = random.randint(0, 23)
        code += alpha[r]
        r = random.randint(0, 7)
        code += num[r]
        code += '-'
        r = random.randint(0, 23)
        code += alpha[r]
        r = random.randint(0, 7)
        code += num[r]
        code += '-'
        r = random.randint(0, 23)
        code += alpha[r]
        r = random.randint(0, 7)
        code += num[r]
        
        with psycopg.connect(host=os.environ['PGHOST'],
             dbname=os.environ['PGDATABASE'],
             user=os.environ['PGUSER'],
             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "SELECT * FROM quizids WHERE quizId = %s"
                data = (code, )
    
                cur.execute(SQL, data)
                r = cur.fetchall()
    
                if r:
                    keep_going = True
    
                else:
                    keep_going = False
                    with psycopg.connect(host=os.environ['PGHOST'],
                         dbname=os.environ['PGDATABASE'],
                         user=os.environ['PGUSER'],
                         password=os.environ['PGPASSWORD']) as conn:
                        with conn.cursor() as cur:
            

                            SQL = "INSERT INTO quizids (quizId) VALUES (%s)"
                            data = (code, )
        
                            cur.execute(SQL, data)

                    
                            return code
                



def getDatabaseConnection(query):

    with psycopg.connect(host=os.environ['PGHOST'],
                         dbname=os.environ['PGDATABASE'],
                         user=os.environ['PGUSER'],
                         password=os.environ['PGPASSWORD']) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            list = cur.fetchall()

    # print(list)
    return list

    # global conn
    # print(conn.closed)

    # while True:
    #     if conn.closed == 2:
    #         print("new connection")
    #         conn = psycopg2.connect(
    #                 host=os.environ['PGHOST'],
    #                 database=os.environ['PGDATABASE'],
    #                 user=os.environ['PGUSER'],
    #                 password=os.environ['PGPASSWORD']
    #                 )
    #         cur = conn.cursor()
    #         return cur
    #         break

    #     try:
    #         cur = conn.cursor()
    #         print("re-using connection")
    #         return cur
    #         break
    #     except:
    #         print("new connection in except block")
    #         conn = psycopg2.connect(
    #                 host=os.environ['PGHOST'],
    #                 database=os.environ['PGDATABASE'],
    #                 user=os.environ['PGUSER'],
    #                 password=os.environ['PGPASSWORD']
    #                 )
    #         # cur = conn.cursor()
    #         continue


# while True:
#     conn = psycopg2.connect(database="****", user="postgres", password="*****", host="localhost", port="5432")
#     cur = conn.cursor()
#     try:
#         cur.execute('''select * from xyz''')
#     except psycopg2.OperationalError:
#         continue
#     break;

# if conn.closed == 1:
#     print("new connection")
#     conn = psycopg2.connect(
#             host=os.environ['PGHOST'],
#             database=os.environ['PGDATABASE'],
#             user=os.environ['PGUSER'],
#             password=os.environ['PGPASSWORD']
#             )
#     cur = conn.cursor()
#     return cur
# else:
#     print("re-using connection")
#     cur = conn.cursor()
# return cur


def get_private_question_sets(teacherId):


    with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
        with conn.cursor() as cur:
            # SQL = "SELECT DISTINCT quizId, questionSetTitle, questionSetDescription FROM complete_questions WHERE teacherId = %s ORDER BY questionSetTitle"
            SQL = "SELECT DISTINCT ON (questionSetTitle, quizId) quizId, questionSetTitle, questionSetDescription timestamp FROM complete_questions WHERE teacherId = %s ORDER BY questionSetTitle, quizId"
            data = (teacherId, )

            cur.execute(SQL, data)
            myresult = cur.fetchall()



    return myresult


def get_all_question_sets():


    
    query = """
         SELECT DISTINCT quizId, questionSetTitle, questionSetDescription, subject
         FROM complete_questions
         WHERE questionSetPrivate = '0'
         """
    myresult = getDatabaseConnection(query)

    return myresult


def getOneQuestionSet(questionSetId):


    with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
        with conn.cursor() as cur:
            SQL = "SELECT * FROM complete_questions WHERE quizId = %s ORDER BY questionNumber, id DESC"
            data = (questionSetId, )

            cur.execute(SQL, data)
            myresult = cur.fetchall()

  
    return myresult


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    # cur = getDatabaseConnection()
    if request.method == 'POST' and 'token' in request.form:
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            # change filename to random value here
            filename = get_random_string() + ".csv"

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # print(filename)


            questionSetTitle = request.form['QuestionSetTitle']
            questionSetDescription = request.form['QuestionSetDescription']
   

            if request.form.get('questionSetPrivate'):
                questionSetPrivate = '1'
            else:
                questionSetPrivate = '0'

            # print(questionSetPrivate)

      
            subject = request.form['subject']
            teacherId = request.form['teacherId']
            teacherId = int(teacherId)
            listOfQuestions = csv_to_dict(f"uploads/{filename}",
                                          questionSetTitle,
                                          questionSetDescription,
                                          questionSetPrivate, teacherId,subject)

            quizId = filename[:-4]

     

            with psycopg.connect(host=os.environ['PGHOST'],
                                 dbname=os.environ['PGDATABASE'],
                                 user=os.environ['PGUSER'],
                                 password=os.environ['PGPASSWORD']) as conn:
                for question in listOfQuestions:
                    with conn.cursor() as cur:
                        cur.execute(
                            f"INSERT INTO complete_questions (quizId, questionNumber, questionText, answer1, answer2, answer3,answer4,correctAnswer,questionSetTitle,questionSetDescription,questionSetPrivate,teacherId, subject) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (f"{quizId}", question['questionNumber'],
                             f"{question['questionText']}",
                             f"{question['answer1']}",
                             f"{question['answer2']}",
                             f"{question['answer3']}",
                             f"{question['answer4']}",
                             f"{question['correctAnswer']}",
                             f"{question['questionSetTitle']}",
                             f"{question['questionSetDescription']}",
                             f"{question['questionSetPrivate']}",
                             question['teacherId'],f"{question['subject']}"))


            try:
                os.remove(f"uploads/{filename}")
            except OSError:
                pass

            return redirect(url_for('displayPrivateQuestionSets'))
    return redirect(url_for('upload'))


def json_to_string(file):
    with open(f"jsons/{file}.json", "r") as fo:
        json_string = fo.read()


#     print(json_string)
    return (json_string)


@app.route('/getQuestionSet/<set>')
def getQuestionSet(set):

    with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
        with conn.cursor() as cur:
            SQL = "SELECT row_to_json(complete_questions) FROM complete_questions WHERE quizid = %s;"
            data = (set, )

            cur.execute(SQL, data)
            myresult = cur.fetchall()

    


    return myresult


# @app.route('/game2')
# def game2():
#     name = "gametemplate.html"
#     response = send_from_directory(f'./templates', name)
#     response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
#     response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
#     return response

@app.route('/climb')
def climb():
    loggedIn, subscribed, teacherId = checkPermissions()
    response = make_response(
        render_template('climb.html', subscribed=subscribed))
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response


@app.route('/arthur')
def arthur():
    loggedIn, subscribed, teacherId = checkPermissions()
    response = make_response(
        render_template('gametemplate.html', subscribed=subscribed))
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route('/cannon')
def cannon():
    loggedIn, subscribed, teacherId = checkPermissions()
    response = make_response(
        render_template('cannon.html', subscribed=subscribed))
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route('/memory')
def memory():
    loggedIn, subscribed, teacherId = checkPermissions()
    response = make_response(
        render_template('memory.html', subscribed=subscribed))
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route('/tower')
def tower():
    loggedIn, subscribed, teacherId = checkPermissions()
    response = make_response(
        render_template('tower.html', subscribed=subscribed))
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response


@app.route('/asteroido')
def asteroido():
    loggedIn, subscribed, teacherId = checkPermissions()
    response = make_response(
        render_template('asteroido.html', subscribed=subscribed))
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route('/warehouse')
def warehouse():
    loggedIn, subscribed, teacherId = checkPermissions()
    response = make_response(
        render_template('warehouse.html', subscribed=subscribed))
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route('/cybercity')
def cybercity():
    loggedIn, subscribed, teacherId = checkPermissions()
    response = make_response(
        render_template('cybercity.html', subscribed=subscribed))
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route('/outpostAssault')
def outpost():
    loggedIn, subscribed, teacherId = checkPermissions()
    response = make_response(
        render_template('assault.html', subscribed=subscribed))
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route('/upload_success/<code>')
def upload_success(code):
    return render_template("upload_success.html", code=code)


def makeRandomTableName():
    string = ""
    alpha = "abcdefghijklmnopqrstuvwxyz"

    for _ in range(10):
        index = random.randint(0, 25)
        string += alpha[index]

    return string
    
    
    

@app.route('/copy/<quizid>')
def copy(quizid):
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
        newQuizId = get_random_string()

        dbname = makeRandomTableName()
        
        with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
            with conn.cursor() as cur:
                SQL = f"CREATE table {dbname} AS SELECT * FROM complete_questions WHERE quizid = %s"
                data = (quizid, )
                cur.execute(SQL, data)

                SQL = f"UPDATE {dbname} SET quizid = %s, teacherid = %s"
                data = (newQuizId, teacherId, )
                cur.execute(SQL, data)

                SQL = f"ALTER TABLE {dbname} DROP COLUMN id"
                cur.execute(SQL)


                SQL = f"""INSERT INTO complete_questions (quizid, questionnumber, questiontext, answer1, answer2, answer3, answer4, correctanswer, questionsettitle, questionsetdescription, questionsetprivate, teacherid, subject)
SELECT quizid, questionnumber, questiontext, answer1, answer2, answer3, answer4, correctanswer, questionsettitle, questionsetdescription, questionsetprivate, teacherid, subject
FROM {dbname};"""
                cur.execute(SQL)

                

                SQL = f"DROP TABLE {dbname}"
                cur.execute(SQL)
                
              
    

    return redirect(url_for("displayPrivateQuestionSets"))


@sitemapper.include(lastmod="2024-06-23")
@app.route('/')
def home():

    # for _ in range(10):
    #     print(get_random_string())

    
    loggedIn, subscribed, teacherId = checkPermissions()

    return render_template("index.html",
                           loggedIn=loggedIn,
                           subscribed=subscribed)



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True:
        username = session['username']

    # print(loggedIn)
    # print(subscribed)
    # print(teacherId)
    token = uuid.uuid4()
    session['token'] = token
    if loggedIn == True and subscribed == True:
        return render_template('upload.html',
                               subscribed=subscribed,
                               teacherId=teacherId,
                               loggedIn=loggedIn,
                               token=token)
    else:
        return render_template('account.html',
                               subscribed=subscribed,
                               loggedIn=loggedIn,
                               username=username,
                               teacherId=teacherId)


def checkPermissions():
    subscribed = False
    loggedIn = False
    teacherId = 0
    if "loggedin" in session and session['subscribed'] == True:
        loggedIn = True
        subscribed = True
        teacherId = session['id']
    elif "loggedin" in session and session['subscribed'] == False:
        subscribed = False
        loggedIn = True
        teacherId = session['id']
    else:
        subscribed = False
        loggedIn = False
        teacherId = ""

    return (loggedIn, subscribed, teacherId)

@app.route('/games')
def games():

    loggedIn, subscribed, teacherId = checkPermissions()

    return render_template("games.html", subscribed=subscribed)

@app.route('/displayQuestionSets')
def displayQuestionSets():
    result = get_all_question_sets()

    loggedIn, subscribed, teacherId = checkPermissions()

    return render_template("displayQuestionSets.html",
                           result=result,
                           loggedIn=loggedIn,
                           subscribed=subscribed)




@app.route('/displayOneQuestionSet/<id>')
def displayOneQuestionSet(id):
    result = getOneQuestionSet(id)

    loggedIn, subscribed, teacherId = checkPermissions()

    return render_template("displayOneQuestionSet.html",
                           result=result,
                           subscribed=subscribed,
                           teacherId=teacherId,
                           loggedIn=loggedIn)


@app.route('/displayPrivateQuestionSets')
def displayPrivateQuestionSets():
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True:
        username = session['username']
    if loggedIn == True and subscribed == True:
        result = get_private_question_sets(teacherId)
        return render_template('displayPrivateQuestionSets.html',
                               subscribed=subscribed,
                               loggedIn=loggedIn,
                               result=result)
    return render_template('account.html',
                           subscribed=subscribed,
                           loggedIn=loggedIn,
                           username=username,
                           teacherId=teacherId)


@app.route('/account')
def account():
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
        username = session['username']
        # print("logged in" + str(loggedIn))
        # print("subscribed in" + str(subscribed))
        # print(teacherId)
        return render_template('account.html',
                               subscribed=subscribed,
                               loggedIn=loggedIn,
                               username=username,
                               teacherId=teacherId)
    return redirect(url_for("home"))


# authur/index.html
@app.route("/arthur/<path:name>")
def arthurGame(name):
    response = send_from_directory(f'./arthur', name)
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route("/cannon/<path:name>")
def cannonGame(name):
    response = send_from_directory(f'./cannon', name)
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route("/memory/<path:name>")
def memoryGame(name):
    response = send_from_directory(f'./memory', name)
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route("/tower/<path:name>")
def towerGame(name):
    response = send_from_directory(f'./tower', name)
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route("/asteroido/<path:name>")
def asteroidoGame(name):
    response = send_from_directory(f'./asteroido', name)
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route("/climb/<path:name>")
def climbGame(name):
    response = send_from_directory(f'./climb', name)
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route("/warehouse/<path:name>")
def warehouseGame(name):
    response = send_from_directory(f'./warehouse', name)
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route("/cybercity/<path:name>")
def cybercityGame(name):
    response = send_from_directory(f'./cybercity', name)
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response

@app.route("/outpostAssault/<path:name>")
def outpostGame(name):
    response = send_from_directory(f'./outpostAssault', name)
    response.headers.add('Cross-Origin-Opener-Policy', 'same-origin')
    response.headers.add('Cross-Origin-Embedder-Policy', 'require-corp')
    return response



@app.route('/edit_one_question/<id>')
def edit_one_question(id):
    question = getOneQuestion(id)

    loggedIn, subscribed, teacherId = checkPermissions()

    return render_template("edit_one.html",
                           q=question[0],
                           subscribed=subscribed,
                           loggedIn=loggedIn)

@app.route('/pricing')
def pricing():

    loggedIn, subscribed, teacherId = checkPermissions()

    return render_template("pricing.html",
                           subscribed=subscribed,
                           loggedIn=loggedIn)


def validate_password(password):
    # define our regex pattern for validation
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

    # We use the re.match function to test the password against the pattern
    match = re.match(pattern, password)

    # return True if the password matches the pattern, False otherwise
    return bool(match)




@app.route('/register', methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST" and 'email' in request.form and 'password' in request.form and 'token' in request.form and 'fname' in request.form and 'lname' in request.form and 'school' in request.form:
        fname = request.form['fname']
        lname = request.form['lname']
        school = request.form['school']

        email = request.form['email']
        password = request.form['password']
        passwordrepeat = request.form['passwordrepeat']
        formphone = request.form['phone']

        if passwordrepeat != password:
            msg = "Passwords Don't Match!"
            return render_template("register.html", msg=msg)

        if validate_password(password) == False:
            msg = "Password must be at least 8 characters, at least one uppercase, one lower case and one digit"
            return render_template("register.html", msg=msg)

   

        

        if len(formphone) > 12:
            msg = "Please Enter Phone numbers in the following format 555-555-5555"
            return render_template("register.html", msg=msg)

        
        formphone = formphone.replace("-", "")
        if len(formphone) == 10:
            phone = "+1" + formphone

        salt = password + os.environ['APP_SECRET']
        salt = salt.encode()
        password = hashlib.sha256(salt).hexdigest()

        with psycopg.connect(host=os.environ['PGHOST'],
                             dbname=os.environ['PGDATABASE'],
                             user=os.environ['PGUSER'],
                             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "SELECT * FROM users WHERE email = %s AND password = %s LIMIT 1"
                data = (
                    email,
                    password,
                )

                cur.execute(SQL, data)
                r = cur.fetchall()

    

        if r:
            msg = "Account already exists!"
            return render_template("register.html", msg=msg)

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template("register.html", msg=msg)
        elif not password or not email:
            msg = 'Please fill out the form!'
            return render_template("register.html", msg=msg)
        else:

            keysalt = email + os.environ['APP_SECRET']
            keysalt = keysalt.encode()
            key = hashlib.sha256(salt).hexdigest()

            subscribed = '0'
            tfa = uuid.uuid4()
            tfa = str(tfa)
            tfa = tfa[:4]
            tfa = tfa.upper()

            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ip = request.environ['REMOTE_ADDR']

            with psycopg.connect(host=os.environ['PGHOST'],
                                 dbname=os.environ['PGDATABASE'],
                                 user=os.environ['PGUSER'],
                                 password=os.environ['PGPASSWORD']) as conn:
                with conn.cursor() as cur:
                    # cur.execute(f"INSERT INTO users (email, password,subscribed, key, tfa, thedate, ip, phone) VALUES ('{email}', '{password}', '{subscribed}','{key}','{tfa}','{now}','{ip}','{phone}')")

                    SQL = "INSERT INTO users (email, password,subscribed, key, tfa, thedate, ip, phone, fname, lname, school) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    data = (
                        email,
                        password,
                        subscribed,
                        key,
                        tfa,
                        now,
                        ip,
                        phone,
                        fname,
                        lname,
                        school,
                    )

                    cur.execute(SQL, data)

            # query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}' LIMIT 1"
            # r = getDatabaseConnection(query)

            with psycopg.connect(host=os.environ['PGHOST'],
                                 dbname=os.environ['PGDATABASE'],
                                 user=os.environ['PGUSER'],
                                 password=os.environ['PGPASSWORD']) as conn:
                with conn.cursor() as cur:
                    SQL = "SELECT * FROM users WHERE email = %s AND password = %s LIMIT 1"
                    data = (
                        email,
                        password,
                    )

                    cur.execute(SQL, data)
                    r = cur.fetchall()

            # print(r)
            if r:
                session['loggedin'] = False
                session['id'] = r[0][0]
                session['username'] = r[0][1]
                session['subscribed'] = False
                
                phone = r[0][8]

                #send code
                sendCode(phone)

                return redirect(url_for('twofactor'))

            else:
                msg = "Error Creating Account"
                return render_template("register.html", msg=msg, token=token)

    elif request.method == "POST":
        msg = "Please Complete the Form!"
        return render_template("register.html", msg=msg)

    token = uuid.uuid4()
    session['token'] = token
    return render_template("register.html", token=token)


def sendCode(phone):
    verification = twilioClient.verify \
                         .v2 \
                         .services('VAd75f9822ef937c024e4aa6ee06d0433c') \
                         .verifications \
                         .create(to=phone, channel='sms')

    # print(verification.account_sid)


@app.route('/twofactor', methods=['GET', 'POST'])
def twofactor():
    token = uuid.uuid4()
    session['token'] = token
    msg = ""
    loggedIn, subscribed, teacherId = checkPermissions()

    query = f"SELECT * FROM users WHERE teacherid = '{teacherId}'"

    myresult = getDatabaseConnection(query)

    phone = myresult[0][8]

    # #send code
    # sendCode(phone):
    
 
    
    if request.method == "POST" and 'code' in request.form and 'token' in request.form:
        c = request.form['code']

        verification_check = twilioClient.verify \
                             .v2 \
                             .services('VAd75f9822ef937c024e4aa6ee06d0433c') \
                             .verification_checks \
                             .create(to=phone, code=c)

        #verification_check should be approved.

        # print(verification_check.status)
        if verification_check.status == "approved":
            #should go to payment now
            session['loggedin'] = True
            session['id'] = teacherId
            # test link

            if myresult[0][3] == '0':

                #return redirect("https://buy.stripe.com/test_bIYdRO87XdLy8EM288")

                #production link
                return redirect("https://buy.stripe.com/6oE7ua8Amdi17Be4gj")
           
            else:
                return redirect(url_for('account'))

        else:
            msg = "Incorrect Code"
            # session['loggedin'] = False
            # session['subscribed'] = False
            return render_template("twofactor.html",
                                   token=token,
                                   msg=msg,
                                   phone=phone)

    return render_template("twofactor.html", token=token, msg=msg, phone=phone)

@app.route('/forgotpassword', methods=['GET','POST'])
def forgotpassword():
    token = uuid.uuid4()
    session['token'] = token
    msg = ""
    if request.method == "POST" and 'email' in request.form and 'token' in request.form:
        email = request.form['email']
        with psycopg.connect(host=os.environ['PGHOST'],
             dbname=os.environ['PGDATABASE'],
             user=os.environ['PGUSER'],
             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "SELECT * FROM users WHERE email = %s"
                data = (email, )
        
                cur.execute(SQL, data)
                list = cur.fetchall()

                if list:
                    # print(list)
                    phone = list[0][8]
                    #send code with phone
                    sendCode(phone)
                    
                    if phone:
                        session['username'] = email
                        return redirect(url_for('twofactorpassword'))
    
                    else:
                        msg="No Account Found"
                        return render_template("forgotpassword.html", token=token, msg=msg)
                else:
                    msg="No Account Found"
                    return render_template("forgotpassword.html", token=token, msg=msg)
   

    

    return render_template("forgotpassword.html", token=token, msg=msg)




@app.route('/twofactorpassword', methods=['GET', 'POST'])
def twofactorpassword():
    token = uuid.uuid4()
    session['token'] = token
    msg = ""
    email = session['username']
    with psycopg.connect(host=os.environ['PGHOST'],
         dbname=os.environ['PGDATABASE'],
         user=os.environ['PGUSER'],
         password=os.environ['PGPASSWORD']) as conn:
        with conn.cursor() as cur:
            SQL = "SELECT * FROM users WHERE email = %s"
            data = (email, )

            cur.execute(SQL, data)
            list = cur.fetchall()
            
            # print(list)
            phone = list[0][8]
            email = list[0][1]




    if request.method == "POST" and 'code' in request.form and 'token' in request.form:
        c = request.form['code']

        verification_check = twilioClient.verify \
                             .v2 \
                             .services('VAd75f9822ef937c024e4aa6ee06d0433c') \
                             .verification_checks \
                             .create(to=phone, code=c)

        #verification_check should be approved.

        # print(verification_check.status)
        if verification_check.status == "approved":
            session['username'] = email
            return render_template("newpassword.html")
           

        else:
            msg = "Incorrect Code"
            # session['loggedin'] = False
            # session['subscribed'] = False
            return render_template("twofactorpassword.html",
                                   token=token,
                                   msg=msg,
                                   phone=phone)

    return render_template("twofactorpassword.html", token=token, msg=msg, phone=phone)

@app.route('/newpassword', methods=['GET', 'POST'])
def newpassword():
    token = uuid.uuid4()
    session['token'] = token
    msg = ""
    email = session['username'] 
    if request.method == "POST" and 'password' in request.form and 'token' in request.form:
        pw = request.form['password']
        if validate_password(pw) == False:
            msg = "Password must be at least 8 characters, at least one uppercase, one lower case and one digit"
            return render_template('newpassword.html', token=token)


        salt = pw + os.environ['APP_SECRET']
        salt = salt.encode()
        newpass = hashlib.sha256(salt).hexdigest()

        
        with psycopg.connect(host=os.environ['PGHOST'],
             dbname=os.environ['PGDATABASE'],
             user=os.environ['PGUSER'],
             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "UPDATE users SET password = %s WHERE email = %s"
                data = (newpass, email, )

                cur.execute(SQL, data)

                return redirect(url_for('login'))
        

    return render_template('newpassword.html', token=token)
        
@app.route('/confirmation/<checkout_session_id>', methods=['GET'])
def confirmation(checkout_session_id):
    # print("checkout id")
    # print(checkout_session_id)
    if checkout_session_id:
        teacherId = session['id']
        with psycopg.connect(host=os.environ['PGHOST'],
                             dbname=os.environ['PGDATABASE'],
                             user=os.environ['PGUSER'],
                             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "SELECT * FROM users WHERE teacherid = %s"
                data = (teacherId, )

                cur.execute(SQL, data)
                list = cur.fetchall()

                # print("the db lookup")
                # print(list)
        with psycopg.connect(host=os.environ['PGHOST'],
                             dbname=os.environ['PGDATABASE'],
                             user=os.environ['PGUSER'],
                             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "UPDATE users SET subscribed = %s WHERE teacherid = %s"
                data = (
                    1,
                    teacherId,
                )

                cur.execute(SQL, data)

        session['subscribed'] = True
        session['loggedin'] = True

        #turn subscribed on
        # set session cookies
        return redirect(url_for('account'))
    else:
        with psycopg.connect(host=os.environ['PGHOST'],
                             dbname=os.environ['PGDATABASE'],
                             user=os.environ['PGUSER'],
                             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "DELETE FROM users WHERE teacherid = %s"
                data = (teacherId, )

                cur.execute(SQL, data)
        return redirect(url_for('home'))





def getOneQuestion(id):

    with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
        with conn.cursor() as cur:
            SQL = "SELECT * FROM complete_questions WHERE id = %s"
            data = (id, )

            cur.execute(SQL, data)
            myresult = cur.fetchall()




    
    # query = f"SELECT * FROM complete_questions WHERE id = '{id}'"

    # myresult = getDatabaseConnection(query)
    return myresult


@app.route('/editSubmit', methods=['GET', 'POST'])
def editSubmit():
    if request.method == 'POST':
        id = request.form['id']
        quizId = request.form['quizId']
        # questionNumber = request.form['questionNumber']

        questionText = request.form['questionText']
        questionText = questionText.replace("'", "''")

        answer1 = request.form['answer1']
        answer1 = answer1.replace("'", "''")
        answer2 = request.form['answer2']
        answer2 = answer2.replace("'", "''")
        answer3 = request.form['answer3']
        answer3 = answer3.replace("'", "''")
        answer4 = request.form['answer4']
        answer4 = answer4.replace("'", "''")

        if request.form['correctAnswer'] == 'A':
            correctAnswer = "1"
        if request.form['correctAnswer'] == 'B':
            correctAnswer = "2"
        if request.form['correctAnswer'] == 'C':
            correctAnswer = "3"
        if request.form['correctAnswer'] == 'D':
            correctAnswer = "4"

        # questionSetTitle = request.form['questionSetTitle']
        # questionSetDescription = request.form['questionSetDescription']
        questionSetPrivate = request.form['questionSetPrivate']
        # questionSetTitle= request.form['questionSetTitle']
        # teacherId= request.form['teacherId']

        # cur = getDatabaseConnection()

        with psycopg.connect(host=os.environ['PGHOST'],
                             dbname=os.environ['PGDATABASE'],
                             user=os.environ['PGUSER'],
                             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "UPDATE complete_questions SET questionText = %s WHERE id = %s;"
                Data = (questionText, id, )
                cur.execute(SQL,Data)
                # cur.execute(
                #     f"""UPDATE complete_questions SET questionText = '{questionText}' WHERE id = {id};"""
                # )
                SQL = "UPDATE complete_questions SET answer1 = %s WHERE id = %s;"
                Data = (answer1, id, )
                cur.execute(SQL,Data)
                # cur.execute(
                #     f"""UPDATE complete_questions SET answer1 = '{answer1}' WHERE id = {id};"""
                # )
                SQL = "UPDATE complete_questions SET answer2 = %s WHERE id = %s;"
                Data = (answer2, id, )
                cur.execute(SQL,Data)
                # cur.execute(
                #     f"""UPDATE complete_questions SET answer2 = '{answer2}' WHERE id = {id};"""
                # )
                SQL = "UPDATE complete_questions SET answer3 = %s WHERE id = %s;"
                Data = (answer3, id, )
                cur.execute(SQL,Data)
                # cur.execute(
                #     f"""UPDATE complete_questions SET answer3 = '{answer3}' WHERE id = {id};"""
                # )
                SQL = "UPDATE complete_questions SET answer4 = %s WHERE id = %s;"
                Data = (answer4, id, )
                cur.execute(SQL,Data)
                # cur.execute(
                #     f"""UPDATE complete_questions SET answer4 = '{answer4}' WHERE id = {id};"""
                # )
                SQL = "UPDATE complete_questions SET correctAnswer = %s WHERE id = %s;"
                Data = (correctAnswer, id, )
                cur.execute(SQL,Data)
                # cur.execute(
                #     f"""UPDATE complete_questions SET correctAnswer='{correctAnswer}' WHERE id = {id};"""
                # )
                SQL = "UPDATE complete_questions SET questionSetPrivate = %s WHERE id = %s;"
                Data = (questionSetPrivate, id, )
                cur.execute(SQL,Data)
                # cur.execute(
                #     f"""UPDATE complete_questions SET questionSetPrivate='{questionSetPrivate}' WHERE id = {id};"""
                # )

        return redirect(url_for('displayOneQuestionSet', id=quizId))


@app.route('/togglePrivacyOn/<quizId>')
def togglePrivacyOn(quizId):
    loggedIn, subscribed, teacherId = checkPermissions()

    if loggedIn == True and subscribed == True:

        with psycopg.connect(host=os.environ['PGHOST'],
                             dbname=os.environ['PGDATABASE'],
                             user=os.environ['PGUSER'],
                             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "UPDATE complete_questions SET questionsetprivate = '1' WHERE quizId = %s;"
                Data = (quizId, )
                cur.execute(SQL,Data)
                

        return redirect(url_for('displayOneQuestionSet', id=quizId))
    return render_template("index.html",
                           loggedIn=loggedIn,
                           subscribed=subscribed)


@app.route('/togglePrivacyOff/<quizId>')
def togglePrivacyOff(quizId):
    loggedIn, subscribed, teacherId = checkPermissions()

    if loggedIn == True and subscribed == True:
        with psycopg.connect(host=os.environ['PGHOST'],
                             dbname=os.environ['PGDATABASE'],
                             user=os.environ['PGUSER'],
                             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "UPDATE complete_questions SET questionsetprivate = '0' WHERE quizId = %s;"
                Data = (quizId, )
                cur.execute(SQL,Data)


        return redirect(url_for('displayOneQuestionSet', id=quizId))
    return render_template("index.html",
                           loggedIn=loggedIn,
                           subscribed=subscribed)





def csv_to_dict(path, questionSetTitle, questionSetDescription,
                questionSetPrivate, teacherId,subject):
    question_list = []
    dictionary_list = []
    headers = [
        "questionNumber", "questionText", "answer1", "answer2", "answer3",
        "answer4", "correctAnswer", "questionSetTitle",
        "questionSetDescription", "questionSetPrivate", "teacherId","subject"
    ]
    with open(f"{path}", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            question_list.append(row)
    question_list.pop(0)

  
  

    for question in question_list:
        if question[2] == '':
            question[2] = 'Blank'
        if question[3] == '':
            question[3] = 'Blank'
        if question[4] == '':
            question[4] = 'Blank'
        if question[5] == '':
            question[5] = 'Blank'



        d = {
            headers[0]: question[0],
            headers[1]: question[1],
            headers[2]: question[2],
            headers[3]: question[3],
            headers[4]: question[4],
            headers[5]: question[5],
            headers[6]: question[6],
            headers[7]: questionSetTitle,
            headers[8]: questionSetDescription,
            headers[9]: questionSetPrivate,
            headers[10]: teacherId,
            headers[11]: subject
        }
        dictionary_list.append(d)
    # print(dictionary_list)

    return (dictionary_list)


# def getOneUser(email, password):
#     with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
#         with conn.cursor() as cur:
#             SQL = "SELECT * FROM users WHERE email = %s AND password = %s LIMIT 1"
#             data = (email, password, )

#             cur.execute(SQL, data)
#             myresult = cur.fetchall()

#     if myresult:
#         return myresult[0]
#     else:
#         return "Error"


def bruteForce(email,ip):
    with psycopg.connect(host=os.environ['PGHOST'],
         dbname=os.environ['PGDATABASE'],
         user=os.environ['PGUSER'],
         password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "SELECT * FROM login_attempts WHERE ip = %s AND email = %s LIMIT 1"
                data = (ip, email, )
                
            
                cur.execute(SQL, data)
                r = cur.fetchone()

                if not r:
                 
                    attempts = 1
                    with psycopg.connect(host=os.environ['PGHOST'],
                         dbname=os.environ['PGDATABASE'],
                         user=os.environ['PGUSER'],
                         password=os.environ['PGPASSWORD']) as conn:
                            with conn.cursor() as cur:
                                SQL = "INSERT INTO login_attempts (ip, email, attempts) VALUES (%s,%s,%s);"
                                data = (ip, email, attempts)
                                

                                cur.execute(SQL, data)
                                msg = "Incorrect Email/Password"
                                return msg
                else:
                   
                    new_attempts = r[3] + 1
                    if new_attempts <= 5:
                        with psycopg.connect(host=os.environ['PGHOST'],
                             dbname=os.environ['PGDATABASE'],
                             user=os.environ['PGUSER'],
                             password=os.environ['PGPASSWORD']) as conn:
                                with conn.cursor() as cur:
                                    SQL = "UPDATE login_attempts SET attempts = %s WHERE ip = %s"
                                    data = (new_attempts, ip)
    
    
                                    cur.execute(SQL, data)
                                    msg = "Incorrect Email/Password"
                                    return msg
                    else:
                        msg = """Too Many Login Attempts, Contact Customer Service at support@quizplayground.com Or Use Forgot Password"""
                        return msg
                    
                    
              
        
def clearEmail(email,ip):
    try:
        with psycopg.connect(host=os.environ['PGHOST'],
             dbname=os.environ['PGDATABASE'],
             user=os.environ['PGUSER'],
             password=os.environ['PGPASSWORD']) as conn:
                with conn.cursor() as cur:
                    SQL = "DELETE FROM login_attempts WHERE ip = %s and email = %s"
                    data = (ip, email, )
    
    
                    cur.execute(SQL, data)
    except:
        return
    


@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST" and 'email' in request.form and 'password' in request.form and 'token' in request.form:

    
        
        email = request.form['email']
        password = request.form['password']
        salt = password + os.environ['APP_SECRET']
        salt = salt.encode()
        password = hashlib.sha256(salt).hexdigest()

        with psycopg.connect(host=os.environ['PGHOST'],
                             dbname=os.environ['PGDATABASE'],
                             user=os.environ['PGUSER'],
                             password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "SELECT * FROM users WHERE email = %s AND password = %s LIMIT 1"
                data = (
                    email,
                    password,
                )

                cur.execute(SQL, data)
                r = cur.fetchall()

        if r:
            session['loggedin'] = True
            session['id'] = r[0][0]
            session['username'] = r[0][1]
            if r[0][3] == '1':
                session['subscribed'] = True
                #clear email from login attempts
                ip = request.environ['REMOTE_ADDR']
                clearEmail(email,ip)
                return redirect(url_for("account"))
            else:
                #user didn't finish payment reauthenticate and submit for payment
                session['subscribed'] = False

                # send a new code
                phone = r[0][8]
                sendCode(phone)
                return redirect(url_for('twofactor'))

        else:
            
            #brute force protection
            ip = request.environ['REMOTE_ADDR']
            msg = bruteForce(email,ip)
            


    
    token = uuid.uuid4()
    session['token'] = token
    return render_template("login.html", msg=msg, token=token)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('subscribed', None)
    # Redirect to login page
    return render_template('index.html')


@app.route('/faq')
def faq():

    loggedIn, subscribed, teacherId = checkPermissions()

    return render_template('faq.html', loggedIn=loggedIn, subscribed=subscribed, teacherId=teacherId)

@app.route('/help')
def help():

    loggedIn, subscribed, teacherId = checkPermissions()

    return render_template('help.html', loggedIn=loggedIn, subscribed=subscribed, teacherId=teacherId)

@app.route('/credits')
def credits():

    loggedIn, subscribed, teacherId = checkPermissions()

    return render_template('credits.html', loggedIn=loggedIn, subscribed=subscribed, teacherId=teacherId)

@app.route('/randomQuiz')
def randomQuiz():
    return redirect(url_for('triviaQuiz'))
    
    # query = """
    #  SELECT DISTINCT quizId
    #  FROM complete_questions
    #  WHERE questionSetPrivate = '0'
    #  """
    # myresult1 = getDatabaseConnection(query)
    # # print(myresult1)
    # randomList = random.choice(myresult1)
    # randomQuiz = randomList[0]

    # query = f"SELECT row_to_json(complete_questions) FROM complete_questions WHERE quizid = '{randomQuiz}';"
    # myresult2 = getDatabaseConnection(query)

    # return myresult2


@app.route('/myresults')
def myresults():
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True:
        username = session['username']
    if loggedIn == True and subscribed == True:

        with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "SELECT DISTINCT ON (quizid) quizid, quiztitle, teacherid, questionid, correct, id FROM results WHERE teacherId = %s"
                data = (teacherId, )
        
                cur.execute(SQL, data)
                myresult = cur.fetchall()
                

        
                return render_template("myresults.html",
                                       subscribed=subscribed,
                                       loggedIn=loggedIn,
                                       teacherId=teacherId,
                                       myresult=myresult)
    else:
        return render_template(url_for('home'))



@app.route('/addQuestion/<set>/<teacherid>')
def addQuestion(set, teacherid):
    token = uuid.uuid4()
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
        return render_template("addQuestion.html", set=set, teacherid=teacherid, loggedIn=loggedIn, subscribed=subscribed, token=token)


    return redirect(url_for('home'))


@app.route('/addQuestionForm', methods=['GET', 'POST'])
def addQuestionForm():
    msg = ""
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
       
        if request.method == "POST" and 'correctAnswer' in request.form and 'questionText' in request.form and 'token' in request.form:
          
            correctAnswer =  request.form['correctAnswer']

            if correctAnswer == 'A':
                correctAnswer = '1'
            elif correctAnswer == 'B':
                correctAnswer = '2'
            elif correctAnswer == 'C':
                correctAnswer = '3'
            elif correctAnswer == 'D':
                correctAnswer = '4'

            
            quizId = request.form['quizId']
            teacherId = request.form['teacherId']
            questionText = request.form['questionText']


            with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD']) as conn:
                with conn.cursor() as cur:
                    SQL = "SELECT * FROM complete_questions WHERE quizId = %s AND teacherid = %s"
                    data = (quizId, teacherId,  )

                    cur.execute(SQL, data)
                    
                    myresult = cur.fetchall()

            if myresult:
                # print(myresult[0])

            
                questionssettitle = myresult[0][9]
                questionsetdescription =myresult[0][10]
                questionsetprivate = myresult[0][11]
                subject = myresult[0][13]
                questionnumber = myresult[0][2]
    
                if request.form['answer1']:
                    answer1 = request.form['answer1']
                else:
                    answer1 = "blank"
                if request.form['answer2']:
                    answer2 = request.form['answer2']
                else:
                    answer2 = "blank"
                if request.form['answer3']:
                    answer3 = request.form['answer3']
                else:
                    answer3 = "blank"
                if request.form['answer4']:
                    answer4 = request.form['answer4']
                else:
                    answer4 = "blank"
            
                with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD']) as conn:
                    with conn.cursor() as cur:
                        SQL = "INSERT INTO complete_questions (quizid, questionnumber, questiontext, answer1, answer2, answer3, answer4, correctanswer, questionsettitle, questionsetdescription, questionsetprivate, teacherid, subject) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        data = (quizId,questionnumber,  questionText, answer1, answer2, answer3, answer4, correctAnswer, questionssettitle, questionsetdescription, questionsetprivate, teacherId,subject  )
    
                        cur.execute(SQL, data)

                return redirect(url_for('displayOneQuestionSet', id=quizId))
                      
            else:
                msg = "Access Denied"
                return render_template('addQuestionForm.html', msg=msg,loggedIn=loggedIn, subscribed=subscribed, teacherId=teacherId)
                
        


    return redirect(url_for('home'))




@app.route('/addNewQuiz', methods=['POST', 'GET'])
def addNewQuiz():
    token = uuid.uuid4()
    msg=""
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
        if request.method == 'POST' and 'token' in request.form and "quizname" in request.form and "quizdescription" in request.form:
            quizId = get_random_string()
            
            questionsettitle = request.form["quizname"]
            questionsetdescription = request.form["quizdescription"]
            questionsetprivate = "1"
            teacherid = request.form['teacherId']
            subject = request.form['subject']
            questionnumber = 1
            questiontext = "Edit This Question"
            answer1 = "Edit Me"
            answer2 = "Edit Me"
            answer3 = "Edit Me"
            answer4 = "Edit Me"
            correctanswer = "1"
            
            with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
                with conn.cursor() as cur:
                    SQL = "INSERT INTO complete_questions (quizid, questionsettitle, questionsetdescription, questionsetprivate, teacherid, subject, questionnumber, questiontext, answer1, answer2, answer3, answer4, correctanswer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    data = (quizId,questionsettitle,questionsetdescription,questionsetprivate,teacherid,subject,questionnumber,questiontext, answer1, answer2, answer3,answer4,correctanswer  )

                    cur.execute(SQL, data)
            return redirect(url_for('displayPrivateQuestionSets'))
        


        else:
            msg="You Must Complete The Form!"    
            return render_template('addNewQuiz.html', token=token, teacherId = teacherId, loggedIn=loggedIn, subscribed=subscribed)


        return render_template('addNewQuiz.html', token=token, teacherId = teacherId, loggedIn=loggedIn, subscribed=subscribed)

    else:
        return render_template(url_for('home', loggedIn=loggedIn, subscribed=subscribed, teacherId = teacherId))
        


@app.route('/assignQuiz/<quizid>')
def assignQuiz(quizid):
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:

        return render_template('assignQuiz.html', loggedIn=loggedIn, subscribed=subscribed, teacherId = teacherId, quizid=quizid)
    else:
        return render_template('assignQuiz.html', loggedIn=loggedIn, subscribed=subscribed, teacherId = teacherId, quizid=quizid)

    

    return redirect(url_for('home'))


@app.route('/deleteResult/<quizid>')
def deleteResult(quizid):
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
        with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "DELETE FROM results WHERE quizid = %s AND teacherid = %s;"
                data = (quizid, teacherId, )

                cur.execute(SQL, data)

            


                return redirect(url_for('myresults'))


    return redirect(url_for('home'))
   
@app.route('/deleteQuiz/<quizid>')
def deleteQuiz(quizid):
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
        with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "DELETE FROM complete_questions WHERE quizid = %s AND teacherid = %s;"
                data = (quizid, teacherId, )

                cur.execute(SQL, data)

                SQL = "DELETE FROM quizids WHERE quizid = %s;"
                data = (quizid, )

                cur.execute(SQL, data)
        
        
                return redirect(url_for('displayPrivateQuestionSets'))


    return redirect(url_for('home'))

# @app.route('/editTitle/<quizid>')
# def editTitle(quizid):
#     loggedIn, subscribed, teacherId = checkPermissions()
#     if loggedIn == True and subscribed == True:
        

#         return redirect(url_for('editTitleForm', loggedIn=loggedIn, subscribed=subscribed, teacherId=teacherId, quizid=quizid ))


#     return redirect(url_for('home'))

@app.route('/editTitleForm/<quizid>', methods=['POST', 'GET'])
def editTitleForm(quizid):
    token = uuid.uuid4()
    msg=""
    loggedIn, subscribed, teacherId = checkPermissions()

    
    if loggedIn == True and subscribed == True:

        with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
            with conn.cursor() as cur:
                SQL = "SELECT * FROM complete_questions WHERE quizid = %s"
                data = (quizid, )

                cur.execute(SQL, data)
                myresult = cur.fetchall()
                result = myresult[0]


        
        if request.method == 'POST' and 'token' in request.form and "quiztitle" in request.form and "quizdescription" in request.form:
            quiztitle = request.form['quiztitle']
            quizdescription = request.form['quizdescription']
            with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
                with conn.cursor() as cur:
                    SQL = "UPDATE complete_questions SET questionsettitle = %s, questionsetdescription = %s WHERE quizid = %s;"
                    data = (quiztitle, quizdescription, quizid,  )

                    cur.execute(SQL, data)

                    return redirect(url_for('displayPrivateQuestionSets'))

            

    

    return render_template('editTitleForm.html', loggedIn=loggedIn, subscribed=subscribed, teacherId=teacherId, quizid=quizid, msg=msg, token=token, result=result)


    return redirect(url_for('home'))


@app.route('/deletejava/<quizid>')
def deletejava(quizid):
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
        if "userInput" in request.form:
            if request.form['userInput'] == "True":

        
                with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD']) as conn:
                    with conn.cursor() as cur:
                        SQL = "DELETE FROM complete_questions WHERE quizid = %s AND teacherid = %s;"
                        data = (quizid, teacherId, )
        
                        cur.execute(SQL, data)
        
                        return redirect(url_for('displayPrivateQuestionSets'))
            else:
                return redirect(url_for('displayPrivateQuestionSets'))
                
        else:
            return redirect(url_for('displayPrivateQuestionSets'))
    return redirect(url_for('home'))


@app.route('/deleteQuestion/<id>/<set>/<teacherId>')
def deleteQuestion(id, set, teacherId):
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
        with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD']) as conn:
            with conn.cursor() as cur:
                SQL = "DELETE FROM complete_questions WHERE id = %s AND teacherid = %s;"
                data = (id, teacherId, )

                cur.execute(SQL, data)

                return redirect(url_for('displayOneQuestionSet', id=set))


    return redirect(url_for('home'))
        



@app.route('/oneresult/<string:quizid>/')
def oneresult(quizid):
    loggedIn, subscribed, teacherId = checkPermissions()
    if loggedIn == True and subscribed == True:
        # print(quizid)
      
        with psycopg.connect(host=os.environ['PGHOST'],dbname=os.environ['PGDATABASE'],user=os.environ['PGUSER'],password=os.environ['PGPASSWORD'])    as conn:
            with conn.cursor() as cur:
                SQL = "SELECT questiontext, SUM (correct) AS total, SUM (incorrect) AS isum FROM results WHERE teacherId = %s AND quizid = %s GROUP BY questiontext ORDER BY total"
                data = (teacherId, quizid, )

                cur.execute(SQL, data)
                myresult = cur.fetchall()


                SQL = "SELECT * FROM complete_questions WHERE quizid = %s"
                data = (quizid, )
                cur.execute(SQL, data)
                result = cur.fetchall()

                if result:
                    firstrow = result[0]
                else:
                    firstrow = ""
 

        return render_template("oneresult.html",
                               subscribed=subscribed,
                               loggedIn=loggedIn,
                               teacherId=teacherId,
                               myresult=myresult, firstrow=firstrow)
    return render_template("index.html",
                           subscribed=subscribed,
                           loggedIn=loggedIn)


@app.route(
    '/recordAnswer/<id>/<correct>/<incorrect>/<teacherId>/<quizid>/<quiztitle>/<questiontext>'
)
def recordAnswer(id, correct, incorrect, teacherId, quizid, quiztitle,
                 questiontext):
    correct = int(correct)
    questionId = int(id)
    teacherId = int(teacherId)
    incorrect = int(incorrect)

    # cur = getDatabaseConnection()

    with psycopg.connect(host=os.environ['PGHOST'],
                         dbname=os.environ['PGDATABASE'],
                         user=os.environ['PGUSER'],
                         password=os.environ['PGPASSWORD']) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO results (questionId, correct,incorrect, teacherId, quizid, quiztitle,questiontext) VALUES ({questionId}, {correct}, {incorrect},{teacherId},'{quizid}','{quiztitle}','{questiontext}')"
            )

    return jsonify({'error': 'None'})

@app.route("/sitemap.xml")
def sitemap():
  return sitemapper.generate()


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/ads.txt')
def ads():
       return send_from_directory(app.static_folder, request.path[1:])




@app.route('/google2ae4206fc72af134.html')
def google2ae4206fc72af134():
    return render_template("google2ae4206fc72af134.html")

@app.route('/triviaQuiz')
def triviaQuiz():
    
    try:
        response = requests.get('https://opentdb.com/api.php?amount=50&category=9&type=multiple')
        #print(response.text)
        json = response.json()
        # print(json)
        questions = json['results']
        #   print(questions)
        quiz = []
        count = 1
        for data in questions:
            emptyList = []
            question = {}
            question["answer1"] = html.unescape(data['incorrect_answers'][0])
            question["answer2"] = html.unescape(data['incorrect_answers'][1])
            question["answer3"] = html.unescape(data['incorrect_answers'][2])
            question["answer4"] = html.unescape(data['correct_answer'])
            question["correctanswer"] = "4"
            question["id"] = count
            question["questionnumber"] = count
            question["questionsetdescription"] = "Trivia"
            question["questionsetprivate"] = "1"
            question["questionsettitle"] = "Trivia"
            question["questiontext"] = html.unescape(data['question'])
            question["quizid"] = ""
            question["subject"] = "Trivia"
            question["teacherid"] = 2
            question["timestamp"] = "1978-06-29T01:00:00.000000"
            emptyList.append(question)
            quiz.append(emptyList)
            count += 1
        # print(quiz)
        return jsonify(quiz)
    except:
        return "error"

def get_ai_mc_question(text):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates educational questions."},
            {"role": "user", "content": f"Based on the following text, produce a JSON object.  The object should contain a multiple choice question with the key 'questiontext' and each answer having the keys 'answer1', 'answer2', 'answer3', 'answer4'.  The correct answer should have the key, 'correctanswer' and be a number from 1 to 4:\n\n{text}"}
        ],
        max_tokens=200,
        temperature=0.7
    )


    mc_question = response.choices[0].message.content.strip()

    cleaned = clean_json_string(mc_question)


    return cleaned

def clean_json_string(json_string):
    pattern = r'^```json\s*(.*?)\s*```$'
    cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL)
    cleaned_string = cleaned_string.replace("\n", "")

    return cleaned_string.strip()


def aiquestion(text=""):
    
    result = YouTubeTranscriptApi.get_transcript("V_HRW-NzBg4&list=PLMb6Yv6-w-RWngEjn_YeMzVwgyXBZ73Bf&index=3&t=701s")
    # print(result)

    text = ""
    for content in result:
        text += content['text']

    length = len(text)
    if length > 10000:
        text = text[:10000]

    questions_json = generate_multiple_choice_questions(text, num_questions=10)
#     print(questions_json)

    for question in questions_json:
        print("\n\n")
        print(question["questiontext"])
        print(question["answer1"])
        print(question["correctanswer"])
        print("\n\n")
    return questions_json


def generate_multiple_choice_questions(learning_text, num_questions=10):
    questions = []

    for _ in range(num_questions):
        question_data = get_ai_mc_question(learning_text)



#         print(question_data)
        my_dict = json.loads(question_data)
        questions.append(my_dict)
#         print(my_dict)


    return questions










aiquestion()







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

