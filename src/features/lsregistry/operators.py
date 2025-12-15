"""
LSRegistry Operators
Operators cho LSRegistry feature với exception handling
"""

import bpy
import os
import requests
import zipfile
import shutil
from pathlib import Path
from vendor import yaml

from ...exception.base_handler import OperatorExceptionMixin
from ...exception.handler.lsregistry_handler import LSRegistryHandler
from ...exception.model.lspotato_exceptions import (
    InvalidNamespaceException,
    RegistryListNotFoundException,
    RegistryYMLParseException,
    RegistryDownloadException,
    RegistryExtractionException,
    GithubAPIException,
    FileSystemException,
    CredentialsNotFoundException
)
from ...utils.logger import get_logger
from ...constants.app_const import REGISTRY_COLLECTION_COLOR, REGISTRY_COLLECTION_NAME
from ...constants.registry_url import getCreatorRegistrryDLURL, getRegistryDLUrl


logger = get_logger("LSRegistry")


# ==========================================
# Helper Functions
# ==========================================

def link_object_relative(relative_path_blender: str, object_name: str):
    """Link a single object from a .blend file using RELATIVE path"""
    previous_libs = set(bpy.data.libraries)
    
    with bpy.data.libraries.load(relative_path_blender, link=True) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects = [object_name]
    
    new_libs = set(bpy.data.libraries) - previous_libs
    for lib in new_libs:
        lib.filepath = relative_path_blender
    
    return [obj for obj in data_to.objects if obj]


def get_or_create_collection(name, parent=None):
    """Get existing collection or create new one"""
    if name in bpy.data.collections:
        collection = bpy.data.collections[name]
    else:
        collection = bpy.data.collections.new(name)
        if parent:
            parent.children.link(collection)
        else:
            bpy.context.scene.collection.children.link(collection)
    return collection


def get_github_token(namespace, context):
    """Get GitHub token for specific namespace"""
    props = context.scene.lsregistry
    for cred in props.credentials:
        if cred.namespace == namespace:
            return cred.token
    return ""


# ==========================================
# Operators
# ==========================================

class LSREGISTRY_OT_add_credential(bpy.types.Operator):
    """Add a new credential for private registries"""
    bl_idname = "lsregistry.add_credential"
    bl_label = "Add Credential"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.lsregistry
        new_cred = props.credentials.add()
        new_cred.namespace = ""
        new_cred.token = ""
        props.credentials_index = len(props.credentials) - 1
        return {"FINISHED"}


class LSREGISTRY_OT_remove_credential(bpy.types.Operator):
    """Remove a credential"""
    bl_idname = "lsregistry.remove_credential"
    bl_label = "Remove Credential"
    bl_options = {"REGISTER", "UNDO"}

    index: bpy.props.IntProperty()

    def execute(self, context):
        props = context.scene.lsregistry
        if 0 <= self.index < len(props.credentials):
            props.credentials.remove(self.index)
            if props.credentials_index >= len(props.credentials):
                props.credentials_index = max(0, len(props.credentials) - 1)
        return {"FINISHED"}


class LSREGISTRY_OT_clear_installed(bpy.types.Operator):
    """Clear the installed registries list"""
    bl_idname = "lsregistry.clear_installed"
    bl_label = "Clear Installed List"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="This will clear the installed registries list.")
        layout.label(text="Files and collections will NOT be removed.")
        layout.label(text="Do you want to continue?")

    def execute(self, context):
        props = context.scene.lsregistry
        props.current_registries = ""
        self.report({"INFO"}, "✅ Installed registries list cleared")
        return {"FINISHED"}


class LSREGISTRY_OT_create_registry_text(bpy.types.Operator):
    """Create a new text datablock for registry list"""
    bl_idname = "lsregistry.create_registry_text"
    bl_label = "Create Registry Text"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.lsregistry
        
        text = bpy.data.texts.new("LSRegistry_List")
        text.write("# Enter registries here, one per line\n")
        text.write("# Example:\n")
        text.write("# io.github.lvoxx.world-builder:dummy\n")
        text.write("# io.github.user.another-repo:2.0.0\n")
        text.write("\n")
        
        props.registry_text = text.name
        return {"FINISHED"}


