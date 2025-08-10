import bpy  # type: ignore


class MakeLocalOperator(bpy.types.Operator):
    bl_idname = "bpotato.make_local"
    bl_label = "Make Local"
    bl_description = "Makes all objects local, removing links. This can help lock the version and make it shareable with others."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Select all objects
        bpy.ops.object.select_all(action="SELECT")
        # Make everything local
        bpy.ops.object.make_local(type="ALL")
        # Purge unused data
        bpy.ops.outliner.orphans_purge(
            do_local_ids=True, do_linked_ids=True, do_recursive=True
        )
        self.report({"INFO"}, "All objects and data made local.")
        return {"FINISHED"}
