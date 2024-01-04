# Networktables
| Name      | Type     | Value                                 | Example Value |
|-----------|----------|---------------------------------------|---------------|
| Hash      | String   | The hash of the current git commit    | 2d88ab5dbb83f |
| Branch    | String   | The current git branch                | main          |
| config    | String   | The configuration represented in json |               |
| <cam_num> | SubTable | The subtable for a camera             | see below     |


## Camera subtable
Note: When only one tag is detected, `Pose` will be relative to the tag. When multiple tags are detected, `Pose` is the field position. 

| Name          | Type         | Value                                                               | Example Value       | Explanation of example      |
|---------------|--------------|---------------------------------------------------------------------|---------------------|-----------------------------|
| Pose          | double array | The apriltag pose detected, in the order of x, y, z, qw, qx, qy, qz | [1,0.2,0.5,1,0,0,0] |                             |
| IDs           | String array | The ids of the apriltags detected                                   | ["1", "3"]          | Two poses, with ids 1 and 3 |
| RMSError      | double       | The error of the detection                                          |                     |                             |
| isRecording   | boolean      | Whether it is recording or not                                      |                     |                             |
| recordingPath | String       | The path of the recording                                           |                     |                             |
