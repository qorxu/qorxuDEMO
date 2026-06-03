import sqlite3
from eralchemy import render_er

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Roles (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               role_name TEXT NOT NULL)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               login TEXT NOT NULL unique,
               password TEXT NOT NULL,
               role_id INTEGER NOT NULL,
               FOREIGN KEY (role_id) REFERENCES Roles (id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Applications (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name_service TEXT NOT NULL unique,
               date DATE NOT NULL,
               payment TEXT NOT NULL,
               status DEFAULT 'Новая',
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               user_id INTEGER NOT NULL,
               FOREIGN KEY (user_id) REFERENCES Users (id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Feedbacks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               application_id INTEGER NOT NULL,
               user_id INTEGER NOT NULL,
               comment TEXT NOT NULL,
               FOREIGN KEY (user_id) REFERENCES Users (id),
               FOREIGN KEY (application_id) REFERENCES Applications (id))
""")

cursor.execute("SELECT COUNT(*) FROM Roles")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO Roles (role_name) VALUES ('user')")
    cursor.execute("INSERT INTO Roles (role_name) VALUES ('admin')")

conn.commit()
conn.close()
render_er('sqlite:///database.db', 'erd.md')