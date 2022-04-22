from flask import Flask, render_template, url_for,flash, redirect, request, jsonify
from apurva_flask_app.forms import RegistrationForm, LoginForm, addemployeeform
from apurva_flask_app.model import User,Offices,Employees
from apurva_flask_app import app, db, bcrypt,Base
from flask_login import login_user,current_user,logout_user,login_required
import json
from flask_cors import CORS
from sqlalchemy import desc
#offices = db.Table('offices', db.metadata, autoload=True,autoload_with = db.engine)


Office = Base.classes.offices
Employee = Base.classes.employees

        
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/office", methods=["GET","POST"])
@login_required
def office():
    data=db.session.query(Office).all()
    return render_template("offices.html",offices=data)


@app.route("/office/<officeid>/employees/",methods=["GET","POST"])
@login_required
def employee(officeid):
    data=db.session.query(Employee).filter_by(officeCode=officeid)
    return render_template("employee.html",employees=data,officeid=officeid)


@app.route("/office/<officeid>/employees/add",methods=['GET','POST'])
@login_required
def addemployee(officeid):
    if current_user.role == 'admin':
        emp_form = addemployeeform()
        if emp_form.validate_on_submit():
            if current_user.role == 'admin':
                emp_data = Employee(employeeNumber=emp_form.employeeNumber.data,lastName=emp_form.lastName.data,firstName=emp_form.firstName.data,
                extension=emp_form.extension.data,email=emp_form.email.data,jobTitle=emp_form.jobTitle.data,officeCode=officeid)
                db.session.add(emp_data)
                db.session.commit()
                return redirect(url_for('employee',officeid=officeid))
            else:
                flash("You dont have these rights")
        return render_template('addemployee.html',form=emp_form)
    else:
        return redirect(url_for('home'))

    

@app.route("/register",  methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(role=form.role.data, username=form.username.data, email=form.email.data, lastName=form.lastName.data,firstName=form.firstName.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form = form) 


@app.route("/login",  methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("login Unsuccessfull.Please check email and password",'danger')

    return render_template('login.html', form = form) 

@app.route("/logout",  methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/api/offices",methods=["GET","POST"])
def api():
    json_data=db.session.query(Offices).all()
    jsondata = [k.serialize() for k in json_data]
    return jsonify(jsondata)


@app.route('/api/offices/employees/<int:officeCode>', methods=['GET'])
def get_Employees(officeCode):
    # emp =db.session.query(Employees).filter(Employees.officeCode == officeCode)
    #emp_details = Employee.query.filter_by(officeCode=officeCode).all()
    emp_details=db.session.query(Employees).filter_by(officeCode=officeCode)

    # result = db.session.query(Offices).join(Employees).filter(Offices.officeCode == Employees.officeCode).all()
    #emp_list=[]
    #for emp in emp_details:
        #emp_list.append(emp.converter())
    jsondata = [k.serialize() for k in emp_details]
    return jsonify(jsondata)

@app.route("/api/new_employee/<officeCode>/", methods=['GET', 'POST'])
def set_employee(officeCode):
  data = request.get_json()
  print("json data:- ", data)
  isValid = validate(data)

  if(isValid.get('ok') == True):
    newEmployeeNumber = db.session.query(Employees).order_by(desc('employeeNumber')).first()
    newEmployeeNumber = newEmployeeNumber.employeeNumber+1
    new_emp = Employees(employeeNumber=newEmployeeNumber, 
                        lastName=data.get('lastName'),
                        firstName=data.get('firstName'), 
                        extension=data.get('extension'),
                        email=data.get('email'), 
                        officeCode=officeCode,
                        jobTitle=data.get('jobTitle'))
    db.session.add(new_emp)
    print(new_emp)
    db.session.commit()

  return isValid

def validate(data):
    toReturn = {"ok": True}
    isEmail = db.session.execute(
        f"SELECT * FROM employees WHERE email = " + "'" +
        str(data.get('email'))+"'").fetchall()
    if(isEmail != []):
        toReturn = {"ok": False,
                    "error": "Email already registered."}
        return toReturn
    return toReturn



