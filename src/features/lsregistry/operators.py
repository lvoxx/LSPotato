import bpy  # type: ignore
import os
from vendor import yaml
import requests
import zipfile
import shutil
from pathlib import Path

from ...constants.app_const import REGISTRY_COLLECTION_COLOR
from ...constants.registry_url import getCreatorRegistrryDLURL, getRegistryDLUrl
from ...utils.draw_ui import show_custom_popup


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

    index: bpy.props.IntProperty() # type: ignore

    def execute(self, context):
        props = context.scene.lsregistry
        if 0 <= self.index < len(props.credentials):
            props.credentials.remove(self.index)
            if props.credentials_index >= len(props.credentials):
                props.credentials_index = max(0, len(props.credentials) - 1)
        return {"FINISHED"}


class LSREGISTRY_OT_get(bpy.types.Operator):
    """Download and install registry packages"""

    bl_idname = "lsregistry.get"
    bl_label = "Get Registries"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.lsregistry
        registry_input = props.registry_input.strip()

        if not registry_input:
            show_custom_popup("Please enter registry namespaces", "Error", "ERROR")
            return {"CANCELLED"}

        # Parse multiple lines
        registry_lines = [
            line.strip() for line in registry_input.split("\n") if line.strip()
        ]

        if not registry_lines:
            show_custom_popup("Please enter at least one registry", "Error", "ERROR")
            return {"CANCELLED"}

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
                    metadata_path = self.download_registry_metadata(namespace)

                    # Step 2: Parse metadata
                    registry_info = self.parse_registry_metadata(metadata_path)

                    # Step 3: Download registry.ls.yaml
                    ls_metadata_path = self.download_ls_metadata(
                        namespace, registry_info, context
                    )

                    # Step 4: Parse ls metadata and get version info
                    version_info = self.parse_ls_metadata(ls_metadata_path, version)

                    # Step 5: Download and extract release
                    self.download_and_extract_release(
                        registry_info, version_info, namespace, version, context
                    )

                    # Step 6: Link objects from blend files
                    self.link_objects(ls_metadata_path, namespace, version)

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

        except Exception as e:
            show_custom_popup(str(e), "Error", "ERROR")
            return {"CANCELLED"}
        finally:
            props.is_downloading = False

        return {"FINISHED"}

    def download_registry_metadata(self, namespace):
        """Download registry.yaml from LSRegistry repo"""
        # Convert namespace to path (e.g., io.github.lvoxx.world-builder -> io/github/lvoxx/world-builder)
        path_parts = namespace.split(".")
        registry_path = "/".join(path_parts)

        url = getRegistryDLUrl(registry_path)

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch registry metadata: {response.status_code}"
            )

        # Save to .\registry\metadata\namespace\
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
            "credentials": metadata.get(
                "credentails", "none"
            ),  # Note: typo in your example
            "branch": metadata.get("branch", "main"),
        }

    def download_ls_metadata(self, namespace, registry_info, context):
        """Download registry.ls.yaml from the creator's actual repo"""
        user = registry_info["user"]
        repo = registry_info["repository"]
        branch = registry_info["branch"]

        # Build URL to creator's repo
        url = getCreatorRegistrryDLURL(user, repo, branch)

        # Check if credentials needed
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

        # Save to same metadata directory
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

        # Construct download URL
        url = f"https://github.com/{user}/{repo}/releases/download/{tag}/{release_file}"

        # Check if credentials needed
        headers = {}
        if registry_info["credentials"] != "none":
            token = self.get_github_token(namespace, context)
            if token:
                headers["Authorization"] = f"token {token}"

        response = requests.get(url, headers=headers, stream=True)
        if response.status_code != 200:
            raise Exception(f"Failed to download release: {response.status_code}")

        # Save zip file
        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        registry_dir = blend_dir / "registry"
        registry_dir.mkdir(exist_ok=True)

        zip_path = registry_dir / release_file
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract zip
        extract_dir = registry_dir / f"{namespace}_{version}"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        # Remove zip file
        zip_path.unlink()

    def link_objects(self, ls_metadata_path, namespace, version):
        """Link objects from blend files based on registry.ls.yaml"""
        with open(ls_metadata_path, "r") as f:
            data = yaml.safe_load(f)

        linked_objects = data.get("linked-objects-in-files", {})

        if not linked_objects:
            return

        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        extract_dir = blend_dir / "registry" / f"{namespace}_{version}"

        # Create or get LSRegistry collection (blue color)
        lsregistry_col = self.get_or_create_collection("LSRegistry", None)
        lsregistry_col.color_tag = REGISTRY_COLLECTION_COLOR  # Blue color

        # Disable (hide) the LSRegistry collection in viewport
        lsregistry_col.hide_viewport = True

        # Create or get namespace-version collection inside LSRegistry
        registry_name = f"{namespace.replace('.', '-')}-{version}"
        registry_col = self.get_or_create_collection(registry_name, lsregistry_col)

        for blend_file, object_name in linked_objects.items():
            blend_path = extract_dir / blend_file

            if not blend_path.exists():
                print(f"Warning: Blend file not found: {blend_path}")
                continue

            # Link object from blend file
            with bpy.data.libraries.load(str(blend_path), link=True) as (
                data_from,
                data_to,
            ):
                if object_name in data_from.objects:
                    data_to.objects = [object_name]

            # Add to registry collection
            for obj in data_to.objects:
                if obj:
                    registry_col.objects.link(obj)

    def get_or_create_collection(self, name, parent=None):
        """Get existing collection or create new one"""
        # Check if collection exists
        if name in bpy.data.collections:
            collection = bpy.data.collections[name]
        else:
            # Create new collection
            collection = bpy.data.collections.new(name)

            # Link to parent or scene
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
    """Repair broken registry installation"""

    bl_idname = "lsregistry.repair"
    bl_label = "Repair Registry"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="This will re-download and re-link the registry.")
        layout.label(text="Do you want to continue?")

    def execute(self, context):
        props = context.scene.lsregistry

        # Check if LSRegistry collection exists
        if "LSRegistry" not in bpy.data.collections:
            show_custom_popup("No LSRegistry collection found", "Error", "ERROR")
            return {"CANCELLED"}

        lsregistry_col = bpy.data.collections["LSRegistry"]

        # Find all registry collections to repair
        registries_to_repair = []
        for child_col in lsregistry_col.children:
            # Parse collection name format: namespace-version
            col_name = child_col.name
            if "-" in col_name:
                # Get the last part as version, rest as namespace
                parts = col_name.rsplit("-", 1)
                if len(parts) == 2:
                    namespace_part, version_part = parts
                    # Replace - back to . for namespace
                    namespace = namespace_part.replace("-", ".")
                    version = version_part
                    registries_to_repair.append(
                        {
                            "namespace": namespace,
                            "version": version,
                            "collection": child_col,
                            "name": col_name,
                        }
                    )

        if not registries_to_repair:
            show_custom_popup("No registries found to repair", "Error", "ERROR")
            return {"CANCELLED"}

        # If current_registries is set, only repair those
        if props.current_registries:
            current_set = set(props.current_registries.split(","))
            registries_to_repair = [
                r
                for r in registries_to_repair
                if f"{r['namespace']}:{r['version']}" in current_set
            ]

            if not registries_to_repair:
                show_custom_popup(
                    "No matching registries found to repair", "Error", "ERROR"
                )
                return {"CANCELLED"}

        try:
            blend_file_path = bpy.data.filepath
            if not blend_file_path:
                raise Exception("Please save your blend file first")

            blend_dir = Path(blend_file_path).parent

            # Repair each registry
            for registry_info in registries_to_repair:
                namespace = registry_info["namespace"]
                version = registry_info["version"]
                collection = registry_info["collection"]

                # Check if metadata exists
                ls_metadata_path = (
                    blend_dir / "registry" / "metadata" / namespace / "registry.ls.yaml"
                )
                registry_metadata_path = (
                    blend_dir / "registry" / "metadata" / namespace / "registry.yaml"
                )

                if not ls_metadata_path.exists() or not registry_metadata_path.exists():
                    print(
                        f"Warning: Metadata not found for {namespace}:{version}, skipping"
                    )
                    continue

                # Read metadata
                with open(ls_metadata_path, "r") as f:
                    data = yaml.safe_load(f)

                with open(registry_metadata_path, "r") as f:
                    registry_data = yaml.safe_load(f)

                metadata = registry_data.get("metadata", {})
                registry_repo_info = {
                    "user": metadata.get("user"),
                    "repository": metadata.get("repository"),
                    "platform": metadata.get("platform", "github"),
                    "credentials": metadata.get("credentails", "none"),
                    "branch": metadata.get("branch", "main"),
                }

                versions = data.get("versions", {})
                if version not in versions:
                    print(
                        f"Warning: Version {version} not found for {namespace}, skipping"
                    )
                    continue

                version_data = versions[version]
                version_info = {
                    "tag": version_data.get("tag"),
                    "release_file": version_data.get("release-file"),
                    "linked_objects": data.get("linked-objects-in-files", {}),
                }

                # Remove broken objects from this collection
                self.remove_broken_links_from_collection(collection)

                # Re-download and extract
                get_operator = LSREGISTRY_OT_get()
                get_operator.download_and_extract_release(
                    registry_repo_info, version_info, namespace, version, context
                )

                # Re-link objects
                get_operator.link_objects(ls_metadata_path, namespace, version)

                print(f"Successfully repaired {namespace}:{version}")

            show_custom_popup(
                "Successfully repaired registries", "Success", "CHECKMARK"
            )

        except Exception as e:
            show_custom_popup(str(e), "Error", "ERROR")
            return {"CANCELLED"}

        return {"FINISHED"}

    def remove_broken_links_from_collection(self, collection):
        """Remove broken library links from a specific collection"""
        objects_to_remove = []

        for obj in collection.objects:
            if (
                obj.library
                and not Path(bpy.path.abspath(obj.library.filepath)).exists()
            ):
                objects_to_remove.append(obj)

        for obj in objects_to_remove:
            bpy.data.objects.remove(obj)

    """Download and install registry package"""
    bl_idname = "lsregistry.get"
    bl_label = "Get Registry"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.lsregistry
        registry_input = props.registry_input.strip()

        if not registry_input:
            show_custom_popup("Please enter a registry namespace", "Error", "ERROR")
            return {"CANCELLED"}

        # Parse namespace:version
        if ":" not in registry_input:
            show_custom_popup(
                "Invalid format. Use: namespace:version", "Error", "ERROR"
            )
            return {"CANCELLED"}

        namespace, version = registry_input.split(":", 1)

        # Check if already installed
        if props.current_registry and props.current_registry != registry_input:
            show_custom_popup(
                f"Registry {props.current_registry} is already installed. Please remove it first.",
                "Error",
                "ERROR",
            )
            return {"CANCELLED"}

        props.is_downloading = True

        try:
            # Step 1: Download registry.yaml metadata
            metadata_path = self.download_registry_metadata(namespace)

            # Step 2: Parse metadata
            registry_info = self.parse_registry_metadata(metadata_path)

            # Step 3: Download registry.ls.yaml
            ls_metadata_path = self.download_ls_metadata(namespace, registry_info)

            # Step 4: Parse ls metadata and get version info
            version_info = self.parse_ls_metadata(ls_metadata_path, version)

            # Step 5: Download and extract release
            self.download_and_extract_release(
                registry_info, version_info, namespace, version
            )

            # Step 6: Link objects from blend files
            self.link_objects(ls_metadata_path, namespace, version)

            props.current_registry = registry_input
            show_custom_popup(
                f"Successfully installed {registry_input}", "Success", "CHECKMARK"
            )

        except Exception as e:
            show_custom_popup(str(e), "Error", "ERROR")
            return {"CANCELLED"}
        finally:
            props.is_downloading = False

        return {"FINISHED"}

    def download_registry_metadata(self, namespace):
        """Download registry.yaml from LSRegistry repo"""
        # Convert namespace to path (e.g., io.github.lvoxx.world-builder -> io/github/lvoxx/world-builder)
        path_parts = namespace.split(".")
        registry_path = "/".join(path_parts)

        url = f"https://raw.githubusercontent.com/lvoxx/LSRegistry/main/{registry_path}/registry.yaml"

        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch registry metadata: {response.status_code}"
            )

        # Save to .\registry\metadata\namespace\
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
            "credentials": metadata.get(
                "credentails", "none"
            ),  # Note: typo in your example
            "branch": metadata.get("branch", "main"),
        }

    def download_ls_metadata(self, namespace, registry_info):
        """Download registry.ls.yaml from the creator's actual repo"""
        user = registry_info["user"]
        repo = registry_info["repository"]
        branch = registry_info["branch"]

        # Build URL to creator's repo
        url = (
            f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/registry.ls.yaml"
        )

        # Check if credentials needed
        headers = {}
        if registry_info["credentials"] != "none":
            token = self.get_github_token(registry_info["credentials"])
            if token:
                headers["Authorization"] = f"token {token}"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch registry.ls.yaml from {user}/{repo}: {response.status_code}"
            )

        # Save to same metadata directory
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
        self, registry_info, version_info, namespace, version
    ):
        """Download release zip and extract to registry folder"""
        user = registry_info["user"]
        repo = registry_info["repository"]
        tag = version_info["tag"]
        release_file = version_info["release_file"]

        # Construct download URL
        url = f"https://github.com/{user}/{repo}/releases/download/{tag}/{release_file}"

        # Check if credentials needed
        headers = {}
        if registry_info["credentials"] != "none":
            token = self.get_github_token(registry_info["credentials"])
            if token:
                headers["Authorization"] = f"token {token}"

        response = requests.get(url, headers=headers, stream=True)
        if response.status_code != 200:
            raise Exception(f"Failed to download release: {response.status_code}")

        # Save zip file
        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        registry_dir = blend_dir / "registry"
        registry_dir.mkdir(exist_ok=True)

        zip_path = registry_dir / release_file
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract zip
        extract_dir = registry_dir / f"{namespace}_{version}"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        # Remove zip file
        zip_path.unlink()

    def link_objects(self, ls_metadata_path, namespace, version):
        """Link objects from blend files based on registry.ls.yaml"""
        with open(ls_metadata_path, "r") as f:
            data = yaml.safe_load(f)

        linked_objects = data.get("linked-objects-in-files", {})

        if not linked_objects:
            return

        blend_file_path = bpy.data.filepath
        blend_dir = Path(blend_file_path).parent
        extract_dir = blend_dir / "registry" / f"{namespace}_{version}"

        # Create or get LSRegistry collection (blue color)
        lsregistry_col = self.get_or_create_collection("LSRegistry", None)
        lsregistry_col.color_tag = "COLOR_04"  # Blue color

        # Create or get namespace-version collection inside LSRegistry
        registry_name = f"{namespace}-{version}"
        registry_col = self.get_or_create_collection(registry_name, lsregistry_col)

        for blend_file, object_name in linked_objects.items():
            blend_path = extract_dir / blend_file

            if not blend_path.exists():
                print(f"Warning: Blend file not found: {blend_path}")
                continue

            # Link object from blend file
            with bpy.data.libraries.load(str(blend_path), link=True) as (
                data_from,
                data_to,
            ):
                if object_name in data_from.objects:
                    data_to.objects = [object_name]

            # Add to registry collection
            for obj in data_to.objects:
                if obj:
                    registry_col.objects.link(obj)

    def get_or_create_collection(self, name, parent=None):
        """Get existing collection or create new one"""
        # Check if collection exists
        if name in bpy.data.collections:
            collection = bpy.data.collections[name]
        else:
            # Create new collection
            collection = bpy.data.collections.new(name)

            # Link to parent or scene
            if parent:
                parent.children.link(collection)
            else:
                bpy.context.scene.collection.children.link(collection)

        return collection

    def get_github_token(self, credential_name):
        """Get GitHub token from addon preferences"""
        addon_prefs = bpy.context.preferences.addons.get(__package__.split(".")[0])
        if addon_prefs:
            return getattr(
                addon_prefs.preferences, f"github_token_{credential_name}", ""
            )
        return ""


