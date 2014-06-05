import cv2
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='home',
             renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'frame_server'}

@view_config(route_name='frame_count',
             renderer='json')
def frame_count(request):
    return request.dataset.shape[0]

@view_config(route_name='frame',
             request_method='GET')
def frame(request):
    data = request.dataset[int(request.matchdict['index'])]
    rval, buff = cv2.imencode('.png', data)
    rslt = str(buff.data)
    resp = Response(body=rslt,
                    content_type='image/png')
    return resp

@view_config(route_name='viewer',
             renderer='templates/viewer.pt')
def viewer(request):
    return {'frame_count': request.dataset.shape[0] }
