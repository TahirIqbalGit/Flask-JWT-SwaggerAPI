from main import db

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    # public_id = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
   
    products = db.relationship("ProductModel", lazy="dynamic", primaryjoin="UserModel.id == ProductModel.user_id")
    
    def __init__(self, username, email, password, is_admin, **kwargs):
        # self.public_id = public_id
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin
        
    def __repr__(self):
        return 'UserModel(username=%s, is_admin=%s' % (self.username, self.is_admin)
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()