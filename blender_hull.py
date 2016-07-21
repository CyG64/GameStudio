import bpy
import math

# use the pipe to separate cross-sections cs1|cs2|cs3
# use the comma to separate points
# use the semi-colon to separate the parameter blocks
line = "H:p1,p2,p3|l=2;pA,pB,pC|l=3;o=1;pM,pN,pO" #Hull from 3 Cross-Sections, default length 1

if line[0:2] == 'H:': #Hull
    print('generating Hull')
    
token = ''
for c in range(0,len(line)):
    cc = line[c:c+1]
    #print(c, cc)
    if cc == '|':
        print(token)
        token=''
    else:
        token = token + cc  
    
#parameter l is length
#parameter o is offset horizontal, vertical, or both
#parameter w is wise (clock wise CW, counter clock wise CCW)

#new point N, eg :N3.2,4.1,5.8 : this will be implemented much later (perhaps)


line = "H:CCW:cs:pos=2,p1,p2,p3:cs:pos=3,pA,pB,pC" #Hull from Cross-Sections

# section length is pos(1) - pos(0)

nCS = 3 # nb of cross-sections
nPts = 6 # nb of points on section


# mesh arrays
verts = []
faces = []

# define the cross-sections here, use CCW for list of points
lines = [] # the lines can be read from a text file
lines.append("p=0;1,0, 1,1, 0,2, -1,1, -1,0, 1,0") #the points are after the last ;
lines.append("p=2; 3,0, 1.5,1.5, 0,2.5, -1.5,1, -1.5,0, 3,0")
lines.append("p=4; 1,0, 1,1, 0,2, -1,1, -1,0, 1,0")

for s in range(len(lines)):
    
    # separate heading parameters from trailing point section
    params = lines[s].split(";")
    # the points are encoded after the last ;
    points = params[len(params)-1]

    vert2D = points.split(',')
    
    #CS s
    p = 0 + s #position cs
    #vert2D = (1,0, 1,1, 0,2, -1,1, -1,0, 0,-1) #0, #1, ...
    for v in range(0,len(vert2D),2):
        vert = (float(vert2D[v]), float(vert2D[v+1]), p)
        verts.append(vert)


 
#fill faces array
#f = 0
#for alat in range (0, nbLat - 1):
#
#    for alon in range (0, nbLon - 1):
#
#        face = (alon + alat * nbLon, alon + alat * nbLon + 1, alon + (alat+1) * nbLon + 1, alon+ (alat+1) * nbLon )
#        faces.append(face)


for cs in range (0, nCS-1):
    for pt in range (0, nPts-1):

    #section 1
        face = (pt+cs*nPts, pt+cs*nPts+1, pt+1+(cs+1)*nPts, pt+(cs+1)*nPts)
        faces.append(face)

    
    face = (nPts-1, 0, 5, 9)
    #faces.append(face)




        
#create mesh and object
mesh = bpy.data.meshes.new("cs")
object = bpy.data.objects.new("hull",mesh)
 
#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
#create mesh from python data
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)
