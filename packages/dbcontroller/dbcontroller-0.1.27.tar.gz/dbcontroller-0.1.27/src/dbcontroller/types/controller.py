"""
    Database Controller
"""
import dataclasses as dc
import functools
import typing

from .dbmanager import Database


@dc.dataclass
class DatabaseController:
    """Single Controller"""

    engine: str
    model: typing.Any
    admin: typing.Any


@dc.dataclass
class Controller:
    """Full Controller"""

    sql: typing.Any
    mongo: typing.Any


def create_database_manager(
    all_models: list, engine_type: str = None, active_db: typing.Any = None
):
    """Create a { Database Manager }"""
    if not isinstance(all_models, list):
        all_models = [all_models]
    match engine_type:
        case "sql":
            manager = active_db.manage(all_models).sql
        case "mongo":
            manager = active_db.manage(all_models).mongo
    return manager


def create_database(engine_type: str, url: str, fastberry: bool = False):
    """Create a { Database }"""
    active_db = None
    out_db = None
    match engine_type:
        case "sql":
            active_db = Database(sql=url, fastberry=fastberry)
            active_admin = functools.partial(
                create_database_manager, engine_type=engine_type, active_db=active_db
            )
            out_db = DatabaseController(
                engine=engine_type, model=active_db.model.sql, admin=active_admin
            )
        case "mongo":
            active_db = Database(mongo=url, fastberry=fastberry)
            active_admin = functools.partial(
                create_database_manager, engine_type=engine_type, active_db=active_db
            )
            out_db = DatabaseController(
                engine=engine_type, model=active_db.model.mongo, admin=active_admin
            )
    return out_db


def process_databases(
    databases: dict, engine_type: str = "sql", fastberry: bool = False
):
    """Process all { Databases }"""
    active_db = databases.get(engine_type)
    all_dbs_manager = {}
    if active_db:
        db_name = "default"
        db_url = active_db.get(db_name)
        all_dbs_manager[db_name] = create_database(engine_type, db_url, fastberry)
        for db_name, db_url in active_db.items():
            if db_name != "default":
                manager = create_database(engine_type, db_url, fastberry)
                all_dbs_manager[db_name] = manager
    return all_dbs_manager


def create_controllers(databases, fastberry: bool = False):
    """Controller Builder"""
    mongo_dbs = process_databases(databases, "mongo", fastberry=fastberry)
    sql_dbs = process_databases(databases, "sql", fastberry=fastberry)
    return Controller(sql=sql_dbs, mongo=mongo_dbs)
