from website import api, app, mail
from flask_restful import Resource, request
from .models import Users, db
from .serializer import *
from flask import jsonify, request, Flask, make_response
from email_validator import validate_email, EmailNotValidError
from website.authentication import *
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_mail import Message
import datetime, re


@app.post("/create/admin/<int:pk>")
def admin_crt(pk):
    create_admin_key = "ihsa99cn9aKAGIA344ADF4bf8d7f21eb"
    data = request.get_json()
    if create_admin_key == data.get("admin_key"):
        user = Users.query.filter_by(user_id=pk).first()
        user.is_guest = True
        user.is_registered = True
        user.is_manager = True
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        return "ADMIN CREATED SUCCESSFULLY"
    else:
        return "ADMIN KEY IS WRONG"


@app.get("/login/")
@basic_authentication_user
def login(a, b):
    user = Users.query.filter_by(username=request.authorization.username).first()
    is_pass_correct = user.verify_password(request.authorization.password)
    if is_pass_correct:
        refresh = create_refresh_token(identity=user.username)
        access = create_access_token(identity=user.username)
        context = {}
        context = {
            "Username  ": user.username,
            "Refresh_Token  ": refresh,
            "Access_Token  ": access,
        }
        return context, 200
    else:
        return make_response(
            jsonify({"error": "Invalid username or password"}), status=401
        )


def send_email(user, token, un):
    msg = Message("hello User", sender="arjunvaghasiya361@gmail.com", recipients=[user])
    msg.body = f"Hit This Link For Email Activation \n \n === > 'Veryfy for Activation' : \n http://127.0.0.1:5000/verify/{token}/{un}/"
    mail.send(msg)


def verify(token, un):
    # import pdb;pdb.set_trace()
    user = Users.query.filter_by(username=un).first()
    if user:
        user.is_registered = True
        db.session.add(user)
        db.session.commit()
        return {
            "Status": "you have registerd succesfully",
            "Username": f"Username is {user}",
            "Token": f"{token}",
        }, 200
    else:
        return {"Error": "User Not Found"}


app.add_url_rule("/verify/<token>/<un>/", "verify", verify)


class RegisterUser(Resource):
    def post(self):
        try:
            data = request.get_json()

            if data.get("password") == data.get("password_verify"):
                try:
                    validate_email(data.get("email"))
                    # import pdb;pdb.set_trace()
                    if (
                        datetime.datetime.strptime(data.get("dob"), "%Y-%m-%d").date()
                        >= datetime.datetime.now().date()
                    ):
                        return make_response(
                            jsonify(
                                {
                                    "error": "Date is invalid, do format like year-month-date, or enter valid date"
                                }
                            ),
                            400,
                        )
                    # if (
                    #     not re.search(
                    #         "[0-9]{1,20}( [a-zA-Z.]*){1,50},?( [a-zA-Z]*){1,15},? [a-zA-Z]{2},? [0-9]{6}", str(data.get("address")))
                    #     or data.get("address") == ""
                    # ):
                    #     return make_response(jsonify({"error": "enter valid address"}), 400)
                    user = Users(
                        username=data.get("username"),
                        email=data.get("email"),
                        first_name=data.get("first_name"),
                        last_name=data.get("last_name"),
                        gender=data.get("gender"),
                        dob=data.get("dob"),
                        phone=data.get("phone"),
                        password=data.get("password"),
                        address=data.get("address"),
                    )
                    db.session.add(user)
                    db.session.commit()
                    access = create_access_token(identity=user.username)
                    send_email(user.email, access, user.username)
                    serializer = RegisterSerializer()
                    data = serializer.dump(user)
                    return data, 200
                except EmailNotValidError as e:
                    return make_response(
                        jsonify({"error": f"email is not proper {e}"}), 401
                    )

            else:
                return make_response(jsonify({"error": "passsord is not matched"}), 401)
        except:
            return make_response(jsonify({"error": "DATABASE ERROR"}), 401)

    # @basic_authentication_SuperUser_Admin
    def get(self):
        try:
            db.create_all()
            return make_response(jsonify({"success": "Tables Created"}), 200)
        except:
            return make_response(jsonify({"error": "DATABASE ERROR"}), 401)


