bl_info = {
    "name": "Simple View Switcher",
    "author": "Osamu Watanabe",
    "version": (1, 4),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Simple View Switcher Tab / Header",
    "description": "Switch views and toggle wire display.",
    "category": "3D View",
}

import bpy


# ----------------------------
# Preferences
# ----------------------------
class ViewSwitcherPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    use_icons: bpy.props.BoolProperty(
        name="Use Icons",
        default=True,
    )

    display_location: bpy.props.EnumProperty(
        name="Display Location",
        items=[
            ('HEADER', "Header", ""),
            ('SIDEBAR', "Sidebar", ""),
            ('BOTH', "Both", ""),
        ],
        default='HEADER'
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "use_icons")
        layout.prop(self, "display_location")


# ----------------------------
# Wire Toggle Operator
# ----------------------------
class VIEW3D_OT_toggle_wire(bpy.types.Operator):
    bl_idname = "view3d.toggle_wire"
    bl_label = "Toggle Wire"
    bl_description = "Toggle Wireframe Overlay on selected object"

    def execute(self, context):

        obj = context.object

        if obj is None:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}

        obj.show_wire = not obj.show_wire
        obj.show_all_edges = obj.show_wire

        return {'FINISHED'}


# ----------------------------
# Sidebar Panel
# ----------------------------
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

        layout.label(text="View")

        layout.operator("view3d.view_axis", text="Front").type = 'FRONT'
        layout.operator("view3d.view_axis", text="Back").type = 'BACK'
        layout.operator("view3d.view_axis", text="Right").type = 'RIGHT'
        layout.operator("view3d.view_axis", text="Left").type = 'LEFT'
        layout.operator("view3d.view_axis", text="Top").type = 'TOP'
        layout.operator("view3d.view_axis", text="Bottom").type = 'BOTTOM'

        layout.separator()

        layout.operator("view3d.view_camera", text="Camera View")
        layout.operator("view3d.view_selected", text="Focus", icon="VIEWZOOM")

        layout.separator()

        # Wire Toggle Button
        obj = context.object

        if obj and obj.show_wire:
            layout.operator("view3d.toggle_wire",
                            text="Wire OFF",
                            icon="SHADING_WIRE")
        else:
            layout.operator("view3d.toggle_wire",
                            text="Wire ON",
                            icon="SHADING_SOLID")


# ----------------------------
# Context Menu
# ----------------------------
class VIEW3D_MT_view_switcher_menu(bpy.types.Menu):
    bl_label = "Simple View Switcher"
    bl_idname = "VIEW3D_MT_view_switcher_menu"

    def draw(self, context):

        layout = self.layout

        layout.operator("view3d.toggle_wire",
                        icon="SHADING_SOLID")


def menu_func(self, context):

    self.layout.separator()
    self.layout.menu(VIEW3D_MT_view_switcher_menu.bl_idname)


# ----------------------------
# Header
# ----------------------------
def draw_view_switcher_in_header(self, context):

    prefs = bpy.context.preferences.addons[__name__].preferences

    if prefs.display_location not in {'HEADER', 'BOTH'}:
        return

    layout = self.layout

    layout.separator()

    row = layout.row(align=True)

    prefs = bpy.context.preferences.addons[__name__].preferences

    if prefs.use_icons:

        row.operator("view3d.view_axis", text="", icon='TRIA_UP').type = 'TOP'
        row.operator("view3d.view_axis", text="", icon='TRIA_LEFT').type = 'LEFT'
        row.operator("view3d.view_axis", text="", icon='TRIA_RIGHT').type = 'RIGHT'
        row.operator("view3d.view_axis", text="", icon='TRIA_DOWN').type = 'FRONT'

        row.operator("view3d.view_camera",
                     text="",
                     icon='CAMERA_DATA')

        row.operator("view3d.view_selected",
                     text="",
                     icon='VIEWZOOM')

        # Wire icon toggle

        obj = context.object

        if obj and obj.show_wire:
            row.operator("view3d.toggle_wire",
                         text="",
                         icon="SHADING_SOLID")
        else:
            row.operator("view3d.toggle_wire",
                         text="",
                         icon="SHADING_WIRE")

    else:

        row.operator("view3d.toggle_wire",
                     text="Wire Toggle")


# ----------------------------
# Register
# ----------------------------
classes = [

    ViewSwitcherPreferences,
    VIEW3D_OT_toggle_wire,
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