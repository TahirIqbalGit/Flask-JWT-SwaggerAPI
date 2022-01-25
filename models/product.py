from main import db

class ProductModel(db.Model):
    __tablename__ = "product"
    
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("UserModel",)
    
    def __init__(self, name, price, category, user_id):
        self.name = name
        self.price = price
        self.category = category
        self.user_id = user_id
        
    def __repr__(self):
        return 'User(name=%s, price=%s, category=%s,user_id=%s' % (self.name, self.price, self.category, self.user_id)
    
    def json(self):
        return {'name': self.name, 'price': self.price}
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_category(cls, category):
        return cls.query.filter_by(category=category).all()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()