import hashlib

from flask import Flask, render_template, url_for, redirect, session, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# from models import Students

app = Flask(__name__)
db = SQLAlchemy(app)
Bootstrap(app)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///431.db'


class Students(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(32))
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    major = db.Column(db.String(128))
    street = db.Column(db.String(128))
    zipcode = db.Column(db.Integer)

    def __repr__(self):
        return f"Students('{self.email}', '{self.password}', '{self.name}', '{self.age}', '{self.age}'," \
               f" '{self.gender}', '{self.major}', '{self.street}', '{self.zipcode}') "


class Enrolls(db.Model):
    __tablename__ = "enrolls"
    student_email = db.Column(db.String(128), primary_key=True)
    course_id = db.Column(db.String(32), primary_key=True)
    section_no = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"Enrolls('{self.student_email}', '{self.course_id}', '{self.section_no}')"


class Courses(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.String(32), primary_key=True)
    course_name = db.Column(db.String(128))
    course_description = db.Column(db.Text)
    late_drop_deadline = db.Column(db.TEXT)

    def __repr__(self):
        return f"Courses('{self.course_id}', '{self.course_name}', '{self.course_description}', " \
               f"'{self.late_drop_deadline}')"


class Sections(db.Model):
    __tablename__ = "sections"
    course_id = db.Column(db.String(32), primary_key=True)
    sec_no = db.Column(db.Integer, primary_key=True)
    limit = db.Column(db.Integer)
    teaching_team_id = db.Column(db.Integer)

    def __repr__(self):
        return f"Sections('{self.course_id}', '{self.sec_no}', '{self.limit}', '{self.teaching_team_id}')"


class Professors(db.Model):
    __tablename__ = "professors"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    office_address = db.Column(db.String(128))
    department = db.Column(db.String(128))
    title = db.Column(db.String(128))

    def __repr__(self):
        return f"Professors('{self.email}', '{self.password}', '{self.name}', '{self.age}', '{self.gender}', " \
               f"'{self.office_address}', '{self.department}', '{self.title}')"


class Prof_teaching_teams(db.Model):
    __tablename__ = "prof_teaching_teams"
    prof_email = db.Column(db.String(128), primary_key=True)
    teaching_team_id = db.Column(db.INT)

    def __repr__(self):
        return f"Prof_teaching_teams('{self.prof_email}', '{self.teaching_team_id}')"


class Homeworks(db.Model):
    __tablename__ = "homeworks"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(32))
    sec_no = db.Column(db.Integer)
    hw_no = db.Column(db.Integer)
    hw_details = db.Column(db.Text)

    def __repr__(self):
        return f"Homeworks('{self.id}','{self.course_id}', '{self.sec_no}', '{self.hw_no}', '{self.hw_details}')"


class Homework_grades(db.Model):
    __tablename__ = "homework_grades"
    student_email = db.Column(db.String(128), primary_key=True)
    course_id = db.Column(db.String(32), primary_key=True)
    sec_no = db.Column(db.Integer, primary_key=True)
    hw_no = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Float)

    def __repr__(self):
        return f"Homework_grades('{self.student_email}', '{self.course_id}', '{self.sec_no}', " \
               f"'{self.hw_no}', '{self.grade}')"


class Exams(db.Model):
    __tablename__ = "exams"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(32))
    sec_no = db.Column(db.Integer)
    exam_no = db.Column(db.Integer)
    exam_details = db.Column(db.Text)

    def __repr__(self):
        return f"Exams('{self.id}','{self.course_id}', '{self.sec_no}', '{self.exam_no}', " \
               f"'{self.exam_details}')"


class Exam_grades(db.Model):
    __tablename__ = "exam_grades"
    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(128))
    course_id = db.Column(db.String(32))
    sec_no = db.Column(db.Integer)
    exam_no = db.Column(db.Integer)
    grades = db.Column(db.Float)

    def __repr__(self):
        return f"Exam_grades('{self.student_email}', '{self.course_id}', '{self.sec_no}', " \
               f"'{self.exam_no}', '{self.grades}')"


class Posts(db.Model):
    __tablename__ = "posts"
    course_id = db.Column(db.CHAR(100))
    post_no = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(128))
    post_info = db.Column(db.TEXT)

    def __repr__(self):
        return f"Posts('{self.course_id}', '{self.post_no}', '{self.student_email}', " \
               f"'{self.post_info}')"


class Comments(db.Model):
    __tablename__ = "comments"
    course_id = db.Column(db.CHAR(100))
    post_no = db.Column(db.Integer)
    comment_no = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(128))
    comment_info = db.Column(db.TEXT)

    def __repr__(self):
        return f"Comments('{self.course_id}', '{self.post_no}', '{self.comment_no}', " \
               f"'{self.student_email}', '{self.comment_info}')"


@app.route("/")
def index():
    return render_template('index.html')


