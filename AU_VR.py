bl_info = {
    "name": "Uncertainty quantification",
    "blender": (2, 80, 0),
    "Location": "Side panel (N shortcut) > Uncertainty",
    "category": "Model Analysis",
    "author": "Riccardo Foschi and Chat GPT",
    "description": "Allows to calculate the average uncertainty weighted with the volume (AU_V) and the average uncertainty weighted with the volume and relevance (AU_VR) for hypothetical 3D architectural reconstruction models",
    "version": (1, 8, 0),
}




import bpy
import bmesh
from mathutils import Vector
from bpy.props import FloatVectorProperty
from bpy.types import Panel, PropertyGroup


# Definisci un nuovo PropertyGroup per il colore
class ColorProperties(PropertyGroup):
    color1: FloatVectorProperty(
        name="Color 1",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(1.0, 1.0, 1.0, 1.0) # white color with alpha
    )
    color2: FloatVectorProperty(
        name="Color 2",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(0.0, 0.0, 1.0, 1.0) # blue color with alpha
    )
    color3: FloatVectorProperty(
        name="Color 3",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(0.0, 1.0, 1.0, 1.0) # cyan color with alpha
    )
    color4: FloatVectorProperty(
        name="Color 4",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(0.0, 1.0, 0.0, 1.0) # green color with alpha
    )
    color5: FloatVectorProperty(
        name="Color 5",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(1.0, 1.0, 0.0, 1.0) # yellow color with alpha
    )
    color6: FloatVectorProperty(
        name="Color 6",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(1.0, 0.333, 0.0, 1.0) # orange color with alpha
    )
    color7: FloatVectorProperty(
        name="Color 7",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(1.0, 0.0, 0.0, 1.0) # red color with alpha
    )     
    color8: FloatVectorProperty(
        name="Color 8",
        subtype='COLOR',
        min=0.0, max=1.0,
        size=4,
        default=(0.0, 0.0, 0.0, 1.0) # black color with alpha
    )   



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

def assign_uncertainty_level(level):
    color_map = {
        1: (1, 1, 1, 1),
        2: (0, 0, 1, 1),
        3: (0, 1, 1, 1),
        4: (0, 1, 0, 1),
        5: (1, 1, 0, 1),
        6: (1, 0.333, 0, 1),
        7: (1, 0, 0, 1)
    }

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
            obj["Uncertainty Level"] = level
            obj["Uncertainty Percentage"] = percentage_map[level]
            update_material(obj, color_map[level])
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














    
def apply_scale_selection():
    for obj in bpy.context.selected_objects:
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.context.view_layer.update()
    return {'Scale applied'}


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



class AssignUncertaintyLevel(bpy.types.Operator):
    bl_idname = "object.assign_uncertainty_level"
    bl_label = "Assign Uncertainty Level"

    level: bpy.props.IntProperty()

    def execute(self, context):
        assign_uncertainty_level(self.level)
        
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












class ApplyScaleSelection(bpy.types.Operator):
    bl_idname = "object.apply_scale_selection"
    bl_label = "Apply Scale to Selection"
    

    def execute(self, context):
        apply_scale_selection()
        
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
        au_v = calculate_average_uncertainty()
        context.scene.au_v_result = f"{au_v:.2f}%"
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class CalculateAUVR(bpy.types.Operator):
    bl_idname = "object.calculate_au_vr"
    bl_label = "Calculate AU_VR"

    def execute(self, context):
        au_vr = calculate_average_uncertainty_with_relevance()
        context.scene.au_vr_result = f"{au_vr:.2f}%"
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
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
    
    
    
    
    
    
    
    
    
    
    

