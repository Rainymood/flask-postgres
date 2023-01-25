import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, redirect

load_dotenv()

IMAGES_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER

def add_leading_slash(image_link):
    """For some reason static/images/image.png doesn't work, /static/images/image.png does"""
    if not image_link.startswith("/"): 
        return "/" + image_link

HAPPY_SMILEY = add_leading_slash(os.path.join(IMAGES_FOLDER, "happy.png"))
NEUTRAL_SMILEY = add_leading_slash(os.path.join(IMAGES_FOLDER, "neutral.png"))
SAD_SMILEY = add_leading_slash(os.path.join(IMAGES_FOLDER, "SAD.png"))


def get_db_connection():
    """Return connection to postgres db"""
    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
    )
    return conn


@app.route("/create/", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        pages_num = int(request.form["pages_num"])
        review = request.form["review"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, pages_num, review)"
            "VALUES (%s, %s, %s, %s)",
            (title, author, pages_num, review),
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("index"))
    return render_template("create.html")


@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books;")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", books=books)

@app.route("/request/<uuid:id>/")
def generated_request(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT request_feedback_on FROM requests where id = '{id}';")
    text = cur.fetchone()[0]
    cur.close()
    conn.close()

    return render_template("give.html", request_feedback_on=text, happy=HAPPY_SMILEY, neutral=NEUTRAL_SMILEY, sad=SAD_SMILEY)


@app.route("/copy/<uuid:id>/")
def copy(id):
    url = url_for("generated_request",id=id, _external=True)
    return render_template("copy.html", url=url)

@app.route("/request/", methods=["GET", "POST"])
def request_feedback():
    # If we fill in the form
    if request.method == "POST":
        request_feedback_on = request.form["request_feedback_on"]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO requests (request_feedback_on) VALUES ('{request_feedback_on}') RETURNING id")
        id = str(cur.fetchone()[0])
        conn.commit()
        cur.close()
        conn.close()
        # redirect to url with param
        return redirect(url_for("copy", id=id))
    # Otherwise render template
    return render_template("request.html")
