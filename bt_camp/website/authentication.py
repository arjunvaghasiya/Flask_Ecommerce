from sre_constants import AT
from website.models import *
from flask_restful import request,Resource
from flask import jsonify,make_response



def basic_authentication_for_super_admin(func):
    # import pdb;pdb.set_trace()
    def inner(self='',pk=''):
        user = Users.query.filter_by(username = request.authorization.username).first()
        if not user:
            return make_response(jsonify({'Not Found !: User NOT-FOUND'}),401)
        else:
            if user.verify_password(request.authorization.password) == True:
                if user.is_registered and user.is_manager and user.is_admin:
                    return func(self,pk)
                else:
                    return make_response(jsonify({'Error !: Un-Authorized User'}),401)
            else:
                return make_response(jsonify({'Error !: Invalid User or Password'}),401)
    return inner

from sqlalchemy.orm.exc import UnmappedError
def basic_authentication_SuperUser_Admin(func):
    def inner(self='',pk =''):
        try:
            user = Users.query.filter_by(username = request.authorization.username).first()
            if user:
                if user.verify_password(request.authorization.password) == True:
                    if user.is_manager or user.is_admin:
                        return func(self,pk)
                    else:
                        return make_response(jsonify({'Error !: Un-Authorized User'}),401)
                else:
                    return make_response(jsonify({'Error !: Invalid User or Password'}),401)
            else:
                return make_response(jsonify({'Not Found !: Invalid User'}),401)
            
        except UnmappedError as e:
            raise  AttributeError({e})
        
    return inner

def basic_authentication_user(func):
    def inner(self='',pk =''):
        user = Users.query.filter_by(username = request.authorization.username).first()
        if not user:
            return make_response(jsonify({'Error':'User not found'}),401)
        else:
            if user.verify_password(request.authorization.password) == True:
                if user.is_registered or user.is_manager or user.is_admin:
                    return func(self,pk)
                else:
                    return make_response(jsonify({'Error !: Un-Authorized User'}),401)
            else:
                return make_response(jsonify({'Error !: Invalid User or Password'}),401)
    return inner
