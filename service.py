from flask import Flask, request, jsonify, send_from_directory, redirect
import redis
import psycopg2
import os
import hashlib

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Get hostname to identify which instance is serving
HOSTNAME = os.getenv('HOSTNAME', 'unknown')

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "shortener")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
cursor = conn.cursor()

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.json
    long_url = data.get("url")
    if not long_url:
        return jsonify({"error": "URL is required"}), 400
    short_hash = hashlib.md5(long_url.encode()).hexdigest()[:6]
    r.set(short_hash, long_url)
    cursor.execute("INSERT INTO urls (short, long) VALUES (%s, %s) ON CONFLICT (short) DO NOTHING", (short_hash, long_url))
    conn.commit()
    return jsonify({"short_url": short_hash})

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route("/instance")
def instance():
    return jsonify({"instance": HOSTNAME})

@app.route("/<short>", methods=["GET"])
def redirect_short(short):
    long_url = r.get(short)
    if not long_url:
        cursor.execute("SELECT long FROM urls WHERE short = %s", (short,))
        result = cursor.fetchone()
        if result:
            long_url = result[0]
            r.set(short, long_url)
            return redirect(long_url)
        else:
            return jsonify({"error": "Short URL not found"}), 404
    return redirect(long_url)

@app.route("/expand", methods=["GET"])
def expand():
    short_url = request.args.get('url')
    if not short_url:
        return jsonify({"error": "URL parameter is required"}), 400
    # Extract the short code from the URL
    short_code = short_url.split('/')[-1]
    long_url = r.get(short_code)
    if not long_url:
        cursor.execute("SELECT long FROM urls WHERE short = %s", (short_code,))
        result = cursor.fetchone()
        if result:
            long_url = result[0]
            r.set(short_code, long_url)
        else:
            return jsonify({"error": "Short URL not found"}), 404
    return jsonify({"long_url": long_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
