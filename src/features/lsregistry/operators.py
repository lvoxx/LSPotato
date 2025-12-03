import bpy  # type: ignore
import os
from vendor import yaml
import requests
import zipfile
import shutil
from pathlib import Path

from ...constants.app_const import REGISTRY_COLLECTION_COLOR, REGISTRY_COLLECTION_NAME
from ...constants.registry_url import getCreatorRegistrryDLURL, getRegistryDLUrl
from ...utils.draw_ui import show_custom_popup


# ==========================================
# Helper Functions - Shared between operators
# ==========================================

def download_registry_metadata(namespace):
    """Download registry.yaml from LSRegistry repo"""
    path_parts = namespace.split(".")
    registry_path = "/".join(path_parts)

    url = getRegistryDLUrl(registry_path)

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch registry metadata: {response.status_code}"
        )

    blend_file_path = bpy.data.filepath
    if not blend_file_path:
        raise Exception("Please save your blend file first")

    blend_dir = Path(blend_file_path).parent
    metadata_dir = blend_dir / "registry" / "metadata" / namespace
    metadata_dir.mkdir(parents=True, exist_ok=True)

    metadata_file = metadata_dir / "registry.yaml"
    metadata_file.write_bytes(response.content)

    return metadata_file


def parse_registry_metadata(metadata_path):
    """Parse registry.yaml to get repo information"""
    with open(metadata_path, "r") as f:
        data = yaml.safe_load(f)

    metadata = data.get("metadata", {})
    return {
        "user": metadata.get("user"),
        "repository": metadata.get("repository"),
        "platform": metadata.get("platform", "github"),
        "credentials": metadata.get("credentails", "none"),
        "branch": metadata.get("branch", "main"),
    }


def download_ls_metadata(namespace, registry_info, context):
    """Download registry.ls.yaml from the creator's actual repo"""
    user = registry_info["user"]
    repo = registry_info["repository"]
    branch = registry_info["branch"]

    url = getCreatorRegistrryDLURL(user, repo, branch)

    headers = {}
    if registry_info["credentials"] != "none":
        token = get_github_token(namespace, context)
        if token:
            headers["Authorization"] = f"token {token}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch registry.ls.yaml from {user}/{repo}: {response.status_code}"
        )

    blend_file_path = bpy.data.filepath
    blend_dir = Path(blend_file_path).parent
    metadata_dir = blend_dir / "registry" / "metadata" / namespace

    ls_metadata_file = metadata_dir / "registry.ls.yaml"
    ls_metadata_file.write_bytes(response.content)

    return ls_metadata_file


def parse_ls_metadata(ls_metadata_path, version):
    """Parse registry.ls.yaml to get version information"""
    with open(ls_metadata_path, "r") as f:
        data = yaml.safe_load(f)

    versions = data.get("versions", {})
    if version not in versions:
        raise Exception(f"Version {version} not found in registry")

    version_data = versions[version]
    linked_objects = data.get("linked-objects-in-files", {})

    return {
        "tag": version_data.get("tag"),
        "release_file": version_data.get("release-file"),
        "linked_objects": linked_objects,
    }

def link_object_relative(relative_path_blender: str, object_name: str):
    """
    Load & link a single object from a .blend file using a RELATIVE path.
    Ensures Blender does NOT convert it to absolute by overriding Library.filepath.
    """

    # Track existing libraries
    previous_libs = set(bpy.data.libraries)

    # Load library (Blender will convert path → absolute internally)
    with bpy.data.libraries.load(relative_path_blender, link=True) as (data_from, data_to):
        if object_name in data_from.objects:
            data_to.objects = [object_name]

    # Detect newly created libraries
    new_libs = set(bpy.data.libraries) - previous_libs

    # Force their filepath back to relative
    for lib in new_libs:
        lib.filepath = relative_path_blender

    # Return linked objects
    return [obj for obj in data_to.objects if obj]


