import hashlib
import os

def hash_password(password):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), b"manii-cafe", 120000
    ).hex()

def verify_password(password, stored):
    return hash_password(password) == stored
