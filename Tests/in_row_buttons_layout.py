import bpy

class SimpleOperatorLeft(bpy.types.Operator):
    bl_idname = "object.simple_operator_left"
    bl_label = "Sinistro"
    
    def execute(self, context):
        self.report({'INFO'}, "Bottone Sinistro cliccato")
        return {'FINISHED'}

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
        row = layout.row()
        col = row.column()
        col.operator("object.simple_operator_left")
        col = row.column()
        col.operator("object.simple_operator_right")

def register():
    bpy.utils.register_class(SimpleOperatorLeft)
    bpy.utils.register_class(SimpleOperatorRight)
    bpy.utils.register_class(SimplePanel)

def unregister():
    bpy.utils.unregister_class(SimpleOperatorLeft)
    bpy.utils.unregister_class(SimpleOperatorRight)
    bpy.utils.unregister_class(SimplePanel)

if __name__ == "__main__":
    register()
