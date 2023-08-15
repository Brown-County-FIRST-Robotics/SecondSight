# Description
The specific attributes for each camera

# Type
List[Dict]

# Key/Value descriptions
| key         | type                       | description                             | possible values      |
|-------------|----------------------------|-----------------------------------------|----------------------|
| port        | str                        | The port that the camera runs on        | n/a                  |
| pos         | Tuple[float, float, float] | The position of the camera on the robot | n/a                  |
| role        | List[str]                  | The role of the camera                  | apriltags gamepieces |
| calibration | Dict[str, List[float]]     | The calibration of the camera           | n/a                  |

## Calibration Information
| key             | type              | description                                     |
|-----------------|-------------------|-------------------------------------------------|
| camera_matrix   | List[List[float]] | The camera matrix                               |
| dist            | List[float]       | The distortion coefficients                     |
| calibration_res | Tuple[int, int]   | The resolution of the camera during calibration |
| processing_res  | Tuple[int, int]   | The export resolution of the camera             |
