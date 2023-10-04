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
    "2023": {
        '1': [610.77 * 2.54, 42.19 * 2.54, 18.22 * 2.54, 180],
        '2': [610.77 * 2.54, 108.19 * 2.54, 18.22 * 2.54, 180],
        '3': [610.77 * 2.54, 174.19 * 2.54, 18.22 * 2.54, 180],
        '4': [636.96 * 2.54, 265.74 * 2.54, 27.38 * 2.54, 180],
        '5': [14.25 * 2.54, 265.74 * 2.54, 27.38 * 2.54, 0],
        '6': [40.45 * 2.54, 174.19 * 2.54, 18.22 * 2.54, 0],
        '7': [40.45 * 2.54, 108.19 * 2.54, 18.22 * 2.54, 0],
        '8': [40.45 * 2.54, 42.19 * 2.54, 18.22 * 2.54, 0]
    }
}

tag_size = 6 * .0254

"""
3       2
    4
0       1
"""
apriltagFeatures = {
    '2023': {
        '1': [
            610.77 * .0254, 42.19 * .0254 + tag_size / 2, 18.22 * .0254 - tag_size / 2,
            610.77 * .0254, 42.19 * .0254 - tag_size / 2, 18.22 * .0254 - tag_size / 2,
            610.77 * .0254, 42.19 * .0254 - tag_size / 2, 18.22 * .0254 + tag_size / 2,
            610.77 * .0254, 42.19 * .0254 + tag_size / 2, 18.22 * .0254 + tag_size / 2,
            610.77 * .0254, 42.19 * .0254, 18.22 * .0254
        ],
        '2': [
            610.77 * .0254, 108.19 * .0254 + tag_size / 2, 18.22 * .0254 - tag_size / 2,
            610.77 * .0254, 108.19 * .0254 - tag_size / 2, 18.22 * .0254 - tag_size / 2,
            610.77 * .0254, 108.19 * .0254 - tag_size / 2, 18.22 * .0254 + tag_size / 2,
            610.77 * .0254, 108.19 * .0254 + tag_size / 2, 18.22 * .0254 + tag_size / 2,
            610.77 * .0254, 108.19 * .0254, 18.22 * .0254
        ],
        '3': [
            610.77 * .0254, 174.19 * .0254 + tag_size / 2, 18.22 * .0254 - tag_size / 2,
            610.77 * .0254, 174.19 * .0254 - tag_size / 2, 18.22 * .0254 - tag_size / 2,
            610.77 * .0254, 174.19 * .0254 - tag_size / 2, 18.22 * .0254 + tag_size / 2,
            610.77 * .0254, 174.19 * .0254 + tag_size / 2, 18.22 * .0254 + tag_size / 2,
            610.77 * .0254, 174.19 * .0254, 18.22 * .0254
        ],
        '4': [
            636.96 * .0254, 265.74 * .0254 + tag_size / 2, 27.38 * .0254 - tag_size / 2,
            636.96 * .0254, 265.74 * .0254 - tag_size / 2, 27.38 * .0254 - tag_size / 2,
            636.96 * .0254, 265.74 * .0254 - tag_size / 2, 27.38 * .0254 + tag_size / 2,
            636.96 * .0254, 265.74 * .0254 + tag_size / 2, 27.38 * .0254 + tag_size / 2,
            636.96 * .0254, 265.74 * .0254, 27.38 * .0254
        ],
        '5': [
            14.25 * .0254, 265.74 * .0254 - tag_size / 2, 27.38 * .0254 - tag_size / 2,
            14.25 * .0254, 265.74 * .0254 + tag_size / 2, 27.38 * .0254 - tag_size / 2,
            14.25 * .0254, 265.74 * .0254 + tag_size / 2, 27.38 * .0254 + tag_size / 2,
            14.25 * .0254, 265.74 * .0254 - tag_size / 2, 27.38 * .0254 + tag_size / 2,
            14.25 * .0254, 265.74 * .0254, 27.38 * .0254
        ],
        '6': [
            40.45 * .0254, 174.19 * .0254 - tag_size / 2, 18.22 * .0254 - tag_size / 2,
            40.45 * .0254, 174.19 * .0254 + tag_size / 2, 18.22 * .0254 - tag_size / 2,
            40.45 * .0254, 174.19 * .0254 + tag_size / 2, 18.22 * .0254 + tag_size / 2,
            40.45 * .0254, 174.19 * .0254 - tag_size / 2, 18.22 * .0254 + tag_size / 2,
            40.45 * .0254, 174.19 * .0254, 18.22 * .0254
        ],
        '7': [
            40.45 * .0254, 108.19 * .0254 - tag_size / 2, 18.22 * .0254 - tag_size / 2,
            40.45 * .0254, 108.19 * .0254 + tag_size / 2, 18.22 * .0254 - tag_size / 2,
            40.45 * .0254, 108.19 * .0254 + tag_size / 2, 18.22 * .0254 + tag_size / 2,
            40.45 * .0254, 108.19 * .0254 - tag_size / 2, 18.22 * .0254 + tag_size / 2,
            40.45 * .0254, 108.19 * .0254, 18.22 * .0254
        ],
        '8': [
            40.45 * .0254, 42.19 * .0254 - tag_size / 2, 18.22 * .0254 - tag_size / 2,
            40.45 * .0254, 42.19 * .0254 + tag_size / 2, 18.22 * .0254 - tag_size / 2,
            40.45 * .0254, 42.19 * .0254 + tag_size / 2, 18.22 * .0254 + tag_size / 2,
            40.45 * .0254, 42.19 * .0254 - tag_size / 2, 18.22 * .0254 + tag_size / 2,
            40.45 * .0254, 42.19 * .0254, 18.22 * .0254
        ],

    }
}
