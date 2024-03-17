import os
from flask import Flask, render_template, redirect,request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Double

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://userInventory:Inventory@mysqldb/Inventory"

db = SQLAlchemy(app)

class Inventory(db.Model):
    __tablename__:'inventory'
    id = db.Column(Integer,primary_key=True,autoincrement=True)
    name = db.Column(String(50))
    price = db.Column(Double)
    mac_address = db.Column(String(50))
    serial_number = db.Column(String(50))
    manufacturer = db.Column(String(50))
    description = db.Column(String(140))


@app.route("/",methods=["GET"])
def home():
    objects = db.session.execute(db.select(Inventory).order_by(Inventory.id)).scalars().all()
    return render_template('index.html',inventory=objects)

@app.route("/add",methods=['GET',"POST"])
def add_object():
    if request.method == "POST":
        new_item = Inventory(
            name=request.form['name'],
            price=request.form['price'],
            mac_address=request.form['mac_address'],
            serial_number=request.form['serial_number'],
            manufacturer=request.form['manufacturer'],
            description=request.form['description']
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect("/",code=302)
    return render_template('create-form.html')

@app.route("/edit/<int:id>", methods=['GET','POST'])
def update_object(id):
    item = db.get_or_404(Inventory,id)
    if request.method == "POST":
        item.name = request.form['name']
        item.price = request.form['price']
        item.mac_address = request.form['mac_address']
        item.serial_number = request.form['serial_number']
        item.manufacturer = request.form['manufacturer']
        item.description = request.form['description']
        db.session.commit()
        return redirect ("/",code=302)
    return render_template('update-form.html',inventory=item)

@app.route("/delete/<int:id>",methods=['GET'])
def delete_object(id):
    item = db.get_or_404(Inventory,id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host="0.0.0.0")