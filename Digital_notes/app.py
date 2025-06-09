# minimal flask code
import secrets

from flask import Flask, Response, redirect, render_template, request, session, url_for

from database import Database
from mail_service import EmailService
from utils import not_valid_password

app = Flask(__name__)
app.secret_key ="I_am_not_a_secret_key"
task = []

@app.route("/")
def home():
    if request.method == "GET":
        return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        db_obj = Database(email=email, password=password)

        if not db_obj.check_email():
            return render_template("log-in.html", message="email not found")
        
        if not db_obj.check_password():
            return render_template("log-in.html", message="Wrong password", email=email)
        
        # Get user ID and store in session
        user_id = db_obj.get_user_id(email)
        session['user_id'] = user_id
        session['logged_in'] = True
        
        return redirect(url_for('notes'))

    else:
        return render_template("log-in.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        re_password = request.form.get("re-password")

        db_obj = Database(email=email, password=password)
        if not db_obj.check_email():

            if password != re_password:
                return render_template(
                    "sign-up.html", message="*password not matched", email=email
                )
            else:
                not_valid_message = not_valid_password(password)

                if not_valid_message:
                    return render_template(
                        "sign-up.html", message=not_valid_message, email=email
                    )
                db_obj.insert_detail()
                return redirect("/login")
        else:
            return render_template(
                "log-in.html", message="email already exist", email=email
            )
    else:

        return render_template("sign-up.html")


@app.route("/forgot-password", methods=["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            if not email:
                return render_template("email.html", message="Email is required")
            
            print(f"Processing reset request for email: {email}")
            
            token = secrets.token_urlsafe(50)
            print(f"Generated token: {token}")

            db_obj = Database(email=email, password=None)
            if not db_obj.check_email():
                print(f"Email {email} not found in database")
                return render_template("email.html", message="Account with this email does not exist")
            
            # Store token in database
            token_stored = db_obj.reset_password(token)
            if not token_stored:
                print("Failed to store token in database")
                return render_template("email.html", message="Error generating reset token")
            
            # Send email
            email_obj = EmailService()
            email_sent = email_obj.send_reset_email(receiver_email=email, reset_token=token)
            
            if email_sent:
                print(f"Reset email sent successfully to {email}")
                return render_template("email.html", message="Reset link sent to your email")
            else:
                print("Failed to send reset email")
                return render_template("email.html", message="Error sending email")
                
        except Exception as e:
            print(f"Error in forgot_password: {str(e)}")
            return render_template("email.html", message="An error occurred")

    return render_template("email.html")


@app.route("/forgot-password/<string:token>", methods=["POST", "GET"])
def token_verification(token):
    if request.method == 'GET':
        db_obj = Database(email=None, password=None)
        if db_obj.verify_token(token):
            return render_template("password.html", token=token)  # Pass token to template
        return render_template("email.html", message='Invalid token or expired')
    
    if request.method == 'POST':
        password = request.form.get('password')
        not_valid_message = not_valid_password(password)
        
        if not_valid_message:
            return render_template("password.html", message=not_valid_message, token=token)
            
        db_obj = Database(email=None, password=password)
        if db_obj.update_password(token):
            return redirect("/login", message="Password reset successfilly")
        return render_template("password.html", message="Error resetting password", token=token)
    
@app.route("/notes", methods=["GET", "POST"])
def notes():
    if 'logged_in' not in session or 'user_id' not in session:
        return render_template('log-in.html', message='logged in or user id not found')
    
    user_id = session['user_id']
    db_obj = Database(email=None,password=None)
    
    if request.method == "POST":
        task = request.form.get('task')
        print(task)
        if task:
            task = task.strip()
            db_obj.add_notes(user_id=user_id, task=task)
             # Redirect after POST to prevent form resubmission
            return redirect(url_for('notes'))
    notes = db_obj.get_user_notes(user_id)
    print("inside app /n list notes: ",notes)
    return render_template("notes.html",notes= notes)    
    
@app.route("/delete_note/<int:note_id>", methods=['POST'])
def delete_note(note_id):
    if 'logged_in' not in session or 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    db_obj = Database(email=None, password=None)
    
    # Add delete_note method to Database class
    if db_obj.delete_note(note_id, user_id):
        return redirect(url_for('notes'))
    return "Note not found", 404

if __name__ == "__main__":
    app.run(debug=True, port=8000)