api.add_resource(RegisterUser, "/")


class AdminUpdateUser(Resource):
    @basic_authentication_for_super_admin
    def put(self, pk):
        query = Users.query.filter_by(user_id=int(pk)).first()
        data = request.get_json()

        if data.get("email") != "":
            query.email = data.get("email")
        if data.get("gender") != "":
            query.gender = data.get("gender")
        if data.get("dob") != "":
            if (
                datetime.datetime.strptime(data.get("dob"), "%Y-%m-%d").date()
                >= datetime.datetime.now().date()
            ):
                return make_response(
                    jsonify(
                        {
                            "error": "Date is invalid, do format like year-month-date, or enter valid date"
                        }
                    ),
                    400,
                )
            query.dob = data.get("dob")
        if data.get("is_manager") != "":
            query.is_manager = data.get("is_manager")
        if data.get("first_name") != "":
            query.first_name = data.get("first_name")
        if data.get("last_name") != "":
            query.last_name = data.get("last_name")
        if data.get("phone") != "":
            query.phone = data.get("phone")
        if data.get("address") != "":
            query.address = data.get("address")
        db.session.add(query)
        db.session.commit()
        result = Users.query.filter_by(user_id=int(pk)).first()
        serializer = SuperUserRegisterSerializer()
        data1 = serializer.dump(result)
        return jsonify(data1)
        # import pdb;pdb.set_trace()

    @basic_authentication_SuperUser_Admin
    def get(self, pk):
        users = Users.query.all()
        serializer = RegisterSerializer(many=True)
        data = serializer.dump(users)
        return jsonify(data)


api.add_resource(AdminUpdateUser, "/admin/user_update/<int:pk>", endpoint="user_update")
api.add_resource(AdminUpdateUser, "/admin/all_users/", endpoint="all_users")


class CartManagement(Resource):
    @basic_authentication_user
    def get(self, pk):
        try:
            # import pdb; pdb.set_trace()
            user = Users.query.filter_by(
                username=request.authorization.username
            ).first()
            cart = MyCart.query.filter_by(user_id_fk=int(user.user_id)).all()
        except:
            return make_response(jsonify({"error": "SQL error"}), 401)
        serializer = MyCartSerializer(many=True)
        data = serializer.dump(cart)
        if not data:
            return make_response(jsonify({"error": "Data not found"}), 401)
        else:
            return jsonify(data)

    @basic_authentication_user
    def post(self, pk):
        data = request.get_json()
        try:
            user = Users.query.filter_by(
                username=request.authorization.username
            ).first()
            product = Products.query.filter(
                Products.product_name.ilike(str(data.get("product_name")))
            ).first()
            total_itm_prc = float(product.product_price) * int(data.get("total_items"))
            if (int(data.get("total_items"))) > product.available_items:
                return make_response(
                    jsonify({"error": "You can order upto avaliable stock"}), 401
                )
            mycart = MyCart(
                user_id_fk=int(user.user_id),
                product_id_fk=product.product_id,
                item_name=product.product_name,
                total_items=data.get("total_items"),
                item_amount=product.product_price,
                total_items_price=total_itm_prc,
            )
            db.session.add(mycart)
            db.session.commit()
        except:
            return make_response(jsonify({"error": "SQL error"}), 401)

        return make_response(jsonify({"success": "Item Added into cart"}), 200)

    @basic_authentication_user
    def delete(self, pk):
        try:
            # import pdb;pdb.set_trace()
            user = Users.query.filter_by(
                username=request.authorization.username
            ).first()
            mycart = MyCart.query.filter(
                MyCart.cart_id == pk, MyCart.user_id_fk == user.user_id
            ).first()
            db.session.delete(mycart)
            db.session.commit()
        except:
            return make_response(jsonify({"error": "SQL error"}), 500)

        return make_response(jsonify({"success": "Cart deleted successfully"}), 200)


