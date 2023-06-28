import numpy as np

# TODO: add real color values
CUBE_2023_SIZE = 10  # CM
CUBE_2023_COLOR_RANGE = ((110, 150, 145), (124, 180, 180))  # This acts as a default color when the color picker is not used

# TODO: check values
CONE_2023_HEIGHT = 33  # CM
CONE_2023_WIDTH = 21  # CM
CONE_2023_COLOR_RANGE = ((110, 150, 145), (124, 180, 180))  # This acts as a default color when the color picker is not used

PTS = {'cube2023': np.array([-CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2] +
                            [CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2] +
                            [CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2] +
                            [-CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2]).reshape(4, 3),
       'cone2023': np.array([-CONE_2023_WIDTH / 2, -CONE_2023_HEIGHT / 2, CONE_2023_WIDTH / 2] +
                            [CONE_2023_WIDTH / 2, -CONE_2023_HEIGHT / 2, -CONE_2023_WIDTH / 2] +
                            [CONE_2023_WIDTH / 2, CONE_2023_HEIGHT / 2, 0] +
                            [-CONE_2023_WIDTH / 2, CONE_2023_HEIGHT / 2, 0]).reshape(4, 3)
       }

PIECE_NAMES = ['cube2023', 'cone2023']