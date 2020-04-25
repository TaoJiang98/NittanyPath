# import sqlite3 as sql
# import hashlib
# from flask import Flask, render_template, redirect, url_for, request
#
# app = Flask(__name__)
#
# host = 'http://127.0.0.1:5000/'
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# def index_to_login():
#     if request.form['submit_button'] == 'Login Here':
#         # return redirect(url_for('login'))
#         return render_template('login.html')
#
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         username = request.form["username"]
#         password = request.form["password"]
#         result = getPass(username, password)
#         if result:
#             # name = getName(username)
#             return getCourse(username)
#         else:
#             error = "invalid username or password"
#     return render_template('user_login.html', error=error)
#
#
# # def getName(email):
# #     connection = sql.connect('431dabase.db')
# #     cursor = connection.execute('select name from Students where email=?;', "email")
# #     return cursor.fetchall()
#
#
# def getPass(username, password):
#     md5 = hashlib.md5()
#     md5.update(password.encode())
#     hashedpw = md5.hexdigest()
#     connection = sql.connect('431dabase.db')
#     cursor = connection.execute('select * from Students where email=? AND password=?;', (username, hashedpw))
#     return cursor.fetchall()
#
#
# @app.route('/login/<username>')
# def getCourse(username):
#     connection = sql.connect('431dabase.db')
#     # cursor = connection.execute('select course_id from Enrolls where student_email=?;', username)
#     # cursor = connection.execute('select course_id from Enrolls where student_email="al4613@nittany.edu";')
#     cursor = connection.execute('select course_id, course_name, course_description from Courses where course_id in ('
#                                 'select course_id from Enrolls '
#                                 'where student_email="al4613@nittany.edu");')
#     courses = cursor.fetchall()
#     query1 = 'select prof_email from Prof_teaching_teams where teaching_team_id in (select teaching_team_id from ' \
#              'Sections S, Enrolls E where S.course_id = E.course_id And S.sec_no = E.section_no AND E.student_email = ' \
#              '"al4613@nittany.edu"); '
#     cursor = connection.execute(query1)
#     prof_email = cursor.fetchall()
#
#     return render_template('CourseInfo.html', username=username, courses=courses, prof_email=prof_email)
#
#
# @app.route('/changePassword')
# def changePass():
#     return render_template('changePass.html')
#
#
# if __name__ == '__main__':
#     app.run()
