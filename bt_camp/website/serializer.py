from .models import *
from email_validator import validate_email


from marshmallow import Schema, fields


class SuperUserRegisterSerializer(Schema):
    password_verify = fields.String()

    class Meta:
        model = Users
        fields = (
            "email",
            "first_name",
            "last_name",
            "gender",
            "dob",
            "address",
            "phone",
            "is_manager",
        )


class RegisterSerializer(Schema):
    password_verify = fields.String()

    class Meta:
        model = Users
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "phone",
            "gender",
            "dob",
            "address",
        )


class UpdateRegisterSerializer(Schema):
    class Meta:
        model = Users
        fields = (
            "email",
            "first_name",
            "last_name",
            "gender",
            "dob",
            "address",
            "phone",
            "is_manager",
            "is_admin",
        )


class MyCartSerializer(Schema):
    class Meta:
        model = MyCart
        fields = (
            "user_id_fk",
            "cart_id",
            "item_name",
            "total_items",
            "item_amount",
            "total_items_price",
        )


class ProductSerializer(Schema):
    class Meta:
        model = Products
        fields = (
            "product_name",
            "product_discription",
            "product_price",
            "available_items",
        )


class AdminProductSerializer(Schema):
    class Meta:
        model = Products
        fields = (
            "product_id",
            "product_name",
            "product_discription",
            "product_price",
            "available_items",
            "total_items",
        )


class PaymentSerializer(Schema):
    class Meta:
        model = PaymentDetails
        fields = (
            "user_id_fk",
            "payment_id",
            "payment_method",
            "product_name",
            "product_price",
            "total_items",
            "paid_amount",
        )
