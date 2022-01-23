from main import ma
from models.product import ProductModel
from models.user import UserModel

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel
        load_instance = True
        load_only = ("user",)
        include_fk = True