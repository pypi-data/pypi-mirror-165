import uuid
from datetime import datetime
from pathlib import Path
from typing import Union

from cloudpathlib import CloudPath
from lamin_logger import logger
from lndb_setup import settings
from supabase import Client


class Entities:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.instance = Instance(self.hub)
        self.user_instance = UserInstance(self.hub)
        self.dtransform = Dtransform(self.hub)
        self.pipeline = Pipeline(self.hub)
        self.jupynb = Jupynb(self.hub)
        self.pipeline_run = PipelineRun(self.hub)
        self.dtransform_in = DtransformIn(self.hub)
        self.dobject = Dobject(self.hub)
        self.storage = Storage(self.hub)
        self.usage = Usage(self.hub)


class Entity:
    def __init__(self, hub: Client, table_name: str, primary_keys: list) -> None:
        self.hub = hub
        self.table_name = table_name
        self.primary_keys = primary_keys

    def exists(self, primary_keys_values: dict):
        statement = self.hub.table(self.table_name).select("*")
        for key in self.primary_keys:
            statement = statement.eq(key, primary_keys_values[key])
        data = statement.execute()
        if len(data.data) > 0:
            return True
        return False

    def delete(self, primary_keys_values: dict):
        statement = self.hub.table(self.table_name).delete()
        for key in self.primary_keys:
            statement = statement.eq(key, primary_keys_values[key])
        statement.execute()

    def insert(self, fields: dict):
        data = self.hub.table(self.table_name).insert(fields).execute()
        assert len(data.data) == 1
        return data.data[0]


class Instance:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.instance_entity = Entity(hub, "instance", ["id"])
        self.user_instance_entity = Entity(
            hub, "user_instance", ["user_id", "instance_id"]
        )

    def get_or_create(self, storage_id: str):
        instance = self.get()
        if instance is None:
            instance = self.insert(storage_id)
            logger.info("Pushing instance.")
        if not self.user_instance_entity.exists(
            {
                "instance_id": instance["id"],
                "user_id": self.hub.auth.session().user.id.hex,
            }
        ):
            self.user_instance_entity.insert(
                {
                    "instance_id": instance["id"],
                    "user_id": self.hub.auth.session().user.id.hex,
                }
            )
        return instance

    def get(self):
        data = (
            self.hub.table("instance")
            .select("*")
            .eq("name", settings.instance.name)
            .execute()
        )
        if len(data.data) > 0:
            return data.data[0]
        return None

    def delete(self):
        (
            self.hub.table("instance")
            .delete()
            .eq("name", settings.instance.name)
            .execute()
        )

    def insert(self, storage_id: str):
        return self.instance_entity.insert(
            {
                "id": str(uuid.uuid4()),
                "name": settings.instance.name,
                "owner_id": self.hub.auth.session().user.id.hex,
                "storage_id": storage_id,
                "dbconfig": settings.instance._dbconfig,
                "cache_dir": str(settings.instance.cache_dir),
                "sqlite_file": str(settings.instance._sqlite_file),
                "sqlite_file_local": str(settings.instance._sqlite_file_local),
                "db": settings.instance.db,
            }
        )

    def user_count(self, instance_id: str):
        statement = (
            self.hub.table("user_instance").select("*").eq("instance_id", instance_id)
        )
        data = statement.execute()
        return len(data.data)


class UserInstance:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.user_instance_entity = Entity(
            hub, "user_instance", ["user_id", "instance_id"]
        )

    def exists(self, instance_id: str):
        return self.user_instance_entity.exists(
            {"user_id": self.hub.auth.session().user.id.hex, "instance_id": instance_id}
        )

    def delete(self, instance_id: str):
        self.user_instance_entity.delete(
            {"user_id": self.hub.auth.session().user.id.hex, "instance_id": instance_id}
        )

    def insert(self, instance_id: str):
        return self.user_instance_entity.delete(
            {"user_id": self.hub.auth.session().user.id.hex, "instance_id": instance_id}
        )


