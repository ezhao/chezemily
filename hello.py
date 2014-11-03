from flask import Flask
from flask import render_template
from flask import request, session, g, redirect, url_for, abort, flash
import os
from flask.ext.sqlalchemy import SQLAlchemy

# Create application
app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    #DATABASE=os.path.join(app.root_path, 'flaskr.db'), #TODO(emily) investigate "Instance Folders"
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
    SECRET_KEY='2g2JXhqfutWCzRBAnuUpTRVNoneadventureatatimebaconandburrata',
    USERNAME='snowman',
    PASSWORD='pumpkin'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def init_db():
    print os.environ['DATABASE_URL']
    with app.app_context():
        db = get_db()
        db.create_all()

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'postgresql_db'):
        g.postgresql_db = SQLAlchemy(app)
    return g.postgresql_db

'''
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

'''


'''

# Routes for fake blog application and other testing
@app.route('/app')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/app/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/app/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/app/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

'''



@app.route('/')
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


# Routes for ezhao.herokuapp
@app.route('/blog/')
def blog():
    return render_template('blog.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/studio/')
def studio():
    return render_template('studio.html')

@app.route('/project/<project>/')
def project(project=None):
    if project == 'setlist':
        return render_template('setlist.html')
    return render_template('hello.html', name='test')


# Run
def run_for_test():
    app.debug = True
    app.run()

if __name__ == '__main__':
    app.debug = False # Only deploy with "False"
    app.run()
