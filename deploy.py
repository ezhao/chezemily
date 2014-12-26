from hello import app
from setlist.setlist import setlist

app.register_blueprint(setlist, url_prefix='/setlist')
app.debug = False # Only deploy with "False"
app.run()
