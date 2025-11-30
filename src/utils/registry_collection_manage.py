"""
Helper functions for LSRegistry collection management
This is part of the operators.py but separated here for clarity
"""

import bpy


def get_or_create_collection(name, parent=None):
    """
    Get existing collection or create new one
    
    Args:
        name: Collection name
        parent: Parent collection (None for scene root)
    
    Returns:
        Collection object
    """
    # Check if collection exists
    if name in bpy.data.collections:
        collection = bpy.data.collections[name]
        
        # Ensure it's linked to the correct parent
        if parent:
            if collection.name not in [c.name for c in parent.children]:
                parent.children.link(collection)
        else:
            if collection.name not in [c.name for c in bpy.context.scene.collection.children]:
                bpy.context.scene.collection.children.link(collection)
    else:
        # Create new collection
        collection = bpy.data.collections.new(name)
        
        # Link to parent or scene
        if parent:
            parent.children.link(collection)
        else:
            bpy.context.scene.collection.children.link(collection)
    
    return collection


def format_collection_name(namespace, version):
    """
    Format namespace and version into collection name
    
    Args:
        namespace: e.g., "io.github.lvoxx.world-builder"
        version: e.g., "dummy" or "1.0.0"
    
    Returns:
        Collection name: e.g., "io-github-lvoxx-world-builder-dummy"
    """
    return f"{namespace.replace('.', '-')}-{version}"


def parse_collection_name(collection_name):
    """
    Parse collection name back to namespace and version
    
    Args:
        collection_name: e.g., "io-github-lvoxx-world-builder-dummy"
    
    Returns:
        tuple: (namespace, version) or (None, None) if invalid
        e.g., ("io.github.lvoxx.world-builder", "dummy")
    """
    # Split by last dash to get version
    parts = collection_name.rsplit('-', 1)
    
    if len(parts) != 2:
        return None, None
    
    namespace_part, version = parts
    
    # Convert namespace back (hyphens to dots)
    # But we need to be smart about it - only convert the domain-like parts
    # Pattern: io-github-username-repo -> io.github.username.repo
    namespace = namespace_part.replace('-', '.')
    
    return namespace, version


def remove_broken_links_from_collection(collection):
    """
    Remove broken library links from a specific collection
    
    Args:
        collection: Blender collection object
    """
    from pathlib import Path
    
    objects_to_remove = []
    
    for obj in collection.objects:
        if obj.library:
            lib_path = bpy.path.abspath(obj.library.filepath)
            if not Path(lib_path).exists():
                objects_to_remove.append(obj)
    
    for obj in objects_to_remove:
        try:
            bpy.data.objects.remove(obj)
            print(f"Removed broken link: {obj.name}")
        except Exception as e:
            print(f"Failed to remove {obj.name}: {e}")


def get_all_registry_collections():
    """
    Get all registry collections from LSRegistry
    
    Returns:
        list: List of dicts with collection info
        [
            {
                'collection': bpy.types.Collection,
                'name': str,
                'namespace': str,
                'version': str
            },
            ...
        ]
    """
    if "LSRegistry" not in bpy.data.collections:
        return []
    
    lsregistry_col = bpy.data.collections["LSRegistry"]
    registries = []
    
    for child_col in lsregistry_col.children:
        namespace, version = parse_collection_name(child_col.name)
        
        if namespace and version:
            registries.append({
                'collection': child_col,
                'name': child_col.name,
                'namespace': namespace,
                'version': version
            })
    
    return registries


# Example usage in operators:
"""
# In LSREGISTRY_OT_get.link_objects():
from .collection_helpers import get_or_create_collection, format_collection_name

# Create collection structure
lsregistry_col = get_or_create_collection("LSRegistry", None)
lsregistry_col.color_tag = 'COLOR_04'  # Blue

registry_name = format_collection_name(namespace, version)
registry_col = get_or_create_collection(registry_name, lsregistry_col)

# In LSREGISTRY_OT_repair.execute():
from .collection_helpers import get_all_registry_collections, remove_broken_links_from_collection

registries_to_repair = get_all_registry_collections()

for registry_info in registries_to_repair:
    remove_broken_links_from_collection(registry_info['collection'])
"""