from flask import Flask, session, render_template, request, \
					redirect, g, url_for, send_file, Response, \
					make_response, send_from_directory
from os import path
import os
from downoloader import groups_down as downoload_music_from_group
from downoloader import search_down as downoload_music_from_search
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)
actions = {"group":downoload_music_from_group, "search":downoload_music_from_search}
path_to_static = "/home/mark/my_pythons/vkmusic_downoloader/my_site/static"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            user_folder = path.join(path_to_static, session["user"]);
            if not path.exists(user_folder):
            	os.makedirs(user_folder)
            return redirect(url_for('protected', username = session['user']))
        else:
        	return render_template('index.html')

    return render_template('index.html')

@app.route('/<username>', methods=['GET', 'POST'])
def protected(username):
    if (request.method == 'POST') and (request.form["group"] !='') and (request.form["deep"]!=""):
    	#downoload_music_from_group(request.form["group"], request.form["deep"])
    	actions['group'](request.form["group"], request.form["deep"])
    	#return send_file("/home/mark/my_pythons/vkmusic_downoloader/my_site/static/music.mp3", attachment_filename = "music.mp3")
    	return redirect(url_for('download'))

    return render_template("protected.html")

@app.route('/download')
def download():
	if len(os.listdir(path.join(path_to_static, session["user"]))) == 0:
		#render_template("downloader.html")
		#time.sleep(3)
		return render_template("downloader.html")

	else:
		return redirect(url_for("zip_")) 
		#return send_from_directory(directory=path.join(path_to_static, session["user"]), filename="your_music.zip", as_attachment=True)

@app.route("/zip")
def zip_():
	return send_from_directory(directory=path.join(path_to_static, session["user"]) \
		, filename="your_music.zip", as_attachment=True)

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'Not logged in!'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return 'Dropped!'

if __name__ == '__main__':
	app.run(debug=True)