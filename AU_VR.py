bl_info = {
    "name": "Uncertainty quantification",
    "blender": (2, 80, 0),
    "Location": "Side panel (N shortcut) > Uncertainty",
    "category": "Model Analysis",
    "author": "Riccardo Foschi and Chat GPT",
    "description": "Allows to calculate the average uncertainty weighted with the volume (AU_V) and the average uncertainty weighted with the volume and relevance (AU_VR) for hypothetical 3D architectural reconstruction models",
    "version": (2, 2, 5),
}

import bpy
import bmesh
from bpy.props import FloatVectorProperty
from mathutils import Vector
from bpy.props import FloatVectorProperty
from bpy.types import Panel, PropertyGroup


#region Color

def execute_reset_colors():
    bpy.ops.object.reset_colors_to_defaults()
    return None  # Stop the timer 

def update_material(self, context):
    color1 = self.color1
    color2 = self.color2
    color3 = self.color3
    color4 = self.color4
    color5 = self.color5
    color6 = self.color6
    color7 = self.color7
    color8 = self.color8

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

    # Controlla se esiste già un materiale chiamato "CustomMaterial3"
    mat3 = bpy.data.materials.get("CustomMaterial3")
    bsdf3 = mat3.node_tree.nodes.get("Principled BSDF")
    if bsdf3:
        bsdf3.inputs['Base Color'].default_value = (color3[0], color3[1], color3[2], 1)
        bsdf3.inputs['Roughness'].default_value = 1.0

    # Controlla se esiste già un materiale chiamato "CustomMaterial4"
    mat4 = bpy.data.materials.get("CustomMaterial4")
    bsdf4 = mat4.node_tree.nodes.get("Principled BSDF")
    if bsdf4:
        bsdf4.inputs['Base Color'].default_value = (color4[0], color4[1], color4[2], 1)
        bsdf4.inputs['Roughness'].default_value = 1.0

    # Controlla se esiste già un materiale chiamato "CustomMaterial5"
    mat5 = bpy.data.materials.get("CustomMaterial5")
    bsdf5 = mat5.node_tree.nodes.get("Principled BSDF")
    if bsdf5:
        bsdf5.inputs['Base Color'].default_value = (color5[0], color5[1], color5[2], 1)
        bsdf5.inputs['Roughness'].default_value = 1.0

    # Controlla se esiste già un materiale chiamato "CustomMaterial6"
    mat6 = bpy.data.materials.get("CustomMaterial6")
    bsdf6 = mat6.node_tree.nodes.get("Principled BSDF")
    if bsdf6:
        bsdf6.inputs['Base Color'].default_value = (color6[0], color6[1], color6[2], 1)
        bsdf6.inputs['Roughness'].default_value = 1.0

    # Controlla se esiste già un materiale chiamato "CustomMaterial7"
    mat7 = bpy.data.materials.get("CustomMaterial7")
    bsdf7 = mat7.node_tree.nodes.get("Principled BSDF")
    if bsdf7:
        bsdf7.inputs['Base Color'].default_value = (color7[0], color7[1], color7[2], 1)
        bsdf7.inputs['Roughness'].default_value = 1.0

    # Controlla se esiste già un materiale chiamato "CustomMaterial8"
    mat8 = bpy.data.materials.get("CustomMaterial8")
    bsdf8 = mat8.node_tree.nodes.get("Principled BSDF")
    if bsdf8:
        bsdf8.inputs['Base Color'].default_value = (color8[0], color8[1], color8[2], 1)
        bsdf8.inputs['Roughness'].default_value = 1.0

def assign_uncertainty_level(level):            
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
    return {'FINISHED'}

    bpy.context.view_layer.update()

def reset_uncertainty_level():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            if "Uncertainty Level" in obj:
                del obj["Uncertainty Level"]
            if "Uncertainty Percentage" in obj:
                del obj["Uncertainty Percentage"]
    bpy.context.view_layer.update() 

