import sqlmodel as sqm
from lamin_logger import logger
from lndb_setup import settings
from supabase import Client


def get_schema_version():
    assert settings.instance._sqlite_file.exists()
    import lnschema_core  # noqa

    with sqm.Session(settings.instance.db_engine()) as session:
        version = session.exec(sqm.select(lnschema_core.version_yvzi)).all()[-1].v
    return version


def check_schema_version(hub: Client):
    current_version = get_schema_version()
    data = hub.table("version_yvzi").select("*").eq("v", current_version).execute()
    assert len(data.data) == 1
    if data.data[0]["require_upgrade"]:
        logger.error("Your core schema module version is not compatible with the hub.")
        logger.info(
            "Did you already migrate your db to core schema v{current_version}? (y/n)"
        )
        logger.info(
            f"If yes, run `lndb_setup._db.insert.version_yvzi({current_version},"
            " db.settings.user.id)`"
        )
        logger.warning(
            "If no, either migrate your instance db schema to version"
            f" {current_version}.\nOr install the latest version."
        )
        raise RuntimeError("hub needs higher lnschema_core_v")
