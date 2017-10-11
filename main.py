from flask import Flask, request, redirect, render_template, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy
#import forecastio
#from geopy.geocoders import Nominatim

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "root"

db = SQLAlchemy(app)


class Blog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	body = db.Column(db.String(500))
	
	def __init__(self, title, body):
		self.title = title
		self.body = body



@app.route('/')
def index():
    count = int(request.cookies.get('visit-count', 0))
    count += 1
    message = 'You have visited this page ' + str(count) + ' times'

    # make a response, set cookie, return
    resp = make_response(message)
    resp.set_cookie('visit-count', str(count))
    return render_template("cookie_splash_page.html")		



@app.route("/blog")

def blog():
	

	
	if request.args.get('id'):
		blog_id = request.args.get('id')
		blog = Blog.query.filter_by(id=blog_id).first()
		
		return render_template("id_splash_page.html", blog = blog)
	
	else:
		
		entries = Blog.query.all()
		
		return render_template("blog.html", entries=entries)
	
@app.route("/newpost", methods=['POST', 'GET'])

def newpost():
	if request.method == 'POST':
		if not request.form['title'] or not request.form['body']:
			if not request.form['title']:
				flash("*'Title for new blog' text area cannot be blank.")
			if not request.form['body']:
				flash("*'Your new blog' text area can't be empty")
			return render_template("newpost.html")
		
		blog_title = request.form['title']
		blog_body = request.form['body']
		post = Blog(blog_title, blog_body)
		db.session.add(post)
		db.session.commit()
		
		id = str(post.id)
		
		return redirect("/blog?id=" + id)
	
	return render_template("newpost.html")


def get_weather(address):
    api_key = "31fa9e666ed5ad3d3511e188e7c4d143"
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    forecast = forecastio.load_forecast(api_key, latitude, longitude).currently()
    summary = forecast.summary
    temperature = forecast.temperature
    return render_template("weather.html")


		
if __name__ == "__main__":
	app.run()