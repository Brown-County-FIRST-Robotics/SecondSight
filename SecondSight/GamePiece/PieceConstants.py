import numpy as np

CUBE_2023_SIZE = 10  # CM
CUBE_2023_COLOR_RANGE = ((110, 150, 145), (124, 180, 180))  # This acts as a default color when the color picker is not used

PTS = {'cube2023': np.array([-CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2] +
                            [CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2] +
                            [CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2] +
                            [-CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2]).reshape(4, 3)
       }
