from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for using session

# ---------- ROUTES ----------

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('goldsgym.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM tbl_user WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = user['username']  # 🧠 store user in session
            return redirect(url_for('home'))        # redirect to home page
        else:
            return "Invalid username or password."

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['full-name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('goldsgym.db')
        c = conn.cursor()
        c.execute("INSERT INTO tbl_user (username, email, password) VALUES (?, ?, ?)",
                  (username, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/program')
def program():
    return render_template('program.html')


@app.route('/coaches')
def coaches():
    return render_template('coaches.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/inquire', methods=['GET', 'POST'])
def inquire():
    if request.method == 'POST':
        coach = request.form['coach-name']
        email = request.form['user-email']
        message = request.form['message']

        conn = sqlite3.connect('goldsgym.db')
        c = conn.cursor()
        c.execute("INSERT INTO tbl_inquire (coach, email, message) VALUES (?, ?, ?)",
                  (coach, email, message))
        conn.commit()
        conn.close()

        return render_template('inquiry_success.html')


    coach_name = request.args.get('coach', '')
    return render_template('inquire.html', coach_name=coach_name)






if __name__ == '__main__':
    app.run(debug=True)