class LSREGISTRY_OT_get(bpy.types.Operator, OperatorExceptionMixin):
    """Download and install registry packages"""
    bl_idname = "lsregistry.get"
    bl_label = "Get Registries"
    bl_options = {"REGISTER", "UNDO"}
    
    handler_class = LSRegistryHandler

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)
    
    def _execute_impl(self, context):
        props = context.scene.lsregistry

        # Validate registry text exists
        if not props.registry_text:
            raise RegistryListNotFoundException("No registry text selected")
        
        text_block = bpy.data.texts.get(props.registry_text)
        if not text_block:
            raise RegistryListNotFoundException(f"Text '{props.registry_text}' not found")
        
        registry_text = text_block.as_string().strip()
        if not registry_text:
            raise RegistryListNotFoundException("Registry text is empty")
        
        # Parse registry lines
        registry_lines = [
            line.strip()
            for line in registry_text.split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]
        
        if not registry_lines:
            raise RegistryListNotFoundException("No valid registries found in text")
        
        # Verify installed registries
        props.current_registries = self._verify_and_clean_installed(context, props.current_registries)
        
        props.is_downloading = True
        installed_registries = []
        current_registries_set = set(props.current_registries.split(",")) if props.current_registries else set()
        
        try:
            for registry_line in registry_lines:
                # Parse namespace:version
                if ":" not in registry_line:
                    logger.warning(f"Skipping invalid format: {registry_line}")
                    continue
                
                namespace, version = registry_line.split(":", 1)
                
                # Check if already installed
                if registry_line in current_registries_set:
                    logger.info(f"Registry {registry_line} already installed, skipping")
                    continue
                
                try:
                    self._install_registry(namespace, version, context)
                    installed_registries.append(registry_line)
                    logger.info(f"Successfully installed {registry_line}")
                
                except Exception as e:
                    logger.error(f"Failed to install {registry_line}: {e}")
                    # Continue với registries khác
                    continue
            
            # Update installed list
            if installed_registries:
                current_registries_set.update(installed_registries)
                props.current_registries = ",".join(sorted(current_registries_set))
                self.report({"INFO"}, f"✅ Installed {len(installed_registries)} registry(ies)")
            else:
                self.report({"INFO"}, "All registries are already installed")
        
        finally:
            props.is_downloading = False
        
        return {"FINISHED"}
    
    def _install_registry(self, namespace, version, context):
        """Install a single registry - throws exceptions on error"""
        # Step 1: Download registry.yaml
        metadata_path = self._download_registry_metadata(namespace)
        
        # Step 2: Parse metadata
        registry_info = self._parse_registry_metadata(metadata_path)
        
        # Step 3: Download registry.ls.yaml
        ls_metadata_path = self._download_ls_metadata(namespace, registry_info, context)
        
        # Step 4: Parse ls metadata
        version_info = self._parse_ls_metadata(ls_metadata_path, version)
        
        # Step 5: Download and extract release
        self._download_and_extract_release(registry_info, version_info, namespace, version, context)
        
        # Step 6: Link objects
        self._link_objects(context, ls_metadata_path, namespace, version)
    
    def _download_registry_metadata(self, namespace):
        """Download registry.yaml from LSRegistry repo"""
        # Validate namespace format
        if "." not in namespace:
            raise InvalidNamespaceException(namespace)
        
        path_parts = namespace.split(".")
        registry_path = "/".join(path_parts)
        url = getRegistryDLUrl(registry_path)
        
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                raise GithubAPIException(
                    response.status_code,
                    f"Failed to fetch registry metadata from {url}"
                )
        except requests.RequestException as e:
            raise RegistryDownloadException(namespace, url, str(e))
        
        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            raise FileSystemException("save", "blend file", "Please save your blend file first")
        
        blend_dir = Path(blend_file_path).parent
        metadata_dir = blend_dir / "registry" / "metadata" / namespace
        
        try:
            metadata_dir.mkdir(parents=True, exist_ok=True)
            metadata_file = metadata_dir / "registry.yaml"
            metadata_file.write_bytes(response.content)
        except Exception as e:
            raise FileSystemException("write", str(metadata_dir), str(e))
        
        return metadata_file
    
    def _parse_registry_metadata(self, metadata_path):
        """Parse registry.yaml"""
        try:
            with open(metadata_path, "r") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise RegistryYMLParseException(str(metadata_path), str(e))
        
        metadata = data.get("metadata", {})
        return {
            "user": metadata.get("user"),
            "repository": metadata.get("repository"),
            "platform": metadata.get("platform", "github"),
            "credentials": metadata.get("credentails", "none"),
            "branch": metadata.get("branch", "main"),
        }
    
    def _download_ls_metadata(self, namespace, registry_info, context):
        """Download registry.ls.yaml from creator's repo"""
        user = registry_info["user"]
        repo = registry_info["repository"]
        branch = registry_info["branch"]
        url = getCreatorRegistrryDLURL(user, repo, branch)
        
        headers = {}
        if registry_info["credentials"] != "none":
            token = get_github_token(namespace, context)
            if not token:
                raise CredentialsNotFoundException(namespace)
            headers["Authorization"] = f"token {token}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code != 200:
                raise GithubAPIException(
                    response.status_code,
                    f"Failed to fetch registry.ls.yaml from {user}/{repo}"
                )
        except requests.RequestException as e:
            raise RegistryDownloadException(namespace, url, str(e))
        
        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        metadata_dir = blend_dir / "registry" / "metadata" / namespace
        
        ls_metadata_file = metadata_dir / "registry.ls.yaml"
        ls_metadata_file.write_bytes(response.content)
        
        return ls_metadata_file
    
    def _parse_ls_metadata(self, ls_metadata_path, version):
        """Parse registry.ls.yaml"""
        try:
            with open(ls_metadata_path, "r") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise RegistryYMLParseException(str(ls_metadata_path), str(e))
        
        versions = data.get("versions", {})
        if version not in versions:
            raise RegistryYMLParseException(
                str(ls_metadata_path),
                f"Version {version} not found in registry"
            )
        
        version_data = versions[version]
        linked_objects = data.get("linked-objects-in-files", {})
        
        return {
            "tag": version_data.get("tag"),
            "release_file": version_data.get("release-file"),
            "linked_objects": linked_objects,
        }
    
    def _download_and_extract_release(self, registry_info, version_info, namespace, version, context):
        """Download and extract release zip"""
        user = registry_info["user"]
        repo = registry_info["repository"]
        tag = version_info["tag"]
        release_file = version_info["release_file"]
        url = f"https://github.com/{user}/{repo}/releases/download/{tag}/{release_file}"
        
        headers = {}
        if registry_info["credentials"] != "none":
            token = get_github_token(namespace, context)
            if token:
                headers["Authorization"] = f"token {token}"
        
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=60)
            if response.status_code != 200:
                raise GithubAPIException(response.status_code, f"Failed to download release from {url}")
        except requests.RequestException as e:
            raise RegistryDownloadException(namespace, url, str(e))
        
        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        registry_dir = blend_dir / "registry"
        registry_dir.mkdir(exist_ok=True)
        
        zip_path = registry_dir / release_file
        try:
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        except Exception as e:
            raise FileSystemException("write", str(zip_path), str(e))
        
        extract_dir = registry_dir / f"{namespace}_{version}"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        
        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
            zip_path.unlink()
        except Exception as e:
            raise RegistryExtractionException(namespace, str(zip_path), str(e))
    
    def _link_objects(self, context, ls_metadata_path, namespace, version):
        """Link objects from blend files"""
        with open(ls_metadata_path, "r") as f:
            data = yaml.safe_load(f)
        
        linked_objects = data.get("linked-objects-in-files", {})
        if not linked_objects:
            return
        
        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        extract_dir = blend_dir / "registry" / f"{namespace}_{version}"
        
        # Create collections
        lsregistry_col = get_or_create_collection(REGISTRY_COLLECTION_NAME, None)
        lsregistry_col.color_tag = REGISTRY_COLLECTION_COLOR
        
        # Exclude from outliner
        for layer_coll in context.view_layer.layer_collection.children:
            if layer_coll.collection.name == REGISTRY_COLLECTION_NAME:
                layer_coll.exclude = True
                break
        
        registry_name = f"{namespace}:{version}"
        registry_col = get_or_create_collection(registry_name, lsregistry_col)
        
        # Link objects
        for blend_file, object_name in linked_objects.items():
            blend_path = extract_dir / blend_file
            
            if not blend_path.exists():
                logger.warning(f"Blend file not found: {blend_path}")
                continue
            
            relative_path = os.path.relpath(blend_path, blend_dir)
            relative_path_blender = "//" + relative_path.replace("\\", "/")
            
            linked_objs = link_object_relative(relative_path_blender, object_name)
            for obj in linked_objs:
                registry_col.objects.link(obj)
    
    def _verify_and_clean_installed(self, context, current_registries_str):
        """Verify and clean installed registries"""
        if not current_registries_str:
            return ""
        
        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            return current_registries_str
        
        blend_dir = Path(blend_file_path).parent
        verified_registries = []
        
        if REGISTRY_COLLECTION_NAME not in bpy.data.collections:
            logger.warning("LSRegistry collection not found, clearing list")
            return ""
        
        lsregistry_col = bpy.data.collections[REGISTRY_COLLECTION_NAME]
        
        for registry_str in current_registries_str.split(","):
            registry_str = registry_str.strip()
            if not registry_str or ":" not in registry_str:
                continue
            
            namespace, version = registry_str.split(":", 1)
            collection_name = f"{namespace}:{version}"
            
            # Verify existence
            collection_exists = collection_name in [col.name for col in lsregistry_col.children]
            extract_dir = blend_dir / "registry" / f"{namespace}_{version}"
            folder_exists = extract_dir.exists()
            
            ls_metadata_path = blend_dir / "registry" / "metadata" / namespace / "registry.ls.yaml"
            registry_metadata_path = blend_dir / "registry" / "metadata" / namespace / "registry.yaml"
            metadata_exists = ls_metadata_path.exists() and registry_metadata_path.exists()
            
            if collection_exists and folder_exists and metadata_exists:
                verified_registries.append(registry_str)
        
        return ",".join(verified_registries)


