from flask import jsonify

from cmd.api import bp
from cmd.models import Post


# GET   /api/blog
@bp.route('/blog', methods=['GET'])
def get_posts():
    # Get collection of all blog posts
    pass

# GET   /api/blog/<simple_title>    return a blog in HTML
@bp.route('/blog/<simple_title>', methods=['GET'])
def get_post(simple_title):
    return jsonify(Post.query.filter_by(simple_title=simple_title).\
        first_or_404().to_dict())
    
    
# POST  /api/blog                   create a new blog entry
@bp.route('/blog', methods=['POST'])
def create_post():
    pass
