import os
import html

from flask import render_template, flash, redirect, url_for, request,\
    current_app, g, jsonify, abort
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

from cmd import db
from cmd.models import User, Post, Tag
from cmd.blog import bp
from cmd.blog.forms import PostForm
import cmd.blog.helpers
from cmd.blog.helpers import get_prev_url, get_next_url, generate_post_list,\
    create_post, update_post, simplify_title, get_post_body, allowed_file


@bp.route('/')
def main():
    """Main blog page; render the most recent post."""
    generate_post_list()
    post = Post.query.order_by(Post.timestamp.desc())
    if not current_user.is_authenticated:
        post = post.filter_by(public=True)
    post = post.first()
    prev_url = get_prev_url(post) if post else None
    next_url = None
    body = get_post_body(post.title)

    return render_template(
        'blog/view_post.html', 
        title=current_app.config['BLOG_TITLE'], 
        description=current_app.config['BLOG_DESCRIPTION'],
        post=post,
        body=body,
        prev_url=prev_url,
        next_url=next_url
    )


@bp.route('/<simple_title>')
def by_title(simple_title):
    """Retrieve a post by its simple title and render it."""
    generate_post_list()
    post = Post.query.filter_by(simple_title=simple_title).first_or_404()
    if not post.public and not current_user.is_authenticated:
        return abort(404)
    prev_url = get_prev_url(post)
    next_url = get_next_url(post)
    body = get_post_body(post.title)

    return render_template(
        'blog/view_post.html', 
        title=current_app.config['BLOG_TITLE'], 
        description=current_app.config['BLOG_DESCRIPTION'],
        post=post,
        body=body,
        prev_url=prev_url,
        next_url=next_url)    


@bp.route('/tag/<tag_text>')
def tag_search(tag_text):
    """Render the search page with all posts tagged by tag_text."""
    page = request.args.get('page', 1, type=int)
    pager = Post.query.\
        join(Post.tags).\
        filter(Tag.text == tag_text)
    if not current_user.is_authenticated:
        pager = pager.filter(Post.public == True)
    pager = pager.paginate(page, current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    # Show last page if a non-existent page is requested
    if page > pager.pages:
        return redirect(url_for('.tag_search', tag_text=tag_text, page=pager.pages))

    return render_template('blog/search.html', title=tag_text, posts=pager.items, \
        pager=pager, pagination_url=url_for('.tag_search', tag_text=tag_text))


@bp.route('/posts')
def all_posts():
    """Render the search page with all posts, in descending chronological order."""
    page = request.args.get('page', 1, type=int)
    pager = Post.query.\
        order_by(Post.timestamp.desc())
    if not current_user.is_authenticated:
        pager = pager.filter_by(public=True)
    pager = pager.paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    # if a page with no posts was requested, show the last page
    if page > pager.pages:
        return redirect(url_for('.all_posts', page=pager.pages))
    return render_template('blog/search.html', title='All posts', posts=pager.items, \
        pager=pager, pagination_url=url_for('.all_posts'))


@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    """Create a new post or edit an existing post."""
    form = PostForm()
    page_title = 'New post'
    g.show_upload = True
    post_id = request.args.get('post_id', 0, type=int)
    # On successful POST submit...
    if form.validate_on_submit():
        # Edit of an exisiting post
        if post_id:
            update_post(
                post_id=post_id, 
                title=form.title.data,
                summary=form.summary.data, 
                body=form.body.data, 
                tags=form.tags.data,
                public=form.public.data)
            flash('Post updated.')
        # New post
        else:
            post_id = create_post(
                title=form.title.data, 
                summary=form.summary.data,
                body=form.body.data, 
                tags=form.tags.data,
                public=form.public.data)
            flash('Post submitted.')
        return redirect(url_for('.by_title', simple_title=simplify_title(form.title.data)))
    # ...or, GET request to edit an existing post
    elif request.method == 'GET' and post_id:
        post = Post.query.get(post_id)
        if not post:
            return redirect(url_for('.main'))
        form.id_.data = post.id
        form.title.data = post.title
        form.summary.data = post.summary
        form.body.data = get_post_body(post.title)
        form.tags.data = ', '.join(list(map(str, post.tags)))
        form.public.data = post.public
        g.show_upload = False
        page_title = 'Edit post'

    return render_template('blog/new_post.html', title=page_title, form=form)


@bp.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('No file selected.')
        return redirect(url_for('.new_post'))
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(filename)
        form = PostForm()
        with open(filename) as f:
            form.body.data = f.read()
        if os.path.exists(filename):
            os.remove(filename)
        g.show_upload = False
        return render_template('blog/new_post.html', title='New post', form=form)
    
    flash('Extension not allowed (must be .txt or .md)') if file else flash('Upload failed.')
    return redirect(url_for('.new_post'))


@bp.route('/save_post', methods=['POST'])
@login_required
def save_post():
    post_id = request.form.get('id_', 0, type=int)
    if not post_id:
        # new post
        post_id = create_post(
            title=request.form.get('title', '', type=str),
            summary=request.form.get('summary', '', type=str),
            body=request.form.get('body', '', type=str),
            tags=request.form.get('tags', '', type=str),
            public=request.form.get('public', False, type=bool))
    else:
        # update post
        update_post(
            post_id=post_id,
            title=request.form.get('title', '', type=str),
            summary=request.form.get('summary', '', type=str),
            body=request.form.get('body', '', type=str),
            tags=request.form.get('tags', '', type=str),
            public=request.form.get('public', False, type=bool))
        
    return jsonify(succes=True, message='Post saved.', post_id=post_id)


@bp.route('/delete_post', methods=['POST'])
@login_required
#TODO: change this function/view name to 'remove_post' to avoid conflict with helpers.delete_post
def delete_post():
    post_id = request.form.get('post_id', 0, type=int)
    if post_id and cmd.blog.helpers.delete_post(post_id):        
        flash('Post deleted')
    return url_for('blog.main')
