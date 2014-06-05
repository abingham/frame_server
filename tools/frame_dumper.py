from contextlib import closing

import click
import cv2
import h5py


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dataset_name')
@click.argument('root_name')
def dump_frames(src, dataset_name, root_name):
    with closing(h5py.File(src, 'r')) as hfile:
        dataset = hfile[dataset_name]
        for idx in range(dataset.shape[0]):
            frame = dataset[idx]
            cv2.imwrite('{}{}.png'.format(root_name, idx),
                        frame)

if __name__ == '__main__':
    dump_frames()
