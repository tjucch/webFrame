from urllib.parse import unquote_plus

from routes import (
    current_user,
    html_response,
)


def index(request):
    u = current_user(request)
    result = request.query.get('result', '')
    if request:
        result = unquote_plus(result)
        return html_response('index.html', username=u.username, result=result)
    else:
        return html_response('index.html', username=u.username)


def static(request):
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def route_dict():
    d = {
        '/': index,
        '/static': static,
    }
    return d
