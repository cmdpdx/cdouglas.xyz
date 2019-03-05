import html
from markdown import markdown

from flask import render_template, flash, redirect, url_for, request,\
    current_app, g, jsonify, abort
from flask_login import login_required, current_user

from cmd import db
from cmd.models import User, Post, SimpleTitle
from cmd.blog import bp
from cmd.blog.forms import PostForm
from cmd.blog.helpers import generate_post_list, create_post, update_post


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
        prev_url = get_prev_url(post)   
    else:
        post = Post.query.get(post_id)
        if not post or (not post.public and not current_user.is_authenticated):
            return redirect(url_for('.main'))

        # Generate URLs for previous and next posts
        prev_url = get_prev_url(post)
        next_url = get_next_url(post)

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

@bp.route('/t/<simple_title>')
def by_title(simple_title):
    generate_post_list()
    st = SimpleTitle.query.filter_by(text=simple_title).first_or_404()
    post = st.post
    if not post.public and not current_user.is_authenticated:
        return abort(404)

    prev_url = get_prev_url(post)
    next_url = get_next_url(post) 
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
            update_post(post_id, form.title.data, form.body.data, form.public.data)
            flash('Post updated.')
        # New post
        else:
            post_id = create_post(form.title.data, form.body.data, form.public.data)
            flash('Post submitted.')

        return redirect(url_for('.main', post=post_id))
    # ...or, GET request to edit an existing post
    elif request.method == 'GET' and post_id:
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            return redirect(url_for('.main'))
        form.id_.data = post.id
        form.title.data = post.title
        form.body.data = post.body
        form.public.data = post.public
        page_title = 'Edit post'

    return render_template('blog/new_post.html', title=page_title, form=form)

@bp.route('/save_post', methods=['POST'])
@login_required
def save_post():
    post_id = request.form.get('id_', 0, type=int)
    if not post_id:
        # new post
        post_id = create_post(
            title=request.form.get('title', '', type=str),
            body=request.form.get('body', '', type=str),
            public=request.form.get('public', False, type=bool))
    else:
        # update post
        update_post(
            post_id=post_id,
            title=request.form.get('title', '', type=str),
            body=request.form.get('body', '', type=str),
            public=request.form.get('public', False, type=bool))
        
    return jsonify(succes=True, message='Post saved.', post_id=post_id)

@bp.route('/delete_post', methods=['POST'])
@login_required
def delete_post():
    post_id = request.form.get('post_id', 0, type=int)
    if post_id:  
        post = Post.query.get(post_id)
        if post:
            current_app.logger.info(f'{current_user.username} DELETED post id={post_id}, title={post.title}')
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted')
    return url_for('blog.main')