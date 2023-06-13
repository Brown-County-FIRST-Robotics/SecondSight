import numpy as np

CUBE_2023_SIZE = 10  # CM

PTS = {'cube2023': np.array([-CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2] +
                            [CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2, -CUBE_2023_SIZE / 2] +
                            [CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2] +
                            [-CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2, CUBE_2023_SIZE / 2]).reshape(4, 3)
       }
