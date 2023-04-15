# GET
### Query Parameters: 
None
### Meant For:
API users
### Returns:
JSON data containing apriltag detections
### Return Format:
```
[
  {
      "left_right":  %The left/right position of the apriltag%,
      "up_down":  %The up/down position of the apriltag%,
      "distance":  %The distance of the apriltag%,
      "roll":  %The roll of the apriltag%,
      "yaw":  %The yaw of the apriltag%,
      "pitch":  %The pitch of the apriltag%,
      "left_right_std":  %The error of the "left_right" measurment%,
      "distance_std":  %The error of the "distance" measurment%,
      "yaw_std":  %The error of the "yaw" measurment%,
      "rms":  %The RMS of the reprojection error%,
      "error":  %The overall error of the apriltag detection%,
      "tagid": %The id of the apriltag detected%,
      "camera": %The camera that detected the apriltag%
  }, ...
]
```
