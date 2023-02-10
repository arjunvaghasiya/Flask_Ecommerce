from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from werkzeug.security import check_password_hash , generate_password_hash
from sqlalchemy import Float, ForeignKey, Integer,Column,String,Boolean,Date


db = SQLAlchemy()

class Users(db.Model,UserMixin):
    
    __tablename__ = "users"
    user_id = Column(Integer,primary_key  = True,autoincrement = True)
    username = Column(String(300),nullable = False, unique = True)
    email = Column(String(300),nullable = False, unique = True)
    first_name =  Column( String(100),nullable = True)
    last_name =  Column( String(100),nullable = True)
    gender = Column(String(100),nullable =True)
    dob = Column( Date,nullable = True)
    phone =  Column( String(400),nullable = True,unique = True)
    address =  Column( String(400),nullable = True)
    password_hash = Column(String(300),nullable = False,server_default= '')
    is_guest = Column(Boolean(),server_default='1')
    is_registered = Column(Boolean(),server_default='0')
    is_manager = Column(Boolean(),server_default='0')
    is_admin = Column(Boolean(),server_default='0')
    
    @property
    def password(self):
        raise AttributeError(' password is not readable')
    
    @password.setter
    def password(self,password):
        # import pdb;pdb.set_trace()
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)    
    
    def __repr__(self) -> str:
        return self.username

class Products( db.Model,UserMixin):
    __tablename__ = "products"
    product_id =  Column( Integer,primary_key  = True,autoincrement = True)
    product_name = Column( String(400),nullable = True)
    product_discription = Column( String(600),nullable = True)
    product_price = Column( Float,nullable = True)
    total_items = Column(Integer,nullable = True)
    available_items = Column(Integer,nullable = True)
    
    
    def __repr__(self) -> str:
        return self.product_id
    
class PaymentDetails(db.Model,UserMixin):
    
    user_id_fk = Column(Integer,ForeignKey('users.user_id'))
    product_id_fk = Column(Integer,ForeignKey('products.product_id'))
    payment_id = Column(Integer,primary_key  = True,autoincrement = True)
    payment_method = Column( String(400),nullable = True)
    product_name = Column(String(400),nullable = True)
    product_price = Column( Float,nullable = True)
    total_items = Column( Integer,nullable = True)
    payment_amount = Column(Float,nullable=True)

    def __repr__(self) -> str:
        return self.payment_id 
    
class MyCart(db.Model,UserMixin):
    
    user_id_fk = Column(Integer,ForeignKey('users.user_id'))
    product_id_fk = Column(Integer,ForeignKey('products.product_id'))
    cart_id = Column(Integer,primary_key  = True,autoincrement = True)
    item_name = Column( String(400),nullable = True)
    total_items = Column( Integer,nullable = True)
    item_amount = Column(Float,nullable=True)
    total_items_price = Column(Float,nullable=True)
    
    def __repr__(self) -> str:
        return self.cart_id 