import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()



# Connect to flask_db with psycopgg2
conn = psycopg2.connect(
    host="localhost",
    database="flask_db",
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
)

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute(f"DROP TABLE IF EXISTS requests;")
cur.execute(
    f"CREATE TABLE requests (id uuid DEFAULT gen_random_uuid() PRIMARY KEY,"
    "request_feedback_on text NOT NULL,"
    "date_added date DEFAULT CURRENT_TIMESTAMP);"
)

cur.execute(f"INSERT INTO requests (request_feedback_on) VALUES ('I want feedback on nothing.') RETURNING id")

id_of_new_row = cur.fetchone()[0]

cur.execute(f"SELECT * from requests where id = '{id_of_new_row}'")

results = cur.fetchone()

print(results)


# Execute a command: this creates a new table
# DROP TABLE IF EXISTS
cur.execute("DROP TABLE IF EXISTS books;")

# CREATE TABLE BOOKS
cur.execute(
    "CREATE TABLE books (id serial PRIMARY KEY,"
    "title varchar (150) NOT NULL,"
    "author varchar (50) NOT NULL,"
    "pages_num integer NOT NULL,"
    "review text,"
    "date_added date DEFAULT CURRENT_TIMESTAMP);"
)

# Insert data into the table
cur.execute(
    "INSERT INTO books (title, author, pages_num, review)" "VALUES (%s, %s, %s, %s)",
    ("A Tale of Two Cities", "Charles Dickens", 489, "A great classic!"),
)

cur.execute(
    "INSERT INTO books (title, author, pages_num, review)" "VALUES (%s, %s, %s, %s)",
    ("Anna Karenina", "Leo Tolstoy", 864, "Another great classic!"),
)


conn.commit()

cur.close()
conn.close()
