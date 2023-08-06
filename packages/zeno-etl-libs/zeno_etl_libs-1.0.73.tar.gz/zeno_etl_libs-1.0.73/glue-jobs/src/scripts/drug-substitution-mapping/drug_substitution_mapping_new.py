"""
Owner: kuldeep.singh@zeno.health
Purpose: This script calculates the drug substitutes. Which means, what all drug ids can be
substituted by each other.
And lastly, it is stored in a table.
"""
import argparse
import sys
import os

import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB, MySQL

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-mtp', '--main_table_prefix', default="NA", type=str, required=False)
parser.add_argument('-ttp', '--temp_table_prefix', default="pre", type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
main_table_prefix = args.main_table_prefix
temp_table_prefix = f"-{args.temp_table_prefix}"
main_table_prefix = "" if main_table_prefix == "NA" else main_table_prefix

os.environ['env'] = env
logger = get_logger()

mysql_write_db = MySQL(read_only=False)
mysql_write_db.open_connection()

table_name = "drug-substitution-mapping"
rs_source_schema = "test-generico" if env in ("dev", "stage") else "prod2-generico"
ms_source_schema = "test-generico" if env == "stage" else "prod2-generico"
ms_target_schema = ms_source_schema

temp_table_name = f"`{ms_target_schema}`.`{table_name}{temp_table_prefix}`"
main_table_name = f"`{ms_target_schema}`.`{table_name}{main_table_prefix}`"


def get_drug_groups_mysql():
    """
    Reads the drugs data from mysql database
    """
    mysql_read_db = MySQL()
    mysql_read_db.open_connection()

    query = f"""
    
    SELECT
        `drug-id`,
        GROUP_CONCAT(DISTINCT `molecule-combination`) as combination,
        md5(GROUP_CONCAT(DISTINCT `molecule-combination`)) as `group`
    from
        (
        SELECT
            `drug-id`,
            CONCAT(' name_or_group:' , dm.`molecule-group-or-name` ,
                ' strength:' , dm.`strength-in-smallest-unit` , dm.`smallest-unit` ,
                ' release-pattern:' , `release-pattern-group` , 
                ' available-in:' , `available-in-dose-form-group`) as "molecule-combination"
        from
            (
            select
                d.id as `drug-id`,
                case
                    when (mm.`molecule-group` = ''
                    or mm.`molecule-group` is null) then mm.name
                    else mm.`molecule-group`
                end as `molecule-group-or-name`,
                cmmmm.`unit-type-value` * uomm.`smallest-unit-value` as `strength-in-smallest-unit`,
                uomm.`smallest-unit` as `smallest-unit`,
                case 
                    WHEN d.`release` = 'No' then 'N'
                    WHEN (d.`release` = 'Yes'
                    and rpm.`group` is null) then 'EMPTY'
                    else rpm.`group`
                end as `release-pattern-group`,
                aidfm.`available-group` as `available-in-dose-form-group`
            from
                `{ms_source_schema}`.drugs d
            inner join `{ms_source_schema}`.`composition-master` cm on
                d.`composition-master-id` = cm.id
            inner join `{ms_source_schema}`.`composition-master-molecules-master-mapping` cmmmm on
                cm.id = cmmmm.`composition-master-id`
            inner join `{ms_source_schema}`.`molecule-master` mm on
                mm.id = cmmmm.`molecule-master-id`
            left join `{ms_source_schema}`.`drug-molecule-release` dmr on
                d.id = dmr.`drug-id`
                and cmmmm.`composition-master-id` = dmr.`composition-master-id`
                and cmmmm.`molecule-master-id` = dmr.`molecule-master-id`
            inner join `{ms_source_schema}`.`available-in-group-mapping` aidfm on
                d.`available-in` = aidfm.`available-in`
            left join `{ms_source_schema}`.`release-pattern-master` rpm on
                dmr.`release` = rpm.name
            inner join `{ms_source_schema}`.`unit-of-measurement-master` uomm on
                cmmmm.`unit-type` = uomm.unit
            where
                cmmmm.`unit-type-value` != '') dm
        order by
            2) a
    group by
        a.`drug-id` 
    """

    df = pd.read_sql_query(con=mysql_write_db.connection, sql=query)
    mysql_read_db.close()
    return df


def get_drug_groups_redshift():
    """
    Reads the drugs data from redshift database
    """

    """ read connection """
    db = DB()
    db.open_connection()

    query = f"""
    select
        dm."drug-id",
        listagg(distinct ' name_or_group:' || dm."molecule-group-or-name" || 
        ' strength:' || dm."strength-in-smallest-unit" || dm."smallest-unit" || 
        ' release-pattern:' || "release-pattern-group" || 
        ' available-in:' || "available-in-dose-form-group") within group (
    order by
        dm."molecule-group-or-name") as "combination",
        md5(combination) as "group"
    from
        (
        select
            d.id as "drug-id",
            case
                when (mm."molecule-group" = ''
                or mm."molecule-group" is null) then mm.name
                else mm."molecule-group"
            end as "molecule-group-or-name",
            cmmmm."unit-type-value" * uomm."smallest-unit-value" as "strength-in-smallest-unit",
            uomm."smallest-unit" as "smallest-unit",
            rpm."group" as "release-pattern-group",
            aidfm."available-group" as "available-in-dose-form-group"
        from
            "{rs_source_schema}".drugs d
        inner join "{rs_source_schema}"."composition-master" cm on
            d."composition-master-id" = cm.id
        inner join "{rs_source_schema}"."composition-master-molecules-master-mapping" cmmmm on
            cm.id = cmmmm."composition-master-id"
        inner join "{rs_source_schema}"."molecule-master" mm on
            mm.id = cmmmm."molecule-master-id"
        inner join "{rs_source_schema}"."drug-molecule-release" dmr on
            d.id = dmr."drug-id"
            and cmmmm."molecule-master-id" = dmr."molecule-master-id"
        inner join "{rs_source_schema}"."available-in-dosage-form-mapping" aidfm on
            d."available-in" = aidfm."available-in"
            and d."dosage-form" = aidfm."dosage-form"
        inner join "{rs_source_schema}"."release-pattern-master" rpm on
            dmr."release" = rpm.name
        inner join "{rs_source_schema}"."unit-of-measurement-master" uomm on
            cmmmm."unit-type" = uomm.unit
        where
            cmmmm."unit-type-value" != '') dm
    group by
        dm."drug-id";
    """
    df = db.get_df(query=query)
    db.close_connection()
    return df


# Truncate the temp table before starting
query = f""" delete from  {temp_table_name};"""
mysql_write_db.engine.execute(query)

# drug_group_df = get_drug_groups_redshift()
drug_group_df = get_drug_groups_mysql()
total_count = len(drug_group_df)
logger.info(f"Total drug count: {total_count}")

# store the data in the temp table
drug_group_df.to_sql(
    con=mysql_write_db.engine, name=f"{table_name}{temp_table_prefix}", schema=ms_target_schema,
    if_exists="append", chunksize=500, index=False)

# Delete the data from temp table which is already present in main table
query = f""" DELETE FROM t1 USING {temp_table_name} t1 INNER JOIN {main_table_name} t2 ON
        ( t1.`drug-id` = t2.`drug-id` and t1.group = t2.group); """

response = mysql_write_db.engine.execute(query)
present_correct_count = response.rowcount
logger.info(f"Correct drug-ids count: {present_correct_count}")

# Delete the incorrect substitutes from main table
query = f""" DELETE FROM t1 USING {main_table_name} t1 INNER JOIN {temp_table_name} t2 ON
        ( t1.`drug-id` = t2.`drug-id` );"""

response = mysql_write_db.engine.execute(query)
present_incorrect_count = response.rowcount
logger.info(f"Incorrect drug-ids count: {present_incorrect_count}")

# Now Insert the records in main table
query = f""" INSERT INTO {main_table_name} (`drug-id`, `combination`, `group`)
        SELECT `drug-id`, `combination`, `group` FROM {temp_table_name} """
response = mysql_write_db.engine.execute(query)
new_insert_count = response.rowcount
logger.info(f"Insert/Update drug-ids count: {new_insert_count}")

if total_count == present_correct_count + new_insert_count:
    logger.info("Drug substitute data updated successfully")
else:
    raise Exception("Data count mismatch")
