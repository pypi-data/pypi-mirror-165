import lnschema_core as schema
import sqlmodel as sqm
from lamin_logger import logger
from lndb_setup import settings
from lndb_setup._hub import connect_hub
from supabase import Client

from ._entities import Entities
from ._schema import check_schema_version


def get_hub_with_authentication():
    hub = connect_hub()
    session = hub.auth.sign_in(
        email=settings.user.email, password=settings.user.password
    )
    hub.postgrest.auth(session.access_token)
    check_schema_version(hub)
    return hub


class hub:
    """Access the hub."""

    @classmethod
    def _load_entity(cls, entity):
        # we need to do this right now as we can't do a cyclic import
        # we first need to import all of lamindb (including load)
        # then lndb_hub is imported
        # once it's imported load can be imported here
        from lamindb.db._query import query

        return query.table_as_df(entity)

    @classmethod
    def push_instance(cls):
        """Push instance with all dobjects."""
        hub = get_hub_with_authentication()
        dobject_df = cls._load_entity("dobject")
        for id, v in dobject_df.index:
            cls.push_dobject(id, v, hub)

    @classmethod
    def push_dobject(cls, id: str, v: str = "1", hub: Client = None):
        """Push a single dobject."""
        if hub is None:
            hub = get_hub_with_authentication()
        entities = Entities(hub)
        with sqm.Session(settings.instance.db_engine()) as session:
            storage = session.exec(
                sqm.select(schema.storage).where(
                    schema.storage.root == str(settings.instance.storage_dir)
                )
            ).first()
            assert storage
            cls.__push_storage(entities, storage)

            instance = entities.instance.get_or_create(storage.id)

            dobject = session.get(schema.dobject, (id, v))
            assert dobject

            dtransform = session.get(schema.dtransform, dobject.dtransform_id)
            assert dtransform

            dtransform_ins = session.exec(
                sqm.select(schema.dtransform_in)
                .where(schema.dtransform_in.dobject_id == dobject.id)
                .where(schema.dtransform_in.dobject_v == dobject.v)
            ).all()

            jupynb = session.get(
                schema.jupynb, (dtransform.jupynb_id, dtransform.jupynb_v)
            )

            pipeline_run = session.get(schema.pipeline_run, dtransform.pipeline_run_id)

            usages = session.exec(
                sqm.select(schema.usage)
                .where(schema.usage.dobject_id == dobject.id)
                .where(schema.usage.dobject_v == dobject.v)
            ).all()

        assert jupynb or pipeline_run
        if jupynb:
            cls.__push_jupynb(entities, jupynb, instance["id"])
        if pipeline_run:
            pipeline = session.get(
                schema.pipeline, (pipeline_run.pipeline_id, pipeline_run.pipeline_v)
            )
            assert pipeline
            cls.__push_pipeline(entities, pipeline, instance["id"])
            cls.__push_pipeline_run(entities, pipeline_run, instance["id"])
        cls.__push_dtransform(entities, dtransform, instance["id"])
        cls.__push_dobject(entities, dobject, instance["id"])
        for dtransform_in in dtransform_ins:
            cls.__push_dtransform_in(entities, dtransform_in, instance["id"])
        for usage in usages:
            cls.__push_usage(entities, usage, instance["id"])

    @classmethod
    def delete_instance(cls):
        """Delete the instance on the hub."""
        hub = get_hub_with_authentication()
        entities = Entities(hub)
        instance = entities.instance.get()
        dobject_df = cls._load_entity("dobject")
        usage_df = cls._load_entity("usage")
        dtransform_in_df = cls._load_entity("dtransform_in")
        jupynb_df = cls._load_entity("jupynb")
        dtransform_df = cls._load_entity("dtransform")
        pipeline_df = cls._load_entity("pipeline")
        pipeline_run_df = cls._load_entity("pipeline_run")
        storage_df = cls._load_entity("storage")
        for id, v in dobject_df.index:
            logger.info(f"Delete dobject ({id}, {v}).")
            for dtransform_id in dtransform_in_df[
                (dtransform_in_df["dobject_id"] == id)
                & (dtransform_in_df["dobject_v"] == v)  # noqa
            ]["dtransform_id"].values:
                entities.dtransform_in.delete(dtransform_id, id, v)
            for usage_id in usage_df[
                (usage_df["dobject_id"] == id) & (usage_df["dobject_v"] == v)
            ].index:
                entities.usage.delete(usage_id)
            entities.dobject.delete(id, v, instance["id"])
        for id in dtransform_df.index:
            logger.info(f"Delete dtransform ({id}).")
            entities.dtransform.delete(id, instance["id"])
        for id, v in jupynb_df.index:
            logger.info(f"Delete jupynb ({id}, {v}).")
            entities.jupynb.delete(id, v, instance["id"])
        for id in pipeline_run_df.index:
            logger.info(f"Delete pipeline run ({id}).")
            entities.pipeline_run.delete(id, instance["id"])
        for id, v in pipeline_df.index:
            logger.info(f"Delete pipeline ({id}, {v}).")
            entities.pipeline.delete(id, v, instance["id"])
        entities.user_instance.delete(instance["id"])
        if entities.instance.user_count(instance["id"]) == 0:
            entities.instance.delete()
        for id in storage_df.index:
            logger.info(f"Delete storage ({id}).")
            if entities.storage.instance_count(id) == 0:
                entities.storage.delete(id)

    @classmethod
    def __push_storage(cls, entities: Entities, storage: schema.storage):
        if not entities.storage.exists(storage.root):
            logger.info(f"Push storage ({storage.root}).")
            entities.storage.insert(
                storage.id,
                storage.root,
                storage.region,
                storage.type,
            )
        else:
            logger.warning(
                f"storage ({storage.root}) already exists and is not pushed."
            )

    @classmethod
    def __push_dtransform(
        cls, entities: Entities, dtransform: schema.dtransform, instance_id: str
    ):
        if not entities.dtransform.exists(dtransform.id, instance_id):
            logger.info(f"Push dtransform ({dtransform.id}).")
            entities.dtransform.insert(
                dtransform.id, dtransform.jupynb_id, dtransform.jupynb_v, instance_id
            )
        else:
            logger.warning(
                f"dtransform ({dtransform.id}) already exists and is not pushed."
            )

    @classmethod
    def __push_jupynb(cls, entities: Entities, jupynb: schema.jupynb, instance_id: str):
        if not entities.jupynb.exists(jupynb.id, jupynb.v, instance_id):
            logger.info(f"Push jupynb ({jupynb.id}, {jupynb.v}).")
            entities.jupynb.insert(
                jupynb.id,
                jupynb.v,
                jupynb.name,
                instance_id,
                jupynb.time_created,
                jupynb.time_updated,
            )
        else:
            logger.warning(
                f"jupynb ({jupynb.id}, {jupynb.v}) already exists and is not pushed."
            )

    @classmethod
    def __push_pipeline(
        cls, entities: Entities, pipeline: schema.pipeline, instance_id: str
    ):
        if not entities.pipeline.exists(pipeline.id, pipeline.v, instance_id):
            logger.info(f"Push pipeline ({pipeline.id}, {pipeline.v}).")
            entities.pipeline.insert(
                pipeline.id,
                pipeline.v,
                pipeline.name,
                instance_id,
                pipeline.reference,
                pipeline.time_created,
            )
        else:
            logger.warning(
                f"pipeline ({pipeline.id}, {pipeline.v}) already exists and is not"
                " pushed."
            )

    @classmethod
    def __push_pipeline_run(
        cls, entities: Entities, pipeline_run: schema.pipeline_run, instance_id: str
    ):
        if not entities.pipeline_run.exists(pipeline_run.id, instance_id):
            logger.info(f"Push pipeline_run ({pipeline_run.id}).")
            entities.pipeline_run.insert(
                pipeline_run.id,
                pipeline_run.pipeline_id,
                pipeline_run.pipeline_v,
                pipeline_run.name,
                instance_id,
                pipeline_run.time_created,
            )
        else:
            logger.warning(
                f"pipeline ({pipeline_run.id}) already exists and is not pushed."
            )

    @classmethod
    def __push_dobject(
        cls, entities: Entities, dobject: schema.dobject, instance_id: str
    ):
        if not entities.dobject.exists(dobject.id, dobject.v, instance_id):
            logger.info(f"Push dobject ({dobject.id}, {dobject.v}).")
            entities.dobject.insert(
                dobject.id,
                dobject.v,
                dobject.name,
                dobject.file_suffix,
                dobject.dtransform_id,
                dobject.storage_id,
                instance_id,
                dobject.time_created,
                dobject.time_updated,
            )
        else:
            logger.warning(
                f"dobject ({dobject.id}, {dobject.v}) already exists and is not pushed."
            )

    @classmethod
    def __push_dtransform_in(
        cls, entities: Entities, dtransform_in: schema.dtransform_in, instance_id: str
    ):
        if not entities.dtransform_in.exists(
            dtransform_in.dtransform_id,
            dtransform_in.dobject_id,
            dtransform_in.dobject_v,
        ):
            entities.dtransform_in.insert(
                dtransform_in.dtransform_id,
                dtransform_in.dobject_id,
                dtransform_in.dobject_v,
                instance_id,
            )

    @classmethod
    def __push_usage(cls, entities: Entities, usage: schema.usage, instance_id: str):
        if not entities.usage.exists(usage.id):
            entities.usage.insert(
                usage.id,
                usage.type,
                instance_id,
                usage.time,
                usage.dobject_id,
                usage.dobject_v,
            )
