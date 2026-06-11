# Geometry node library package.
#
# Ships the compiled geometry node groups as binary assets rather than Python:
#   library.blend  — every geometry node group, written by the NodeCompiler
#   hashes.json    — { group_name: md5_hex } manifest for change detection
#
# loader.init_geometry_nodes() appends those groups into the open file on demand.
# Unlike shader/, this package is NOT scanned by NodeLib — geometry groups are
# appended as modifier node-trees, not registered as Add-Shader menu entries.
