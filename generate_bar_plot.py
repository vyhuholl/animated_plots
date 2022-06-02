import argparse
import os
from random import randint
from warnings import filterwarnings

import imageio
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
import seaborn as sns  # type: ignore

filterwarnings('ignore')
sns.set_style('darkgrid')


def main(size: int, filename: str, frames_dir: str, smooth_coef: int):
    '''
    Generates a GIF of a bar plot.

    Parameters:
        size: int
        filename: str
        frames_dir: str
        smooth_coef: int

    Returns:
        None
    '''
    x_axis = [x + 1 for x in range(size)]

    y_axis_list = [
        [randint(0, 9) for x in range(size)] for i in range(10)
        ]

    png_files = []

    for i in range(0, len(y_axis_list) - 1):
        plt.rcParams['figure.figsize'] = (16, 10)
        y_axis_curr = y_axis_list[i]
        y_axis_next = y_axis_list[i + 1]
        y_diff = np.array(y_axis_next) - np.array(y_axis_curr)
        for j in range(0, smooth_coef + 1):
            y_axis = (y_axis_curr + (y_diff / smooth_coef) * j)
            sns.barplot(x_axis, y_axis)
            plt.ylim(0, 10)
            png_name = os.path.join(frames_dir, f'bar-{i}-{j}.png')
            png_files.append(png_name)
            if j == smooth_coef:
                for _ in range(5):
                    png_files.append(png_name)
            plt.savefig(png_name)
            plt.close()

    with imageio.get_writer(filename, mode='i') as writer:
        for png_name in png_files:
            image = imageio.v2.imread(png_name)
            writer.append_data(image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='generate_line_plot',
        description='Generates a GIF of a bar plot.'
        )

    parser.add_argument('size', type=int, help='number of bars to plot')

    parser.add_argument(
        '-c', '--coef', type=int, default=10, help='smooth coefficient'
        )

    parser.add_argument(
        '-o', '--output', default='bar.gif', help='name of the output file'
        )

    parser.add_argument(
        '-f', '--frames', default='frames/bar', help='path to the frames dir'
        )

    args = parser.parse_args()
    main(args.size, args.output, args.frames, args.coef)
