import bpy
from bpy.props import FloatVectorProperty
from bpy.types import Panel, PropertyGroup

# Definisci un nuovo PropertyGroup per il colore
class ColorProperties(PropertyGroup):
    color: FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(1.0, 0.0, 0.0, 1.0)  # Rosso con trasparenza 0
    )

class SimpleOperatorRight(bpy.types.Operator):
    bl_idname = "object.simple_operator_right"
    bl_label = "Destro"
    
    def execute(self, context):
        self.report({'INFO'}, "Bottone Destro cliccato")
        return {'FINISHED'}

class SimplePanel(bpy.types.Panel):
    bl_label = "Bottoni Affiancati Prova"
    bl_idname = "OBJECT_PT_simple_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Bottoni Affiancati Prova"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        color_props = scene.color_props
        
        row = layout.row()
        
        # Aggiungi il selettore di colore senza label
        col = row.column()
        col.prop(color_props, "color", text="")
        
        # Aggiungi il bottone destro
        col = row.column()
        col.operator("object.simple_operator_right")

def register():
    bpy.utils.register_class(ColorProperties)
    bpy.types.Scene.color_props = bpy.props.PointerProperty(type=ColorProperties)
    bpy.utils.register_class(SimpleOperatorRight)
    bpy.utils.register_class(SimplePanel)

def unregister():
    bpy.utils.unregister_class(SimplePanel)
    del bpy.types.Scene.color_props
    bpy.utils.unregister_class(SimpleOperatorRight)
    bpy.utils.unregister_class(ColorProperties)

if __name__ == "__main__":
    register()
