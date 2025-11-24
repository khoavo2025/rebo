from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",    # sửa nếu có mật khẩu
        database="vat_tu_db"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/danh-sach")
def danh_sach():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM vat_tu")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("danh_sach.html", vat_tu=data)

@app.route("/nhap", methods=["GET", "POST"])
def nhap():
    if request.method == "POST":
        vat_tu_id = request.form["vat_tu_id"]
        so_luong = int(request.form["so_luong"])

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE vat_tu SET so_luong = so_luong + %s WHERE id = %s",
                       (so_luong, vat_tu_id))

        cursor.execute(
            "INSERT INTO lich_su (vat_tu_id, loai, so_luong, ngay) VALUES (%s, 'nhap', %s, %s)",
            (vat_tu_id, so_luong, datetime.now())
        )

        db.commit()
        cursor.close()
        db.close()
        return redirect("/danh-sach")

    return render_template("nhap.html")

@app.route("/xuat", methods=["GET", "POST"])
def xuat():
    if request.method == "POST":
        vat_tu_id = request.form["vat_tu_id"]
        so_luong = int(request.form["so_luong"])

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT so_luong FROM vat_tu WHERE id = %s", (vat_tu_id,))
        ton = cursor.fetchone()

        if ton and ton[0] >= so_luong:
            cursor.execute("UPDATE vat_tu SET so_luong = so_luong - %s WHERE id = %s",
                           (so_luong, vat_tu_id))

            cursor.execute(
                "INSERT INTO lich_su (vat_tu_id, loai, so_luong, ngay) VALUES (%s, 'xuat', %s, %s)",
                (vat_tu_id, so_luong, datetime.now())
            )
            db.commit()

        cursor.close()
        db.close()
        return redirect("/danh-sach")

    return render_template("xuat.html")

if __name__ == "__main__":
    app.run(debug=True)
