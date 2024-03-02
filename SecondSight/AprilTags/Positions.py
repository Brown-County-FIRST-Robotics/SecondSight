"""
________________________________________
|                                       |
|5                                     4|
|                                       |
|                                       |
|6                                     3|
|7   [|]b charge|        |r charge[|]  2|
|8                                     1|
*_______________________________________|

[|] denotes an autonomous entrance
* is the origin
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

positions
*all units are CM and degrees
"""
import math

# page 4:
# https://firstfrc.blob.core.windows.net/frc2023/FieldAssets/2023LayoutMarkingDiagram.pdf
# https://firstfrc.blob.core.windows.net/frc2024/FieldAssets/2024LayoutMarkingDiagram.pdf


# apriltagNumber:[x,y,z,roll]
# From the rules. in inches.
apriltagPositions = {
    "2023": {
        '1': [610.77, 42.19, 18.22, 180],
        '2': [610.77, 108.19, 18.22, 180],
        '3': [610.77, 174.19, 18.22, 180],
        '4': [636.96, 265.74, 27.38, 180],
        '5': [14.25, 265.74, 27.38, 0],
        '6': [40.45, 174.19, 18.22, 0],
        '7': [40.45, 108.19, 18.22, 0],
        '8': [40.45, 42.19, 18.22, 0]
    },
    "2024": {
        '1': [593.68, 9.68, 53.38, 120],
        '2': [637.21, 34.79, 53.38, 120],
        '3': [652.73, 196.17, 57.13, 180],
        '4': [652.73, 218.42, 57.13, 180],
        '5': [578.77, 323.00, 53.38, 270],
        '6': [72.5, 323.00, 53.38, 270],
        '7': [-1.50, 218.42, 57.13, 0],
        '8': [-1.50, 196.17, 57.13, 0],
        '9': [14.02, 34.79, 53.38, 60],
        '10': [57.54, 9.68, 53.38, 60],
        '11': [468.69, 146.19, 52.00, 300],
        '12': [468.69, 177.10, 52.00, 60],
        '13': [441.74, 161.62, 52.00, 180],
        '14': [209.48, 161.62, 52.00, 0],
        '15': [182.73, 177.10, 52.00, 120],
        '16': [182.73, 146.19, 52.00, 240]
    }
}

tag_size_in = {
    '2023': 6,
    '2024': 6.5
}  # inches
tag_size = {i: ts * .0254 for i, ts in tag_size_in.items()}  # meters

"""
0       1
     
3       2
"""


def toOurCoords(rulesX, rulesY, rulesZ):
    # inchs to meters
    rulesX, rulesY, rulesZ = [.0254 * v for v in [rulesX, rulesY, rulesZ]]
    return -rulesY, -rulesZ, rulesX


def rotate(p, theta):
    c=math.cos(math.radians(theta))
    s=math.sin(math.radians(theta))
    return c*p[0]-s*p[1],s*p[0]+c*p[1],p[2]


def corners(rulesX, rulesY, rulesZ, rulesZRot, year):
    out = []
    for i, j, k in [rotate(z,rulesZRot) for z in [(0,-.5, .5), (0,.5, .5), (0,.5, -.5), (0,-.5, -.5)]]:
        out.append(toOurCoords(rulesX + i * tag_size_in[year], rulesY + j * tag_size_in[year], rulesZ + k * tag_size_in[year]))
    return out


apriltagFeatures = {year: {i: corners(x, y, z, r, year) for i, (x, y, z, r) in poses.items()} for year, poses in apriltagPositions.items()}
