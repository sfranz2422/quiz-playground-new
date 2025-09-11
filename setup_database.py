
import psycopg
import os

def setup_database():
    with psycopg.connect(
        host=os.environ['PGHOST'],
        dbname=os.environ['PGDATABASE'],
        user=os.environ['PGUSER'],
        password=os.environ['PGPASSWORD']
    ) as conn:
        with conn.cursor() as cur:
            # Create users table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    teacherId SERIAL PRIMARY KEY,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    subscribed VARCHAR(10) DEFAULT '0',
                    key VARCHAR(255),
                    tfa VARCHAR(10),
                    thedate TIMESTAMP,
                    ip VARCHAR(50),
                    phone VARCHAR(20),
                    fname VARCHAR(100),
                    lname VARCHAR(100),
                    school VARCHAR(200)
                )
            """)

            # Create complete_questions table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS complete_questions (
                    id SERIAL PRIMARY KEY,
                    quizId VARCHAR(255),
                    questionNumber VARCHAR(255),
                    questionText TEXT,
                    answer1 TEXT,
                    answer2 TEXT,
                    answer3 TEXT,
                    answer4 TEXT,
                    correctAnswer VARCHAR(255),
                    questionSetTitle TEXT,
                    questionSetDescription TEXT,
                    questionSetPrivate VARCHAR(255),
                    teacherId INTEGER,
                    subject VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    youtubeurl TEXT
                )
            """)

            # Create results table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id SERIAL PRIMARY KEY,
                    questionId INTEGER,
                    correct INTEGER,
                    incorrect INTEGER,
                    teacherId INTEGER,
                    quizid VARCHAR(255),
                    quiztitle TEXT,
                    questiontext TEXT
                )
            """)

            # Create quizids table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS quizids (
                    id SERIAL PRIMARY KEY,
                    quizId VARCHAR(255) UNIQUE
                )
            """)

            # Create login_attempts table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id SERIAL PRIMARY KEY,
                    ip VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    attempts INTEGER DEFAULT 1,
                    date VARCHAR(255)
                )
            """)

            print("Database tables created successfully!")

if __name__ == "__main__":
    setup_database()
