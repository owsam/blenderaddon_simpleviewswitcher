bl_info = {
    "name": "Simple View Switcher",
    "author": "Osamu Watanabe",
    "version": (1, 5),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Simple View Switcher Tab / Right Click Menu / Header",
    "description": "Switch views and toggle Wireframe / Face Orientation",
    "category": "3D View",
}

import bpy

# =========================
# Preferences
# =========================
class ViewSwitcherPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    use_icons: bpy.props.BoolProperty(
        name="Use Icons",
        description="Display icons instead of text in the header",
        default=True,
    )

    display_location: bpy.props.EnumProperty(
        name="Display Location",
        description="Where to show the view switcher buttons",
        items=[
            ('HEADER', "Header", "Show in the 3D View Header"),
            ('SIDEBAR', "Sidebar", "Show in the Sidebar Panel"),
            ('BOTH', "Both", "Show in both places"),
        ],
        default='HEADER'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "use_icons")
        layout.prop(self, "display_location")


# =========================
# Operators
# =========================
class VIEW3D_OT_toggle_wire(bpy.types.Operator):
    bl_idname = "view3d.toggle_wire"
    bl_label = "Toggle Wireframe"
    bl_description = "Toggle object wireframe display"

    def execute(self, context):
        obj = context.object
        if obj:
            obj.show_wire = not obj.show_wire
            obj.show_all_edges = obj.show_wire
        return {'FINISHED'}


class VIEW3D_OT_toggle_face_orientation(bpy.types.Operator):
    bl_idname = "view3d.toggle_face_orientation"
    bl_label = "Toggle Face Orientation"
    bl_description = "Toggle face orientation overlay"

    def execute(self, context):
        overlay = context.space_data.overlay
        overlay.show_face_orientation = not overlay.show_face_orientation
        return {'FINISHED'}


# =========================
# Sidebar Panel
# =========================
class VIEW3D_PT_ViewButtons(bpy.types.Panel):
    bl_label = "Simple View Switcher"
    bl_idname = "VIEW3D_PT_view_switcher"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simple View Switcher'

    @classmethod
    def poll(cls, context):
        prefs = bpy.context.preferences.addons[__name__].preferences
        return prefs.display_location in {'SIDEBAR', 'BOTH'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("view3d.view_axis", text="Front").type = 'FRONT'
        row = layout.row()
        row.operator("view3d.view_axis", text="Back").type = 'BACK'
        row = layout.row()
        row.operator("view3d.view_axis", text="Right").type = 'RIGHT'
        row = layout.row()
        row.operator("view3d.view_axis", text="Left").type = 'LEFT'
        row = layout.row()
        row.operator("view3d.view_axis", text="Top").type = 'TOP'
        row = layout.row()
        row.operator("view3d.view_axis", text="Bottom").type = 'BOTTOM'
        row = layout.row()
        row.operator("view3d.view_camera", text="Camera View")
        row = layout.row()
        row.operator("view3d.view_selected", text="Focus on Selection", icon="VIEWZOOM")

        layout.separator()

        obj = context.object
        icon_wire = "SHADING_WIRE" if obj and obj.show_wire else "SHADING_SOLID"
        layout.operator("view3d.toggle_wire", text="Wireframe", icon=icon_wire)

        overlay = context.space_data.overlay
        icon_face = "FACESEL" if overlay.show_face_orientation else "NORMALS_FACE"
        layout.operator("view3d.toggle_face_orientation", text="Face Orientation", icon=icon_face)


# =========================
# Right Click Menu
# =========================
class VIEW3D_MT_view_switcher_menu(bpy.types.Menu):
    bl_label = "Simple View Switcher"
    bl_idname = "VIEW3D_MT_view_switcher_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.view_axis", text="Front").type = 'FRONT'
        layout.operator("view3d.view_axis", text="Back").type = 'BACK'
        layout.operator("view3d.view_axis", text="Right").type = 'RIGHT'
        layout.operator("view3d.view_axis", text="Left").type = 'LEFT'
        layout.operator("view3d.view_axis", text="Top").type = 'TOP'
        layout.operator("view3d.view_axis", text="Bottom").type = 'BOTTOM'
        layout.operator("view3d.view_camera", text="Camera View")
        layout.operator("view3d.view_selected", text="Focus on Selection", icon="VIEWZOOM")
        layout.separator()
        layout.operator("view3d.toggle_wire", icon="SHADING_WIRE")
        layout.operator("view3d.toggle_face_orientation", icon="FACESEL")


def menu_func(self, context):
    self.layout.separator()
    self.layout.menu(VIEW3D_MT_view_switcher_menu.bl_idname)


# =========================
# Header
# =========================
def draw_view_switcher_in_header(self, context):
    prefs = bpy.context.preferences.addons[__name__].preferences
    if prefs.display_location not in {'HEADER', 'BOTH'}:
        return

    layout = self.layout
    layout.separator()
    row = layout.row(align=True)

    if prefs.use_icons:
        row.operator("view3d.view_axis", text="", icon='TRIA_UP').type = 'TOP'
        row.operator("view3d.view_axis", text="", icon='TRIA_LEFT').type = 'LEFT'
        row.operator("view3d.view_axis", text="", icon='TRIA_RIGHT').type = 'RIGHT'
        row.operator("view3d.view_axis", text="", icon='TRIA_DOWN').type = 'FRONT'
        row.operator("view3d.view_camera", text="", icon='CAMERA_DATA')
        row.operator("view3d.view_selected", text="", icon='VIEWZOOM')

        # Wire toggle
        obj = context.object
        icon_wire = "SHADING_WIRE" if obj and obj.show_wire else "SHADING_SOLID"
        row.operator("view3d.toggle_wire", text="", icon=icon_wire)

        # Face Orientation toggle
        overlay = context.space_data.overlay
        icon_face = "FACESEL" if overlay.show_face_orientation else "NORMALS_FACE"
        row.operator("view3d.toggle_face_orientation", text="", icon=icon_face)

    else:
        row.operator("view3d.toggle_wire", text="Wire")
        row.operator("view3d.toggle_face_orientation", text="Face")


# =========================
# Register
# =========================
classes = [
    ViewSwitcherPreferences,
    VIEW3D_OT_toggle_wire,
    VIEW3D_OT_toggle_face_orientation,
    VIEW3D_PT_ViewButtons,
    VIEW3D_MT_view_switcher_menu,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)
    bpy.types.VIEW3D_HT_header.append(draw_view_switcher_in_header)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    bpy.types.VIEW3D_HT_header.remove(draw_view_switcher_in_header)


if __name__ == "__main__":
    register()