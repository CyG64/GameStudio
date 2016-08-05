import bpy
from bpy.props import *
import bmesh
import math

def add_box(llat, ulat, UIsteps, width, height, depth):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    verts = []
    faces = []
    steps=int(UIsteps) #longitude 
    
    #latitude steps
    #lat_steps = int(180/(ulat-llat) -----------------------------to do
    for s_lat in range(5): #steps for all lattitudes

        # lowest ring
        for s in range(steps):
            a_lat = llat+s_lat*15 #angle for lattitude
            r_lat = math.cos(math.radians(a_lat)) #radius for lattitude
            a = s * 360 / steps
            vert = (r_lat*math.cos(math.radians(a)), r_lat*math.sin(math.radians(a)), math.sin(math.radians(a_lat)))
            verts.append(vert)
        

    # first ring
    for f in range(steps-1): #--------------last face vertices
        face = (f+0, f+1, steps+f+1, steps+f)
        faces.append(face)
    # second ring    
    for f in range(steps-1): #--------------last face vertices
        face = (steps+f+0, steps+f+1, steps+steps+f+1, steps+steps+f)
        faces.append(face)
    # third ring    
    for f in range(steps-1): #--------------last face vertices
        face = (2*steps+f+0, 2*steps+f+1, 2*steps+steps+f+1, 2*steps+steps+f)
        faces.append(face)
        
    # 4th ring    
    for f in range(steps-1): #--------------last face vertices
        face = (3*steps+f+0, 3*steps+f+1, 3*steps+steps+f+1, 3*steps+steps+f)
        faces.append(face)
        

    # apply size
    for i, v in enumerate(verts):
        verts[i] = v[0] * width, v[1] * depth, v[2] * height

    return verts, faces


from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty


class AddBox(bpy.types.Operator):
    """Add a Partial Sphere mesh"""
    bl_idname = "mesh.primitive_box_add"
    bl_label = "Partial Sphere"
    bl_options = {'REGISTER', 'UNDO'}

    steps = IntProperty(
            name="Vertices",
            description="vertices for full circle",
            min=12, max=48, step=1,
            default=12
            )
    llat = FloatProperty(
            name="lower lattitude",
            description="lower lattitude",
            min=-90.0, max=90.0,
            default=0.0,
            )      
    ulat = FloatProperty(
            name="upper lattitude",
            description="upper lattitude",
            min=-90.0, max=90.0,
            default=0.0,
            )      
                  
    width = FloatProperty(
            name="Width",
            description="Box Width",
            min=0.01, max=100.0,
            default=1.0,
            )
    height = FloatProperty(
            name="Height",
            description="Box Height",
            min=0.01, max=100.0,
            default=1.0,
            )
    depth = FloatProperty(
            name="Depth",
            description="Box Depth",
            min=0.01, max=100.0,
            default=1.0,
            )

    # generic transform props
    view_align = BoolProperty(
            name="Align to View",
            default=False,
            )
    location = FloatVectorProperty(
            name="Location",
            subtype='TRANSLATION',
            )
    rotation = FloatVectorProperty(
            name="Rotation",
            subtype='EULER',
            )

    def execute(self, context):

        verts_loc, faces = add_box(self.llat, self.ulat,self.steps,
                                   self.width,
                                   self.height,
                                   self.depth,
                                   )

        mesh = bpy.data.meshes.new("Box")

        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.new(v_co)

        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])

        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddBox.bl_idname, icon='MESH_SPHERE')


def register():
    bpy.utils.register_class(AddBox)
    bpy.types.INFO_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddBox)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mesh.primitive_box_add()
