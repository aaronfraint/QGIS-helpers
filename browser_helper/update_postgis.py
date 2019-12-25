"""
Summary of ``update_postgis.py``
--------------------------------

Use the database connections defined in postGIS_tools.get_postGIS_config()
to add DB connections under PostGIS within the QGIS Browser.

"""

from qgis.PyQt.QtCore import QSettings
from qgis.utils import iface

import postGIS_tools


def remove_all_connections() -> None:
    """ Remove all entries under PostGIS in the Browser """
    qs = QSettings()

    for k in sorted(qs.allKeys()):
        if "PostgreSQL/connections/" in k:
            qs.remove(k)

    iface.reloadConnections()


def sync_postgis_config(
    dbs_to_ignore: list = ["defaultdb", "_dodb"],
    remove_existing: bool = True,
) -> None:
    """
    Add a database connection for all DBs that exist on the clusters
    defined in the user's config.txt

    For more details, see postGIS_tools.get_postGIS_config()

    :param dbs_to_ignore: list of databases to skip creating entries for
    :param remove_existing: if True, start by removing the user's DB list
    """

    if remove_existing:
        remove_all_connections()

    # Read the user's config.txt
    config, super_config = postGIS_tools.get_postGIS_config()

    # Iterate over each host defined in the file
    for host in config:

        this_config = config[host]

        # Get a list of all databases on the host host cluster
        super_uri = postGIS_tools.make_uri(**super_config[host])
        db_list = postGIS_tools.get_database_list(super_uri, debug=False)

        for db in db_list:

            if db not in dbs_to_ignore:

                # Define the name it will show in the QGIS Browser
                entry = f"{db} {host.upper()}"

                values = {
                    "database": db,
                    "host": this_config["host"],
                    "port": this_config["port"],
                    "username": this_config["username"],
                    "password": this_config["password"],
                    "projectsInDatabase": "true",
                    "savePassword": "true",
                    "saveUsername": "true"
                }

                if "sslmode" in this_config:
                    values["sslmode"] = this_config["sslmode"]

                for value_name in values:
                    val = values[value_name]
                    QSettings().setValue(f"PostgreSQL/connections/{entry}/{value_name}", val)

    iface.reloadConnections()