class LSREGISTRY_OT_repair(bpy.types.Operator, OperatorExceptionMixin):
    """Repair broken registry installation"""
    bl_idname = "lsregistry.repair"
    bl_label = "Repair Registry"
    bl_options = {"REGISTER", "UNDO"}
    
    handler_class = LSRegistryHandler

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="This will remove and re-install all registries")
        layout.label(text="found in the installed list.")
        layout.label(text="Do you want to continue?")

    def execute(self, context):
        return self.safe_execute(self._execute_impl, context)
    
    def _execute_impl(self, context):
        props = context.scene.lsregistry
        
        if not props.current_registries:
            raise RegistryListNotFoundException("No installed registries to repair")
        
        registries_to_repair = [r.strip() for r in props.current_registries.split(",") if r.strip()]
        if not registries_to_repair:
            raise RegistryListNotFoundException("No registries to repair")
        
        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            raise FileSystemException("save", "blend file", "Please save your blend file first")
        
        blend_dir = Path(blend_file_path).parent
        
        # Cleanup old installations
        logger.info("Cleaning up old installations...")
        self._cleanup_registries(context, registries_to_repair, blend_dir)
        
        # Clear installed list
        props.current_registries = ""
        
        # Re-install
        logger.info("Re-installing registries...")
        props.is_downloading = True
        installed_registries = []
        
        try:
            for registry_line in registries_to_repair:
                if ":" not in registry_line:
                    continue
                
                namespace, version = registry_line.split(":", 1)
                
                try:
                    # Use same install logic from Get operator
                    get_operator = LSREGISTRY_OT_get()
                    get_operator._install_registry(namespace, version, context)
                    installed_registries.append(registry_line)
                    logger.info(f"Successfully re-installed {registry_line}")
                
                except Exception as e:
                    logger.error(f"Failed to re-install {registry_line}: {e}")
                    continue
            
            if installed_registries:
                props.current_registries = ",".join(sorted(installed_registries))
                self.report({"INFO"}, f"✅ Repaired {len(installed_registries)} registry(ies)")
            else:
                self.report({"WARNING"}, "No registries were repaired")
        
        finally:
            props.is_downloading = False
        
        return {"FINISHED"}
    
    def _cleanup_registries(self, context, registries_to_repair, blend_dir):
        """Clean up old installations"""
        if REGISTRY_COLLECTION_NAME not in bpy.data.collections:
            return
        
        lsregistry_col = bpy.data.collections[REGISTRY_COLLECTION_NAME]
        
        for registry_line in registries_to_repair:
            if ":" not in registry_line:
                continue
            
            namespace, version = registry_line.split(":", 1)
            collection_name = f"{namespace}:{version}"
            
            # Remove collection
            if collection_name in bpy.data.collections:
                col = bpy.data.collections[collection_name]
                
                for obj in list(col.objects):
                    col.objects.unlink(obj)
                    if obj.library:
                        try:
                            bpy.data.objects.remove(obj)
                        except:
                            pass
                
                if col.name in [c.name for c in lsregistry_col.children]:
                    lsregistry_col.children.unlink(col)
                
                bpy.data.collections.remove(col)
                logger.debug(f"Removed collection: {collection_name}")
            
            # Remove folders
            extract_dir = blend_dir / "registry" / f"{namespace}_{version}"
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
                logger.debug(f"Removed folder: {extract_dir}")
            
            metadata_dir = blend_dir / "registry" / "metadata" / namespace
            if metadata_dir.exists():
                shutil.rmtree(metadata_dir)
                logger.debug(f"Removed metadata: {metadata_dir}")