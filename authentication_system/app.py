# minimal flask code
from flask import Flask, request, render_template, Response, redirect
from database import Database
from utils import not_valid_password

app = Flask(__name__)
@app.route("/")
def home():
    if request.method == "GET":
        return render_template('home.html')
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        db_obj = Database(email= email, password=password)

        if not db_obj.check_email():
            return render_template('log-in.html', message="email not found")
        not_valid_message = not_valid_password(password)

        if not_valid_message:
            return render_template('log-in.html',message= not_valid_message, email=email)

        if not db_obj.check_password():
            return render_template('log-in.html',message="Wrong password", email=email)
        return Response("success")

    else:
        return render_template('log-in.html')

@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        re_password = request.form.get("re-password")

        db_obj = Database(email=email, password=password)
        if not db_obj.check_email():

            if password != re_password:
                return render_template('sign-up.html', message="*password not matched",email=email)
            else:
                not_valid_message = not_valid_password(password)

                if not_valid_message:
                    return render_template('sign-up.html',message= not_valid_message, email=email)
                db_obj.insert_detail()
                return redirect('/login')
        else:
            return render_template('log-in.html', message="email already exist", email=email)
    else:
    
        return render_template('sign-up.html')
@app.route("/forgot-password", methodes=["GET","POST"])
def forgot_password():
    email = request.form.get("email")
    new_password = request.form.get("password")

    db_obj = Database(email= email, password=new_password)
    if not db_obj.check_email():
        pass
    return render_template('forgot-password.html', message="account with this email not exist")

@app.route("/product")
def product():
    return "<p>This is a product page</p>"

if __name__ == "__main__":
    app.run(debug=True, port=8000)