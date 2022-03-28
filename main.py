from api import app
from flask import render_template, session,make_response,request
from db import Goods
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import login_manager
import base64
limiter = Limiter(app, key_func=get_remote_address)
import json
@login_manager.user_loader
def load_user(user_id):

    return  Goods.query.filter_by(id =user_id ).first()



@app.after_request
def add_header(response):
    response.headers['Server'] = ''



    return response

@app.route('/start_counter',methods = ['POST'])
def start_counter():

    resp = make_response(f"The Cookie has been set")
    my_list = [
    {
        "id":3,
        "count":3
    },
    {
        "id": 2,
        "count": 2
    }
    ]
    json_encoded_list = json.dumps(my_list)
    b64_encoded_list = base64.b64encode(json_encoded_list.encode())
    resp.set_cookie('_basket', b64_encoded_list)
    return resp

@app.route('/count')
def count():
    name = request.cookies.get('_basket')
    name_decoded = base64.b64decode(name).decode('utf-8')
    return name_decoded


@app.route('/goods')
def goods():
    return render_template("goods.html")

@app.route('/basket')
def basket():
    goods = request.cookies.get("_basket")
    if goods is not None:
            encode = base64.b64decode(goods).decode('utf-8')
            return encode
    else:
        return "basket is empty"


@app.route('/order')
def order():
    return render_template("order.html")
if __name__ == '__main__':
    session.clear()
    app.run(debug=True)

