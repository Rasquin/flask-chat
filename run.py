import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

"""  make the secret key an environment variable.
So to do that I'm going to say app.secret_key = os.getenv And it's going to look for a variable called "SECRET".
I'm going to leave "randomstring123" in there as the second argument because this becomes the default value 
app.secret_key = "randomstring123"
"""
app.secret_key = os.getenv("SECRET", "randomstring123")
messages = []


def add_message(username, message):
    """Add messages to the `messages` list"""
    
    now = datetime.now().strftime("%H:%M:%S") #The strftime() method takes a date/time object and then converts that to a string according to a given format.
   
    """At the moment, all of our chat information is stored in a list, which is fine, but it doesn't allow us to access certain parts by name.
    We can't specify, for example, which parts of the data we want to access.
    So inside our add_messages() function, we're going to create a dictionary to store our message information.
    To do this, we'll create a new variable called messages_dict.
    
     messages.append("({}) {}: {}".format(now, username, message)) # python also accept {} without number indicator
    
    After adding messages_dict, we don't need anymore  the get_all_messages()
    def get_all_messages():
    "Get all of the messages and separate them with a `br`"
    return "<br>".join(messages)
    
    If we take the dictionary, and we paste it directly into the append() method, we won't need te messages_dicr variable
    messages_dict = {"timestamp": now, "from": username, "message": message}
    """
    
    messages.append({"timestamp": now, "from": username, "message": message})
   

    
@app.route("/", methods = ["GET", "POST"])
def index():
    """Main page with instructions"""
    if request.method == "POST":
        session["username"] = request.form["username"]

    if "username" in session:
        #return redirect(session["username"])
        return redirect(url_for("user", username=session["username"]))
        
    return render_template("index.html")
    
    
    
@app.route("/chat/<username>", methods = ["GET", "POST"])
def user(username):
    """Add and display chat messages"""
    
    if request.method == "POST":
        username = session["username"]
        message = request.form["message"]
        add_message(username, message)
        #return redirect(session["username"])
        return redirect(url_for("user", username=session["username"]))
        # if we don't return here redirect, the message will be coming up again.The problem will be that every time the page reloads, it will be resending the post data. So the messages will continue forever. We get around this by using a redirect, rather than the standard render_template.
        
    #return "<h1>Welcome {0}</h1> {1}".format(username, messages)
    return render_template("chat.html", username=username, chat_messages=messages)
    
    
"""
now we're using the textbox for our chat. We no longer need this '/username/message' route and view so that can be removed as well, also shortening our code.

@app.route("/<username>/<message>")
def send_message(username, message):
    "Create a new message and redirect back to the chat page"
    #return "{0}: {1}".format(username, message)
    add_messages(username, message)
    return redirect("/" + username) #remember to import redirect from flask
"""    
app.run(host=os.getenv("IP", "0.0.0.0"),port=int(os.getenv("PORT", "5000")), debug=False)
"""
See that we already set the IP and PORT variable values, so we don't need to do it in heroku
debug=True only during development, before deployment change to False
"""