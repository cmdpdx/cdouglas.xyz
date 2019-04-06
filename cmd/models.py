import os

from flask import current_app, url_for
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from markdown import markdown

from cmd import db, login


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page+1, per_page=per_page, **kwargs) \
                    if resources.has_next else None,
                'prev': url_for(endpoint, page=page-1, per_page=per_page, **kwargs) \
                    if resources.has_prev else None
            }
        }
        return data


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


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    simple_title = db.Column(db.String(100), index=True, unique=True)
    summary = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    public = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('posts', lazy=True))

    @property
    def filename(self):
        if not self.simple_title:
            return ''
        return os.path.join(current_app.config['BLOG_POST_DIR'], f'{self.simple_title}.md')
    
    @property
    def body(self):
        """Get the body of the Post."""
        try:
            with open(self.filename) as f:
                body = f.read()
            return body
        except FileNotFoundError:
            return 'No post file found.'
        except:
            return 'Error retrieving post file.'

    @body.setter
    def body(self, value):
        """Set the body of the Post."""
        with open(self.filename, 'w') as f:
            f.write(value)

    @body.deleter
    def body(self):
        """Delete the body of the Post."""
        os.remove(self.filename)
    
    @property
    def body_html(self):
        """Get the body of the Post in HTML."""
        return markdown(self.body)
    

    def to_dict(self):
        """Serlialize this Post to a dictionary."""
        data = {
            'title': self.title,
            'simple_title': self.simple_title,
            'summary': self.summary,
            'timestamp': self.timestamp.isoformat() + 'Z',
            'author': self.author.username,
            'body': self.body_html, 
            'url': url_for('blog.by_title', simple_title=self.simple_title),
            'tags': [str(tag) for tag in self.tags]
        }
        return data

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

