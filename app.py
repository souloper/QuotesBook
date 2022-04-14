from operator import pos
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# from werkzeug.utils import redirect

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db=SQLAlchemy(app)

# class Todo(db.Model):
#     id=db.Column(db.Integer, primary_key=True)
#     content=db.Column(db.String(255), nullable=False)
#     completed=db.Column(db.Integer, default=0)
#     date_created=db.Column(db.DateTime, default=datetime.utcnow)


#     def __repr__(self):       
#         return '<Task %r>' % self.id



# @app.route('/', methods=['POST','GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Todo(content=task_content)

#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue adding your task'

#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks=tasks)
        
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return 'Blog post ' + str(self.id)


all_posts = [{
    'title': 'Post 1',
    'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Vel turpis nunc eget lorem dolor sed.',
    'author': 'Lorem Ipsum'
}]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def posts():


    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')

    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':    
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')

    else:
        return render_template('edit.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    
    if request.method == 'POST':    
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')



if __name__ == '__main__':
    app.run(debug=True)