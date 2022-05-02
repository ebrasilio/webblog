from flask import Flask, render_template, request, url_for, flash, redirect
import os, datetime
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort


# caminhos para pasta do projeto
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}", format(os.path.join(project_dir, "database.db"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)   # criar objeto tipo sqlachemy para acessar o banco

# @emilia - não funcionou desta maneira
# @emilia - não consigo consultar o banco via objeto
#criar a classe correspondente a tabela, com 4 atributos correspondente a tabela no banco
# class Posts(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#    title = db.Column(db.String(80), nullable=False)
#    content = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    #caso o objeto funcione basta substituir as linhas acima por esta (apenas)
    #posts = Posts.query.all()       
    return render_template('index.html', posts=posts)  

#se a conexão via objeto funcionar essa função não é necessária
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    conn.close()
    #caso o objeto funcione basta substituir as linhas acima por esta (apenas)
    #post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)
    return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is requerid!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            #post = Posts(title=title, content=content)
            #db.session.add(post)
            #db.session.commit()
            return redirect(url_for('index'))
   
    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is requerid!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title=?, content=? WHERE id=?', (title, content, id))
            conn.commit()
            conn.close()
            # post.title = title
            # post.content = content
            # db.session.commit()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id=?', (id,))
    conn.commit()
    conn.close()
    # db.session.delete(post)
    # db.session.commit()
    flash('"{}" was successfully deleted!'.format(post['title']))
    # post.title = title
    # post.content = content
    # db.session.commit()
    return redirect(url_for('index'))