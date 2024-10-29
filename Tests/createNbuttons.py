import bpy

class UncertaintyPanel(bpy.types.Panel):
    bl_label = "Uncertainty"
    bl_idname = "VIEW3D_PT_uncertainty"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Uncertainty"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Slider per selezionare il numero di bottoni
        layout.prop(scene, "uncertainty_levels", text="Uncertainty levels", slider=True)

        # Area per i bottoni generati
        box = layout.box()
        for i in range(scene.uncertainty_levels):
            box.operator("object.uncertainty_button_{}".format(i + 1), text=str(i + 1))

# Operatore per la generazione della scala
class GenerateUncertaintyScaleOperator(bpy.types.Operator):
    bl_idname = "object.generate_uncertainty_levels"
    bl_label = "Generate uncertainty scale"

    def execute(self, context):
        return {'FINISHED'}

# Creazione di operatori per i bottoni dinamici
def create_dynamic_button_class(index):
    class DynamicButton(bpy.types.Operator):
        bl_idname = "object.uncertainty_button_{}".format(index)
        bl_label = "Uncertainty Button {}".format(index)

        def execute(self, context):
            self.report({'INFO'}, f"Button {index} clicked!")
            return {'FINISHED'}
    return DynamicButton

# Registrazione dinamica delle classi dei bottoni
def register_buttons():
    for i in range(1, 11):
        bpy.utils.register_class(create_dynamic_button_class(i))

def unregister_buttons():
    for i in range(1, 11):
        try:
            bpy.utils.unregister_class(create_dynamic_button_class(i))
        except RuntimeError:
            pass

def register():
    bpy.types.Scene.uncertainty_levels = bpy.props.IntProperty(
        name="Uncertainty Scale",
        default=3,
        min=2,
        max=10
    )
    bpy.utils.register_class(UncertaintyPanel)
    bpy.utils.register_class(GenerateUncertaintyScaleOperator)
    register_buttons()

def unregister():
    del bpy.types.Scene.uncertainty_levels
    bpy.utils.unregister_class(UncertaintyPanel)
    bpy.utils.unregister_class(GenerateUncertaintyScaleOperator)
    unregister_buttons()

if __name__ == "__main__":
    register()
