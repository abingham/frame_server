import logging

import h5py
from pyramid.config import Configurator


log = logging.getLogger()

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    h5_filename = settings['frames.filename']
    dataset_name = settings['frames.dataset']

    log.info('HDF5 filename: {}'.format(h5_filename))
    log.info('HFD5 dataset: {}'.format(dataset_name))

    hfile = h5py.File(h5_filename, 'r')
    dset = hfile[dataset_name]

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