class ResetColorsToDefaults(bpy.types.Operator):
    bl_idname = "object.reset_colors_to_defaults"
    bl_label = "Reset colors to defaults"

    def execute(self, context):
        
        color_map = {
            1: (1, 1, 1),
            2: (0, 0, 1),
            3: (0, 1, 1),
            4: (0, 1, 0),
            5: (1, 1, 0),
            6: (1, 0.333, 0),
            7: (1, 0, 0),
            8: (0, 0, 0)
        }
        
        context.scene.my_tool.color1 = color_map[1]
        context.scene.my_tool.color2 = color_map[2]
        context.scene.my_tool.color3 = color_map[3]
        context.scene.my_tool.color4 = color_map[4]
        context.scene.my_tool.color5 = color_map[5]
        context.scene.my_tool.color6 = color_map[6]
        context.scene.my_tool.color7 = color_map[7]
        context.scene.my_tool.color8 = color_map[8]
        
        return {'FINISHED'}

class SimpleOperator1(bpy.types.Operator):
    bl_idname = "object.apply_material1"
    bl_label = "Apply Material 1"
            
    def execute(self, context):
        selected_objects = context.selected_objects
        color = context.scene.my_tool.color1
        
        # Controlla se esiste già un materiale chiamato "CustomMaterial1"
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
            assign_uncertainty_level(1)                
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
            assign_uncertainty_level(2)        
        return {'FINISHED'}

class SimpleOperator3(bpy.types.Operator):
    bl_idname = "object.apply_material3"
    bl_label = "Apply Material 3"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        color = context.scene.my_tool.color3
        
        # Controlla se esiste già un materiale chiamato "CustomMaterial3"
        mat = bpy.data.materials.get("CustomMaterial3")
        if mat is None:
            mat = bpy.data.materials.new(name="CustomMaterial3")
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
            assign_uncertainty_level(3)          
        return {'FINISHED'}

class SimpleOperator4(bpy.types.Operator):
    bl_idname = "object.apply_material4"
    bl_label = "Apply Material 4"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        color = context.scene.my_tool.color4

        
        # Controlla se esiste già un materiale chiamato "CustomMaterial4"
        mat = bpy.data.materials.get("CustomMaterial4")
        if mat is None:
            mat = bpy.data.materials.new(name="CustomMaterial4")
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
            assign_uncertainty_level(4)          
        return {'FINISHED'}

class SimpleOperator5(bpy.types.Operator):
    bl_idname = "object.apply_material5"
    bl_label = "Apply Material 5"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        color = context.scene.my_tool.color5
        
        # Controlla se esiste già un materiale chiamato "CustomMaterial5"
        mat = bpy.data.materials.get("CustomMaterial5")
        if mat is None:
            mat = bpy.data.materials.new(name="CustomMaterial5")
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
            assign_uncertainty_level(5)          
        return {'FINISHED'}

class SimpleOperator6(bpy.types.Operator):
    bl_idname = "object.apply_material6"
    bl_label = "Apply Material 6"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        color = context.scene.my_tool.color6

        
        # Controlla se esiste già un materiale chiamato "CustomMaterial6"
        mat = bpy.data.materials.get("CustomMaterial6")
        if mat is None:
            mat = bpy.data.materials.new(name="CustomMaterial6")
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
            assign_uncertainty_level(6)          
        return {'FINISHED'}

class SimpleOperator7(bpy.types.Operator):
    bl_idname = "object.apply_material7"
    bl_label = "Apply Material 7"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        color = context.scene.my_tool.color7
        
        # Controlla se esiste già un materiale chiamato "CustomMaterial7"
        mat = bpy.data.materials.get("CustomMaterial7")
        if mat is None:
            mat = bpy.data.materials.new(name="CustomMaterial7")
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
            assign_uncertainty_level(7)          
        return {'FINISHED'}

