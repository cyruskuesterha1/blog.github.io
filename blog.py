from flask import Flask, render_template, url_for, flash, redirect, request
from datetime import datetime
from forms import PostForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fhskfsjdsjh2h4hdsjh3841d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f"Post('{self.title}', '{self.author}', '{self.date_posted}')"

def get_categories(posts):
    categories = ['All']
    print(posts)
    for post in posts:
        if post.category not in categories:
            categories.append(post.category)
    return categories


@app.route('/')
@app.route('/home', methods=['GET','POST'])
def home():
    posts = Post.query.all()
    categories = get_categories(posts)
    return render_template('home.html', posts=posts, categories=categories)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/new', methods=['GET','POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, author=form.author.data, content= form.content.data, category= form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', form=form, legend="Create a New Post")

@app.route('/post/<int:post_id>/delete', methods=['GET','POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash('Post Deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/post/int:<post_id>/update', methods=['GET','POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.content = form.content.data
        post.category = form.category.data
        db.session.commit()
        flash('Post Updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.author.data = post.author
        form.content.data = post.content
        form.category.data = post.category
    return render_template('new_post.html', form=form, legend="Update Post")

@app.route('/home/filter/<category>', methods=['GET'])
def filter_posts(category):
    posts = Post.query.all()
    categories = get_categories(posts)
    return render_template('home.html', posts=posts, categories=categories, selected_category=category)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')