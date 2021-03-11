from flask import Flask, request, abort
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

videos = {}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=str, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=str, help="Likes on the video", required=True)

# Data validation: 404 is status code that means does not exist
def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos: 
        abort(404, message="Could not find video...")

# make a resource / class - THIS IS AN API ENDPOINT
class Video(Resource):
    def get(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        return videos[video_id]

    # making a new video method (put)
    def put(self, video_id):
        # data sent { } is sent in a form
        args = video_put_args.parse_args()
        videos[video_id] = args 
        return videos[video_id], 201

# register resource/ class as a resource to the API
# and make it accessible through a URL 
# angle brackets <> define parameters in the endpoint request
api.add_resource(Video, "/video/<int:video_id>")


# starts development environment
if __name__ == "__main__":
    app.run(debug = True) 




