# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///microblog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    following = db.Column(db.String(255), default="")  # 存储关注用户的ID，用逗号分隔


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# 路由
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 发布新动态
        content = request.form["content"]
        author = request.form["author"]
        user = User.query.filter_by(username=author).first()
        if not user:
            user = User(username=author)
            db.session.add(user)
            db.session.commit()

        post = Post(content=content, author_id=user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("index"))

    # 获取所有动态
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", posts=posts)


@app.route("/follow/<username>")
def follow(username):
    # 关注用户（简化版）
    user_to_follow = User.query.filter_by(username=username).first()
    if user_to_follow:
        current_user = User.query.get(1)  # 简化：假设当前用户ID为1
        if str(user_to_follow.id) not in current_user.following.split(","):
            current_user.following += f",{user_to_follow.id}"
            db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
