from flask import render_template, request, session, redirect, url_for, abort, flash
from deploy import app
from models import db, Entries, Sticker, PCResponse

############################
# Routes for stickers      #
############################

@app.route('/stickers')
def show_stickers():
    stickers = Sticker.query.all()
    print "Emily printing the stickers", stickers
    return render_template('stickers.html', stickers=stickers)

@app.route('/stickers/<id>')
def show_sticker(id):
    sticker = Sticker.query.get(id)
    return render_template('sticker.html', sticker=sticker)

STICKER_COLS = ['file', 'height', 'width', 'fullheight', 'fullwidth', 'offsetx', 'offsety', 'animationx', 'animationy', 'gridwidth', 'gridsize']

@app.route('/stickers/add', methods=['POST'])
def add_sticker():
    if not session.get('logged_in'):
        abort(401)
    params = dict()
    for sticker_col in STICKER_COLS:
        params[sticker_col] = request.form[sticker_col]
    db.session.add(Sticker(**params))
    db.session.commit()
    flash('New sticker was successfully posted')
    return redirect(url_for('show_stickers'))

@app.route('/stickers/edit', methods=['POST'])
def edit_sticker():
    if not session.get('logged_in'):
        abort(401)
    try:
        stickerid = int(request.form['stickerid'])
    except ValueError:
        flash('Bad sticker id. We got \'%s\', which may not be an integer' % request.form['stickerid'])
        return redirect(url_for('show_stickers'))
    sticker = Sticker.query.get(stickerid)
    for sticker_col in STICKER_COLS:
        setattr(sticker, sticker_col, request.form[sticker_col])
    db.session.commit()
    flash('Sticker was successfully edited')
    return redirect(url_for('show_sticker', id=stickerid))

@app.route('/stickers/delete/<id>')
def delete_sticker(id):
    db.session.delete(Sticker.query.get(id))
    db.session.commit()
    return redirect(url_for('show_stickers'))



############################
# Routes for pc            #
############################

def pc_get_latest():
    if not session.get('pc_logged_in'):
        return 'pc_login'
    return 'pc_invite'

@app.route('/pc')
def pc():
    return redirect(url_for(pc_get_latest()))

@app.route('/pc/login', methods=['GET', 'POST'])
def pc_login():
    error = None
    if request.method == 'POST':
        if request.form['name'].lower() not in app.config['PC_NAME']:
            error = 'Nope'
        else:
            session['pc_logged_in'] = True
            return redirect(url_for('pc'))
    return render_template('pc.html', page="login", error=error)

@app.route('/pc/logout')
def pc_logout():
    session.pop('pc_logged_in', None)
    return redirect(url_for('pc'))

@app.route('/pc/invite')
def pc_invite():
    if not session.get('pc_logged_in'):
        abort(401)
    return render_template('pc.html', page="invite")

@app.route('/pc/avatar')
def pc_avatar_picker():
    if not session.get('pc_logged_in'):
        abort(401)
    avatars = [
        "outdoors",
        "casual",
        "classy",
    ]
    return render_template('pc.html', page="avatar", avatars=avatars)

ACTIVITIES = [
    dict(activity='katanaya', time_of_day=-1, image='ramen.jpg', casual=True, classy=False, outdoors=True),
    dict(activity='wilson_wilson', time_of_day=-1, image='whiskey.jpg', casual=True, classy=True, outdoors=False),
    dict(activity='monks_kettle', time_of_day=-1, image='belgian.jpg', casual=True, classy=True, outdoors=False),
    dict(activity='bootie', time_of_day=-1, image='dance.jpg', casual=True, classy=False, outdoors=True),
    dict(activity='corona_heights_night', time_of_day=-1, image='hillnight.jpg', casual=True, classy=False, outdoors=True),
    dict(activity='frances', time_of_day=-1, image='newamerican.jpg', casual=False, classy=True, outdoors=False),
    dict(activity='el_farolito', time_of_day=-1, image='burritos.jpg', casual=False, classy=False, outdoors=True),
    dict(activity='cooking', time_of_day=-1, image='chef.jpg', casual=True, classy=False, outdoors=True),
    dict(activity='union_square', time_of_day=0, image='skates.jpg', casual=True, classy=False, outdoors=True),
    dict(activity='humphrey', time_of_day=0, image='icecream.jpg', casual=True, classy=True, outdoors=True),
    dict(activity='boba_guys', time_of_day=0, image='boba.jpg', casual=True, classy=False, outdoors=True),
    dict(activity='corona_heights_day', time_of_day=1, image='hillday.jpg', casual=True, classy=False, outdoors=True),
    dict(activity='dolores_park', time_of_day=1, image='park.jpg', casual=True, classy=False, outdoors=True),
    dict(activity='starbelly', time_of_day=1, image='brunch.png', casual=True, classy=True, outdoors=False),
    dict(activity='little_skillet', time_of_day=1, image='chickwaffles.jpg', casual=True, classy=True, outdoors=True),
    dict(activity='brendas', time_of_day=1, image='beignets.jpg', casual=True, classy=True, outdoors=False),
    dict(activity='blue_bottle', time_of_day=1, image='coffee.jpg', casual=True, classy=False, outdoors=False),
    dict(activity='painting', time_of_day=1, image='painting.jpg', casual=True, classy=False, outdoors=False),
    dict(activity='exploratorium', time_of_day=1, image='explore.jpg', casual=True, classy=True, outdoors=False),
    dict(activity='farmers_market', time_of_day=1, image='market.jpg', casual=True, classy=True, outdoors=True),
    dict(activity='ggultimate', time_of_day=1, image='frisbee.jpg', casual=False, classy=False, outdoors=True),
    dict(activity='smugglers_cove', time_of_day=-1, image='cove.jpg', casual=True, classy=True, outdoors=False),
]

