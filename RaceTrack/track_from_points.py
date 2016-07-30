import bpy
import math

# calculate alpha, beta
# if beta < alpha the track goes CCW, else CW
# 
d = 0.5 #distance of track borders from center line (symmetric for now)

# use atan2 to calculate angle
#define points, later will fetch the points from selected object
p = []

# get points from active object
myob = bpy.context.active_object  
bpy.ops.object.mode_set(mode = 'OBJECT')  
  
#print('vertices at:')
for v in range(len(myob.data.vertices)):
    p.append(myob.data.vertices[v].co.x)
    p.append(myob.data.vertices[v].co.y)

segs = int(len(p)/2) - 1
print(len(p), 'entries', segs, 'segments')

        
angles = [] #angles of segments
for a in range(0, 2*(int(len(p)/2)-1), 2): #open path, not closed circuit

    alpha = math.degrees(math.atan2(p[a+3]-p[a+1], p[a+2]-p[a+0])) #p1y-p0y, p1x - p0x
    if alpha < 0:
        alpha = 360 + alpha
    print (a, alpha)
    angles.append(alpha)

pR = []
pL = []

# if first and last point are the same, then the circuit is closed
# if circuit is open (just a path) the the first and the last points are just perpendicular at distance d

# calculating RS and LS (RightStart, LeftStart)

RSx = p[0] + d * math.cos(math.radians(90 - angles[0])) # p[0] = Sx
RSy = p[1] - d * math.sin(math.radians(90 - angles[0])) # p[1] = Sy

pR.append(RSx)
pR.append(RSy)

#print('R0x=', pR[0], 'R0y=', pR[0+1])

L0x = p[0] - d * math.cos(math.radians(90 - angles[0])) # p[0] = Sx
L0y = p[1] + d * math.sin(math.radians(90 - angles[0])) # p[1] = Sy

pL.append(L0x)
pL.append(L0y)

#print('L0x=', pL[0], 'L0y=', pL[0+1])

# from corner point half of difference between seg2.angle - seg1.angle
# the distance is d / cos(deltaAngle) ... gets very long if delta angle goes 180

# angle of d at corner is angle of segment-90
# angle of D (Distance from cornerCenter to CornerRight = angleD
 
 
# turns
for seg in range(segs-1):
    #turning left
    if angles[seg+1] > angles[seg]: 
        print('turning left', angles[seg+1], angles[seg] )  
        
        sweepL = 180 - (angles[seg+1] - angles[seg])
        print('sweepL', sweepL)  
        sweepR = 360 - sweepL
        print('sweepR', sweepR)

    #turning right
    if angles[seg+1] < angles[seg]:
        print('turning right', angles[seg+1], angles[seg] )  
        
        sweepL = 180 - (angles[seg+1] - angles[seg])
        print('sweepL', sweepL)  
        sweepR = 360 - sweepL
        print('sweepR', sweepR)



    angleD = angles[seg+1] - sweepR / 2
    print('angleD', angleD)

    angled = angles[seg] - 90 
    angle_dD = angleD - angled
    print('angle_dD', angle_dD)


    lengthD = d / math.cos(math.radians(angle_dD))

    Dx = p[seg*2+2] + lengthD * math.cos(math.radians(angleD)) # n.th corner x
    Dy = p[seg*2+2+1] + lengthD * math.sin(math.radians(angleD))

    pR.append(Dx)
    pR.append(Dy)
    
    

#add final point if  open circuit, aka path
print('segs --->', segs)
REx = p[2*segs] + d * math.cos(math.radians(90 - angles[segs-1])) # p[0] = Sx
REy = p[2*segs + 1] - d * math.sin(math.radians(90 - angles[segs-1])) # p[1] = Sy

pR.append(REx)
pR.append(REy)

# create verts and faces
verts = []

# seg n
for seg in range(segs):
    vert = (float(pR[seg*2]), float(pR[seg*2+1]), 0) #x,y,z=0 ; seg*2, seg*2+1
    verts.append(vert)

    vert = (float(pR[seg*2+2]), float(pR[seg*2+2+1]), 0) #x,y,z=0 ; seg*2+2, seg*2+2+1
    verts.append(vert)

    vert = (float(p[seg*2+2]), float(p[seg*2+2+1]), 0) #x,y,z=0 ; seg*2+2, seg*2+2+1
    verts.append(vert)

    vert = (float(p[seg*2]), float(p[seg*2+1]), 0) #x,y,z=0 ; seg*2, seg*2+1
    verts.append(vert)





faces = []
# for s in range(int(len(p)/2)): # number of segments   
#     face = (s*4+0, s*4+1, s*4+2, s*4+3)
#     faces.append(face)    

for seg in range(segs):
    face = (seg*4+0,seg*4+1,seg*4+2,seg*4+3)
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