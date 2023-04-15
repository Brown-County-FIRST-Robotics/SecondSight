# This page is meant for all /camera_feed/* URLs
## "*" is the camera number
# GET
### Query Parameters: 
| Paramater    | Values      | Function                                           |
|--------------|-------------|----------------------------------------------------|
| uncalibrated | true, false | Specifies if the feed should be before remapping   |
| framerate    | {float}     | Specifies the camera's framerate (Hz) (Default:10) |
### Meant For:
Other pages
### Returns:
A JPEG stream from the specified camera. 
