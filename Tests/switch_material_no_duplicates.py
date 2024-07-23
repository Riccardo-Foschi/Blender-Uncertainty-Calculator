import bpy

class AssignMaterialOperator(bpy.types.Operator):
    bl_idname = "object.assign_material"
    bl_label = "Assign Material"
    
    material_name: bpy.props.StringProperty()
    material_color: bpy.props.FloatVectorProperty(size=4)  # 4-component vector for RGBA
    
    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected")
            return {'CANCELLED'}
        else:    
            mat = bpy.data.materials.get(self.material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=self.material_name)
        
            mat.use_nodes = True
            mat.use_fake_user = False
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf is None:
                bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")
            bsdf.inputs["Base Color"].default_value = self.material_color
            bsdf.inputs["Roughness"].default_value = 1.0
        
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
        
        return {'FINISHED'}


class AssignMaterialPanel(bpy.types.Panel):
    bl_label = "Assign Material Test"
    bl_idname = "OBJECT_PT_assign_material"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Assign Material Test"
    
    def draw(self, context):
        layout = self.layout
        
        black_op = layout.operator(AssignMaterialOperator.bl_idname, text="Assign Black Material")
        black_op.material_name = "BlackMaterial"
        black_op.material_color = (0.0, 0.0, 0.0, 1.0)
        
        red_op = layout.operator(AssignMaterialOperator.bl_idname, text="Assign Red Material")
        red_op.material_name = "RedMaterial"
        red_op.material_color = (1.0, 0.0, 0.0, 1.0)


def register():
    bpy.utils.register_class(AssignMaterialOperator)
    bpy.utils.register_class(AssignMaterialPanel)


def unregister():
    bpy.utils.unregister_class(AssignMaterialOperator)
    bpy.utils.unregister_class(AssignMaterialPanel)


if __name__ == "__main__":
    register()