class SimpleOperator8(bpy.types.Operator):
    bl_idname = "object.apply_material8"
    bl_label = "Apply Material 8"
    
    def execute(self, context):
        selected_objects = context.selected_objects
        color = context.scene.my_tool.color8

        
        # Controlla se esiste già un materiale chiamato "CustomMaterial8"
        mat = bpy.data.materials.get("CustomMaterial8")
        if mat is None:
            mat = bpy.data.materials.new(name="CustomMaterial8")
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
            reset_uncertainty_level()          
        return {'FINISHED'}

class ColorProperties(bpy.types.PropertyGroup):
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
    color3: FloatVectorProperty(
        name="Color Picker 3",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        update=update_material,
        description="Choose a color"
    )
    
    color4: FloatVectorProperty(
        name="Color Picker 4",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        update=update_material,
        description="Choose a color"
    )   
    color5: FloatVectorProperty(
        name="Color Picker 5",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        update=update_material,
        description="Choose a color"
    )
    
    color6: FloatVectorProperty(
        name="Color Picker 6",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        update=update_material,
        description="Choose a color"
    )
    color7: FloatVectorProperty(
        name="Color Picker 7",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        update=update_material,
        description="Choose a color"
    )
    
    color8: FloatVectorProperty(
        name="Color Picker 8",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
        update=update_material,
        description="Choose a color"
    ) 

#endregion


#region Relevance

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

#endregion


#region Calculate volume

def apply_scale_selection(self): 
    if bpy.context.selected_objects:
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        self.report({'INFO'}, "Scale correctly applied")                
    else:
        self.report({'ERROR'}, "No object selected")
    return

def calculate_volume(obj, self):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    volume = bm.calc_volume(signed=True)
    bm.free()
    obj["Volume"] = volume
    self.report({'INFO'}, "Volume correctly calculated")    
    bpy.context.view_layer.update()
    return

def reset_volume():
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            if "Volume" in obj:
                del obj["Volume"]
    bpy.context.view_layer.update()

class ApplyScaleSelection(bpy.types.Operator):
    bl_idname = "object.apply_scale_selection"
    bl_label = "Apply Scale of Selection"

    def execute(self, context):
        apply_scale_selection(self)
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class CalculateVolume(bpy.types.Operator):
    bl_idname = "object.calculate_volume"
    bl_label = "Calculate Volume of selection"

    def execute(self, context):
        if bpy.context.selected_objects:     
            for obj in bpy.context.selected_objects:
                if obj.type == 'MESH':
                    calculate_volume(obj, self)           
        else:
            self.report({'ERROR'}, "No object selected")
                
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class ResetVolume(bpy.types.Operator):
    bl_idname = "object.reset_volume"
    bl_label = "Reset Volume"

    def execute(self, context):
        if bpy.context.selected_objects:  
            reset_volume()
        
        else:            
            self.report({'ERROR'}, "No object selected")
            
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

#endregion

#region Calculate AU_V and AU_VR
   
#def calculate AU_V and AU_VR

def calculate_average_uncertainty(self):
    total_volume = 0
    weighted_sum = 0

    for obj in bpy.data.objects:

        if obj.type == 'MESH':          
            if "Uncertainty Level" in obj and "Volume" not in obj:
                self.report({'ERROR'}, "Calculate volume of all objects first")
                au_v = 0
                return au_v

            elif "Uncertainty Level" in obj and "Volume" in obj:
                volume = obj["Volume"]
                uncertainty_percentage = obj["Uncertainty Percentage"]
                weighted_sum += volume * uncertainty_percentage
                total_volume += volume

    if total_volume == 0:
        return 0

    au_v = weighted_sum / total_volume
    return au_v

def calculate_average_uncertainty_with_relevance(self):
    total_volume = 0
    weighted_sum = 0

    for obj in bpy.data.objects:

        if obj.type == 'MESH':
            if "Uncertainty Level" in obj and "Volume" not in obj:
                self.report({'ERROR'}, "Calculate volume of all objects first")
                au_vr = 0
                return au_vr
            
            elif "Uncertainty Level" in obj and "Volume" in obj: 
                volume = obj["Volume"]
                uncertainty_percentage = obj["Uncertainty Percentage"]
                relevance_factor = obj.get("Relevance", 1)
                weighted_sum += volume * uncertainty_percentage * relevance_factor
                total_volume += volume * relevance_factor
                
    if total_volume == 0:
        return 0

    au_vr = weighted_sum / total_volume
    return au_vr

