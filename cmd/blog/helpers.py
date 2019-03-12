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
    post = Post(
        title=title,
        simple_title=simplify_title(title),
        body=body, 
        public=public,
        author=current_user
    )
    
    newpost_tags = [s.strip().lower() for s in tags.split(',')]
    existing_tags = Tag.query.filter(Tag.text.in_(newpost_tags)).all()
    for tag in existing_tags:
        newpost_tags.remove(str(tag))
        post.tags.append(tag)

    for tag_text in newpost_tags:
        tag = Tag(text=tag_text)
        post.tags.append(tag)
        db.session.add(tag)

    db.session.add(post)
    db.session.commit()
    current_app.logger.info(f'{current_user.username} CREATED post id={post.id}, title={post.title}')
    return post.id

def update_post(post_id, title, body, tags, public):
    """Update an exisiting Post, return False if post isn't found"""
    post = Post.query.get(post_id)
    if not post:
        return False
    post.title = title
    post.simple_title = simplify_title(title)
    post.body = body
    post.public = public
    
    # update the tags
    update_tags = [s.strip().lower() for s in tags.split(',')]
    for tag in post.tags:
        if tag in update_tags:
            update_tags.remove(str(tag))
        else:
            post.tags.remove(tag)

    for tag_str in update_tags:
        tag = Tag.query.filter_by(text=tag_str).first()
        if not tag:
            tag = Tag(text=tag_str)
            db.session.add(tag)
        post.tags.append(tag)

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