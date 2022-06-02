import argparse
import os

import imageio
import matplotlib.pyplot as plt  # type: ignore
import numpy as np


def main(size: int, filename: str, frames_dir: str):
    '''
    Generates a GIF of a line plot of a NumPy array.

    Parameters:
        size: int
        filename: str
        frames_dir: str

    Returns:
        None
    '''
    y = np.random.randint(-5, 5, size)

    for i in range(2, size + 1):
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.plot(y[0: i])
        plt.ylim(-10, 10)
        plt.savefig(os.path.join(frames_dir, f'line-{i}.png'))
        plt.close()

    with imageio.get_writer(filename, mode='i') as writer:
        for i in range(2, size + 1):
            image = imageio.v2.imread(
                os.path.join(frames_dir, f'line-{i}.png')
                )
            writer.append_data(image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='generate_line_plot',
        description='Generates a GIF of a line plot of a NumPy array.'
        )

    parser.add_argument('size', type=int, help='size of the array to plot')

    parser.add_argument(
        '-o', '--output', default='line.gif', help='name of the output file'
        )

    parser.add_argument(
        '-f', '--frames', default='frames/line', help='path to the frames dir'
        )

    args = parser.parse_args()
    main(args.size, args.output, args.frames)
