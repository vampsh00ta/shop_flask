import json

from flask_restful import Api,reqparse,Resource
from flask import session,make_response,request
from config import app
from db import db,Goods,Orders
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
import datetime as dt
from mail_sender import mailSender
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import base64
from encrypt import Encrypt

admin  = Admin(app)
admin.add_view(ModelView(Goods,db.session))
admin.add_view(ModelView(Orders,db.session))


limiter = Limiter(app, key_func=get_remote_address)

encr = Encrypt()

api = Api(app)

class AllGoods(Resource):
    @limiter.limit("3/min")
    def get(self):
        # Create the list of people from our data

        return [u.as_dict() for u in Goods.query.all()]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("title")
        parser.add_argument("amount")
        params = parser.parse_args()

        req = Goods(name  =params['name'],title = params['title'],amount= params['amount'] )
        try:
            db.session.add(req)
            db.session.commit()
            return params,201
        except:
            return 400

class Add(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("count")
        parser.add_argument("product_id")
        params = parser.parse_args()
        done = False

        res = make_response(f"The Cookie has been set")
        newBasket = {
            "product_id": int(params['product_id']),
            "count": int(params['count'])
        }
        cookie = request.cookies.get('_basket')

        if cookie:
            cookie_decoded = encr.decode(cookie)



            # for good in  cookie_decoded:
            #     if good['product_id'] ==params['product_id']:
            #         good['count']=good['count'] + int(params['count'])
            #         done = True
            if done == False:
                cookie_decoded.append(newBasket)
                cookie_encoded = encr.encode(cookie_decoded)
                res.set_cookie('_basket', cookie_encoded)
                return res

        else:
            basket = [newBasket]

            cookie_encoded = encr.encode(basket)
            res.set_cookie('_basket', cookie_encoded)



        return  res


class Delete(Resource):
    def delete(self):
        res = make_response("cookie cleared")
        res.set_cookie("_basket", ' ', max_age=0)
        return res
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("count")
        parser.add_argument("product_id")
        params = parser.parse_args()

        for good in session['product_id']:
            if params['count']:
                if good['product_id'] == params['product_id']:
                    good['count'] =  good['product_id']

            else:
                if good['product_id'] == params['product_id']:
                    del good


        return 200

class Buy(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email")
        params = parser.parse_args()
        product = ''
        amount  = ''
        cookie = request.cookies.get('_basket')
        try:
            order = encr.decode(cookie)

            for item in order:

                good = Goods.query.filter_by(id=item['product_id']).first()
                good.amount = good.amount - int(item['count'])
                db.session.add(good)

                product = product + ":"+str(item['product_id'])
                amount = amount +":"+str(item['count'])
            newOrder  = Orders(product_id = product,amount = amount,email = params['email'],date = dt.datetime.now())


            db.session.add(newOrder)
            db.session.commit()
            res = make_response({"order":newOrder.id,"data":newOrder.date})
            res.set_cookie("_basket", ' ', max_age=0)
            mailSender(params['email'], newOrder.id, product)
            return res

        except:
            return 400



api.add_resource(AllGoods, "/api/v1/allGoods")
api.add_resource(Add, "/api/v1/addToBasket")
api.add_resource(Delete, "/api/v1/deleteFromBasket")

api.add_resource(Buy,"/api/v1/buy")


