import numpy as np

CUBE_2023_SIZE = 10  # CM

CUBE_2023_PTS = np.array([-CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2] +
                         [CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2] +
                         [CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2] +
                         [-CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2]).reshape(4, 3)
