from flask import Flask,request ,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Resource , Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']= 'abc'
db= SQLAlchemy(app)
api=Api(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
with app.app_context():
    db.create_all()
 
class UserRegistration(Resource):
    def post(self):
        data=request.get_json()
        username=data["username"]
        password=data["password"]
        if not username or password:
            data={'message':'missing useraname or password'}
            return jsonify(data)
        if User.query.filter_by(username=username).first():
            data={'username':'username alredy taken'}
            return jsonify(data)
        new_user=User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        data={'message':'user created sussesfully'}
        return jsonify(data)

class UserLogin(Resource):
     def post(self):
        data=request.get_json()
        username=data["username"]
        password=data["password"]
        user= User.query.filter_by(username=username).first()
        if user and user.password==password:
            access_token=create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        

            
        data={'message':'invalid credential'}
        return jsonify(data)


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
    
if __name__=="__main__":
    app.run(debug=True)