api.add_resource(
    CartManagement, "/my_cart/delete_cart/<int:pk>", endpoint="delete_cart"
)
api.add_resource(CartManagement, "/my_cart", endpoint="my_cart")
# admin task
@basic_authentication_SuperUser_Admin
@app.get("/all_cart")
def my_cart_items():
    try:
        cart = MyCart.query.all()
    except:
        return make_response(jsonify({"error": "SQL error"}), 500)
    serializer = MyCartSerializer(many=True)
    data = serializer.dump(cart)
    if not data:
        return make_response(jsonify({"error": "Data not found"}), 401)
    else:

        return jsonify(data)


class AdminProductCrud(Resource):
    @basic_authentication_SuperUser_Admin
    def get(self, pk):
        # import pdb;pdb.set_trace()
        products = Products.query.all()
        serializer = AdminProductSerializer(many=True)
        data = serializer.dump(products)
        if not data:
            return make_response(jsonify({"error": "No Data "}), 401)
        else:
            return data

    @basic_authentication_SuperUser_Admin
    def post(self, pk):
        try:
            data = request.get_json()
            product = Products(
                product_name=data.get("product_name"),
                product_discription=data.get("product_discription"),
                product_price=data.get("product_price"),
                total_items=data.get("total_items"),
                available_items=data.get("available_items"),
            )
            db.session.add(product)
            db.session.commit()
            return jsonify(data)
        except:
            return make_response(jsonify({"error": "DATABASE ERROR"}), 401)
        # import pdb;pdb.set_trace()

    @basic_authentication_SuperUser_Admin
    def put(self, pk):
        query = Products.query.filter_by(product_id=int(pk)).first()
        data = request.get_json()
        if data.get("product_name") != "":
            query.product_name = data.get("product_name")
        if data.get("product_discription") != "":
            query.product_discription = data.get("product_discription")
        if data.get("product_price") != "":
            query.product_price = data.get("product_price")
        if data.get("total_items") != "":
            query.total_items = data.get("total_items")
        if data.get("available_items") != "":
            query.available_items = data.get("available_items")

        db.session.add(query)
        db.session.commit()
        return jsonify(data)

    @basic_authentication_SuperUser_Admin
    def delete(self, pk):
        try:
            products = Products.query.filter_by(product_id=int(pk)).first()
            db.session.delete(products)
            db.session.commit()
            return make_response(jsonify({"success": "Item Deleted "}), 200)
        except:
            return make_response(jsonify({"error": "DATABASE ERROR "}), 500)


api.add_resource(AdminProductCrud, "/admin/products/", endpoint="products")
api.add_resource(AdminProductCrud, "/admin/product_add/", endpoint="product_add")
api.add_resource(
    AdminProductCrud, "/admin/product_update/<pk>", endpoint="product_update"
)
api.add_resource(AdminProductCrud, "/admin/products/delete/", endpoint="delete")


@app.post("/update/user/")
@jwt_required()
def update_user():
    user = Users.query.filter_by(username=str(get_jwt_identity())).first()
    data = request.get_json()
    if (
        datetime.datetime.strptime(data.get("dob"), "%Y-%m-%d").date()
        >= datetime.datetime.now().date()
    ):
        return make_response(
            jsonify(
                {
                    "error": "Date is invalid, do format like year-month-date, or enter valid date"
                }
            ),
            400,
        )
    if data.get("email") != "":
        user.email = data.get("email")
    if data.get("gender") != "":
        user.gender = data.get("gender")
    if data.get("first_name") != "":
        user.first_name = data.get("first_name")
    if data.get("last_name") != "":
        user.last_name = data.get("last_name")
    if data.get("phone") != "":
        user.phone = data.get("phone")
    if data.get("dob") != "":
        if (
            datetime.datetime.strptime(data.get("dob"), "%Y-%m-%d").date()
            >= datetime.datetime.now().date()
        ):
            return make_response(
                jsonify(
                    {
                        "error": "Date is invalid, do format like year-month-date, or enter valid date"
                    }
                ),
                400,
            )
        user.dob = data.get("dob")
    if data.get("address") != "":
        user.address = data.get("address")
    db.session.add(user)
    db.session.commit()
    return jsonify(data)


