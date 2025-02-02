import os
import hashlib
import sqlite3
import random
import math
import hashlib

from sympy import nextprime

DB_PATH = "app/db/users.db"
user = "bradley"
pswd = "r0k3t"


def string_to_number(data: str):
    hash_obj = hashlib.sha256(data.encode())
    hash_int = int(hash_obj.hexdigest(), 16)
    return hash_int % (10**9)


def salt(data: str):
    data_number = string_to_number(data.decode())
    SEED = int(math.e * 1e9)
    random.seed(SEED)
    a = nextprime(random.randint(10**8, 10**9))
    b = nextprime(random.randint(10**8, 10**9))
    m = 10**9
    salted_number = (a * data_number + b) % m
    return f"{salted_number:09d}"


def md5_hash(password):
    return hashlib.md5(str(salt(password.encode("utf-8"))).encode("utf-8")).hexdigest()


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"""
    )
    cursor.execute(
        """INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)""",
        (user, md5_hash(pswd)),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