def download_and_extract_release(registry_info, version_info, namespace, version, context):
    """Download release zip and extract to registry folder"""
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

    response = requests.get(url, headers=headers, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download release: {response.status_code}")

    blend_file_path = bpy.data.filepath
    blend_dir = Path(blend_file_path).parent
    registry_dir = blend_dir / "registry"
    registry_dir.mkdir(exist_ok=True)

    zip_path = registry_dir / release_file
    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    extract_dir = registry_dir / f"{namespace}_{version}"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    zip_path.unlink()


def link_objects(context, ls_metadata_path, namespace, version):
    """Link objects from blend files based on registry.ls.yaml using relative paths"""
    with open(ls_metadata_path, "r") as f:
        data = yaml.safe_load(f)

    linked_objects = data.get("linked-objects-in-files", {})

    if not linked_objects:
        return

    blend_file_path = bpy.data.filepath
    blend_dir = Path(blend_file_path).parent
    extract_dir = blend_dir / "registry" / f"{namespace}_{version}"

    # Create or get LSRegistry collection
    lsregistry_col = get_or_create_collection(REGISTRY_COLLECTION_NAME, None)
    lsregistry_col.color_tag = REGISTRY_COLLECTION_COLOR

    # Exclude LSRegistry collection in Outliner
    for layer_coll in context.view_layer.layer_collection.children:
        if layer_coll.collection.name == REGISTRY_COLLECTION_NAME:
            layer_coll.exclude = True
            break

    # Create collection name in format: namespace:version
    registry_name = f"{namespace}:{version}"
    registry_col = get_or_create_collection(registry_name, lsregistry_col)

    for blend_file, object_name in linked_objects.items():
        blend_path = extract_dir / blend_file

        if not blend_path.exists():
            print(f"Warning: Blend file not found: {blend_path}")
            continue

        # Convert to relative path
        relative_path = os.path.relpath(blend_path, blend_dir)
        # Convert to Blender-style relative path
        relative_path_blender = "//" + relative_path.replace("\\", "/")

        # Link object from blend file using relative path
        linked_objs = link_object_relative(relative_path_blender, object_name)

        for obj in linked_objs:
            registry_col.objects.link(obj)

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
    """Get GitHub token for specific namespace from scene credentials"""
    props = context.scene.lsregistry

    for cred in props.credentials:
        if cred.namespace == namespace:
            return cred.token

    return ""


def verify_and_clean_installed_registries(context, current_registries_str):
    """Verify installed registries and remove non-existent ones"""
    if not current_registries_str:
        return ""

    blend_file_path = bpy.data.filepath
    if not blend_file_path:
        return current_registries_str

    blend_dir = Path(blend_file_path).parent
    verified_registries = []

    # Check if LSRegistry collection exists
    if REGISTRY_COLLECTION_NAME not in bpy.data.collections:
        print("LSRegistry collection not found, clearing installed registries list")
        return ""

    lsregistry_col = bpy.data.collections[REGISTRY_COLLECTION_NAME]

    for registry_str in current_registries_str.split(","):
        registry_str = registry_str.strip()
        if not registry_str or ":" not in registry_str:
            continue

        namespace, version = registry_str.split(":", 1)

        # Check 1: Collection exists
        collection_name = f"{namespace}:{version}"
        collection_exists = collection_name in [
            col.name for col in lsregistry_col.children
        ]

        # Check 2: Registry folder exists
        extract_dir = blend_dir / "registry" / f"{namespace}_{version}"
        folder_exists = extract_dir.exists()

        # Check 3: Metadata exists
        ls_metadata_path = (
            blend_dir / "registry" / "metadata" / namespace / "registry.ls.yaml"
        )
        registry_metadata_path = (
            blend_dir / "registry" / "metadata" / namespace / "registry.yaml"
        )
        metadata_exists = ls_metadata_path.exists() and registry_metadata_path.exists()

        # Only keep if all checks pass
        if collection_exists and folder_exists and metadata_exists:
            verified_registries.append(registry_str)
        else:
            print(
                f"Registry {registry_str} verification failed: "
                f"collection={collection_exists}, folder={folder_exists}, metadata={metadata_exists}"
            )

    result = ",".join(verified_registries)
    print(f"Verified registries: {result if result else '(none)'}")
    return result


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

    index: bpy.props.IntProperty()  # type: ignore

    def execute(self, context):
        props = context.scene.lsregistry
        if 0 <= self.index < len(props.credentials):
            props.credentials.remove(self.index)
            if props.credentials_index >= len(props.credentials):
                props.credentials_index = max(0, len(props.credentials) - 1)
        return {"FINISHED"}


class LSREGISTRY_OT_clear_installed(bpy.types.Operator):
    """Clear the installed registries list (does not remove files or collections)"""

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
        show_custom_popup("Installed registries list cleared", "Success", "CHECKMARK")
        return {"FINISHED"}


class LSREGISTRY_OT_create_registry_text(bpy.types.Operator):
    """Create a new text datablock for registry list"""

    bl_idname = "lsregistry.create_registry_text"
    bl_label = "Create Registry Text"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.lsregistry

        # Create new text datablock
        text = bpy.data.texts.new("LSRegistry_List")
        text.write("# Enter registries here, one per line\n")
        text.write("# Example:\n")
        text.write("# io.github.lvoxx.world-builder:dummy\n")
        text.write("# io.github.user.another-repo:2.0.0\n")
        text.write("\n")

        # Store the text name in the string property
        props.registry_text = text.name

        return {"FINISHED"}


class LSREGISTRY_OT_get(bpy.types.Operator):
    """Download and install registry packages"""

    bl_idname = "lsregistry.get"
    bl_label = "Get Registries"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.lsregistry

        if not props.registry_text:
            show_custom_popup(
                "Please create or select a registry text", "Error", "ERROR"
            )
            return {"CANCELLED"}

        # Get text block from its name
        text_block = bpy.data.texts.get(props.registry_text)
        if not text_block:
            show_custom_popup(
                f"Text '{props.registry_text}' not found", "Error", "ERROR"
            )
            return {"CANCELLED"}

        # Get text content
        registry_text = text_block.as_string().strip()

        if not registry_text:
            show_custom_popup("Registry text is empty", "Error", "ERROR")
            return {"CANCELLED"}

        # Parse multiple lines (filter out comments and empty lines)
        registry_lines = [
            line.strip()
            for line in registry_text.split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]

        if not registry_lines:
            show_custom_popup("Please enter at least one registry", "Error", "ERROR")
            return {"CANCELLED"}

        # Clean up current_registries by verifying actual installation
        props.current_registries = verify_and_clean_installed_registries(
            context, props.current_registries
        )

        props.is_downloading = True
        installed_registries = []
        current_registries_set = (
            set(props.current_registries.split(","))
            if props.current_registries
            else set()
        )

        try:
            for registry_line in registry_lines:
                # Parse namespace:version
                if ":" not in registry_line:
                    print(f"Skipping invalid format: {registry_line}")
                    continue

                namespace, version = registry_line.split(":", 1)

                # Check if already installed
                if registry_line in current_registries_set:
                    print(f"Registry {registry_line} is already installed, skipping")
                    continue

                try:
                    # Step 1: Download registry.yaml metadata
                    metadata_path = download_registry_metadata(namespace)

                    # Step 2: Parse metadata
                    registry_info = parse_registry_metadata(metadata_path)

                    # Step 3: Download registry.ls.yaml
                    ls_metadata_path = download_ls_metadata(
                        namespace, registry_info, context
                    )

                    # Step 4: Parse ls metadata and get version info
                    version_info = parse_ls_metadata(ls_metadata_path, version)

                    # Step 5: Download and extract release
                    download_and_extract_release(
                        registry_info, version_info, namespace, version, context
                    )

                    # Step 6: Link objects from blend files
                    link_objects(context, ls_metadata_path, namespace, version)

                    installed_registries.append(registry_line)
                    print(f"Successfully installed {registry_line}")

                except Exception as e:
                    print(f"Failed to install {registry_line}: {e}")
                    show_custom_popup(
                        f"Failed to install {registry_line}: {str(e)}", "Error", "ERROR"
                    )

            # Update current registries
            if installed_registries:
                current_registries_set.update(installed_registries)
                props.current_registries = ",".join(sorted(current_registries_set))

                show_custom_popup(
                    f"Successfully installed {len(installed_registries)} registry(ies)",
                    "Success",
                    "CHECKMARK",
                )
            elif not installed_registries and registry_lines:
                show_custom_popup(
                    "All registries are already installed",
                    "Info",
                    "INFO",
                )

        except Exception as e:
            show_custom_popup(str(e), "Error", "ERROR")
            return {"CANCELLED"}
        finally:
            props.is_downloading = False

        return {"FINISHED"}

    def verify_and_clean_installed_registries(self, context, current_registries_str):
        """Verify installed registries and remove non-existent ones"""
        if not current_registries_str:
            return ""

        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            return current_registries_str

        blend_dir = Path(blend_file_path).parent
        verified_registries = []

        # Check if LSRegistry collection exists
        if REGISTRY_COLLECTION_NAME not in bpy.data.collections:
            print("LSRegistry collection not found, clearing installed registries list")
            return ""

        lsregistry_col = bpy.data.collections[REGISTRY_COLLECTION_NAME]

        for registry_str in current_registries_str.split(","):
            registry_str = registry_str.strip()
            if not registry_str or ":" not in registry_str:
                continue

            namespace, version = registry_str.split(":", 1)

            # Check 1: Collection exists
            collection_name = f"{namespace}:{version}"
            collection_exists = collection_name in [
                col.name for col in lsregistry_col.children
            ]

            # Check 2: Registry folder exists
            extract_dir = blend_dir / "registry" / f"{namespace}_{version}"
            folder_exists = extract_dir.exists()

            # Check 3: Metadata exists
            ls_metadata_path = (
                blend_dir / "registry" / "metadata" / namespace / "registry.ls.yaml"
            )
            registry_metadata_path = (
                blend_dir / "registry" / "metadata" / namespace / "registry.yaml"
            )
            metadata_exists = ls_metadata_path.exists() and registry_metadata_path.exists()

            # Only keep if all checks pass
            if collection_exists and folder_exists and metadata_exists:
                verified_registries.append(registry_str)
            else:
                print(
                    f"Registry {registry_str} verification failed: "
                    f"collection={collection_exists}, folder={folder_exists}, metadata={metadata_exists}"
                )

        result = ",".join(verified_registries)
        print(f"Verified registries: {result if result else '(none)'}")
        return result

    def download_registry_metadata(self, namespace):
        """Download registry.yaml from LSRegistry repo"""
        path_parts = namespace.split(".")
        registry_path = "/".join(path_parts)

        url = getRegistryDLUrl(registry_path)

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch registry metadata: {response.status_code}"
            )

        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            raise Exception("Please save your blend file first")

        blend_dir = Path(blend_file_path).parent
        metadata_dir = blend_dir / "registry" / "metadata" / namespace
        metadata_dir.mkdir(parents=True, exist_ok=True)

        metadata_file = metadata_dir / "registry.yaml"
        metadata_file.write_bytes(response.content)

        return metadata_file

    def parse_registry_metadata(self, metadata_path):
        """Parse registry.yaml to get repo information"""
        with open(metadata_path, "r") as f:
            data = yaml.safe_load(f)

        metadata = data.get("metadata", {})
        return {
            "user": metadata.get("user"),
            "repository": metadata.get("repository"),
            "platform": metadata.get("platform", "github"),
            "credentials": metadata.get("credentails", "none"),
            "branch": metadata.get("branch", "main"),
        }

    def download_ls_metadata(self, namespace, registry_info, context):
        """Download registry.ls.yaml from the creator's actual repo"""
        user = registry_info["user"]
        repo = registry_info["repository"]
        branch = registry_info["branch"]

        url = getCreatorRegistrryDLURL(user, repo, branch)

        headers = {}
        if registry_info["credentials"] != "none":
            token = self.get_github_token(namespace, context)
            if token:
                headers["Authorization"] = f"token {token}"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch registry.ls.yaml from {user}/{repo}: {response.status_code}"
            )

        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        metadata_dir = blend_dir / "registry" / "metadata" / namespace

        ls_metadata_file = metadata_dir / "registry.ls.yaml"
        ls_metadata_file.write_bytes(response.content)

        return ls_metadata_file

    def parse_ls_metadata(self, ls_metadata_path, version):
        """Parse registry.ls.yaml to get version information"""
        with open(ls_metadata_path, "r") as f:
            data = yaml.safe_load(f)

        versions = data.get("versions", {})
        if version not in versions:
            raise Exception(f"Version {version} not found in registry")

        version_data = versions[version]
        linked_objects = data.get("linked-objects-in-files", {})

        return {
            "tag": version_data.get("tag"),
            "release_file": version_data.get("release-file"),
            "linked_objects": linked_objects,
        }

    def download_and_extract_release(
        self, registry_info, version_info, namespace, version, context
    ):
        """Download release zip and extract to registry folder"""
        user = registry_info["user"]
        repo = registry_info["repository"]
        tag = version_info["tag"]
        release_file = version_info["release_file"]

        url = f"https://github.com/{user}/{repo}/releases/download/{tag}/{release_file}"

        headers = {}
        if registry_info["credentials"] != "none":
            token = self.get_github_token(namespace, context)
            if token:
                headers["Authorization"] = f"token {token}"

        response = requests.get(url, headers=headers, stream=True)
        if response.status_code != 200:
            raise Exception(f"Failed to download release: {response.status_code}")

        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        registry_dir = blend_dir / "registry"
        registry_dir.mkdir(exist_ok=True)

        zip_path = registry_dir / release_file
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        extract_dir = registry_dir / f"{namespace}_{version}"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        zip_path.unlink()

    def link_objects(self, context, ls_metadata_path, namespace, version):
        """Link objects from blend files based on registry.ls.yaml using relative paths"""
        with open(ls_metadata_path, "r") as f:
            data = yaml.safe_load(f)

        linked_objects = data.get("linked-objects-in-files", {})

        if not linked_objects:
            return

        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        extract_dir = blend_dir / "registry" / f"{namespace}_{version}"

        # Create or get LSRegistry collection
        lsregistry_col = self.get_or_create_collection(REGISTRY_COLLECTION_NAME, None)
        lsregistry_col.color_tag = REGISTRY_COLLECTION_COLOR

        # Exclude LSRegistry collection in Outliner
        for layer_coll in context.view_layer.layer_collection.children:
            if layer_coll.collection.name == REGISTRY_COLLECTION_NAME:
                layer_coll.exclude = True
                break

        # Create collection name in format: namespace:version
        registry_name = f"{namespace}:{version}"
        registry_col = self.get_or_create_collection(registry_name, lsregistry_col)

        for blend_file, object_name in linked_objects.items():
            blend_path = extract_dir / blend_file

            if not blend_path.exists():
                print(f"Warning: Blend file not found: {blend_path}")
                continue

            # Convert to relative path
            relative_path = os.path.relpath(blend_path, blend_dir)
            # Convert to Blender-style relative path
            relative_path_blender = "//" + relative_path.replace("\\", "/")

            # Link object from blend file using relative path
            linked_objs = link_object_relative(relative_path_blender, object_name)

            for obj in linked_objs:
                registry_col.objects.link(obj)


    def get_or_create_collection(self, name, parent=None):
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

    def get_github_token(self, namespace, context):
        """Get GitHub token for specific namespace from scene credentials"""
        props = context.scene.lsregistry

        for cred in props.credentials:
            if cred.namespace == namespace:
                return cred.token

        return ""

    def download_registry_metadata(self, namespace):
        """Download registry.yaml from LSRegistry repo"""
        path_parts = namespace.split(".")
        registry_path = "/".join(path_parts)

        url = getRegistryDLUrl(registry_path)

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch registry metadata: {response.status_code}"
            )

        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            raise Exception("Please save your blend file first")

        blend_dir = Path(blend_file_path).parent
        metadata_dir = blend_dir / "registry" / "metadata" / namespace
        metadata_dir.mkdir(parents=True, exist_ok=True)

        metadata_file = metadata_dir / "registry.yaml"
        metadata_file.write_bytes(response.content)

        return metadata_file

    def parse_registry_metadata(self, metadata_path):
        """Parse registry.yaml to get repo information"""
        with open(metadata_path, "r") as f:
            data = yaml.safe_load(f)

        metadata = data.get("metadata", {})
        return {
            "user": metadata.get("user"),
            "repository": metadata.get("repository"),
            "platform": metadata.get("platform", "github"),
            "credentials": metadata.get("credentails", "none"),
            "branch": metadata.get("branch", "main"),
        }

    def download_ls_metadata(self, namespace, registry_info, context):
        """Download registry.ls.yaml from the creator's actual repo"""
        user = registry_info["user"]
        repo = registry_info["repository"]
        branch = registry_info["branch"]

        url = getCreatorRegistrryDLURL(user, repo, branch)

        headers = {}
        if registry_info["credentials"] != "none":
            token = self.get_github_token(namespace, context)
            if token:
                headers["Authorization"] = f"token {token}"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch registry.ls.yaml from {user}/{repo}: {response.status_code}"
            )

        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        metadata_dir = blend_dir / "registry" / "metadata" / namespace

        ls_metadata_file = metadata_dir / "registry.ls.yaml"
        ls_metadata_file.write_bytes(response.content)

        return ls_metadata_file

    def parse_ls_metadata(self, ls_metadata_path, version):
        """Parse registry.ls.yaml to get version information"""
        with open(ls_metadata_path, "r") as f:
            data = yaml.safe_load(f)

        versions = data.get("versions", {})
        if version not in versions:
            raise Exception(f"Version {version} not found in registry")

        version_data = versions[version]
        linked_objects = data.get("linked-objects-in-files", {})

        return {
            "tag": version_data.get("tag"),
            "release_file": version_data.get("release-file"),
            "linked_objects": linked_objects,
        }

    def download_and_extract_release(
        self, registry_info, version_info, namespace, version, context
    ):
        """Download release zip and extract to registry folder"""
        user = registry_info["user"]
        repo = registry_info["repository"]
        tag = version_info["tag"]
        release_file = version_info["release_file"]

        url = f"https://github.com/{user}/{repo}/releases/download/{tag}/{release_file}"

        headers = {}
        if registry_info["credentials"] != "none":
            token = self.get_github_token(namespace, context)
            if token:
                headers["Authorization"] = f"token {token}"

        response = requests.get(url, headers=headers, stream=True)
        if response.status_code != 200:
            raise Exception(f"Failed to download release: {response.status_code}")

        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        registry_dir = blend_dir / "registry"
        registry_dir.mkdir(exist_ok=True)

        zip_path = registry_dir / release_file
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        extract_dir = registry_dir / f"{namespace}_{version}"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        zip_path.unlink()

    def link_objects(self, context, ls_metadata_path, namespace, version):
        """Link objects from blend files based on registry.ls.yaml using relative paths"""
        with open(ls_metadata_path, "r") as f:
            data = yaml.safe_load(f)

        linked_objects = data.get("linked-objects-in-files", {})

        if not linked_objects:
            return

        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        extract_dir = blend_dir / "registry" / f"{namespace}_{version}"

        # Create or get LSRegistry collection
        lsregistry_col = self.get_or_create_collection(REGISTRY_COLLECTION_NAME, None)
        lsregistry_col.color_tag = REGISTRY_COLLECTION_COLOR

        # Exclude LSRegistry collection in Outliner
        for layer_coll in context.view_layer.layer_collection.children:
            if layer_coll.collection.name == REGISTRY_COLLECTION_NAME:
                layer_coll.exclude = True
                break

        # Create collection name in format: namespace:version
        registry_name = f"{namespace}:{version}"
        registry_col = self.get_or_create_collection(registry_name, lsregistry_col)

        for blend_file, object_name in linked_objects.items():
            blend_path = extract_dir / blend_file

            if not blend_path.exists():
                print(f"Warning: Blend file not found: {blend_path}")
                continue

            # Convert to relative path
            relative_path = os.path.relpath(blend_path, blend_dir)
            # Convert to Blender-style relative path
            relative_path_blender = "//" + relative_path.replace("\\", "/")

            # Link object from blend file using relative path
            linked_objs = link_object_relative(relative_path_blender, object_name)

            for obj in linked_objs:
                registry_col.objects.link(obj)


    def get_or_create_collection(self, name, parent=None):
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

    def get_github_token(self, namespace, context):
        """Get GitHub token for specific namespace from scene credentials"""
        props = context.scene.lsregistry

        for cred in props.credentials:
            if cred.namespace == namespace:
                return cred.token

        return ""


