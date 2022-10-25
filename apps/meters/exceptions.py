from rest_framework.exceptions import APIException


class MeterNotFound(APIException):
    status_code = 404
    deafult_detail = "The requested Meter does not exist"
