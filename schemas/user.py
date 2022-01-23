from main import ma
from models.user import UserModel
from models.product import ProductModel
from schemas.product import ProductSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    products = ma.Nested(ProductSchema, many=True)
    
    class Meta:
        model = UserModel
        load_instance = True
        include_fk = True