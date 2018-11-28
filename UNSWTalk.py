from app import app


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


# from flask import Flask, render_template, session, request, flash, redirect, url_for
# from pymongo import MongoClient
#
# from functools import wraps
#
# from wtforms import Form, BooleanField, StringField, PasswordField, validators
#
# class RegistrationForm(Form):
#     username = StringField('Username', [validators.Length(min=4, max=25)])
#     email = StringField('Email Address', [validators.Length(min=6, max=35)])
#     password = PasswordField('New Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords must match')
#     ])
#     confirm = PasswordField('Repeat Password')
#     accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
#
#
#
#
#
# client = MongoClient('localhost', 27017)
# db = client["UNSW-Talk"]
#
# students = db["students"]
# posts = db["posts"]
#
#
# # print(students.find_one({"_id": "z5190454"}))
# print([student for student in students.find({})])
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'you-will-never-guess'
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
#
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm(request.form)
#     if request.method == 'POST' and form.validate():
#         user = User(form.username.data, form.email.data,
#                     form.password.data)
#         # db_session.add(user)
#         flash('Thanks for registering')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)
#
#
#
#
# @app.route('/students')
# def students():
#     return [student for student in students.find({})]
#
#
# @app.route('/students/<zid>')
# def student(zid):
#     return students.find_one({"_id": zid})
#
#
#
# # @app.route('/posts')
# # def posts():
# #     return posts.find({})
#
#
# @app.route('/posts/<zid>')
# def posts(zid):
#     return posts.find_one({"_id": zid})
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True, use_reloader=True)
#
#
#
#
