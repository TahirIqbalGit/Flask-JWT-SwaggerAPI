from flask import Flask, Blueprint, request, render_template, session, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models.user import UserModel
from models.product import ProductModel
from main import db

site = Blueprint('site', __name__   )

@site.route('/', methods=['GET'])
def home():
    item = ProductModel.find_all()
    return render_template('index.html', item=item)


@site.route('/signup', methods=['GET', 'POST'])
def signup():
    req = request.form
    print(req)
    if request.method == "POST":
        # getting form data
        username = req.get("username")
        email = req.get("email")
        password = req.get("password")
        rpassword = req.get("rpassword")
        p_id = str(uuid.uuid4())
        print(f'{email},,, {password}')
        if password != rpassword:
            return "Password doesn't match"
        
        
        hashed_password = generate_password_hash(password, method='sha256')
                
        # adding record in database
        record = UserModel(username=username, email=email, password=hashed_password, is_admin=False)
        print(record)
        db.session.add(record)
        db.session.commit()
        session['email'] = email
        session["password"] = password
        return redirect(url_for('site.admin'))
    
    return render_template("signup.html")
    
@site.route('/login', methods=['GET', 'POST'])
def login():
    req = request.form
    print(req)

    if request.method == "POST":
        email = req.get("email")
        password = req.get("password")
        print(email, password)
        
        user = UserModel.find_by_email(email=email)
        if check_password_hash(user.password, password):
            session['email'] = email
            session["password"] = password
            return redirect(url_for('site.admin', user=user))
        return 'Wrong email or password'
    
    if ("email" in session) and ("password" in session):
        user = UserModel.find_by_email(session['email'])
        return redirect(url_for('site.admin', user=user))
    
    return render_template("login.html")


@site.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    session.pop('password', None)
    # return redirect(url_for("login.login_page"))  # route and function name
    return redirect(url_for('site.home'))


@site.route('/dashboard', methods=['GET', 'POST'])
def admin():
    req = request.form
    if ("email" in session) and ("password" in session):
        user = UserModel.find_by_email(session["email"])
        if user.is_admin and request.method == "POST":
            # Validating Empty Fields
            missing = list()
            # Getting Immutable Multi Dict Data
            for k, v in req.items():
                if v == "":
                    missing.append(k)
            if missing:
                comment = f"<h3>Missing field: {',  '.join(missing)}</h3>".title()
                return comment + "<h3><i>Note: Please fill out all fields</i></h3>"
            
            name = req.get('name')
            price = req.get('price')
            category = req.get('category')
            user_id = user.id
            
            record = ProductModel(name, price, category, user_id)
            print(record)
            db.session.add(record)
            db.session.commit()
            return '<h3>Product Added to Store Successfully<br>Click <a href="/">Home</a> to check your product listing on Store</h3>'
        
        return render_template("admin.html", user=user)
    
    return redirect(url_for('site.login'))