class Assign(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Uncertainty'
    bl_label = "Assign"


    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Create Box 1
        box1 = layout.box()
        box1.label(text="Assign Uncertainty level!!2")
                       
        row = box1.row(align=True)
        row.prop(scene.color_props, "color1", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.assign_uncertainty_level", text="Assign Uncertainty 1").level = 1      

        
        row = box1.row(align=True)
        row.prop(scene.color_props, "color2", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.assign_uncertainty_level", text="Assign Uncertainty 2").level = 2   
        
        row = box1.row(align=True)
        row.prop(scene.color_props, "color3", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.assign_uncertainty_level", text="Assign Uncertainty 3").level = 3      

        
        row = box1.row(align=True)
        row.prop(scene.color_props, "color4", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.assign_uncertainty_level", text="Assign Uncertainty 4").level = 4              
        
        row = box1.row(align=True)
        row.prop(scene.color_props, "color5", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.assign_uncertainty_level", text="Assign Uncertainty 5").level = 5   
        
        row = box1.row(align=True)
        row.prop(scene.color_props, "color6", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.assign_uncertainty_level", text="Assign Uncertainty 6").level = 6      

        
        row = box1.row(align=True)
        row.prop(scene.color_props, "color7", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.assign_uncertainty_level", text="Assign Uncertainty 7").level = 7               
            

        row = box1.row(align=True)
        row.prop(scene.color_props, "color8", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.reset_uncertainty_level", text="Reset / Abstention") 

        # Create Box 2
        box2 = layout.box()
        box2.label(text="Assign Relevance Factor")
        
        row = box2.column()
        row.prop(context.scene, "relevance_factor", text="")
        row.operator("object.assign_relevance", text="Assign Relevance")
        
        row = box2.row()
        row.operator("object.reset_relevance", text="Reset Relevance")
        
        
        
class Calculate(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Uncertainty'
    bl_label = "Calculate"


    def draw(self, context):
        layout = self.layout
        scene = context.scene   
        
        # Create Box 1
        box1 = layout.box()
        box1.label(text="Calculate Volume")


        row = box1.column()
        row.operator("object.apply_scale_selection", text="Apply Scale of Selection")

        row.operator("object.calculate_volume", text="Calculate Volume of selection")

        row = box1.column()
        row.operator("object.reset_volume", text="Reset Volume")



        # Create Box 2
        box2 = layout.box()
        box2.label(text="Calculate Average Uncertainty")


        row = box2.column()
        row.operator("object.calculate_au_v", text="Calculate AU_V")

        row.prop(context.scene, "au_v_result", text="AU_V")
        
        row = box2.column()
        row.operator("object.calculate_au_vr", text="Calculate AU_VR")

        row.prop(context.scene, "au_vr_result", text="AU_VR")
        
        
        
        
class Select(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Uncertainty'
    bl_label = "Select"


    def draw(self, context):
        layout = self.layout
        scene = context.scene 
                  
        # Create Box 1
        box1 = layout.box()
        box1.label(text="Select by Uncertainty")
                       
        row = box1.row(align=True)
        for i in range(1, 8):

            row.operator("object.select_by_uncertainty", text=str(i)).level = i



def register():
    bpy.utils.register_class(ColorProperties)
    bpy.types.Scene.color_props = bpy.props.PointerProperty(type=ColorProperties)
    
    bpy.utils.register_class(Assign)
    bpy.utils.register_class(Calculate)
    bpy.utils.register_class(Select)
    
    bpy.utils.register_class(AssignUncertaintyLevel)
    bpy.utils.register_class(ResetUncertaintyLevel)
    bpy.utils.register_class(AssignRelevance)
    bpy.utils.register_class(ResetRelevance)

    bpy.utils.register_class(ApplyScaleSelection)
    
    bpy.utils.register_class(CalculateVolume)
    bpy.utils.register_class(ResetVolume)
    bpy.utils.register_class(CalculateAUV)
    bpy.utils.register_class(CalculateAUVR)
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
    del bpy.types.Scene.color_props
    
    bpy.utils.unregister_class(Assign)
    bpy.utils.unregister_class(Calculate)    
    bpy.utils.unregister_class(Select)
        
    bpy.utils.unregister_class(AssignUncertaintyLevel)
    bpy.utils.unregister_class(ResetUncertaintyLevel)
    bpy.utils.unregister_class(AssignRelevance)
    bpy.utils.unregister_class(ResetRelevance)

    bpy.utils.unregister_class(ApplyScaleSelection)    
        
    bpy.utils.unregister_class(CalculateVolume)
    bpy.utils.unregister_class(ResetVolume)
    bpy.utils.unregister_class(CalculateAUV)
    bpy.utils.unregister_class(CalculateAUVR)
    bpy.utils.unregister_class(SelectByUncertainty)
    
    del bpy.types.Scene.relevance_factor
    del bpy.types.Scene.au_v_result
    del bpy.types.Scene.au_vr_result

if __name__ == "__main__":
    register()
