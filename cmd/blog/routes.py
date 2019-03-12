import html
from markdown import markdown

from flask import render_template, flash, redirect, url_for, request,\
    current_app, g, jsonify, abort
from flask_login import login_required, current_user

from cmd import db
from cmd.models import User, Post, Tag
from cmd.blog import bp
from cmd.blog.forms import PostForm
import cmd.blog.helpers
from cmd.blog.helpers import get_prev_url, get_next_url, generate_post_list,\
    create_post, update_post, simplify_title


@bp.route('/')
def main():
    """Main blog page; render the most recent post."""
    generate_post_list()
    post = Post.query.order_by(Post.timestamp.desc())
    if not current_user.is_authenticated:
        post = post.filter_by(public=True)
    post = post.first()
    prev_url = get_prev_url(post)
    next_url = None
    post.body = markdown(post.body)
    return render_template(
        'blog/post.html', 
        title=current_app.config['BLOG_TITLE'], 
        description=current_app.config['BLOG_DESCRIPTION'],
        post=post,
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
    post.body = markdown(post.body)
    return render_template(
        'blog/post.html', 
        title=current_app.config['BLOG_TITLE'], 
        description=current_app.config['BLOG_DESCRIPTION'],
        post=post,
        prev_url=prev_url,
        next_url=next_url
    )    

@bp.route('/tag/<tag_text>')
def tag_search(tag_text):
    page = request.args.get('page', 1, type=int)
    print(page)
    posts = Post.query.\
        join(Post.tags).\
        filter(Tag.text == tag_text)
    if not current_user.is_authenticated:
        posts = posts.filter(Post.public == True)
    pager = posts.paginate(page, current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    # Show last page if a non-existent page is requested
    if page > pager.pages:
        return redirect(url_for('.tag_search', tag_text=tag_text, page=pager.pages))

    return render_template('blog/tag_search.html', title=tag_text, posts=pager.items, pager=pager)

@bp.route('/posts')
def all_posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.\
        order_by(Post.timestamp.desc())
    if not current_user.is_authenticated:
        posts = posts.filter_by(public=True)
    pager = posts.paginate(page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    
    # if a page with no posts was requested, show the last page
    if page > pager.pages:
        return redirect(url_for('.all_posts', page=pager.pages))
    return render_template('blog/all_posts.html', title='All posts', posts=pager.items, pager=pager)

@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    """Create a new post or edit an existing post."""
    form = PostForm()
    page_title = 'New post'
    post_id = request.args.get('post_id', 0, type=int)
    # On successful POST submit...
    if form.validate_on_submit():
        # Edit of an exisiting post
        if post_id:
            update_post(
                post_id=post_id, 
                title=form.title.data, 
                body=form.body.data, 
                tags=form.tags.data,
                public=form.public.data)
            flash('Post updated.')
        # New post
        else:
            post_id = create_post(
                title=form.title.data, 
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
        form.body.data = post.body
        form.tags.data = ', '.join(list(map(str, post.tags)))
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
            tags=request.form.get('tags', '', type=str),
            public=request.form.get('public', False, type=bool))
    else:
        # update post
        update_post(
            post_id=post_id,
            title=request.form.get('title', '', type=str),
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