class LSREGISTRY_OT_repair(bpy.types.Operator):
    """Repair broken registry installation by re-installing from scratch"""

    bl_idname = "lsregistry.repair"
    bl_label = "Repair Registry"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="This will remove and re-install all registries")
        layout.label(text="found in the installed list.")
        layout.label(text="Do you want to continue?")

    def execute(self, context):
        props = context.scene.lsregistry

        if not props.current_registries:
            show_custom_popup("No installed registries to repair", "Error", "ERROR")
            return {"CANCELLED"}

        try:
            # Get list of registries to repair
            registries_to_repair = [
                r.strip() 
                for r in props.current_registries.split(",") 
                if r.strip()
            ]

            if not registries_to_repair:
                show_custom_popup("No registries to repair", "Error", "ERROR")
                return {"CANCELLED"}

            blend_file_path = bpy.data.filepath
            if not blend_file_path:
                raise Exception("Please save your blend file first")

            blend_dir = Path(blend_file_path).parent

            # Step 1: Clean up old installations
            print("Cleaning up old installations...")
            self.cleanup_registries(context, registries_to_repair, blend_dir)

            # Step 2: Clear the installed list
            props.current_registries = ""

            # Step 3: Re-install using Get operator logic
            print("Re-installing registries...")
            props.is_downloading = True
            installed_registries = []

            for registry_line in registries_to_repair:
                if ":" not in registry_line:
                    print(f"Skipping invalid format: {registry_line}")
                    continue

                namespace, version = registry_line.split(":", 1)

                try:
                    print(f"Re-installing {registry_line}...")

                    # Download registry.yaml metadata
                    metadata_path = download_registry_metadata(namespace)

                    # Parse metadata
                    registry_info = parse_registry_metadata(metadata_path)

                    # Download registry.ls.yaml
                    ls_metadata_path = download_ls_metadata(
                        namespace, registry_info, context
                    )

                    # Parse ls metadata and get version info
                    version_info = parse_ls_metadata(ls_metadata_path, version)

                    # Download and extract release
                    download_and_extract_release(
                        registry_info, version_info, namespace, version, context
                    )

                    # Link objects from blend files
                    link_objects(context, ls_metadata_path, namespace, version)

                    installed_registries.append(registry_line)
                    print(f"Successfully re-installed {registry_line}")

                except Exception as e:
                    print(f"Failed to re-install {registry_line}: {e}")
                    import traceback
                    traceback.print_exc()
                    show_custom_popup(
                        f"Failed to re-install {registry_line}: {str(e)}", 
                        "Warning", 
                        "ERROR"
                    )

            # Update installed list
            if installed_registries:
                props.current_registries = ",".join(sorted(installed_registries))
                show_custom_popup(
                    f"Successfully repaired {len(installed_registries)} registry(ies)", 
                    "Success", 
                    "CHECKMARK"
                )
            else:
                show_custom_popup(
                    "No registries were repaired", 
                    "Warning", 
                    "INFO"
                )

        except Exception as e:
            import traceback
            traceback.print_exc()
            show_custom_popup(str(e), "Error", "ERROR")
            return {"CANCELLED"}
        finally:
            props.is_downloading = False

        return {"FINISHED"}

    def cleanup_registries(self, context, registries_to_repair, blend_dir):
        """Clean up old registry installations"""
        
        # Remove collections
        if REGISTRY_COLLECTION_NAME in bpy.data.collections:
            lsregistry_col = bpy.data.collections[REGISTRY_COLLECTION_NAME]
            
            for registry_line in registries_to_repair:
                if ":" not in registry_line:
                    continue
                    
                namespace, version = registry_line.split(":", 1)
                
                # Try both old and new collection name formats
                collection_names = [
                    f"{namespace}:{version}",  # New format
                    f"{namespace.replace('.', '-')}-{version}"  # Old format
                ]
                
                for col_name in collection_names:
                    if col_name in bpy.data.collections:
                        col = bpy.data.collections[col_name]
                        
                        # Remove all objects from collection
                        objects_to_remove = list(col.objects)
                        for obj in objects_to_remove:
                            col.objects.unlink(obj)
                            if obj.library:
                                try:
                                    bpy.data.objects.remove(obj)
                                except:
                                    pass
                        
                        # Unlink collection from parent
                        if col.name in [c.name for c in lsregistry_col.children]:
                            lsregistry_col.children.unlink(col)
                        
                        # Remove collection
                        bpy.data.collections.remove(col)
                        print(f"Removed collection: {col_name}")
                
                # Remove registry folder
                extract_dir = blend_dir / "registry" / f"{namespace}_{version}"
                if extract_dir.exists():
                    shutil.rmtree(extract_dir)
                    print(f"Removed folder: {extract_dir}")
                
                # Remove metadata folder
                metadata_dir = blend_dir / "registry" / "metadata" / namespace
                if metadata_dir.exists():
                    shutil.rmtree(metadata_dir)
                    print(f"Removed metadata: {metadata_dir}")