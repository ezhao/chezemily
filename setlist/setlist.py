from flask import Blueprint, render_template, request, redirect, url_for
from models import db, SetlistSong

setlist = Blueprint('setlist', __name__,
                    template_folder='templates',
                    static_folder='static')

@setlist.route('/')
def home():
    return redirect(url_for('setlist.setlist_add'))

@setlist.route('/<songid>')
def setlist_song(songid):
    songid = int(songid)
    selected_song = SetlistSong.query.get(songid)
    return render_template('setlist.html',
                           songs = format_song_list(songid),
                           songid = songid,
                           selected_song = selected_song
                           )

@setlist.route('/<songid>/edit', methods=['GET', 'POST'])
def setlist_edit(songid):
    songid = int(songid)
    selected_song = SetlistSong.query.get(songid)
    if request.method == 'POST':
        selected_song.artist = request.form['artist']
        selected_song.title = request.form['title']
        selected_song.lyrics = request.form['lyrics']
        db.session.commit()
    return render_template('setlist.html',
                           songs = format_song_list(songid),
                           songid = songid,
                           selected_song = selected_song,
                           edit = True
                           )

@setlist.route('/add', methods=['GET', 'POST'])
def setlist_add():
    if request.method == 'POST':
        new_song = SetlistSong(
            request.form['artist'],
            request.form['title'],
            '', #TODO(emily) Need YouTube link
            request.form['lyrics']
            )
        db.session.add(new_song)
        db.session.commit()
        return redirect(url_for('setlist.setlist_song', songid=new_song.id))
    return render_template('setlist.html',
                           page="add",
                           songs = format_song_list(),
                           )


def format_song_list(songid = None):
    all_songs = SetlistSong.query.all()
    formatted_songs = [dict(id=song.id, title=song.title, artist=song.artist,
                            selected=True if song.id==songid else False
                            ) for song in all_songs]
    return formatted_songs
