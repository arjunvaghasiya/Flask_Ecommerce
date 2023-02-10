import unittest
import requests
from flask_jwt_extended import create_access_token
from base64 import b64encode


def bearer_auth_for_user(username, password):
    headers = basic_auth_for_user(username, password)
    resp1 = requests.get("http://127.0.0.1:5000/login/", headers=headers)
    data = resp1.json()
    access_token = list(data.items())[0][1]
    headers1 = {"Authorization": "Bearer {}".format(access_token)}
    return headers1


def basic_auth_for_user(username, password):
    data = {"username": username, "password": password}
    headers = {}
    headers["Authorization"] = "Basic " + b64encode(
        (data["username"] + ":" + data["password"]).encode("utf-8")
    ).decode("utf-8")
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    return headers


def user_data_(var_username, var_email, var_password, var_password_verify):
    dict1 = {}
    dict1 = {
        "username": var_username,
        "email": var_email,
        "password": var_password,
        "password_verify": var_password_verify,
    }
    return dict1


class TestAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000/"
    data = {
        "username": "user-1527",
        "email": "yoibaufakassa-1527@yopmail.com",
        "password": "abc123",
        "password_verify": "abc123",
        "first_name": "maux",
        "last_name": "oibeu",
        "gender": "male",
        "dob": "2000-12-21",
        "address": "rajkot",
        "phone": "9367692476",
    }

    product_data = {
        "product_name": "book",
        "product_discription": "gala full scape book ,150 pages",
        "product_price": 75,
        "available_items": 100,
        "total_items": 100,
    }

    add_cart = {"product_name": "book", "total_items": 5}
    payment_data = {"cart_id": 6, "payment_method": "amazon_pay"}

    admin_user_data = {
        "email": "test_admin_@gmail.com",
        "is_admin": True,
        "is_superuser": False,
    }

    def test1_register_user(self):
        resp = requests.post("http://127.0.0.1:5000/", json=self.data)
        self.assertNotEqual(resp.status_code, 200)

    def test2_get_users(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.get("http://127.0.0.1:5000/admin/all_users/", headers=headers)
        self.assertEqual(resp.status_code, 200)
        print("test 2 is completed")

    def test3_get_admin_products(self):
        headers = basic_auth_for_user("user-4321", "abc123")
        resp = requests.get("http://127.0.0.1:5000/admin/products/", headers=headers)
        self.assertEqual(resp.status_code, 200)
        print("test 3 is completed")

    # def test4_add_product(self):
    #     headers = basic_auth_for_user("user-4321", "abc123")
    #     resp = requests.post(
    #         "http://127.0.0.1:5000/admin/product_add/",
    #         json=self.product_data,
    #         headers=headers,
    #     )
    #     self.assertEqual(resp.status_code, 200)
    #     print("test 4 is completed")

    def test5_update_product(self):
        headers = basic_auth_for_user("user-4321", "abc123")
        resp = requests.put(
            "http://127.0.0.1:5000/admin/product_update/4",
            json=self.product_data,
            headers=headers,
        )
        self.assertEqual(resp.status_code, 200)
        print("test 5 is completed")

    def test6_get_products_acoding_to_name_price(self):
        headers1 = bearer_auth_for_user(username="user-1527", password="abc123")
        resp = requests.get(
            "http://127.0.0.1:5000/products/book/100.0/1", headers=headers1
        )
        self.assertEqual(resp.status_code, 200)
        print("test 6 is completed")

    def test7_get_product_acoding_to_name(self):
        headers1 = bearer_auth_for_user(username="user-1527", password="abc123")
        resp = requests.get("http://127.0.0.1:5000/products/eraser/1", headers=headers1)
        self.assertEqual(resp.status_code, 200)
        print("test 7 is completed")

    def test8_get_all_product_by_user(self):
        headers1 = bearer_auth_for_user(username="user-1527", password="abc123")
        resp = requests.get("http://127.0.0.1:5000/products/1", headers=headers1)
        self.assertEqual(resp.status_code, 200)
        print("test 8 is completed")

    def test9_user_add_item_to_cart(self):
        headers = basic_auth_for_user("user-1527", "abc123")
        resp = requests.post(
            "http://127.0.0.1:5000/my_cart",
            json=self.add_cart,
            headers=headers,
        )
        self.assertEqual(resp.status_code, 200)
        print("test 9 is completed")

    def test10_user_get_cart(self):
        headers = basic_auth_for_user("user-1527", "abc123")
        resp = requests.get(
            "http://127.0.0.1:5000/my_cart",
            headers=headers,
        )
        self.assertEqual(resp.status_code, 200)
        print("test 10 is completed")

    def test11_payment(self):
        headers = bearer_auth_for_user("user-1527", "abc123")
        resp = requests.post(
            "http://127.0.0.1:5000/payment",
            json=self.payment_data,
            headers=headers,
        )
        self.assertNotEqual(resp.status_code, 200)
        print("test 10 is completed")

    def test12_user_update_super_admin(self):
        headers = basic_auth_for_user("admin", "abc123")
        resp = requests.put(
            "http://127.0.0.1:5000/admin/user_update/6",
            json={
                "email": "MANAGER@gmail.com",
                "first_name": "",
                "last_name": "",
                "gender": "",
                "dob": "",
                "address": "",
                "phone": "",
                "is_manager": True,
            },
            headers=headers,
        )
        self.assertEqual(resp.status_code, 200)
        print("test 12 is completed")


if __name__ == "__main__":
    tester = TestAPI()
    tester.test1_register_user()
