# app/register_user.py

import streamlit as st
import sqlite3
from passlib.hash import bcrypt

DB_PATH = "users.db"

def create_user_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, name TEXT, email TEXT, password TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, name, email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)",
              (username, name, email, bcrypt.hash(password)))
    conn.commit()
    conn.close()

def user_exists(username, email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
    data = c.fetchone()
    conn.close()
    return data is not None


def registration_form():
    st.title("🔐 Create New Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not (name and email and username and password and confirm):
            st.error("Please fill out all fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        elif user_exists(username, email):
            st.error("Username or Email already exists.")
        else:
            add_user(username, name, email, password)
            st.success("🎉 Registration successful! You can now login.")
