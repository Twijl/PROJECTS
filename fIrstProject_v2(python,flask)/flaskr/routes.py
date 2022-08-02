from flask import render_template, url_for, flash, redirect, request, abort
from flaskr import app, db, bcrypt
from flaskr.forms import RegistrationForm, LoginForm, PostForm
from flaskr.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required 
from datetime import datetime


# posts = [
#     {
#         'author': "Алексей Гордиенко",
#         'title': 'Пчелы, спасители планет !',
#         'content': 'Почему пчелы на столько важны, и какую роль они играют в мироздании.',
#         'time_posted': datetime.utcnow().strftime( "  < %H:%M > ")
#     },
#     {
#         'author': "Даниил Конов",
#         'title': 'Мухоморы, яд или лекарство?!',
#         'content': 'Ядовитые ли мухоморы на самом деле, какие еще секреты от нас скрывают?! ',
#         'time_posted': datetime.utcnow().strftime( "  < %H:%M > ")
#     }]
    
    

@app.route('/')
@app.route('/home')
def home():

    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts=posts)


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))

    form = RegistrationForm()
    # if request.method == 'POST':
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Successful! Now you are able to log in.', 'success')
        return redirect(url_for('login'))
    # else:
    #     flash(f'Failed to create account!', 'error')
    return render_template('register.html', title='register', form=form)



@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect (next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check email and password.', 'error')

    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account')
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)


@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your new post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form,
    legend='New Post')



@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_posted = datetime.utcnow()
        db.session.commit()
        flash('Your post has been updated!', 'info')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'info')
    return redirect(url_for('home'))