list=[]


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        session['email'] = email
        session['password'] = password
        user = Students.query.filter_by(email=email).first()
        professor = Professors.query.filter_by(email=email).first()
        # the login user is a not a student
        if user is None:
            # the login user is not a professor either
            if professor is None:
                error = "No user found"
                return render_template("login.html", error=error)
            # the login user is a professor
            else:
                session['user'] = "professor"
                md5 = hashlib.md5()
                md5.update(password.encode())
                if professor.password == md5.hexdigest():
                    return redirect(url_for('professor'))
                    # return redirect(url_for('prof', name=professor.name))
                    # return render_template("professorPage.html", name=professor.name)
        # the login user is a student
        else:
            session['name'] = user.name
            session['user'] = "student"
            md5 = hashlib.md5()
            md5.update(password.encode())
            if user.password == md5.hexdigest():
                return redirect(url_for('student'))
    return render_template('login.html', error=error)


@app.route('/<email>/changePassword', methods=['GET', 'POST'])
def changePassword(email):
    if request.method == 'POST':
        newPassword = request.form['newPassword']
        md5 = hashlib.md5()
        md5.update(newPassword.encode())
        student = Students.query.filter_by(email=email).first()
        student.password = md5.hexdigest()
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("changePass.html")


@app.route('/professor')
def professor():
    prof = Professors.query.filter_by(email=session['email']).first()
    session['name'] = prof.name
    team = Prof_teaching_teams.query.filter_by(prof_email=session['email']).first().teaching_team_id
    if team is not None:
        # find all the section the professor teaches
        sections = Sections.query.filter_by(teaching_team_id=team).all()
        print(sections)
    return render_template("professorPage.html", name=prof.name, section=sections)


@app.route('/student')
def student():
    enrolls = Enrolls.query.filter_by(student_email=session['email']).all()
    print(enrolls)
    student = Students.query.filter_by(email=session['email']).first()
    return render_template("studentPage.html", student=student, enrolls=enrolls)


@app.route('/post')
def post():
    postInfo = []
    # if the user is professor
    if session['user'] == "professor":
        team = Prof_teaching_teams.query.filter_by(prof_email=session['email']).first()
        if team is not None:
            # find all the section the professor teaches
            sections = Sections.query.filter_by(teaching_team_id=team.teaching_team_id).all()
            print(sections)
            session['course_id'] = 'none'
            for section in sections:
                if section.course_id != session['course_id']:
                    session['course_id'] = section.course_id
                    profpost = Posts.query.filter_by(course_id=section.course_id).all()
                    postInfo.append(profpost)

    else:
        enrolls = Enrolls.query.filter_by(student_email=session['email']).all()
        for enroll in enrolls:
            post = Posts.query.filter_by(course_id=enroll.course_id).all()
            if post is not None:
                postInfo.append(post)
        print(postInfo)
    return render_template("course_posts.html", postInfo=postInfo)


@app.route('/post/<int:postNo>')
def comment(postNo):
    session['postNo'] = postNo
    print("postno is here")
    print(session['postNo'])
    currentpost = Posts.query.filter_by(post_no=postNo).first()
    comments = Comments.query.filter_by(post_no=postNo).all()
    commentInfo = []
    for comm in comments:
        commentInfo.append(comm)
    return render_template("comment.html", commentInfo=commentInfo, post=currentpost)


@app.route('/update_post', methods=['POST', 'GET'])
def update_post():
    if request.method == 'POST':
        courseId = request.form["courseId"]
        # email = request.form["email"]
        postInfo = request.form["postInfo"]
        new_post = Posts(course_id=courseId, student_email=session['email'], post_info=postInfo)
        db.session.add(new_post)
        db.session.commit()
        if session['user'] == "student":
            return render_template("studentPage.html", name=session['name'], list=list)
        elif session['user'] == "professor":
            return render_template("professorPage.html", name=session['name'])
    return render_template("postform.html")


@app.route('/post/update_comment', methods=['POST', 'GET'])
def update_comment():
    if request.method == 'POST':
        courseId = request.form["courseId"]
        # email = request.form["email"]
        commentInfo = request.form["commentInfo"]
        new_comment = Comments(course_id=courseId, student_email=session['email'], comment_info=commentInfo, post_no=session['postNo'])
        db.session.add(new_comment)
        db.session.commit()
        if session['user'] == "student":
            return redirect(url_for('comment', postNo=session['postNo']))
        elif session['user'] == "professor":
            return redirect(url_for('comment', postNo=session['postNo']))
    return render_template("commentform.html")


@app.route('/<courseId>/section<sectionNo>')
def course(courseId, sectionNo):
    session['courseId'] = courseId
    session['sectionNo'] = sectionNo
    # if session['user'] == "professor":
    hw = Homeworks.query.filter_by(course_id=courseId, sec_no=sectionNo).all()
    exam = Exams.query.filter_by(course_id=courseId, sec_no=sectionNo).all()
    courseInfo = Courses.query.filter_by(course_id=courseId).first()
    section = Sections.query.filter_by(course_id=courseId, sec_no=sectionNo).first()
    profEmail = Prof_teaching_teams.query.filter_by(teaching_team_id=section.teaching_team_id).first()
    professor = Professors.query.filter_by(email=profEmail.prof_email).first()
    return render_template("course.html", course=courseId, homework=hw, exam=exam, section=sectionNo,
                           courseInfo=courseInfo, professor=professor)


