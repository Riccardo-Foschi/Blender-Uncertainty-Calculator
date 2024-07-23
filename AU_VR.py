bl_info = {
    "name": "Uncertainty quantification",
    "blender": (2, 80, 0),
    "Location": "Side panel (N shortcut) > Uncertainty",
    "category": "Model Analysis",
    "author": "Riccardo Foschi and Chat GPT",
    "description": "Allows to calculate the average uncertainty weighted with the volume (AU_V) and the average uncertainty weighted with the volume and relevance (AU_VR) for hypothetical 3D architectural reconstruction models",
    "version": (1, 0, 0),
}



import bpy
import bmesh
from mathutils import Vector
from bpy.props import FloatVectorProperty
from bpy.types import Panel, PropertyGroup


class ColorProperties(PropertyGroup):
       
    color: FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(1.0, 1.0, 1.0, 1.0)
    )



# Funzione per aggiornare il materiale
def update_material(obj, color):
    mat_name = "Uncertainty_{}".format(color)
    mat = bpy.data.materials.get(mat_name)
    
    if mat is None:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = 1.0
        mat.use_fake_user = True

    if len(obj.material_slots) == 0:
        bpy.ops.object.material_slot_add()

    obj.material_slots[0].material = mat

def assign_uncertainty_level(level, color):    
    percentage_map = {
        1: 7.143,
        2: 21.429,
        3: 35.714,
        4: 50,
        5: 64.286,
        6: 78.571,
        7: 92.857
    }

    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            if level == 8:
                reset_uncertainty_level()
            else:
                obj["Uncertainty Level"] = level
                obj["Uncertainty Percentage"] = percentage_map[level]
                update_material(obj, color)
            
            # Crea un nuovo materiale
            mat = bpy.data.materials.new(name="TestMaterial")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf:
                bsdf.inputs['Base Color'].default_value = (color)  # Imposta il colore

            # Assegna il materiale all'oggetto
            if len(obj.data.materials):
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
                
    bpy.context.view_layer.update()

def reset_uncertainty_level():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            if "Uncertainty Level" in obj:
                del obj["Uncertainty Level"]
            if "Uncertainty Percentage" in obj:
                del obj["Uncertainty Percentage"]
            update_material(obj, (0, 0, 0, 1))
    bpy.context.view_layer.update()

def assign_relevance_factor(factor):
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            obj["Relevance"] = factor
    bpy.context.view_layer.update()

def reset_relevance_factor():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            if "Relevance" in obj:
                del obj["Relevance"]
    bpy.context.view_layer.update()

