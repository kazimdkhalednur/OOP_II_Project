import json

import requests
from django.conf import settings


class SSLCommerz:
    _session_data = {}
    _order_validation_data = {}

    def __init__(self):
        self.store_id = settings.SSLCOMMERZ_STORE_ID
        self.store_passwd = settings.SSLCOMMERZ_STORE_PASSWD
        self.session_api = settings.SSLCOMMERZ_SESSION_API
        self.order_validation_api = settings.SSLCOMMERZ_ORDER_VALIDATION_API
        self._session_data["store_id"] = self.store_id
        self._session_data["store_passwd"] = self.store_passwd

    def set_urls(self, success_url, fail_url, cancel_url, ipn_url=""):
        self._session_data["success_url"] = success_url
        self._session_data["fail_url"] = fail_url
        self._session_data["cancel_url"] = cancel_url
        if ipn_url != "":
            self._session_data["ipn_url"] = ipn_url

    def set_additional_values(self, value_a="", value_b="", value_c="", value_d=""):
        if value_a != "":
            self._session_data["value_a"] = value_a
        if value_b != "":
            self._session_data["value_b"] = value_b
        if value_c != "":
            self._session_data["value_c"] = value_c
        if value_d != "":
            self._session_data["value_d"] = value_d

    def init_payment(self, transaction, order, user):
        url = self.session_api

        self._session_data["tran_id"] = transaction.id
        self._session_data["total_amount"] = transaction.amount
        self._session_data["currency"] = "BDT"
        self._session_data["product_category"] = "Mixed"
        self._session_data["product_name"] = "order_items"
        self._session_data["num_of_item"] = order.items.count()
        self._session_data["shipping_method"] = "NO"
        self._session_data["product_profile"] = "None"

        self._session_data["cus_name"] = user.get_full_name()
        self._session_data["cus_email"] = user.email
        self._session_data["cus_add1"] = order.get_address()
        if order.get_address_2() != "":
            self._session_data["cus_add2"] = order.get_address_2()
        self._session_data["cus_city"] = order.get_district()
        self._session_data["cus_postcode"] = order.get_postal_code()
        self._session_data["cus_country"] = "Bangladesh"
        self._session_data["cus_phone"] = user.phone_number

        self._session_data["ship_name"] = user.get_full_name()
        self._session_data["ship_add1"] = order.get_address()
        if order.get_address_2() != "":
            self._session_data["ship_add2"] = order.get_address_2()
        self._session_data["ship_city"] = order.get_district()
        self._session_data["ship_postcode"] = order.get_postal_code()
        self._session_data["ship_country"] = "Bangladesh"

        data = self._session_data
        response = requests.post(url, data)
        response_data = {}

        if response.status_code == 200:
            response_json = json.loads(response.text)
            if response_json["status"] == "FAILED":
                response_data["status"] = response_json["status"]
                response_data["failedreason"] = response_json["failedreason"]
                return response_data
            response_data["status"] = response_json["status"]
            response_data["sessionkey"] = response_json["sessionkey"]
            response_data["GatewayPageURL"] = response_json["GatewayPageURL"]
            return response_data
        else:
            response_json = json.loads(response.text)
            response_data["status"] = response_json["status"]
            response_data["failedreason"] = response_json["failedreason"]
            return response_data

    def validate_payment(self, transaction):
        url = self.order_validation_api

        self._order_validation_data["val_id"] = transaction.val_id
        self._order_validation_data["store_id"] = self.store_id
        self._order_validation_data["store_passwd"] = self.store_passwd
        self._order_validation_data["format"] = "json"
        data = json.dumps(self._order_validation_data)

        response = requests.get(url, data)

        if response.status_code != 200:
            return False

        response_data = json.loads(response.text)

        if response_data["tran_id"] != transaction.id:
            return False

        if response_data["amount"] != transaction.amount:
            return False

        return True
