from urllib.parse import urlparse

from flask import jsonify, request

from cmd.api import bp
from cmd.models import Post


# GET   /api/blog
@bp.route('/blog', methods=['GET'])
def get_posts():
    """Get a collection of all blog posts."""
    pass

# GET   /api/blog/<simple_title>
@bp.route('/blog/<simple_title>', methods=['GET'])
def get_post(simple_title):
    """Get a Post object with body in ready-to-display HTML."""
    url_parts = urlparse(request.url_root)
    url_base = f'{url_parts.scheme}://{url_parts.netloc}'
    data = Post.query.filter_by(simple_title=simple_title).first_or_404().to_dict()
    data['url'] = url_base + data['url']
    return jsonify(data)
    
    
# POST  /api/blog                   create a new blog entry
@bp.route('/blog', methods=['POST'])
def create_post():
    pass
