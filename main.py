import smtplib

from flask import Flask, render_template, request
import requests
from smtplib import SMTP

app = Flask(__name__)


all_posts = requests.get("https://api.npoint.io/977459b51673246dc7d6").json()


@app.route("/")
def home():
    return render_template("index.html", posts=all_posts)


@app.route("/post/<int:index>")
def blog(index):

    requested_blog = None
    for each_blog in all_posts:
        if each_blog["id"] == index:
            requested_blog = each_blog
    return render_template("post.html", this_blog=requested_blog)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    else:
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html")


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user="jirayus.didyasarin@gmail.com", password="xxx")
        connection.sendmail(
            from_addr="jirayus.didyasarin@gmail.com",
            to_addrs=email,
            msg=email_message
        )


if __name__ == "__main__":
    app.run(debug=True)