# @jwt_required()
@app.get("/products/<int:pgno>")
@app.get("/products/<name>/<int:pgno>")
@app.get("/products/<name>/<float:price>/<int:pgno>")
@jwt_required()
def products_search(name="", price="", pgno=""):
    # import pdb;pdb.set_trace()user1
    ROWS_PER_PAGE = 4
    page = request.args.get("page", pgno, type=int)
    # import pdb;pdb.set_trace()
    if name == "" and price == "":
        products = Products.query.order_by(Products.product_name).paginate(
            page=page, per_page=ROWS_PER_PAGE
        )
        serializer = ProductSerializer(many=True)
        data = serializer.dump(products.items)
        return jsonify(data)

    if name != "" and price == "":
        products = Products.query.filter(
            Products.product_name.ilike(str(name))
        ).paginate(page=page, per_page=ROWS_PER_PAGE)
        serializer = ProductSerializer(many=True)
        data = serializer.dump(products.items)
        if not data:
            return make_response(jsonify({"error": "Data not found"}), 401)
        else:
            return jsonify(data)

    if name != "" and price != "":
        # import pdb;pdb.set_trace()
        products = Products.query.filter(
            Products.product_name == (str(name)),
            Products.product_price <= price,
        ).paginate(page=page, per_page=ROWS_PER_PAGE)
        serializer = ProductSerializer(many=True)
        data = serializer.dump(products.items)
        if not data:
            return make_response(jsonify({"error": "Data not found"}), 401)
        else:
            return jsonify(data)


# arjunvaghasiya
@app.post("/payment")
@jwt_required()
def purchase_product():
    # import pdb

    # pdb.set_trace()
    print(get_jwt_identity())
    data = request.get_json()

    try:
        if data.get("cart_id") != "" and data.get("payment_method") != "":
            user = Users.query.filter_by(username=str(get_jwt_identity())).first()
            cart = MyCart.query.filter(
                MyCart.cart_id == (int(data.get("cart_id"))),
                MyCart.user_id_fk == int(user.user_id),
            ).first()
            product = Products.query.filter_by(product_id=cart.product_id_fk).first()
            payment = PaymentDetails(
                user_id_fk=user.user_id,
                product_id_fk=cart.product_id_fk,
                product_name=product.product_name,
                product_price=product.product_price,
                payment_method=data.get("payment_method"),
                total_items=cart.total_items,
                payment_amount=cart.total_items_price,
            )
            db.session.add(payment)
            db.session.commit()
            # payment =
        try:

            set_avaliable_items = int(product.available_items) - int(cart.total_items)
            product.available_items = set_avaliable_items
            db.session.add(product)
            db.session.commit()

            try:
                db.session.delete(cart)
                db.session.commit()
                serializer = PaymentSerializer()
                data = serializer.dump(payment)
                if not data:
                    return make_response(jsonify({"error": "Data not found"}), 401)
                else:
                    return jsonify(data)
            except:
                return make_response(
                    jsonify({"Un-Success": "Something Wrong in Payment query"}), 400
                )
        except:
            return make_response(
                jsonify({"Un-Success": "Something Wrong in Product query"}), 400
            )
    except:
        return make_response(
            jsonify({"Un-Success": "Something Wrong in Mycart query"}), 400
        )
