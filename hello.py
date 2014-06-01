from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/blog/')
def blog():
    return render_template('blog.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/studio/')
def studio():
    return render_template('studio.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
