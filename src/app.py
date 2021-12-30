# Project Requirements
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
# Gives us a 404 error page
from werkzeug.exceptions import abort
# Loads environment variables to pass in secrets
from dotenv import load_dotenv
import os
load_dotenv()
# Opens a connection to the database
# Sets the row_factory attribute to sqllite3.Row to get name based access to columns
# This means that the database connection will return rows that behave like dictionaries. 
# Finally, we return the conn object which we will use to access the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
app = Flask(__name__)
# Create a secret key for use in sessions
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

# Accepts a post_id argument that determines what post to return
# We use get_db_connection to open the DB and execute a query to get the blog post associated with post_id
# We add the fetchone method to get the result, and store it in the post variable, then close the connection
# if the post variable has the value None, then no result was found in the database and we display a 404
# if a post was found, we return the value of the post variable

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post
    
# We open a connection to the database
# Execute a SQL Query to select all entries from the posts table
# We use the fetchall() function fetch all the rows of the query result
# This function returns the list of posts we inserted into the databse in init_db.py
# We close the database connection with conn.close()
# Finally, we return the result of rendering the index.html template. We pass the posts object as an argument, which contains the results from the database
# This allows us to access the blog posts in the index.html template
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# We add a VARIABLE RULE to specify that the part after the slash is a positive integer (marked with int) that we need to access the view function
# Flask recognizes this, and passes the value to the post_id keyword argument of the post() view function
# We then use the get_post function to get the  blog post associated with the ID and store the result in the post variable, which we then pass to the post.html template
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

# Creates a new route that accepts GET and POST requests. GET is by default, POST is not.
@app.route('/create', methods=('GET', 'POST'))
def create():
    # only execute if we get a post request
    if request.method == 'POST':
        # Extract titile and content from request.form object
        title = request.form['title']
        content = request.form['content']
        
        # This is bad but apparently something called a ViewModel can help out here. For a later tutorial perhaps.
        # We do validation here and not on the client to achieve server side validation. 
        if not title:
            flash('Title is Required')
        if not content:
            flash('Content is Required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == "__main__":
    app.run()