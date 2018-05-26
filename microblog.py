
from appm import db, cli, create_app
from appm.models import User, Post, Message, Notification, Task
from appm import cli

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task}


