import os
from flask import Flask, redirect

app = Flask(__name__)

messages = []


def add_messages(username, message):
    """Add messages to the `messages` list"""
    messages.append("{}: {}".format(username, message)) # python also accept {} without number indicator

def get_all_messages():
    """Get all of the messages and separate them with a `br`"""
    return "<br>".join(messages)
    
@app.route("/")
def index():
    """Main page with instructions"""
    return "To send a message use: /USERNAME/MESSAGE"
    
@app.route("/<username>")
def user(username):
    """display chat messages"""
    return "<h1>Welcome {0}</h1> {1}".format(username, get_all_messages())
    
@app.route("/<username>/<message>")
def send_message(username, message):
    """Create a new message and redirect back to the chat page"""
    #return "{0}: {1}".format(username, message)
    add_messages(username, message)
    return redirect("/" + username) #remember to import redirect from flask
    
app.run(host=os.getenv("IP"), port=int(os.getenv("PORT")), debug=True)