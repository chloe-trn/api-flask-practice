from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, request, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

#  INSTALL a DATABASE - Alchemy - MYSQL LITE 
app = Flask(__name__)
api = Api(app)
# change configuration settings of your web app, specify location of database
# the database.db file will be stored in the current folder - relative folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# make models in database 
class VideoModel(db.Model):
    # define fields in db Video Model 
    # inside a db there are multiple columns
    # each row is an entry of that model 
    id = db.Column(db.Integer, primary_key=True)
    # this field has to have less than 100 characters, that HAS to have a name
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

# create database 

videos = {}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=str, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=str, help="Likes on the video", required=True)

# Data validation: 404 is status code that means does not exist
def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos: 
        abort(404, message="Could not find video with that id")

def abort_if_video_exists(video_id):
    if video_id in videos: 
        abort(409, message="Video already exists with that ID")

#  make a dict that defines how an OBJECT/INSTANCE should be serialized
#  from the class DB, SQL 
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer, 
    'likes': fields.Integer
}

# make a resource / class - THIS IS AN API ENDPOINT
class Video(Resource):
    # this says that when we return something, SERIALIZE IT with the format in resource_fields
    # Can put this above any method where you want to do this  
    @marshal_with(resource_fields)
    def get(self, video_id):
        # return a query from the SQL database 
        # when you query the Video Model, it will reutrn an INSTANCE Of the VideoModel class
        # How can we deal with these instances?

        result = VideoModel.query.filter_by(id=video_id).first()
        if not result: 
            abort(404, message='Video of that id not found')
        return result 

    # making a new video method (put)
    @marshal_with(resource_fields)
    def put(self, video_id):
        # data sent { } is sent in a form
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result: 
            abort(409, message="Video id taken...")

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        # adds video object to current db session
        db.session.add(video) 
        # permanantly putting in object in db 
        db.session.commit()
        return video, 201
    
    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return 'Video Deleted',204


# register resource/ class as a resource to the API
# and make it accessible through a URL 
# angle brackets <> define parameters in the endpoint request
api.add_resource(Video, "/video/<int:video_id>")


# starts development environment
if __name__ == "__main__":
    app.run(debug = True) 




