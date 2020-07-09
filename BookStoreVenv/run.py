from app import app, db
from app.models import Posts, DescriptionOfBook

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Posts': Posts, 'DescriptionOfBook': DescriptionOfBook}