class Jupynb:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.jupynb_entity = Entity(hub, "jupynb", ["id", "v", "instance_id"])

    def exists(self, id: str, v: str, instance_id: str):
        return self.jupynb_entity.exists({"id": id, "v": v, "instance_id": instance_id})

    def delete(self, id: str, v: str, instance_id: str):
        self.jupynb_entity.delete({"id": id, "v": v, "instance_id": instance_id})

    def insert(
        self,
        id: str,
        v: str,
        name: str,
        instance_id: str,
        time_created: datetime,
        time_updated: datetime,
    ):
        return self.jupynb_entity.insert(
            {
                "id": id,
                "v": v,
                "name": name,
                "instance_id": instance_id,
                "owner_id": self.hub.auth.session().user.id.hex,
                "time_created": time_created.strftime("%Y-%m-%d %H:%M:%S"),
                "time_updated": time_updated.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


class Pipeline:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.pipeline_entity = Entity(hub, "pipeline", ["id", "v", "instance_id"])

    def exists(self, id: str, v: str, instance_id: str):
        return self.pipeline_entity.exists(
            {"id": id, "v": v, "instance_id": instance_id}
        )

    def delete(self, id: str, v: str, instance_id: str):
        self.pipeline_entity.delete({"id": id, "v": v, "instance_id": instance_id})

    def insert(
        self,
        id: str,
        v: str,
        name: str,
        instance_id: str,
        reference: str,
        time_created: datetime,
    ):
        return self.pipeline_entity.insert(
            {
                "id": id,
                "v": v,
                "name": name,
                "instance_id": instance_id,
                "owner_id": self.hub.auth.session().user.id.hex,
                "reference": reference,
                "time_created": time_created.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


class PipelineRun:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.pipeline_run_entity = Entity(hub, "pipeline_run", ["id", "instance_id"])

    def exists(self, id: str, instance_id: str):
        return self.pipeline_run_entity.exists({"id": id, "instance_id": instance_id})

    def delete(self, id: str, instance_id: str):
        self.pipeline_run_entity.delete({"id": id, "instance_id": instance_id})

    def insert(
        self,
        id: str,
        pipeline_id: str,
        pipeline_v: str,
        name: str,
        instance_id: str,
        time_created: datetime,
    ):
        return self.pipeline_run_entity.insert(
            {
                "id": id,
                "pipeline_id": pipeline_id,
                "pipeline_v": pipeline_v,
                "name": name,
                "instance_id": instance_id,
                "owner_id": self.hub.auth.session().user.id.hex,
                "time_created": time_created.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


class Dobject:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.dobject_entity = Entity(hub, "dobject", ["id", "v", "instance_id"])

    def exists(self, id: str, v: str, instance_id: str):
        return self.dobject_entity.exists(
            {"id": id, "v": v, "instance_id": instance_id}
        )

    def delete(self, id: str, v: str, instance_id: str):
        self.dobject_entity.delete({"id": id, "v": v, "instance_id": instance_id})

    def insert(
        self,
        id: str,
        v: str,
        name: str,
        file_suffix: str,
        dtransform_id: str,
        storage_id: str,
        instance_id: str,
        time_created: datetime,
        time_updated: datetime,
    ):
        return self.dobject_entity.insert(
            {
                "id": id,
                "v": v,
                "name": name,
                "file_suffix": file_suffix,
                "dtransform_id": dtransform_id,
                "instance_id": instance_id,
                "storage_id": storage_id,
                "owner_id": self.hub.auth.session().user.id.hex,
                "time_created": time_created.strftime("%Y-%m-%d %H:%M:%S"),
                "time_updated": time_updated.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )


class Dtransform:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.dtransform_entity = Entity(hub, "dtransform", ["id", "instance_id"])

    def exists(self, id: str, instance_id: str):
        return self.dtransform_entity.exists({"id": id, "instance_id": instance_id})

    def delete(self, id: str, instance_id: str):
        self.dtransform_entity.delete({"id": id, "instance_id": instance_id})

    def insert(
        self,
        id: str,
        jupynb_id: str,
        jupynb_v: str,
        instance_id: str,
    ):
        return self.dtransform_entity.insert(
            {
                "id": id,
                "jupynb_id": jupynb_id,
                "jupynb_v": jupynb_v,
                "pipeline_run_id": None,
                "instance_id": instance_id,
                "owner_id": self.hub.auth.session().user.id.hex,
            }
        )


class DtransformIn:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.dtransform_in_entity = Entity(
            hub, "dtransform_in", ["dtransform_id", "dobject_id", "dobject_v"]
        )

    def exists(self, dtransform_id: str, dobject_id: str, dobject_v: str):
        return self.dtransform_in_entity.exists(
            {"id": dtransform_id, "dobject_id": dobject_id, "dobject_v": dobject_v}
        )

    def delete(self, dtransform_id: str, dobject_id: str, dobject_v: str):
        return self.dtransform_in_entity.delete(
            {"id": dtransform_id, "dobject_id": dobject_id, "dobject_v": dobject_v}
        )

    def insert(
        self,
        dtransform_id: str,
        dobject_id: str,
        dobject_v: str,
        instance_id: str,
    ):
        return self.dtransform_in_entity.insert(
            {
                "dtransform_id": dtransform_id,
                "dobject_id": dobject_id,
                "dobject_v": dobject_v,
                "instance_id": instance_id,
                "owner_id": self.hub.auth.session().user.id.hex,
            }
        )


class Storage:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.storage_entity = Entity(hub, "storage", ["id"])

    def exists(self, root: Union[Path, CloudPath, str]):
        statement = self.hub.table("storage").select("*").eq("root", str(root))
        data = statement.execute()
        if len(data.data) > 0:
            return True
        return False

    def delete(self, id: str):
        self.storage_entity.delete(
            {
                "id": id,
            }
        )

    def insert(
        self, id: str, root: Union[Path, CloudPath, str], region: str, type: str
    ):
        return self.storage_entity.insert(
            {
                "id": id,
                "root": str(root),
                "region": region,
                "type": type,
            }
        )

    def instance_count(self, storage_id: str):
        statement = self.hub.table("instance").select("*").eq("storage_id", storage_id)
        data = statement.execute()
        return len(data.data)


class Usage:
    def __init__(self, hub: Client) -> None:
        self.hub = hub
        self.usage_entity = Entity(hub, "usage", ["id"])

    def exists(self, id: str):
        return self.usage_entity.exists(
            {
                "id": str(id),
            }
        )

    def delete(self, id: str):
        self.usage_entity.delete(
            {
                "id": str(id),
            }
        )

    def insert(
        self,
        id: str,
        type: str,
        instance_id: str,
        time: datetime,
        dobject_id: str,
        dobject_v: str,
    ):
        return self.usage_entity.insert(
            {
                "id": id,
                "type": type,
                "owner_id": self.hub.auth.session().user.id.hex,
                "instance_id": instance_id,
                "time": str(time),
                "dobject_id": dobject_id,
                "dobject_v": dobject_v,
            }
        )
