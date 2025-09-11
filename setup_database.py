
import pg8000
import os
import urllib.parse as up

def setup_database():
    url = os.environ['DATABASE_URL']
    p = up.urlparse(url)
    database_name = p.path[1:] if p.path and len(p.path) > 1 else 'neondb'
    
    conn = pg8000.connect(
        host=p.hostname,
        port=p.port or 5432,
        database=database_name,
        user=p.username,
        password=p.password,
        ssl_context=True
    )
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
        conn.commit()
    conn.close()

