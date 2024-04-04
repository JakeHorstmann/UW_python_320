"""API used for social media app"""
# pylint: disable=R0903,R0201
from flask import Flask, jsonify
from flask_restful import Resource, Api
import main
from connection import Connection

app = Flask(__name__)
api = Api(app)

class AllUsers(Resource):
    """Displays all users in db up to limit"""
    def get(self):
        """Get method"""
        user_limit = 50
        users = main.get_all_users(user_table)
        user_counter = 1
        user_list = []
        for user in users:
            user_list.append(user)
            user_counter += 1
            if user_counter == user_limit:
                break
        return jsonify(user_list)

class UserDetail(Resource):
    """Displays user detail"""
    def get(self, user_id):
        """Get method"""
        user = main.search_user(user_id, user_table)
        return jsonify(user)

class AllPictures(Resource):
    """Displays all pictures in db"""
    def get(self):
        """Get method"""
        picture_limit = 50
        pictures = main.get_all_pictures(picture_table)
        picture_counter = 1
        picture_list = []
        for picture in pictures:
            picture_list.append(picture)
            picture_counter += 1
            if picture_counter == picture_limit:
                break
        return jsonify(picture_list)

class PictureDetail(Resource):
    """Displays picture details"""
    def get(self, picture_id):
        """Get method"""
        picture = main.search_picture(picture_id, picture_table)
        return jsonify(picture)

class ReconcilePictures(Resource):
    """Displays differences in pictures in the db and local"""
    def get(self):
        """Get method"""
        missing_from_db, missing_from_local = main.reconcile_pictures(picture_table)
        return jsonify({"missing_from_db": missing_from_db,
                        "missing_from_local": missing_from_local})

def generate_user_html(user):
    """Generates html to display a user's info nicely"""
    html = f"""
    <h3>User ID: {user['user_id']}</h3> 
    <p>User email: {user['user_email']}</p>
    <p>User name: {user['user_name']}</p>
    <p>User last name: {user['user_last_name']}</p>
    """
    return html

def generate_picture_html(picture):
    """Generates html for a picture"""
    html = f"""
    <h3>Picture ID: {picture['picture_id']}</h3> 
    <p>Picture user ID: {picture['user_id']}</p>
    <p>Picture tags: {picture['tags']}</p>
    """
    return html

api.add_resource(AllUsers, "/users")
api.add_resource(UserDetail,"/users/<string:user_id>")
api.add_resource(AllPictures,"/images")
api.add_resource(PictureDetail,"/images/<string:picture_id>")
api.add_resource(ReconcilePictures,"/differences")

if __name__ == "__main__":
    with Connection() as connection:
        user_table = connection.user_table
        status_table = connection.status_table
        picture_table = connection.picture_table
        app.run(debug=True)
