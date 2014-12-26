from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from deploy import app

############################
# Database related stuff   #
############################
db = SQLAlchemy(app)

def init_db():
    db.create_all()


############################
# Models models models     #
############################
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name


class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    text = db.Column(db.String(80))

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Title %r>' % self.title


class Sticker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(80))
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    fullheight = db.Column(db.Integer)
    fullwidth = db.Column(db.Integer)
    offsetx = db.Column(db.Integer)
    offsety = db.Column(db.Integer)
    animationx = db.Column(db.Integer)
    animationy = db.Column(db.Integer)
    gridwidth = db.Column(db.Integer)
    gridsize = db.Column(db.Integer)

    def __init__(self, file, height, width, fullheight, fullwidth, offsetx, offsety, animationx, animationy, gridwidth, gridsize):
        self.file = file
        self.height = height
        self.width = width
        self.fullheight = fullheight
        self.fullwidth = fullwidth
        self.offsetx = offsetx
        self.offsety = offsety
        self.animationx = animationx
        self.animationy = animationy
        self.gridwidth = gridwidth
        self.gridsize = gridsize

    def __repr__(self):
        return '<%r>' % self.file

class StickerTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(40))
    sticker_id = db.Column(db.Integer, db.ForeignKey(Sticker.id))

    def __init__(self, keyword, sticker):
        self.keyword = keyword
        self.sticker_id = sticker.id

    def __repr__(self):
        return '<%r - %r>' % (self.keyword, self.sticker_id)

class PCResponse(db.Model):
    question = db.Column(db.String(100), primary_key=True)
    answer = db.Column(db.String(100))
    ts = db.Column(db.DateTime)

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.ts = datetime.utcnow()

    def __repr__(self):
        return '<%r - %r - %r>' % (self.question, self.answer, self.ts)

class SetlistSong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(200))
    title = db.Column(db.String(200))
    youtubelink = db.Column(db.String(200))
    lyrics = db.Column(db.Text)

    def __init__(self, artist, title, youtubelink, lyrics):
        self.artist = artist
        self.title = title
        self.youtubelink = youtubelink
        self.lyrics = lyrics

    def __repr__(self):
        return "%s - %s" % (self.artist, self.title)
