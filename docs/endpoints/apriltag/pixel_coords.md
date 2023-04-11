# GET
### Query Parameters: 
None
### Meant For:
API users
### Returns:
json data containing apriltag detections
### Return Format:
```
[
  {
      "coords":  %the coordinates of the apriltag%,
      "tagid": %the id of the apriltag detected%,
      "camera": %the camera that detected the apriltag%
  }, ...
]
```