class LSREGISTRY_OT_repair(bpy.types.Operator):
    """Repair broken registry installation"""

    bl_idname = "lsregistry.repair"
    bl_label = "Repair Registry"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def draw(self, context):
        layout = self.layout
        layout.label(text="This will re-download and re-link the registry.")
        layout.label(text="Do you want to continue?")

    def execute(self, context):
        props = context.scene.lsregistry

        # Check if LSRegistry collection exists
        if "LSRegistry" not in bpy.data.collections:
            show_custom_popup("No LSRegistry collection found", "Error", "ERROR")
            return {"CANCELLED"}

        lsregistry_col = bpy.data.collections["LSRegistry"]

        # Find all registry collections to repair
        registries_to_repair = []
        for child_col in lsregistry_col.children:
            # Parse collection name format: namespace-version
            col_name = child_col.name
            if "-" in col_name:
                # Get the last part as version, rest as namespace
                parts = col_name.rsplit("-", 1)
                if len(parts) == 2:
                    namespace_part, version_part = parts
                    # Replace - back to . for namespace
                    namespace = namespace_part.replace("-", ".")
                    version = version_part
                    registries_to_repair.append(
                        {
                            "namespace": namespace,
                            "version": version,
                            "collection": child_col,
                            "name": col_name,
                        }
                    )

        if not registries_to_repair:
            show_custom_popup("No registries found to repair", "Error", "ERROR")
            return {"CANCELLED"}

        # If current_registry is set, only repair that one
        if props.current_registry:
            namespace, version = props.current_registry.split(":", 1)
            registry_name = f"{namespace.replace('.', '-')}-{version}"
            registries_to_repair = [
                r for r in registries_to_repair if r["name"] == registry_name
            ]

            if not registries_to_repair:
                show_custom_popup(
                    f"Registry {props.current_registry} not found in collections",
                    "Error",
                    "ERROR",
                )
                return {"CANCELLED"}

        try:
            blend_file_path = bpy.data.filepath
            if not blend_file_path:
                raise Exception("Please save your blend file first")

            blend_dir = Path(blend_file_path).parent

            # Repair each registry
            for registry_info in registries_to_repair:
                namespace = registry_info["namespace"]
                version = registry_info["version"]
                collection = registry_info["collection"]

                # Check if metadata exists
                ls_metadata_path = (
                    blend_dir / "registry" / "metadata" / namespace / "registry.ls.yaml"
                )
                registry_metadata_path = (
                    blend_dir / "registry" / "metadata" / namespace / "registry.yaml"
                )

                if not ls_metadata_path.exists() or not registry_metadata_path.exists():
                    print(
                        f"Warning: Metadata not found for {namespace}:{version}, skipping"
                    )
                    continue

                # Read metadata
                with open(ls_metadata_path, "r") as f:
                    data = yaml.safe_load(f)

                with open(registry_metadata_path, "r") as f:
                    registry_data = yaml.safe_load(f)

                metadata = registry_data.get("metadata", {})
                registry_repo_info = {
                    "user": metadata.get("user"),
                    "repository": metadata.get("repository"),
                    "platform": metadata.get("platform", "github"),
                    "credentials": metadata.get("credentails", "none"),
                    "branch": metadata.get("branch", "main"),
                }

                versions = data.get("versions", {})
                if version not in versions:
                    print(
                        f"Warning: Version {version} not found for {namespace}, skipping"
                    )
                    continue

                version_data = versions[version]
                version_info = {
                    "tag": version_data.get("tag"),
                    "release_file": version_data.get("release-file"),
                    "linked_objects": data.get("linked-objects-in-files", {}),
                }

                # Remove broken objects from this collection
                self.remove_broken_links_from_collection(collection)

                # Re-download and extract
                get_operator = LSREGISTRY_OT_get()
                get_operator.download_and_extract_release(
                    registry_repo_info, version_info, namespace, version
                )

                # Re-link objects
                get_operator.link_objects(ls_metadata_path, namespace, version)

                print(f"Successfully repaired {namespace}:{version}")

            show_custom_popup(
                "Successfully repaired registries", "Success", "CHECKMARK"
            )

        except Exception as e:
            show_custom_popup(str(e), "Error", "ERROR")
            return {"CANCELLED"}

        return {"FINISHED"}

    def remove_broken_links_from_collection(self, collection):
        """Remove broken library links from a specific collection"""
        objects_to_remove = []

        for obj in collection.objects:
            if (
                obj.library
                and not Path(bpy.path.abspath(obj.library.filepath)).exists()
            ):
                objects_to_remove.append(obj)

        for obj in objects_to_remove:
            bpy.data.objects.remove(obj)
