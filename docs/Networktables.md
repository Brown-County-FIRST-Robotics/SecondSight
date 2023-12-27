# Networktables
| Name      | Type     | Value                                 | Example Value |
|-----------|----------|---------------------------------------|---------------|
| Hash      | String   | The hash of the current git commit    | 2d88ab5dbb83f |
| Branch    | String   | The current git branch                | main          |
| config    | String   | The configuration represented in json |               |
| <cam_num> | SubTable | The subtable for a camera             | see below     |


## Camera subtable
| Name          | Type         | Value                                                                                                   | Example Value                        | Explanation of example                                                                                                    |
|---------------|--------------|---------------------------------------------------------------------------------------------------------|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Poses         | double array | The apriltag poses detected, concatenated into a single array in the order of x, y, z, roll, pitch, yaw | [1,0.2,0.5,3,2,-1, 2,0.3,0,-1,1,0.2] | Two poses, one at x=1, y=0.2, z=0.5, roll=3, pitch=2, yaw=-1; and the other at x=2, y=0.3, z=0, roll=-1, pitch=1, yaw=0.2 |
| IDs           | String array | The ids of the apriltags detected                                                                       | ["1", "3"]                           | Two poses, with ids 1 and 3                                                                                               |
| isRecording   | boolean      | Whether it is recording or not                                                                          |                                      |                                                                                                                           |
| recordingPath | String       | The path of the recording                                                                               |                                      |                                                                                                                           |
