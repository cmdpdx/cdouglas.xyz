from collections import namedtuple

from flask import g, current_app, url_for
from flask_login import current_user

from cmd import db
from cmd.models import Post, Tag


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
            url=url_for('blog.by_title', simple_title=post.simple_title)
        ))

def create_post(title, body, tags, public):
    """Create a new Post and return the new id."""
    # strip spaces from behind commas before splitting
    tags_strings = tags.replace(', ', ',').split(',')
    post = Post(
        title=title,
        simple_title=simplify_title(title),
        body=body, 
        public=public,
        author=current_user
    )
    
    existing_tags = Tag.query.filter(Tag.text.in_(tags_strings)).all()
    for tag in exisiting_tags:
        if str(tag) in tags_strings:
            tags_strings.remove(str(tag))
        post.tags.append(tag)

    for tag in tags_strings:
        t = Tag(text=tag)
        post.tags.append(t)
        db.session.add(t)

    db.session.add(post)
    db.session.commit()
    current_app.logger.info(f'{current_user.username} CREATED post id={post.id}, title={post.title}')
    return post.id

def update_post(post_id, title, body, tags, public):
    """Update an exisiting Post, return False if post isn't found"""
    tags_strings = tags.replace(', ', ',').split(',')
    post = Post.query.get(post_id)
    if not post:
        return False
    post.title = title
    post.simple_title = simplify_title(title)
    post.body = body
    post.public = public
    
    # update the tags
    to_remove = []
    for tag in post.tags:
        if str(tag) in tags_strings:
            tags_strings.remove(str(tag))
        else:
            to_remove.append(tag)

    for tag in to_remove:
        post.tags.remove(tag)

    for tag in tags_strings:
        t = Tag.query.filter_by(text=tag).first()
        if not t:
            t = Tag(text=tag)
            db.session.add(t)
        post.tags.append(t)
        

    db.session.commit()
    current_app.logger.info(f'{current_user.username} UPDATED post id={post.id}, title={post.title}')
    return True

def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return False
    current_app.logger.info(f'{current_user.username} DELETED post id={post_id}, title={post.title}')
    db.session.delete(post)
    db.session.commit()
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
    return url_for('.by_title', simple_title=prev.simple_title) if prev else None  

def get_next_url(post):
    """Generate URL for next post, if available; None otherwise."""
    next_ = Post.query.order_by(Post.timestamp.asc()).filter(Post.id > post.id)
    if not current_user.is_authenticated:
        next_ = next_.filter_by(public=True)
    next_ = next_.first()
    return url_for('.by_title', simple_title=next_.simple_title) if next_ else None