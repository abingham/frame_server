import h5py
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    hfile = h5py.File('test.hdf5', 'r')
    dset = hfile['foo/bar/baz']

    config = Configurator(settings=settings)

    config.add_request_method(lambda _: dset,
                              'dataset',
                              reify=True)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('frame_count', '/frame_count')
    config.add_route('frame', '/frame/{index}')
    config.add_route('viewer', '/viewer')
    config.scan()
    return config.make_wsgi_app()
