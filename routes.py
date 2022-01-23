from flask import Flask, Blueprint, request, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models.user import UserModel
from models.product import ProductModel
from main import db

site = Blueprint('site', __name__   )

@site.route('/', methods=['GET'])
def home():
    item = ProductModel.find_all()
    user = UserModel.find_all()
    return render_template('index.html', item=item, user=user)


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
        return 'Signup Successfully'
    
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
            return 'Logged in Successfully'
        return 'Wrong email or password'
    
    if ("email" in session) and ("password" in session):
        # user = User.query.filter(User.email == session['email'], User.password == session['password']).first()
        # return redirect(url_for("admin.profile"))
        return 'Already Logged in'
    
    return render_template("login.html")


@site.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    session.pop('password', None)
    # return redirect(url_for("login.login_page"))  # route and function name
    return 'Signout Successfully'