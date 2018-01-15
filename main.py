from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:thisisapassword@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1000))

    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route('/blog', methods=['POST', 'GET'])
def index():
    query_id = request.args.get('id')

    if query_id is not None:
        blog = Blog.query.get(query_id)
        return render_template('blogpost.html', blog=blog) 

    blogs = Blog.query.all()
    blogs = list(reversed(blogs))
    return render_template("index.html", blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

    

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        title_error = ""
        content_error = ""
        if title == "" or content == "":
            if title == "":
                title_error += "You can not leave the title blank."
            if content == "":
                content_error += "You can not leave the content blank."
            return render_template("newpost.html", title_error=title_error, content_error=content_error, content_val=content, title_val=title)
        new_blog = Blog(title, content)
        db.session.add(new_blog)
        db.session.commit()
        new_id = new_blog.id
        return redirect("/blog?id={0}".format(new_id))

    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()