from urllib.parse import urlparse

from flask import jsonify, request, g

from cmd.api import bp
from cmd.api.auth import token_auth
from cmd.models import Post


def get_url_base(request):
    url_parts = urlparse(request.url_root)
    return f'{url_parts.scheme}://{url_parts.netloc}'

# GET   /api/blog
@bp.route('/blog', methods=['GET'])
@token_auth.login_required
def get_posts():
    """Get a collection of all blog posts."""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(Post.query, page, per_page, 'api.get_posts')
    
    # Complete any relative links to self, prev, and next 
    url_base = get_url_base(request)
    for link in data['_links'].keys():
        if data['_links'][link]:
            data['_links'][link] = url_base + data['_links'][link]

    # Complete any relative links in the list of Posts
    for post in data['items']:
        post['url'] = url_base + post['url']
        
    return jsonify(data)

# GET   /api/blog/<simple_title>
@bp.route('/blog/<simple_title>', methods=['GET'])
@token_auth.login_required
def get_post(simple_title):
    """Get a Post object with body in ready-to-display HTML."""
    url_base = get_url_base(request)
    data = Post.query.filter_by(simple_title=simple_title).first_or_404().to_dict()
    data['url'] = url_base + data['url']
    return jsonify(data)
    
    
# POST  /api/blog                   create a new blog entry
#@bp.route('/blog', methods=['POST'])
#def create_post():
#    pass
