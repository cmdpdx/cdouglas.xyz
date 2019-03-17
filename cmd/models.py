from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from cmd import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    simple_title = db.Column(db.String(100), index=True, unique=True)
    summary = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'<Post {self.title}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), index=True, unique=True, nullable=False)

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.text == other.text
        elif isinstance(other, str):
            return self.text == other
        else:
            raise TypeError('equality comparison must be with type str or Tag')

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'<Tag {self.text}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))