@app.route('/<courseId>/section<sectionNo>/createHomework', methods=['GET', 'POST'])
def createHw(courseId, sectionNo):
    if request.method == 'POST':
        detail = request.form['newHW']
        no = request.form['hwNo']
        homework = Homeworks(course_id=courseId, sec_no=sectionNo, hw_details=detail, hw_no=no)
        db.session.add(homework)
        hwgrade = Homework_grades.query.filter_by(course_id=courseId, sec_no=sectionNo).all()
        print(hwgrade)
        for grade in hwgrade:
            print(grade.student_email)
            hwrecord = Homework_grades(student_email=grade.student_email, course_id=courseId, sec_no=sectionNo,
                                       hw_no=no, grade=0)
            db.session.add(hwrecord)
        db.session.commit()
        return redirect(url_for('course', courseId=courseId, sectionNo=sectionNo))
    return render_template("createHW.html")


@app.route('/<courseId>/section<sectionNo>/createExam', methods=['GET', 'POST'])
def createExam(courseId, sectionNo):
    if request.method == 'POST':
        detail = request.form['newExam']
        no = request.form['examNo']
        exam = Exams(course_id=courseId, sec_no=sectionNo, exam_details=detail, exam_no=no)
        db.session.add(exam)
        examgrade = Exam_grades.query.filter_by(course_id=courseId, sec_no=sectionNo).all()
        print(examgrade)
        for grade in examgrade:
            print(grade.student_email)
            examrecord = Exam_grades(student_email=grade.student_email, course_id=courseId, sec_no=sectionNo,
                                     exam_no=no, grades=0)
            db.session.add(examrecord)
        db.session.commit()
        return redirect(url_for('course', courseId=courseId, sectionNo=sectionNo))
    return render_template("createExam.html")


@app.route('/<courseId>/section<sectionNo>/homework<hw_no>')
def hwgrade(courseId, sectionNo, hw_no):
    if session['user'] == "professor":
        hw_grades = Homework_grades.query.filter_by(course_id=courseId, sec_no=sectionNo, hw_no=hw_no).all()

    else:
        hw_grades = Homework_grades.query.filter_by(course_id=courseId, sec_no=sectionNo,
                                                    hw_no=hw_no, student_email=session['email']).all()
    return render_template("hw_grade.html", grades=hw_grades)


@app.route('/<courseId>/section<sectionNo>/Exam<exam_no>')
def examgrade(courseId, sectionNo, exam_no):
    if session['user'] == "professor":
        exam_grades = Exam_grades.query.filter_by(course_id=courseId, sec_no=sectionNo, exam_no=exam_no).all()
    else:
        exam_grades = Exam_grades.query.filter_by(course_id=courseId, sec_no=sectionNo,
                                                  exam_no=exam_no, student_email=session['email']).all()
    return render_template("exam_grade.html", grades=exam_grades)


@app.route('/<courseId>/section<sectionNo>/homework<hw_no>/change <user> Grade', methods=['GET', 'POST'])
def changeHWGrade(courseId, sectionNo, hw_no, user):
    if request.method == 'POST':
        newgrade = request.form['newGrade']
        g = Homework_grades.query.filter_by(student_email=user, course_id=courseId, sec_no=sectionNo
                                            , hw_no=hw_no).first()
        g.grade = newgrade
        db.session.commit()
        return redirect(url_for("hwgrade", courseId=courseId,
                                sectionNo=sectionNo, hw_no=hw_no))
    return render_template("changeGrade.html")


@app.route('/<courseId>/section<sectionNo>/exam<exam_no>/change <user> Grade', methods=['GET', 'POST'])
def changeExamGrade(courseId, sectionNo, exam_no, user):
    if request.method == 'POST':
        print("new grade")
        newgrade = request.form['newGrade']
        print(newgrade)
        g = Exam_grades.query.filter_by(student_email=user, course_id=courseId, sec_no=sectionNo,
                                            exam_no=exam_no).first()
        print("old grade")
        print(g.grades)
        g.grades = newgrade
        db.session.commit()
        return redirect(url_for("examgrade", courseId=courseId,
                                sectionNo=sectionNo, exam_no=exam_no))
    return render_template("changeGrade.html")


@app.route('/student/<courseId>/section<sectionNo>/drop')
def drop(courseId, sectionNo):
    # if the student drop this course
    # delete the record in enroll table
    Enrolls.query.filter_by(student_email=session['email'], course_id=courseId, section_no=sectionNo).delete()
    # deletet the record in the comment table
    Comments.query.filter_by(student_email=session['email'], course_id=courseId).delete()
    # delete the record in the post table
    Posts.query.filter_by(student_email=session['email'], course_id=courseId).delete()
    # delete the record in the homework_grade table
    Homework_grades.query.filter_by(student_email=session['email'], course_id=courseId, sec_no=sectionNo).delete()
    # delete the record in the exam_grades table
    Exam_grades.query.filter_by(student_email=session['email'], course_id=courseId, sec_no=sectionNo).delete()
    db.session.commit()
    return redirect(url_for('student', courseId=courseId, sectionNo=sectionNo))


if __name__ == '__main__':
    app.run()
