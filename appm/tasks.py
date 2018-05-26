import json
import sys
from time import sleep

from flask import render_template
from rq import get_current_job

from appm import create_app, db
from appm.email import send_email
from appm.models import Task, User, Post

app = create_app()
app.app_context().push()


def _set_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(), 'progress': progress})

        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_posts(user_id):
    try:
        # 从数据库中读用户文章
        user = User.query.get(user_id)
        _set_progress(0)
        data = []
        total_posts = user.posts.count()
        for i, post in enumerate(user.posts.order_by(Post.timestamp.asc())):
            data.append(
                {'body': post.body, 'timestamp': post.timestamp.isoformat() + 'Z'}
            )
            sleep(5)
            _set_progress(100 * (i+1) // total_posts)

        # 发送邮件
        send_email(
            subject='[Microblog] Your blog post',
            sender=app.config['ADMINS'][0], recipients=[user.email],
            text_body=render_template('email/export_posts.txt', user=user),
            html_body=render_template('email/export_posts.html', user=user),
            attachments=[('post.json', 'application/json',
                          json.dumps({'posts': data}, indent=4))],
            sync=True
        )
    except:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
        _set_progress(100)


def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        sleep(3)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task complete')