class CalculateAUV(bpy.types.Operator):
    bl_idname = "object.calculate_au_v"
    bl_label = "Calculate AU_V"

    def execute(self, context):    
        au_v = calculate_average_uncertainty(self)
        context.scene.au_v_result = f"{au_v:.2f}%"

        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'}

class CalculateAUVR(bpy.types.Operator):
    bl_idname = "object.calculate_au_vr"
    bl_label = "Calculate AU_VR"

    def execute(self, context):
        au_vr = calculate_average_uncertainty_with_relevance(self)
        context.scene.au_vr_result = f"{au_vr:.2f}%"
        
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        return {'FINISHED'} 

#endregion


#region Select

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

#endregion

#region Draw assign panel

class Assign(bpy.types.Panel):
    bl_label = "Assign"
    bl_idname = "OBJECT_PT_test"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Uncertainty"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        box1 = layout.box()
        box1.label(text="Assign Uncertainty level") 

        row = box1.row(align=True)
        row.prop(mytool, "color1", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.apply_material1", text="Uncertainty 1")

        row = box1.row(align=True)
        row.prop(mytool, "color2", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.apply_material2", text="Uncertainty 2")

        row = box1.row(align=True)
        row.prop(mytool, "color3", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.apply_material3", text="Uncertainty 3")

        row = box1.row(align=True)
        row.prop(mytool, "color4", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.apply_material4", text="Uncertainty 4")

        row = box1.row(align=True)
        row.prop(mytool, "color5", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.apply_material5", text="Uncertainty 5")

        row = box1.row(align=True)
        row.prop(mytool, "color6", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.apply_material6", text="Uncertainty 6")

        row = box1.row(align=True)
        row.prop(mytool, "color7", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.apply_material7", text="Uncertainty 7")

        row = box1.row(align=True)
        row.prop(mytool, "color8", text="")
        sub = row.row()
        sub.scale_x = 2.0
        sub.operator("object.apply_material8", text="Abstention")  
        
        row = box1.row()
        
        row = box1.row(align=True)        
        row.operator("object.reset_colors_to_defaults", text="Reset default colours")  

        box2 = layout.box()
        box2.label(text="Assign Relevance Factor")
        
        row = box2.row(align=True)
        row.prop(context.scene, "relevance_factor", text="")
        sub = row.row()
        sub.scale_x = 1.5
        sub.operator("object.assign_relevance", text="Assign Relevance") 
                        
        row = box2.row()
        row.operator("object.reset_relevance", text="Remove Relevance from Selection")

#endregion


#region Draw calculate panel

class Calculate(bpy.types.Panel):
    bl_label = "Calculate"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Uncertainty"
    

    def draw(self, context):
        layout = self.layout
        scene = context.scene        

        # Create Box 1
        box1 = layout.box()
        box1.label(text="Calculate Volume")

        row = box1.column()
        row.operator("object.apply_scale_selection", text="Apply Scale")

        row.operator("object.calculate_volume", text="Calculate Volume")

        row = box1.column()
        row.operator("object.reset_volume", text="Remove Volume Property")     
        
        
        # Create Box 2
        box2 = layout.box()
        box2.label(text="Calculate Average Uncertainty")


        row = box2.column()
        row.operator("object.calculate_au_v", text="Calculate AU_V")
        row.prop(context.scene, "au_v_result", text="AU_V")
        
        row = box2.column()
        row.operator("object.calculate_au_vr", text="Calculate AU_VR")
        row.prop(context.scene, "au_vr_result", text="AU_VR")

#endregion


#region Draw select panel
  
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

#endregion
 
#region register & unregister

def register():
    
    bpy.utils.register_class(Assign)
    bpy.utils.register_class(Calculate)
    bpy.utils.register_class(Select)
        
#region Color
    bpy.utils.register_class(SimpleOperator1)
    bpy.utils.register_class(SimpleOperator2)
    bpy.utils.register_class(SimpleOperator3)
    bpy.utils.register_class(SimpleOperator4)
    bpy.utils.register_class(SimpleOperator5)
    bpy.utils.register_class(SimpleOperator6)
    bpy.utils.register_class(SimpleOperator7)
    bpy.utils.register_class(SimpleOperator8)  
    bpy.utils.register_class(ResetColorsToDefaults) 
    bpy.utils.register_class(ColorProperties)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.color1 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.color2 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.color3 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.color4 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.color5 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.color6 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.color7 = bpy.props.PointerProperty(type=ColorProperties)
    bpy.types.Scene.color8 = bpy.props.PointerProperty(type=ColorProperties)
    #Reset colours at startup
    bpy.app.timers.register(execute_reset_colors, first_interval=0.1)
#endregion
    
#region Relevance   
    bpy.utils.register_class(AssignRelevance)
    bpy.utils.register_class(ResetRelevance)
    bpy.types.Scene.relevance_factor = bpy.props.FloatProperty(
    name="Relevance Factor",
    description="Relevance Factor",
    default=1.0,
    min=0.01,
    max=100.0
    )
#endregion
    
    
#region Volume
    bpy.utils.register_class(ApplyScaleSelection)
    bpy.utils.register_class(CalculateVolume)
    bpy.utils.register_class(ResetVolume)    
#endregion

#region AU_V & AU_VR
    bpy.utils.register_class(CalculateAUV)
    bpy.utils.register_class(CalculateAUVR)
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
#endregion


#region Select by uncertainty
    bpy.utils.register_class(SelectByUncertainty)
#endregion
       
def unregister():
    
    bpy.utils.unregister_class(Assign)
    bpy.utils.unregister_class(Calculate)
    bpy.utils.unregister_class(Select) 
    
#region Color
    bpy.utils.unregister_class(SimpleOperator1)
    bpy.utils.unregister_class(SimpleOperator2)
    bpy.utils.unregister_class(SimpleOperator3)
    bpy.utils.unregister_class(SimpleOperator4)
    bpy.utils.unregister_class(SimpleOperator5)
    bpy.utils.unregister_class(SimpleOperator6)
    bpy.utils.unregister_class(SimpleOperator7)
    bpy.utils.unregister_class(SimpleOperator8)
    del bpy.types.Scene.my_tool
    bpy.utils.unregister_class(ResetColorsToDefaults)
    bpy.utils.unregister_class(ColorProperties)
    del bpy.types.Scene.color1
    del bpy.types.Scene.color2
    del bpy.types.Scene.color3
    del bpy.types.Scene.color4
    del bpy.types.Scene.color5        
    del bpy.types.Scene.color6         
    del bpy.types.Scene.color7        
    del bpy.types.Scene.color8  
#endregion
    
    
#region Relevance
    bpy.utils.unregister_class(AssignRelevance)
    bpy.utils.unregister_class(ResetRelevance)
    del bpy.types.Scene.relevance_factor
#endregion
    
      
#region Volume
    bpy.utils.unregister_class(ApplyScaleSelection)  
    bpy.utils.unregister_class(CalculateVolume)
    bpy.utils.unregister_class(ResetVolume)    
#endregion
    
    
#region AU_V & AU_VR
    bpy.utils.unregister_class(CalculateAUV)
    bpy.utils.unregister_class(CalculateAUVR)
    del bpy.types.Scene.au_v_result
    del bpy.types.Scene.au_vr_result
#endregion


#region Select by uncertainty
    bpy.utils.unregister_class(SelectByUncertainty)
#endregion

#endregion
         
if __name__ == "__main__":
    register()
