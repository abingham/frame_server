from contextlib import closing
from itertools import chain

import click
import cv2
import h5py


def get_frames(source):
    cap = cv2.VideoCapture(source)

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            yield frame
    finally:
        cap.release()


@click.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dest', type=click.Path())
@click.argument('dataset_name')
@click.option('--num_frames',
              default=1000,
              help='Number of frames to store.')
def copy_frames(src, dest, dataset_name, num_frames):
    frames_iter = iter(get_frames(src))
    f1 = next(frames_iter)

    with closing(h5py.File(dest, "w")) as hfile:
        dataset = hfile.create_dataset(dataset_name,
                                       shape=tuple(chain([num_frames],
                                                         f1.shape)),
                                       dtype=f1.dtype)

        for idx, frame in enumerate(chain([f1], frames_iter)):
            dataset[idx] = frame

if __name__ == '__main__':
    copy_frames()
