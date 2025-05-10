# minimal flask code
from flask import Flask, request, render_template, Response, redirect
from database import db_function

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        db_obj = db_function(email= email, password=password)
        db_obj.check_email()
        return Response("success")
    else:
        return render_template('log-in.html')

@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        re_password = request.form.get("re-password")

        db_obj = db_function(email=email, password=password)
        if not db_obj.check_email():

            if password != re_password:
                return render_template('sign-up.html', message="*password not matched")
            else:
                if len(password)>= 8:
                    # db_obj = db_function(email=email, password=password)
                    db_obj.insert_detail()
                    return redirect('/login')
                if len(password)<8:
                    return render_template('sign-up.html',message= "password should at least contain 8 character")
        else:
            return render_template('log-in.html', message="email already exist")
    else:
    
        return render_template('sign-up.html')

@app.route("/product")
def product():
    return "<p>This is a product page</p>"

if __name__ == "__main__":
    app.run(debug=True, port=8000)