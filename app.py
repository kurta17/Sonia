from flask import Flask
import psycopg2
from psycopg2 import pool

app = Flask(__name__)

# Database connection pool
try:
    db_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,
        user="postgres",
        password="your_password",
        host="127.0.0.1",
        port="5432",
        database="shoes_db"
    )
except Exception as e:
    print(f"Error connecting to database: {e}")

@app.route('/')
def index():
    try:
        # Get a connection from the pool
        conn = db_pool.getconn()
        cur = conn.cursor()
        
        # Example query
        cur.execute("SELECT * FROM shoes")
        shoes = cur.fetchall()
        
        # Clean up
        cur.close()
        db_pool.putconn(conn)
        
        return f"Shoes in database: {shoes}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)