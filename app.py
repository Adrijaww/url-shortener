from flask import Flask, request, redirect, render_template
import psycopg2
import os
import string
import random

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS urls (short TEXT, long TEXT)')
    conn.commit()
    conn.close()

def generate_short():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['url']
        short = generate_short()

        conn = get_conn()
        c = conn.cursor()
        c.execute("INSERT INTO urls VALUES (%s, %s)", (short, long_url))
        conn.commit()
        conn.close()

        return f"Short URL: {request.host_url}{short}"

    return render_template('index.html')

@app.route('/<short>')
def redirect_url(short):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT long FROM urls WHERE short=%s", (short,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    return "URL not found!"

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)