def calculate_volume(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    volume = bm.calc_volume(signed=True)
    bm.free()
    obj["Volume"] = volume
    bpy.context.view_layer.update()
    return volume

def reset_volume():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            if "Volume" in obj:
                del obj["Volume"]
    bpy.context.view_layer.update()

def calculate_average_uncertainty():
    total_volume = 0
    weighted_sum = 0

    for obj in bpy.data.objects:
        if "Uncertainty Level" in obj and "Volume" in obj:
            volume = obj["Volume"]
            uncertainty_percentage = obj["Uncertainty Percentage"]
            weighted_sum += volume * uncertainty_percentage
            total_volume += volume

    if total_volume == 0:
        return 0

    au_v = weighted_sum / total_volume
    return au_v

def calculate_average_uncertainty_with_relevance():
    total_volume = 0
    weighted_sum = 0

    for obj in bpy.data.objects:
        if "Uncertainty Level" in obj and "Volume" in obj:
            volume = obj["Volume"]
            uncertainty_percentage = obj["Uncertainty Percentage"]
            relevance_factor = obj.get("Relevance", 1)
            weighted_sum += volume * uncertainty_percentage * relevance_factor
            total_volume += volume * relevance_factor

    if total_volume == 0:
        return 0

    au_vr = weighted_sum / total_volume
    return au_vr

class UncertaintyPanel(bpy.types.Panel):
    bl_label = "Uncertainty"
    bl_idname = "OBJECT_PT_uncertainty"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Uncertainty'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row()
        row.operator("object.reset_colors_to_defaults", text="Reset colors to defaults")
        
        #1
        row = layout.row()
        col = row.column()
        color_props1 = scene.ColorProperties1
        col.prop(color_props1, "color", text="")
        col = row.column()     
        col.operator("object.assign_uncertainty_level", text="Assign 1").level = 1
        #end
            
        #2
        row = layout.row()
        col = row.column()
        color_props2 = scene.ColorProperties2
        col.prop(color_props2, "color", text="")
        col = row.column()     
        col.operator("object.assign_uncertainty_level", text="Assign 2").level = 2
        #end
        
        #3
        row = layout.row()
        col = row.column()
        color_props3 = scene.ColorProperties3
        col.prop(color_props3, "color", text="")
        col = row.column()     
        col.operator("object.assign_uncertainty_level", text="Assign 3").level = 3
        #end
        
        #4
        row = layout.row()
        col = row.column()
        color_props4 = scene.ColorProperties4
        col.prop(color_props4, "color", text="")
        col = row.column()     
        col.operator("object.assign_uncertainty_level", text="Assign 4").level = 4
        #end
        
        #5
        row = layout.row()
        col = row.column()
        color_props5 = scene.ColorProperties5
        col.prop(color_props5, "color", text="")
        col = row.column()     
        col.operator("object.assign_uncertainty_level", text="Assign 5").level = 5
        #end
        
        #6
        row = layout.row()
        col = row.column()
        color_props6 = scene.ColorProperties6
        col.prop(color_props6, "color", text="")
        col = row.column()     
        col.operator("object.assign_uncertainty_level", text="Assign 6").level = 6
        #end
        
        #7
        row = layout.row()
        col = row.column()
        color_props7 = scene.ColorProperties7
        col.prop(color_props7, "color", text="")
        col = row.column()     
        col.operator("object.assign_uncertainty_level", text="Assign 7").level = 7
        #end
        
        #8
        row = layout.row()
        col = row.column()
        color_props8 = scene.ColorProperties8
        col.prop(color_props8, "color", text="")
        col = row.column()     
        col.operator("object.assign_uncertainty_level", text="Assign 8").level = 8
        #end        
        
        row = self.layout.row()
        row.label(text="Assign Uncertainty level")


        row = layout.row()
        col = row.column()
        col.prop(color_props1, "color8", text="")
        row.operator("object.reset_uncertainty_level", text="Abstention/Reset")

        row = layout.row()
        row.label(text="Assign Relevance Factor")

        row = layout.row()
        row.prop(context.scene, "relevance_factor", text="Relevance Factor")

        row = layout.row()
        row.operator("object.assign_relevance", text="Assign Relevance")

        row = layout.row()
        row.operator("object.reset_relevance", text="Reset Relevance")

        row = layout.row()
        row.label(text="Calculate Volume")

        row = layout.row()
        row.operator("object.calculate_volume", text="Calculate Volume of selection")

        row = layout.row()
        row.operator("object.reset_volume", text="Reset Volume")

        row = layout.row()
        row.label(text="Calculate Average Uncertainty")

        row = layout.row()
        row.operator("object.calculate_au_v", text="Calculate AU_V")
        row = layout.row()
        row.prop(context.scene, "au_v_result", text="AU_V Result")

        row = layout.row()
        row.operator("object.calculate_au_vr", text="Calculate AU_VR")
        row = layout.row()
        row.prop(context.scene, "au_vr_result", text="AU_VR Result")

        row = layout.row()
        row.label(text="Select by Uncertainty")

        for i in range(1, 8):
            row = layout.row()
            row.operator("object.select_by_uncertainty", text=str(i)).level = i

class AssignUncertaintyLevel(bpy.types.Operator):
    bl_idname = "object.assign_uncertainty_level"
    bl_label = "Assign Uncertainty Level"

    level: bpy.props.IntProperty()

    def execute(self, context):
        
        scene = context.scene
        if self.level == 1:
            color_props = scene.ColorProperties1
        elif self.level == 2:
            color_props = scene.ColorProperties2
        elif self.level == 3:
            color_props = scene.ColorProperties3
        elif self.level == 4:
            color_props = scene.ColorProperties4
        elif self.level == 5:
            color_props = scene.ColorProperties5
        elif self.level == 6:
            color_props = scene.ColorProperties6
        elif self.level == 7:
            color_props = scene.ColorProperties7
        else:
            color_props = scene.ColorProperties8
        color = color_props.color
        
        assign_uncertainty_level(self.level, color)
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class ResetUncertaintyLevel(bpy.types.Operator):
    bl_idname = "object.reset_uncertainty_level"
    bl_label = "Reset Uncertainty Level"

    def execute(self, context):
        reset_uncertainty_level()
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class AssignRelevance(bpy.types.Operator):
    bl_idname = "object.assign_relevance"
    bl_label = "Assign Relevance"

    def execute(self, context):
        factor = context.scene.relevance_factor
        assign_relevance_factor(factor)
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class ResetRelevance(bpy.types.Operator):
    bl_idname = "object.reset_relevance"
    bl_label = "Reset Relevance"

    def execute(self, context):
        reset_relevance_factor()
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class CalculateVolume(bpy.types.Operator):
    bl_idname = "object.calculate_volume"
    bl_label = "Calculate Volume of selection"

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                calculate_volume(obj)
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class ResetVolume(bpy.types.Operator):
    bl_idname = "object.reset_volume"
    bl_label = "Reset Volume"

    def execute(self, context):
        reset_volume()
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class CalculateAUV(bpy.types.Operator):
    bl_idname = "object.calculate_au_v"
    bl_label = "Calculate AU_V"

    def execute(self, context):
        au_v = int(calculate_average_uncertainty())
        context.scene.au_v_result = f"{au_v:.2f}%"
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class CalculateAUVR(bpy.types.Operator):
    bl_idname = "object.calculate_au_vr"
    bl_label = "Calculate AU_VR"

    def execute(self, context):
        au_vr = int(calculate_average_uncertainty_with_relevance())
        context.scene.au_vr_result = f"{au_vr:.2f}%"
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class ResetColorsToDefaults(bpy.types.Operator):
    bl_idname = "object.reset_colors_to_defaults"
    bl_label = "Reset colors to defaults"

    def execute(self, context):
        
        color_map = {
            1: (1, 1, 1, 1),
            2: (0, 0, 1, 1),
            3: (0, 1, 1, 1),
            4: (0, 1, 0, 1),
            5: (1, 1, 0, 1),
            6: (1, 0.333, 0, 1),
            7: (1, 0, 0, 1),
            8: (0, 0, 0, 1)
        }
        
        context.scene.ColorProperties1.color = color_map[1]
        context.scene.ColorProperties2.color = color_map[2]
        context.scene.ColorProperties3.color = color_map[3]
        context.scene.ColorProperties4.color = color_map[4]
        context.scene.ColorProperties5.color = color_map[5]
        context.scene.ColorProperties6.color = color_map[6]
        context.scene.ColorProperties7.color = color_map[7]
        context.scene.ColorProperties8.color = color_map[8]
        
        return {'FINISHED'}
        
class SelectByUncertainty(bpy.types.Operator):
    bl_idname = "object.select_by_uncertainty"
    bl_label = "Select by Uncertainty"

    level: bpy.props.IntProperty()

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if "Uncertainty Level" in obj and obj["Uncertainty Level"] == self.level:
                obj.select_set(True)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ColorProperties)
    bpy.types.Scene.ColorProperties1 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.ColorProperties2 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.ColorProperties3 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.ColorProperties4 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.ColorProperties5 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.ColorProperties6 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.ColorProperties7 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.ColorProperties8 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.utils.register_class(UncertaintyPanel)
    bpy.utils.register_class(AssignUncertaintyLevel)
    bpy.utils.register_class(ResetUncertaintyLevel)
    bpy.utils.register_class(AssignRelevance)
    bpy.utils.register_class(ResetRelevance)
    bpy.utils.register_class(CalculateVolume)
    bpy.utils.register_class(ResetVolume)
    bpy.utils.register_class(CalculateAUV)
    bpy.utils.register_class(CalculateAUVR)
    bpy.utils.register_class(ResetColorsToDefaults)
    bpy.utils.register_class(SelectByUncertainty)
    
    bpy.types.Scene.relevance_factor = bpy.props.FloatProperty(
        name="Relevance Factor",
        description="Relevance Factor",
        default=1.0,
        min=0.01,
        max=100.0
    )
    bpy.types.Scene.au_v_result = bpy.props.StringProperty(
        name="AU_V Result",
        description="Result of AU_V Calculation",
        default="%"
    )
    bpy.types.Scene.au_vr_result = bpy.props.StringProperty(
        name="AU_VR Result",
        description="Result of AU_VR Calculation",
        default="%"
    )

