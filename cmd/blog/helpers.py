from collections import namedtuple

from flask import g, current_app, url_for
from flask_login import current_user

from cmd import db
from cmd.models import Post, SimpleTitle


def generate_post_list():
    """Create list of recent blog posts and store in Flask global g."""
    g.post_list = []
    PostInfo = namedtuple('PostInfo', ['title', 'timestamp', 'url'])
    posts = Post.query.order_by(Post.timestamp.desc())
    if not current_user.is_authenticated:
        posts = posts.filter_by(public=True)

    for post in posts.all():
        g.post_list.append(PostInfo(
            title=post.title,
            timestamp=post.timestamp,
            url=url_for('blog.by_title', simple_title=post.simple_title.text)
        ))

def create_post(title, body, public):
    """Create a new Post and return the new id."""
    post = Post(
        title=title,
        body=body, 
        public=public,
        author=current_user
    )
    st = SimpleTitle(text=simplify_title(title), post=post)
    
    db.session.add(post)
    db.session.add(st)
    db.session.commit()
    current_app.logger.info(f'{current_user.username} CREATED post id={post.id}, title={post.title}')
    return post.id

def update_post(post_id, title, body, public):
    """Update an exisiting Post, return False if post isn't found"""
    post = Post.query.get(post_id)
    if not post:
        return False
    post.title = title
    post.simple_title.text = simplify_title(title)
    post.body = body
    post.public = public
    db.session.commit()
    current_app.logger.info(f'{current_user.username} UPDATED post id={post.id}, title={post.title}')
    return True

def simplify_title(title):
    builder = []
    for c in title.strip().lower():
        if c.isalnum(): 
            builder.append(c)
        elif c == ' ':
            builder.append('-')
    return ''.join(builder)

def get_prev_url(post):
    """Generate URL for previous post, if available; None otherwise."""
    prev = Post.query.order_by(Post.timestamp.desc()).filter(Post.id < post.id)
    if not current_user.is_authenticated:
        prev = prev.filter_by(public=True)
    prev = prev.first()
    return url_for('.by_title', simple_title=prev.simple_title.text) if prev else None  

def get_next_url(post):
    """Generate URL for next post, if available; None otherwise."""
    next_ = Post.query.order_by(Post.timestamp.asc()).filter(Post.id > post.id)
    if not current_user.is_authenticated:
        next_ = next_.filter_by(public=True)
    next_ = next_.first()
    return url_for('.by_title', simple_title=next_.simple_title.text) if next_ else None