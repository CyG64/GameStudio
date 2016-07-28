import bpy
import math

# calculate alpha, beta
# if beta < alpha the track goes CCW, else CW
# 
d = 0.5 #distance of track borders from center line (symmetric for now)

# use atan2 to calculate angle
#define points, later will fetch the points from selected object
p = (0,0, 1.41,1.41, 0,2.8, 3,2) #2D points X,Y defining the track center line

print(p)

angles = [] #angles of segments
for a in range(0, int(len(p)/2)+1, 2):

    alpha = math.degrees(math.atan2(p[a+3]-p[a+1], p[a+2]-p[a+0])) #p1y-p0y, p1x - p0x
    if alpha < 0:
        alpha = 360 + alpha
    print (alpha)
    angles.append(alpha)

pR = []
pL = []
# calculating R0 and L0 rightStart, leftStart

R0x = p[0] + d * math.cos(math.radians(90 - angles[0])) # p[0] = Sx
R0y = p[1] - d * math.sin(math.radians(90 - angles[0])) # p[1] = Sy

pR.append(R0x)
pR.append(R0y)

print('R0x=', pR[0], 'R0y=', pR[0+1])

L0x = p[0] - d * math.cos(math.radians(90 - angles[0])) # p[0] = Sx
L0y = p[1] + d * math.sin(math.radians(90 - angles[0])) # p[1] = Sy

pL.append(L0x)
pL.append(L0y)

print('L0x=', pL[0], 'L0y=', pL[0+1])

# from corner point half of difference between seg2.angle - seg1.angle
# the distance is d / cos(deltaAngle) ... gets very long if delta angle goes 180

# angle of d at corner is angle of segment-90
# angle of D (Distance from cornerCenter to CornerRight = angleD
 
angleD = angles[0] - (angles[1] - angles[0])/2
lengthD = d / math.cos(math.radians(angles[0]- angleD))

Dx = p[2] + lengthD * math.cos(math.radians(angleD)) #first corner x
Dy = p[3] + lengthD * math.sin(math.radians(angleD))

pR.append(Dx)
pR.append(Dy)

print(lengthD, Dx, Dy)


#add final point (not closed yet)
R2x = p[4] + d * math.cos(math.radians(90 - angles[1])) # p[0] = Sx
R2y = p[5] - d * math.sin(math.radians(90 - angles[1])) # p[1] = Sy

pR.append(R2x)
pR.append(R2y)

# create faces
verts = []
vert = (float(pR[0]), float(pR[0+1]), 0) #x,y,z=0
verts.append(vert)

vert = (float(pR[2]), float(pR[2+1]), 0) #x,y,z=0
verts.append(vert)

vert = (float(p[2]), float(p[2+1]), 0) #x,y,z=0
verts.append(vert)

vert = (float(p[0]), float(p[0+1]), 0) #x,y,z=0
verts.append(vert)

faces = []
face = (0,1,2,3)
faces.append(face)

face = (0,1,2,3)
faces.append(face)

#create mesh and object
mesh = bpy.data.meshes.new("r")
object = bpy.data.objects.new("track",mesh)

#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
#create mesh from python data
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)
