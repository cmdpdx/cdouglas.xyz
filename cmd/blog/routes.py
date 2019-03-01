import html
from markdown import markdown

from flask import render_template, flash, redirect, url_for, request, current_app, g
from flask_login import login_required, current_user

from cmd import db
from cmd.models import User, Post
from cmd.blog import bp
from cmd.blog.forms import PostForm

def generate_post_list():
    g.post_list = []
    posts = db.session.query(Post.id, Post.title).order_by(Post.timestamp.desc())
    if not current_user.is_authenticated:
        posts = posts.filter_by(public=True)
    g.post_list = posts.all()[:]


@bp.route('/')
def main():
    generate_post_list()

    post_id = request.args.get('post', 0, type=int)
    next_url, prev_url, post = None, None, None
    # If no 'post; query string passed, show most recent entry
    if not post_id:
        # Get most recent public post (admin gets non-public)
        post = Post.query.order_by(Post.timestamp.desc())
        if not current_user.is_authenticated:
            post = post.filter_by(public=True)
        post = post.first()

        # Get second most recent public post (admin gets non-public)
        prev = Post.query.order_by(Post.timestamp.desc()).filter(Post.id < post.id)
        if not current_user.is_authenticated:
            prev = prev.filter_by(public=True)
        prev = prev.first()
        prev_url = url_for('.main', post=prev.id) if prev else None    
    else:
        post = Post.query.get(post_id)
        if not post or (not post.public and not current_user.is_authenticated):
            return redirect(url_for('.main'))

        prev = Post.query.order_by(Post.timestamp.desc()).filter(Post.id < post_id)
        next_ = Post.query.order_by(Post.timestamp.asc()).filter(Post.id > post_id)

        if not current_user.is_authenticated:
            prev = prev.filter_by(public=True)
            next_ = next_.filter_by(public=True)
        prev = prev.first()
        next_ = next_.first()
        prev_url = url_for('.main', post=prev.id) if prev else None
        next_url = url_for('.main', post=next_.id) if next_ else None

    # Convert the markdown in the blog body to HTML before rendering template
    post.body = markdown(post.body)
    return render_template(
        'blog/blog.html', 
        title=current_app.config['BLOG_TITLE'], 
        description=current_app.config['BLOG_DESCRIPTION'],
        post=post,
        prev_url=prev_url,
        next_url=next_url
    )

@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    page_title = 'New post'
    post_id = request.args.get('post_id', 0, type=int)
    # On successful POST submit...
    if form.validate_on_submit():
        # Edit of an exisiting post
        if post_id:
            post = Post.query.filter_by(id=post_id).first()
            post.title = form.title.data
            post.body = form.body.data
            post.public = form.public.data
            db.session.commit()
            flash('Post updated.')
        # New post
        else:
            post = Post(
                title=form.title.data, 
                body=form.body.data, 
                public=form.public.data,
                author=current_user
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            flash('Post submitted.')
        return redirect(url_for('.main', post=post_id))
    # ...or, GET request to edit an existing post
    elif request.method == 'GET' and post_id:
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return redirect(url_for('.main'))
        form.title.data = post.title
        form.body.data = post.body
        form.public.data = post.public
        page_title = 'Edit post'

    return render_template('blog/new_post.html', title=page_title, form=form)