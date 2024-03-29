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

# page 4:
# https://firstfrc.blob.core.windows.net/frc2023/FieldAssets/2023LayoutMarkingDiagram.pdf


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


def corners(rulesX, rulesY, rulesZ, rulesZRot, year):
    assert rulesZRot == 0 or rulesZRot == 180
    if rulesZRot == 0:
        out = []
        for i, j in [(-.5, .5), (.5, .5), (.5, -.5), (-.5, -.5)]:
            out.append(toOurCoords(rulesX, rulesY + i * tag_size_in[year], rulesZ + j * tag_size_in[year]))
        return out
    else:
        out = []
        for i, j in [(.5, .5), (-.5, .5), (-.5, -.5), (.5, -.5)]:
            out.append(toOurCoords(rulesX, rulesY + i * tag_size_in[year], rulesZ + j * tag_size_in[year]))
        return out


apriltagFeatures = {year: {i: corners(x, y, z, r, year) for i, (x, y, z, r) in poses.items()} for year, poses in apriltagPositions.items()}
