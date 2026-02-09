from email_validator import validate_email, EmailNotValidError
import os
from dotenv import load_dotenv
load_dotenv()

from flask import (
    Flask, render_template, url_for, 
    redirect, current_app, g, request, flash, 
    )
import logging
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = Flask(__name__)
app.config["SECRET_KEY"] = "ehfiwued273AHbheJ"
app.logger.setLevel(logging.DEBUG)
app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS") == "True"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)
@app.route("/")
def index():
   return "Hello, Flask!"

@app.route("/hello/<name>",
            methods=["GET", "POST"],
            endpoint="hello-endpoint")
def hello(name):
    return "Hello, {}!".format(name)

@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)

with app.test_request_context():
    # /dz
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/AK?page=1
    print(url_for("show_name", name="AK", page="1"))

    with app.test_request_context("/users?updated=true"):
        print(request.args.get("updated"))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # 폼 속성 사용해서 폼의 값을 취득
        username = request.form.get("username","").strip()
        email = request.form.get("email","").strip()
        description = request.form.get("description","").strip()

        is_valid = True

        if not username:
            flash("사용자명을 입력해 주세요")
            is_valid = False

        if not email:
            flash("메일 주소를 입력해 주세요")
            is_valid = False

        else:
            try:
                validate_email(email)
            except EmailNotValidError:
                flash("형식에 맞는 메일 주소를 입력해 주세요")
                is_valid = False

        if not description:
            flash("문의 내용을 입력해 주세요")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        # 이메일 보내기
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )

        flash("문의해 주셔서 감사합니다(✿◡‿◡)")
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")
def send_email(to, subject, template, **kwargs):
    """메일 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
