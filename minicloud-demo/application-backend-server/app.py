from flask import Flask, jsonify, request
import time, requests, os, json
from jose import jwt
import pymysql 

ISSUER = os.getenv("OIDC_ISSUER", "http://localhost:8081/realms/realm_sv001")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "flask-app")

INTERNAL_KEYCLOAK_URL = ISSUER.replace("localhost:8081", "authentication-identity-server:8080")
JWKS_URL = f"{INTERNAL_KEYCLOAK_URL}/protocol/openid-connect/certs"

_JWKS = None; _TS = 0

def get_jwks():
    global _JWKS, _TS
    now = time.time()
    if not _JWKS or now - _TS > 600:
        _JWKS = requests.get(JWKS_URL, timeout=5).json()
        _TS = now
    return _JWKS

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='relational-database-server', 
        user='root',
        password='root', 
        database='studentdb',
        cursorclass=pymysql.cursors.DictCursor 
    )

@app.get("/hello")
def hello(): return jsonify(message="Hello from App Server!")

@app.get("/student")
def student():
    try:
        with open("students.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.get("/student-db")
def student_from_db():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM students"
            cursor.execute(sql)
            result = cursor.fetchall() 
            return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        if conn: conn.close()

@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = auth.split(" ",1)[1]
    try:
        payload = jwt.decode(token, get_jwks(), algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
        return jsonify(message="Secure resource OK", preferred_username=payload.get("preferred_username"))
    except Exception as e:
        return jsonify(error=str(e)), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)