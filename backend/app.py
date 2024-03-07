from flask import Flask,request ,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Resource , Api
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY']= 'abc'
db= SQLAlchemy(app)
api=Api(app)
jwt = JWTManager(app)

# define a simple user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    link_lists = db.relationship('LinkList', backref='user', lazy=True)


# define a link_list Model:
class LinkList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    description=db.Column(db.Text())
    url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

# create table
with app.app_context():
    db.create_all()
 
class UserRegistration(Resource):
    def post(self):
        data=request.get_json()
        username=data["username"]
        password=data["password"]

        if not username or not password:
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
        print(user.__dict__,"dfghjk")
        if user and user.password==password:
            access_token=create_access_token(identity=user.id,additional_claims={'username':user.username})
            return jsonify(access_token=access_token)
        
class ProtectedResourse(Resource):
        @jwt_required()
        def get(self):
            current_user_id= get_jwt_identity()
            data={'message':f"hello user{current_user_id}"}   
            return jsonify(data)
        





# Create a new LinkList
@app.route('/linklists', methods=['POST'])
@jwt_required()
def create_linklist():
    data = request.get_json()
    print(data,"lllllllllllllll")
    # user= data.get("user_id")
    current_user_id = get_jwt_identity()
    print(current_user_id)
    user = User.query.get(current_user_id)
    print(user)

    if not user:
        return jsonify(message='User not found'), 404

    new_linklist = LinkList(name=data["name"], description=data["description"], url=data["url"], user_id=user.id)
    db.session.add(new_linklist)
    db.session.commit()

    return jsonify(message='LinkList created successfully'), 201

# Get all LinkLists
@app.route('/linklists', methods=['GET'])
def get_all_linklists():
    linklists = LinkList.query.all()
    result = [{'name': link.name, 'description': link.description, 'url': link.url, 'user_id': link.user_id} for link in linklists]
    return jsonify(result), 200

# Get a specific LinkList by ID
@app.route('/linklists/<int:linklist_id>', methods=['GET'])
def get_linklist(linklist_id):
    linklist = LinkList.query.get(linklist_id)

    if not linklist:
        return jsonify(message='LinkList not found'), 404

    result = {'name': linklist.name, 'description': linklist.description, 'url': linklist.url, 'user_id': linklist.user_id}
    return jsonify(result), 200

# Update a LinkList by ID
@app.route('/linklists/<int:linklist_id>', methods=['PUT'])
def update_linklist(linklist_id):
    linklist = LinkList.query.get(linklist_id)

    if not linklist:
        return jsonify(message='LinkList not found'), 404

    data = request.get_json()
    linklist.name = data.get('name', linklist.name)
    linklist.description = data.get('description', linklist.description)
    linklist.url = data.get('url', linklist.url)

    db.session.commit()
    return jsonify(message='LinkList updated successfully'), 200

# Delete a LinkList by ID
@app.route('/linklists/<int:linklist_id>', methods=['DELETE'])
def delete_linklist(linklist_id):
    linklist = LinkList.query.get(linklist_id)

    if not linklist:
        return jsonify(message='LinkList not found'), 404

    db.session.delete(linklist)
    db.session.commit()
    return jsonify(message='LinkList deleted successfully'), 200





# user_view = LinkList()
# app.route('/users', methods=['POST'])(user_view.createList)

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResourse, '/secure')


    
if __name__=="__main__":
    app.run(debug=True)