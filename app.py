from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load DB config from db.yaml
db_config = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)

app.config['MYSQL_HOST'] = db_config['mysql_host']
app.config['MYSQL_USER'] = db_config['mysql_user']
app.config['MYSQL_PASSWORD'] = db_config['mysql_password']
app.config['MYSQL_DB'] = db_config['mysql_db']

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session['username'] = username
            return redirect('/')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/suggestions', methods=['POST'])
def suggestions():
    current_location = request.form['current_location']
    destination = request.form['destination']
    days = int(request.form['days'])

    cur = mysql.connection.cursor()

    # Fetch places based on destination and days
    cur.execute("SELECT place_name, place_description FROM places WHERE destination=%s AND days<=%s", (destination, days))
    places = cur.fetchall()

    # Fetch hotels based on destination
    cur.execute("SELECT name, rating, review FROM hotels WHERE destination=%s", (destination,))
    hotels = cur.fetchall()

    cur.close()

    return render_template("suggestions.html", destination=destination, days=days, places=places, hotels=hotels)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
