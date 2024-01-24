#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

@app.route('/baked_goods', methods= ['GET', 'POST','DELETE'])
def baked_goods():
    baked= BakedGood.query.all()
    bake=[]
    if request.method== 'GET':
        for bak in baked:
            baked_dict= bak.to_dict()
            bake.append(baked_dict)
        response= make_response(bake, 200)
        return response
    elif request.method== 'POST':
        new_bakery= Bakery(
            name= request.form.get('name'),
        )
        db.session.add(new_bakery)
        db.session.commit()
        bakers_dict= new_bakery.to_dict()
        response= make_response(bakers_dict, 200)
        return response
    
@app.route('/bakeries/<int:id>',method= ['PATCH'])
def update_bakery(id):
    baker= Bakery.query.filter(Bakery.id==id).first()
    if not baker:
        response= make_response("Invalid id", 404)
        return response
    else:
        for attr in request.form:
            setattr(baker, attr,request.form.get[attr])
        db.session.add(baker)
        db.session.commit()

        bakery_dict= baker.to_dict()
        response= make_response(bakery_dict ,200)
        return response
@app.route('/baked_goods/<int:id>', method=['DELETE'])
def delete_baked_good(id):
    baked_item= BakedGood.query.filter(BakedGood.id ==id)
    if baked_item is None:
        response = make_response("Item does not exist.", 404)
        return response
    else:
        db.session.delete(baked_item)
        db.session.commit()
        response= make_response("Successfully deleted the item.", 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)