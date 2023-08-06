######################################################################################################################
# Copyright (C) 2017-2021 Spine project consortium
# This file is part of Spine Items.
# Spine Items is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

"""
Importer's execute kernel (do_work), as target for a multiprocess.Process

:authors: M. Marin (KTH)
:date:   6.11.2020
"""

import os
import spinedb_api
from spinedb_api.import_mapping.type_conversion import value_to_convert_spec
from spine_engine.utils.helpers import create_log_file_timestamp


def do_work(
    mapping, cancel_on_error, purge_before_writing, on_conflict, logs_dir, sources, connector, urls_downstream, logger
):
    all_data = []
    all_errors = []
    table_mappings = {
        name: mappings
        for name, mappings in mapping.get("table_mappings", {}).items()
        if name in mapping["selected_tables"]
    }
    table_options = {
        name: options
        for name, options in mapping.get("table_options", {}).items()
        if name in mapping["selected_tables"]
    }
    table_column_convert_specs = {
        tn: {int(col): value_to_convert_spec(spec) for col, spec in cols.items()}
        for tn, cols in mapping.get("table_types", {}).items()
    }
    table_row_convert_specs = {
        tn: {int(col): value_to_convert_spec(spec) for col, spec in cols.items()}
        for tn, cols in mapping.get("table_row_types", {}).items()
    }
    for src in sources:
        file_anchor = f"<a style='color:#BB99FF;' title='{src}' href='file:///{src}'>{os.path.basename(src)}</a>"
        logger.msg.emit("Importing " + file_anchor)
        try:
            connector.connect_to_source(src)
        except Exception as error:  # pylint: disable=broad-except
            logger.msg_error.emit(f"Failed to connect to {file_anchor}: {error}")
            return False,
        for name, mappings in table_mappings.items():
            logger.msg.emit(f"Processing table <b>{name}</b>")
            for spec in mappings:
                mapping_name = next(iter(spec.keys()))
                logger.msg.emit(f"* Applying mapping <b>{mapping_name}</b>...")
                try:
                    data, errors = connector.get_mapped_data(
                        {name: [spec]}, table_options, table_column_convert_specs, table_row_convert_specs
                    )
                except spinedb_api.InvalidMapping as error:
                    logger.msg_error.emit(f"Failed to import: {error}")
                    if cancel_on_error:
                        logger.msg_error.emit("Cancel import on error has been set. Bailing out.")
                        return False,
                    logger.msg_warning.emit("Ignoring errors. Set Cancel import on error to bail out instead.")
                    continue
                if not errors:
                    logger.msg.emit(f"Successful ({sum(len(d) for d in data.values())} data to be written).")
                else:
                    logger.msg_warning.emit(
                        f"Read {sum(len(d) for d in data.values())} data with {len(errors)} errors."
                    )
                all_data.append(data)
                all_errors.extend(errors)
    if all_errors:
        # Log errors in a time stamped file into the logs directory
        timestamp = create_log_file_timestamp()
        logfilepath = os.path.abspath(os.path.join(logs_dir, timestamp + "_read_error.log"))
        with open(logfilepath, "w") as f:
            for err in all_errors:
                f.write(f"{err}\n")
        # Make error log file anchor with path as tooltip
        logfile_anchor = (
            "<a style='color:#BB99FF;' title='" + logfilepath + "' href='file:///" + logfilepath + "'>Error log</a>"
        )
        logger.msg_error.emit(logfile_anchor)
        if cancel_on_error:
            logger.msg_error.emit("Cancel import on error has been set. Bailing out.")
            return False,
        logger.msg_warning.emit("Ignoring errors. Set Cancel import on error to bail out instead.")
    if all_data:
        import cProfile
        profile = cProfile.Profile()
        profile.enable()
        for url in urls_downstream:
            success = _import_data_to_url(
                cancel_on_error, purge_before_writing, on_conflict, logs_dir, all_data, url, logger
            )
            if not success and cancel_on_error:
                return False,
        profile.disable()
        profile.dump_stats(r"c:\data\Importer_profile.stats")
    return True,


def _import_data_to_url(cancel_on_error, purge_before_writing, on_conflict, logs_dir, all_data, url, logger):
    if purge_before_writing:
        spinedb_api.create_new_spine_database(url)
    try:
        db_map = spinedb_api.DatabaseMapping(url, upgrade=False, username="Importer")
    except (spinedb_api.SpineDBAPIError, spinedb_api.SpineDBVersionError) as err:
        logger.msg_error.emit(f"Unable to create database mapping, all import operations will be omitted: {err}")
        return False
    all_import_errors = []
    all_import_num = 0
    for data in all_data:
        import_num, import_errors = spinedb_api.import_data(db_map, on_conflict=on_conflict, **data)
        all_import_errors += import_errors
        if import_errors:
            logger.msg_error.emit("Errors while importing a table.")
            if cancel_on_error:
                logger.msg_error.emit("Cancel import on error is set. Bailing out.")
                if db_map.has_pending_changes():
                    logger.msg_error.emit("Rolling back changes.")
                    db_map.rollback_session()
                break
            logger.msg_warning.emit("Ignoring errors. Set Cancel import on error to bail out instead.")
        all_import_num += import_num
    if db_map.has_pending_changes():
        db_map.commit_session("Import data by Spine Toolbox Importer")
        logger.msg_success.emit(
            f"Inserted {all_import_num} data with {len(all_import_errors)} errors into {db_map.codename}"
        )
    else:
        logger.msg_warning.emit("No new data imported")
    db_map.connection.close()
    if all_import_errors:
        # Log errors in a time stamped file into the logs directory
        timestamp = create_log_file_timestamp()
        logfilepath = os.path.abspath(os.path.join(logs_dir, timestamp + "_import_error.log"))
        with open(logfilepath, "w") as f:
            for err in all_import_errors:
                f.write(str(err) + "\n")
        # Make error log file anchor with path as tooltip
        logfile_anchor = (
            "<a style='color:#BB99FF;' title='" + logfilepath + "' href='file:///" + logfilepath + "'>Error log</a>"
        )
        logger.msg_error.emit(logfile_anchor)
        return False
    return True
