from models.comment import Comment
from models.weibo import Weibo
from routes import (
    redirect,
    current_user,
    html_response,
    login_required,
)
from utils import log


def index(request):
    u = current_user(request)
    weibos = Weibo.all(user_id=u.id)
    log('weibos', weibos)
    return html_response('weibo_index.html', weibos=weibos, user=u)


def add(request):
    u = current_user(request)
    form = request.form()
    form['user_id'] = u.id
    Weibo.insert(form)
    return redirect('/weibo/index')


def delete(request):
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    cs = Comment.all(weibo_id=weibo_id)
    for c in cs:
        Comment.delete(c.id)
    return redirect('/weibo/index')


def edit(request):
    weibo_id = int(request.query['id'])
    w = Weibo.one(id=weibo_id)
    return html_response('weibo_edit.html', weibo=w)


def update(request):
    form = request.form()
    id = form.pop('id')
    Weibo.update(id, **form)
    return redirect('/weibo/index')


def comment_add(request):
    u = current_user(request)
    form = request.form()
    form['user_id'] = u.id
    Comment.insert(form)
    return redirect('/weibo/index')


def comment_delete(request):
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    return redirect('/weibo/index')


def comment_edit(request):
    comment_id = int(request.query['id'])
    comment = Comment.one(id=comment_id)
    log('in the comment_edit', comment)
    return html_response('comment_edit.html', comment=comment)


def comment_update(request):
    form = request.form()
    id = form.pop('id')
    Comment.update(id, **form)
    return redirect('/weibo/index')


def weibo_owner_required(route_function):
    def f(request):
        log('weibo_owner_required')
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        w = Weibo.one(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def comment_owner_required(route_function):
    def f(request):
        log('comment_owner_required')
        u = current_user(request)
        if request.method == 'GET':
            cid = int(request.query.get('id'))
        else:
            cid = int(request.form().get('id'))
        c = Comment.one(id=cid)
        if c.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def comment_owner_or_weibo_owner_required(route_function):
    def f(request):
        log('comment_owner_or_weibo_owner_required')
        u = current_user(request)
        if request.method == 'GET':
            cid = int(request.query.get('id'))
        else:
            cid = int(request.form().get('id'))
        c = Comment.one(id=cid)
        w = Weibo.one(id=c.weibo_id)

        if u.id == c.user_id or u.id == w.user_id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def route_dict():
    d = {
        '/weibo/add': login_required(add),
        '/weibo/delete': login_required(weibo_owner_required(delete)),
        '/weibo/edit': login_required(weibo_owner_required(edit)),
        '/weibo/update': login_required(weibo_owner_required(update)),
        '/weibo/index': login_required(index),
        # 评论功能
        '/comment/add': login_required(comment_add),
        '/comment/delete': login_required(comment_owner_or_weibo_owner_required(comment_delete)),
        '/comment/edit': login_required(comment_owner_required(comment_edit)),
        '/comment/update': login_required(comment_owner_required(comment_update)),
    }
    return d
