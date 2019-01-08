from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import Student, Post


@app.route('/', methods=['GET', 'POST'])
# @app.route('/index')
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        message = form.post.data
        # post = Post(body=form.post.data, author=current_user)
        flash(message)
        flash(datetime.now())
        flash(current_user.full_name)
        post = Post(current_user._id, message, datetime.now())
        print(post.json())
        post.save_to_mongo()
        flash('Your post is now live!')
        return redirect(url_for('index', zid=current_user._id))
    # print(current_user._id)
    posts = Post.get_by_id(current_user._id)


    return render_template('index.jinja2', form=form, posts=posts, title='home page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        student = Student.get_by_email(email=form.email.data)
        flash('Login requested for user {}, password {}, remember_me={}'.format(
            form.email.data, form.password.data, form.remember_me.data))

        if student is None or not student.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(student, remember=form.remember_me.data)

        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.jinja2', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        _id = form.zid.data
        email = form.email.data
        password = form.password.data
        full_name = form.full_name.data
        birthday = form.birthday.data.strftime("%Y-%m-%d")
        student = Student(_id, email, password, full_name, birthday)

        student.save_to_mongo()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.jinja2', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/student/<zid>')
@login_required
def student(zid):
    student = Student.get_by_id(zid)

    posts = [
        {'author': student, 'body': 'Test post #1'},
        {'author': student, 'body': 'Test post #2'}
    ]

    return render_template('student.jinja2', student=student, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        # current_user.about_me = form.about_me.data
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        # form.about_me.data = current_user.about_me
    return render_template('edit_profile.jinja2', title='Edit Profile', form=form)


@app.route('/add_friend/<zid>')
@login_required
def add_friend(zid):

    if current_user.friends_with(zid):
        flash('You are already friends with {}'.format(zid))
        return redirect(url_for('index'))
    new_friend = Student.get_by_id(zid)
    if new_friend is None:
        flash('User {} not found.'.format(zid))
        return redirect(url_for('index'))
    if new_friend == current_user:
        flash('You cannot add yourself!')
        return redirect(url_for('student', zid=zid))
    current_user.add_friend(zid)
    flash('You are now friends with {}!'.format(new_friend.full_name))
    print(current_user.friends)
    return redirect(url_for('student', zid=zid))



@app.route('/remove_friend/<zid>')
@login_required
def remove_friend(zid):
    print(current_user.friends)
    if not current_user.friends_with(zid):
        flash('You are not friends with {}'.format(zid))
        return redirect(url_for('index'))
    lost_friend = Student.get_by_id(zid)

    if lost_friend is None:
        flash('User {} not found.'.format(zid))
        return redirect(url_for('index'))
    if lost_friend == current_user:
        flash('You cannot unfriend yourself!')
        return redirect(url_for('student', zid=zid))
    current_user.remove_friend(zid)

    flash('You have unfriended {}!'.format(lost_friend.full_name))

    return redirect(url_for('student', zid=zid))