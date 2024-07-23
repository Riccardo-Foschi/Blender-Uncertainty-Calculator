import bpy
from bpy.props import FloatVectorProperty

def update_material(self, context):
    color1 = self.color1
    color2 = self.color2

    # Controlla se esiste già un materiale chiamato "CustomMaterial1"
    mat1 = bpy.data.materials.get("CustomMaterial1")
    bsdf1 = mat1.node_tree.nodes.get("Principled BSDF")
    if bsdf1:
        bsdf1.inputs['Base Color'].default_value = (color1[0], color1[1], color1[2], 1)
        bsdf1.inputs['Roughness'].default_value = 1.0

    # Controlla se esiste già un materiale chiamato "CustomMaterial2"
    mat2 = bpy.data.materials.get("CustomMaterial2")
    bsdf2 = mat2.node_tree.nodes.get("Principled BSDF")
    if bsdf2:
        bsdf2.inputs['Base Color'].default_value = (color2[0], color2[1], color2[2], 1)
        bsdf2.inputs['Roughness'].default_value = 1.0


class SimpleOperator1(bpy.types.Operator):
    bl_idname = "object.apply_material1"
    bl_label = "Apply Material 1"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        color = context.scene.my_tool.color1
        
        # Controlla se esiste già un materiale chiamato "CustomMaterial2"
        mat = bpy.data.materials.get("CustomMaterial1")
        if mat is None:
            mat = bpy.data.materials.new(name="CustomMaterial1")
            mat.use_nodes = True
        
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (color[0], color[1], color[2], 1)
            bsdf.inputs['Roughness'].default_value = 1.0
        
        for obj in selected_objects:
            if obj.type == 'MESH':
                if obj.data.materials:
                    obj.data.materials[0] = mat
                else:
                    obj.data.materials.append(mat)
        
        return {'FINISHED'}

class SimpleOperator2(bpy.types.Operator):
    bl_idname = "object.apply_material2"
    bl_label = "Apply Material 2"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        color = context.scene.my_tool.color2

        
        # Controlla se esiste già un materiale chiamato "CustomMaterial2"
        mat = bpy.data.materials.get("CustomMaterial2")
        if mat is None:
            mat = bpy.data.materials.new(name="CustomMaterial2")
            mat.use_nodes = True
        
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (color[0], color[1], color[2], 1)
            bsdf.inputs['Roughness'].default_value = 1.0
        
        for obj in selected_objects:
            if obj.type == 'MESH':
                if obj.data.materials:
                    obj.data.materials[0] = mat
                else:
                    obj.data.materials.append(mat)
        
        return {'FINISHED'}

class SimplePanel(bpy.types.Panel):
    bl_label = "Test"
    bl_idname = "OBJECT_PT_test"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Test"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        row = layout.row()
        row.prop(mytool, "color1", text="")
        row.operator("object.apply_material1", text="Apply")
        
        row = layout.row()
        row.prop(mytool, "color2", text="")
        row.operator("object.apply_material2", text="Apply")

class MyProperties(bpy.types.PropertyGroup):
    color1: FloatVectorProperty(
        name="Color Picker 1",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        update=update_material,
        description="Choose a color"
    )
    
    color2: FloatVectorProperty(
        name="Color Picker 2",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        update=update_material,
        description="Choose a color"
    )

def register():
    bpy.utils.register_class(SimpleOperator1)
    bpy.utils.register_class(SimpleOperator2)
    bpy.utils.register_class(SimplePanel)
    bpy.utils.register_class(MyProperties)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)

def unregister():
    bpy.utils.unregister_class(SimpleOperator1)
    bpy.utils.unregister_class(SimpleOperator2)
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(MyProperties)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
