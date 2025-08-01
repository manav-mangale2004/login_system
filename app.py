from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a strong secret in production

# MySQL connection with custom username and password
db = mysql.connector.connect(
    host="localhost",
    user="manav_user",         
    password="manav_pass",    
    database="login_db"        
)
cursor = db.cursor()

# Home Page
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