def unregister():
    bpy.utils.unregister_class(ColorProperties)
    del bpy.types.Scene.ColorProperties1
    del bpy.types.Scene.ColorProperties2
    del bpy.types.Scene.ColorProperties3
    del bpy.types.Scene.ColorProperties4
    del bpy.types.Scene.ColorProperties5        
    del bpy.types.Scene.ColorProperties6         
    del bpy.types.Scene.ColorProperties7        
    del bpy.types.Scene.ColorProperties8
    bpy.utils.unregister_class(UncertaintyPanel)
    bpy.utils.unregister_class(AssignUncertaintyLevel)
    bpy.utils.unregister_class(ResetUncertaintyLevel)
    bpy.utils.unregister_class(AssignRelevance)
    bpy.utils.unregister_class(ResetRelevance)
    bpy.utils.unregister_class(CalculateVolume)
    bpy.utils.unregister_class(ResetVolume)
    bpy.utils.unregister_class(CalculateAUV)
    bpy.utils.unregister_class(CalculateAUVR)
    bpy.utils.unregister_class(ResetColorsToDefaults)
    bpy.utils.unregister_class(SelectByUncertainty)
    del bpy.types.Scene.relevance_factor
    del bpy.types.Scene.au_v_result
    del bpy.types.Scene.au_vr_result

if __name__ == "__main__":
    register()
