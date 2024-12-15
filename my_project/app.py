from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Veritabanını başlatma
def init_db():
    conn = sqlite3.connect("users.db")  # users.db adlı bir veritabanı oluşturur
    cursor = conn.cursor()
    # Kullanıcı tablosu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        try:
            # Veritabanına kullanıcı ekle
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return "Kayıt Başarılı!"
        except sqlite3.IntegrityError:
            return "Bu kullanıcı adı zaten alınmış!"
    
    return render_template("register.html")

if __name__ == "__main__":
    init_db()  # Sunucu başlamadan önce veritabanını oluştur
    app.run(debug=True)
@app.route("/users")
def users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()  # Tüm kullanıcıları al
    conn.close()
    return render_template("users.html", users=users)


