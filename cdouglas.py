from cmd import create_app, db
from cmd.models import User, Post, Tag

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Tag': Tag}