@app.route('/pc/activities')
def pc_activity_picker():
    if not session.get('pc_logged_in'):
        abort(401)
    avatarResponse = PCResponse.query.get("Avatar")
    avatar = avatarResponse.answer if avatarResponse else None
    pickedActivities = []
    for activity in ACTIVITIES:
        if activity.get(avatar):
            pickedActivities.append(activity)
    return render_template('pc.html', page="activity", activities=pickedActivities)

@app.route('/pc/day')
def pc_day_picker():
    if not session.get('pc_logged_in'):
        abort(401)
    days = [
        "Friday",
        "Saturday",
        "Sunday",
    ]
    return render_template('pc.html', page="day", days=days)

TRAINS = [
    dict(day="weekday", arrive="6:47pm", depart="6:06pm"),
    dict(day="weekday", arrive="7:26pm", depart="6:43pm"),
    dict(day="weekday", arrive="7:43pm", depart="6:54pm"),
    dict(day="weekday", arrive="8:02pm", depart="7:10pm"),
    dict(day="weekend", arrive="5:38pm", depart="4:31pm"),
    dict(day="weekend", arrive="6:41pm", depart="5:58pm"),
    dict(day="weekend", arrive="7:38pm", depart="6:31pm"),
]

@app.route('/pc/train')
def pc_train_picker():
    if not session.get('pc_logged_in'):
        abort(401)
    dayResponse = PCResponse.query.get("Day")
    day = dayResponse.answer if dayResponse else None
    trains = []
    if day == "Friday":
        # http://www.caltrain.com/schedules/weekdaytimetable.html
        trains = [train for train in TRAINS if train['day'] == 'weekday']
    elif day in ("Saturday", "Sunday"):
        # http://www.caltrain.com/schedules/weekend-timetable.html
        trains = [train for train in TRAINS if train['day'] == 'weekend']
    return render_template('pc.html', page="train", trains=trains)

@app.route('/pc/done')
def pc_done():
    if not session.get('pc_logged_in'):
        abort(401)
    trainResponse = PCResponse.query.get("Train")
    trainTime = trainResponse.answer if trainResponse else None
    selectedTrain = None
    for train in TRAINS:
        if train['arrive'] == trainTime:
            selectedTrain = train
    activityResponse = PCResponse.query.get("Activities")
    activityList = activityResponse.answer.split(',') if activityResponse else []
    activityList = [a.strip() for a in activityList] # not sure why this happens

    selectedActivities = []
    for activity in ACTIVITIES:
        if activity['activity'] in activityList:
            selectedActivities.append(activity)
    return render_template('pc.html', page="done", train=selectedTrain, activities=selectedActivities)

@app.route('/pc/clear')
def pc_clear():
    if not session.get('pc_logged_in'):
        abort(401)
    PCResponse.query.delete()
    db.session.commit()
    return redirect(url_for(pc_get_latest()))

@app.route('/pc/answer', methods=['POST'])
def pc_answer():
    if not session.get('pc_logged_in'):
        abort(401)
    obj = PCResponse(request.form['question'], request.form['answer'])
    print obj
    db.session.merge(obj)
    if request.form['question'] == 'Day':
        trainResponse = PCResponse.query.get("Train")
        if trainResponse:
            db.session.delete(trainResponse)
    db.session.commit()
    return url_for(pc_get_latest())



########################################################################################

# Routes for fake blog application and other testing
@app.route('/app')
def show_entries():
    entries = Entries.query.all()
    print entries
    return render_template('show_entries.html', entries=entries)

@app.route('/app/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    new_entry = Entries(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
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


from setlist.setlist import setlist
app.register_blueprint(setlist, url_prefix='/setlist')

# Run locally
if __name__ == '__main__':
    app.debug = False # Only deploy with "False"
    app.run()
