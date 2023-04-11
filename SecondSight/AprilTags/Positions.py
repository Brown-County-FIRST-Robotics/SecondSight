"""
________________________________________
|                                       |
|5                                     4|
|                                       |
|                origin                 |
|6                                     3|
|7   [|]b charge|        |r charge[|]  2|
|8                                     1|
|_______________________________________|

[|] denotes an autonomous entrance

y
|
|
|
|
z------x

      90
       |
       |
       |
180---yaw---0
       |
       |
       |
      270

up_down:z
distance:y
left_right:x

positions
*all units are CM and degrees
"""

# page 4:
# https://firstfrc.blob.core.windows.net/frc2023/FieldAssets/2023LayoutMarkingDiagram.pdf


# apriltagNumber:[x,y,z,roll]
apriltagPositions = {
    '1': [724.36, -293.84, 46.28, 180],
    '2': [724.36, -126.2, 46.28, 180],
    '3': [724.36, 41.44, 46.28, 180],
    '4': [790.88, 273.98, 69.55, 180],
    '5': [-790.8, 273.98, 69.55, 0],
    '6': [-724.26, 41.44, 46.28, 0],
    '7': [-724.26, -126.2, 46.28, 0],
    '8': [-724.26, -293.84, 46.28, 0]
}

