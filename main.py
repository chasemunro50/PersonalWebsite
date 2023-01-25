# I believe flask version has to be 2.2.2 for it to work properly

from flask import Flask, render_template_string, redirect
from sqlalchemy import create_engine, MetaData
from flask_login import UserMixin, LoginManager, login_user, logout_user
from flask_blogging import SQLAStorage, BloggingEngine
import os
import base64
from base64 import urlsafe_b64decode, urlsafe_b64encode

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"  # for WTF-forms and login
app.config["BLOGGING_URL_PREFIX"] = "/blog"
app.config["BLOGGING_DISQUS_SITENAME"] = "test"
app.config["BLOGGING_SITEURL"] = "http://localhost:8000"
app.config["BLOGGING_SITENAME"] = "My Site"
app.config["BLOGGING_KEYWORDS"] = ["blog", "meta", "keywords"]
app.config["FILEUPLOAD_IMG_FOLDER"] = "fileupload"
app.config["FILEUPLOAD_PREFIX"] = "/fileupload"
app.config["FILEUPLOAD_ALLOWED_EXTENSIONS"] = ["png", "jpg", "jpeg", "gif"]

# extensions
engine = create_engine('sqlite:////tmp/blog.db')
meta = MetaData()
sql_storage = SQLAStorage(engine, metadata=meta)
blog_engine = BloggingEngine(app, sql_storage)
login_manager = LoginManager(app)
meta.create_all(bind=engine)


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    def get_name(self):
        return "Chase Munro"  # typically the user's name

@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    return User(user_id)



# Importing HTML
with open('main.html', 'r') as f:
    index_template = f.read()


@app.route("/")
def index():
    return render_template_string(index_template)


@app.route("/login/")
def login():  
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd)

    #Login Input
    user = input("Username: ")
    passw = input("Password: ")

    f = open("users.txt", "r")
    for line in f.readlines():
        us, pw = line.strip().split("|")

        #Decoding Username and password
        userSafedecodedBytes =base64.urlsafe_b64decode(us) #Bytes
        decoded_user = str(userSafedecodedBytes, "utf-8") #Str

        passSafedecodedBytes =base64.urlsafe_b64decode(pw) #Bytes
        decoded_pass = str(passSafedecodedBytes, "utf-8") #Str

        login_loop = 1
        
        while login_loop != 0:

            if (user in decoded_user) and (passw in decoded_pass):
                print("Login successful!")
                user = User("user")
                login_user(user)
                return redirect("/")
                login_loop = 0
            else:
                print("Wrong username/password")
                return redirect("/")
   

@app.route("/logout/")
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=True)


#Code for creating new encyrpted usernames/passwords 
'''
name = "username"
userSafeEncodedBytes = base64.urlsafe_b64encode(name.encode("utf-8"))
userSafeEncodedStr = str(userSafeEncodedBytes, "utf-8")
print(userSafeEncodedStr)

password1 = "password"
passSafeEncodedBytes = base64.urlsafe_b64encode(password1.encode("utf-8"))
passSafeEncodedStr = str(passSafeEncodedBytes, "utf-8")
print(passSafeEncodedStr)

user = input("Username: ")
passw = input("Password: ")
'''