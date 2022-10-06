from flask import Flask,request,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from passlib.hash import pbkdf2_sha256
from flask_migrate import Migrate
import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/Hospital_Management'

class Development_Config(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:1234@localhost/Hospital_Management'

class Production_Config(Config):
    uri=os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri=uri.replace("postgres://","postgresql://",1)
    SQLALCHEMY_DATABASE_URI = uri

env = os.environ.get("ENV","Development") #here development is default or get the environment
if env=="Production":
    config_str=Production_Config
else:
    config_str = Development_Config



app=Flask(__name__)
app.config.from_object(config_str)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:1234@localhost/Hospital_Management'
api=Api(app)
db=SQLAlchemy(app)
migrate=Migrate(app,db)


class Medicine(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    medi_name=db.Column(db.String(50),unique=True, nullable=False)
    quantity=db.Column(db.String)
    rate=db.Column(db.String)

    @staticmethod
    def add_medicine(med_name, quantity, rate):
        new_med = Medicine(medi_name=med_name, quantity=quantity, rate=rate)
        db.session.add(new_med)
        db.session.commit()

    @staticmethod
    def get_med_by_name(name):
        return Medicine.query.filter_by(medi_name=name).first()

    @staticmethod
    def get_all_medicines():
        return Medicine.query.all()

    @staticmethod
    def delete_med_by_name(name):
        result = Medicine.query.filter_by(medi_name=name).delete()
        db.session.commit()
        return result

    @staticmethod
    def update_data_by_medname(name, qty, rate):
        print("enter")
        medi_data = Medicine.query.filter_by(medi_name=name).first()
        medi_data.medi_name = name
        medi_data.quantity = qty
        medi_data.rate = rate
        db.session.commit()


class Admin(db.Model):
    emp_id=db.Column(db.Integer, primary_key=True)
    admin_name=db.Column(db.String(50),nullable=False)
    admin_email=db.Column(db.String(20),unique=True)
    admin_password=db.Column(db.String(200),unique=True,nullable=False)

    @staticmethod
    def add_admin(user_name,email,password):
        new_user = Admin(admin_name=user_name, admin_email=email, admin_password=password)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_user_by_name(user_name):
        return Admin.query.filter_by(admin_email=user_name).first()


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(50),unique=True,nullable=False)
    phone_no=db.Column(db.String(10),unique=True)
    age=db.Column(db.String(5))
    bed_type=db.Column(db.String(20))
    address=db.Column(db.String(200))
    state=db.Column(db.String(100))
    city=db.Column(db.String(100))


    @staticmethod
    def add_patient(user_name,phone_no,age,bed_type,address,state,city):
        new_user = Patient(user_name=user_name,phone_no=phone_no,
                           age=age,bed_type=bed_type,address=address,
                           state=state,city=city)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_all_patients():
        return Patient.query.all()


    @staticmethod
    def get_user_by_name(user_name):
        return Patient.query.filter_by(user_name=user_name).first()

    @staticmethod
    def get_user_by_phone_no(phone_no):
        return Patient.query.filter_by(phone_no=phone_no).first()

    @staticmethod
    def delete_patient_by_phone(phone):
        result = Patient.query.filter_by(phone_no=phone).delete()
        db.session.commit()
        return result

    @staticmethod
    def update_data_by_phone(name,phone_no,age,bed_type,address,state,city):
        print("enter")
        patient_data = Patient.query.filter_by(phone_no=phone_no).first()
        print("data")
        patient_data.user_name = name
        print(patient_data.user_name)
        patient_data.phone_no = phone_no
        patient_data.age = age
        patient_data.bed_type = bed_type
        patient_data.address = address
        patient_data.state = state
        patient_data.city = city
        db.session.commit()



@app.route("/",methods=['GET','POST'])
def home_page():
    print("home")
    return render_template("new_home_page.html")

@app.route("/contact",methods=['GET','POST'])
def contact_page():
    return render_template("contact.html")

@app.route("/signup",methods=["GET","POST"])
def first_time_register_page():
    print("Inside")
    if request.method=="POST":
        print("here")
        user=request.form['user_name']
        print(user)
        phone_no=request.form['phone_no']
        age=request.form['age']
        bed_type=request.form['bed_type']
        address=request.form['address']
        state=request.form['state']
        city=request.form['city']

        single_user = Patient.get_user_by_phone_no(phone_no)
        print(single_user)
        if single_user:
            return render_template("signup.html", data="Exists_already")
        else:
            try:
                Patient.add_patient(user, phone_no,age, bed_type, address
                                 , state, city)
            except:
                return render_template("signup.html", data="Exists_already")
        return render_template("signup.html",data="new_user")
    else:
        return render_template("signup.html")


@app.route("/add_medicines",methods=["GET","POST"])
def medi_add_page():
    print("Inside")
    if request.method=="POST":
        print("here")
        med_name=request.form['med_name']
        print(med_name)
        qty=request.form['qty']
        rate=request.form['rate']
        print(rate)
        single_med = Medicine.get_med_by_name(med_name)
        print(single_med)
        if single_med:
            return render_template("add_medi.html", data="Exists_already")
        else:
            try:
                Medicine.add_medicine(med_name, qty,rate)
            except:
                return render_template("add_medi.html", data="Exists_already")
        return render_template("add_medi.html",data="new_med")
    else:
        return render_template("add_medi.html")




@app.route("/admin_sign_up",methods=['GET','POST'])
def admin_signup_page():
    if request.method=="POST":
        print("here")
        user=request.form['user_name']
        print(user)
        email=request.form['email']
        admin_pwd=request.form['admin_pwd']
        hashed_pwd = pbkdf2_sha256.hash(admin_pwd)
        single_user = Admin.get_user_by_name(user)
        print(single_user)
        if single_user:
            return render_template("admin_sign_up.html", data="Exists_already")
        else:
            Admin.add_admin(user,email,hashed_pwd)
        return render_template("admin_sign_up.html", data="new_user")
    else:
        return render_template("admin_sign_up.html")



@app.route("/admin",methods=['GET','POST'])
def admin_login_page():
    print("in admin")
    if request.method == "POST":
        print("inside admin")
        admin_email = request.form["admin_email"]
        password = request.form["pwd"]
        single_user = Admin.get_user_by_name(admin_email)
        print(single_user)
        print(password)
        if single_user and pbkdf2_sha256.verify(password, single_user.admin_password):
            print("Success")
            return render_template("details_info.html")
        else:
            return render_template("admin_login.html", data="user_unidentified")
    else:
        return render_template("admin_login.html", data=None)

@app.route("/get_all_patients",methods=['GET','POST'])
def get_all_patients():
    data=Patient.get_all_patients()
    return render_template("all_patients.html",data=data)

@app.route("/get_all_medicines",methods=['GET','POST'])
def get_all_medicines():
    data=Medicine.get_all_medicines()
    return render_template("all_medicines.html",data=data)

@app.route("/get_single_patient",methods=['GET','POST'])
def get_single_patient():
    print("Inside function single")
    if request.method == "POST":
        print("Single patient")
        phone_no = request.form["phn_no"]
        print(phone_no)
        data=Patient.get_user_by_phone_no(phone_no)
        print(data)
        if data:
            return render_template("single_patient.html", data=data)
        else:
            print("else")
            return render_template("single_patient.html", data="no_match")
    else:
        return render_template("single_patient.html", data=None)

@app.route("/get_medi_by_name",methods=['GET','POST'])
def get_single_medi():
    print("Inside function single med")
    if request.method == "POST":
        print("Single med")
        med_name = request.form["med_name"]
        print(med_name)
        data=Medicine.get_med_by_name(med_name)
        print(data)
        if data:
            return render_template("single_med.html", data=data)
        else:
            print("else")
            return render_template("single_med.html", data="no_match")
    else:
        return render_template("single_med.html", data=None)

@app.route("/delete_single_patient",methods=['GET','POST'])
def delete_patient():
    print("in delete")
    if request.method=="POST":
        phone_no = request.form["phn_no"]
        print(phone_no)
        data1 = Patient.delete_patient_by_phone(phone_no)
        print(data1)
        if data1:
            return render_template("single_patient.html", data="Deleted")
        else:
            return render_template("single_patient.html", data="no_match")

    else:
        return render_template("single_patient.html", data=None)

@app.route("/delete_single_med",methods=['GET','POST'])
def delete_med():
    print("in delete")
    if request.method=="POST":
        med_name = request.form["med_name"]
        print(med_name)
        data1 = Medicine.delete_med_by_name(med_name)
        print(data1)
        if data1:
            return render_template("single_med.html", data="Deleted")
        else:
            return render_template("single_med.html", data="no_match")

    else:
        return render_template("single_med.html", data=None)

@app.route("/back",methods=['GET','POST'])
def back():
    return render_template("details_info.html")


@app.route("/edit_patient",methods=['GET','POST'])
def edit_patient():
    if request.method=="POST":
        print("here")
        phone_no=request.form['phn_no']
        data= Patient.get_user_by_phone_no(phone_no)
        if data:
            return render_template("edit.html",data=data)
        else:
            return render_template("edit.html", data="no_match")
    else:
        return render_template("single_patient.html")


@app.route("/edit",methods=['GET','POST'])
def edit_patient_page():
    print("in edit")
    if request.method=="POST":
        print("in post")
        name=request.form['name']
        print(name)
        phone_no = request.form['phone_no']
        age=request.form['age']
        bed_type = request.form['bed_type']
        addr = request.form['addr']
        state = request.form['state']
        city = request.form['city']
        print(age)
        try:
            Patient.update_data_by_phone(name,phone_no,age,bed_type,addr,state,city)
            return render_template("edit.html",data="success update")
        except:
            return render_template("edit.html", data="Wrong details")
    else:
        return render_template("edit.html")


@app.route("/edit_med",methods=['GET','POST'])
def edit_medicine():
    if request.method=="POST":
        print("here")
        name=request.form['med_name']
        data= Medicine.get_med_by_name(name)
        if data:
            return render_template("edit_med.html",data=data)
        else:
            return render_template("edit_med.html", data="no_match")
    else:
        return render_template("single_med.html")


@app.route("/update_med",methods=["GET","POST"])
def update_page():
    print("in edit")
    if request.method=="POST":
        print("in post")
        name=request.form['med_name']
        print(name)
        qty = request.form['qty']
        rate=request.form['rate']
        print(rate)
        try:
            Medicine.update_data_by_medname(name,qty,rate)
            return render_template("edit_med.html",data="success update")
        except:
            return render_template("edit_med.html", data="Wrong details")
    else:
        return render_template("edit_med.html")


if __name__=="__main__":
    app.run(port=5001)



