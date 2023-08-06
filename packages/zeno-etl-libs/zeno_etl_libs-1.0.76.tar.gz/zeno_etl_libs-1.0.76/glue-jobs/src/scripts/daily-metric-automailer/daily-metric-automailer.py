"""
Author:shubham.gupta@zeno.health, aashish.mishra@zeno.health
Purpose: Daily Review Metrics - Sid
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.parameter.job_parameter import parameter
from zeno_etl_libs.helper.email.email import Email

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default=["shubham.gupta@zeno.health",
                                                  "aashish.mishra@zeno.health"], type=str, required=False)
parser.add_argument('-fr', '--full_run', default=0, type=int, required=False)
args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

job_params = parameter.get_params(job_id=155)

email_to = job_params['email_to']
logger = get_logger()

logger.info(f"env: {env}")

read_schema = "prod2-generico"

rs_db = DB()
rs_db.open_connection()

s3 = S3()

######################################################################
########################## BOGO BILLS ################################
######################################################################

bogo_td_q = f"""
            select
                "line-manager",
                (case 
                    when DATE("created-at") between DATE(date_trunc('month', current_date)) and DATE(dateadd(day,
                    -1,
                    current_date)) then 'MTD'
                    when DATE("created-at") between DATE(date_trunc('month', dateadd(month, -1, current_date))) and DATE(dateadd(day,
                    -1,
                    dateadd(month,
                    -1,
                    current_date))) then 'LMTD'
                    else 'remove'
                end
                ) "td",
                count(distinct case when "promo-code" = 'BOGO' then "bill-id" end) "bogo-bills",
                count(distinct "bill-id") "total-bills",
                round("bogo-bills" * 100.0 / "total-bills", 2) as "bogo %"
            from
                "{read_schema}".sales s
            where
                DATE("created-at") between DATE(date_trunc('month', dateadd(month, -1, current_date))) and DATE(dateadd(day,
                -1,
                current_date))
                and "td" != 'remove'
                and "line-manager" is not null
            group by
                "line-manager",
                "td";
            """

bogo_td = rs_db.get_df(query=bogo_td_q)

bogo_t_q = f"""
            select
                "line-manager",
                (case
                    when DATE("created-at") = DATE(dateadd(day, -1, current_date)) then 'T-1'
                    when DATE("created-at") = DATE(dateadd(day, -2, current_date)) then 'T-2'
                    when DATE("created-at") = DATE(dateadd(day, -3, current_date)) then 'T-3'
                end) as "T",
                count(distinct case when "promo-code" = 'BOGO' then "bill-id" end) "bogo-bills",
                count(distinct "bill-id") "total-bills",
                round("bogo-bills" * 100.0 / "total-bills", 2) as "bogo %"
            from
                "{read_schema}".sales s
            where
                date("created-at") between DATE(dateadd(day, -3, current_date)) and DATE(dateadd(day, -1, current_date))
                and "line-manager" is not null
            group by
                "line-manager", "T";
            """

bogo_t = rs_db.get_df(query=bogo_t_q)
bogo_td['bogo %'] = bogo_td['bogo %'].astype(float)
bogo_t['bogo %'] = bogo_t['bogo %'].astype(float)

bogo1 = pd.pivot_table(data=bogo_td, index='line-manager', columns='td', values='bogo %', aggfunc='mean').reset_index()
bogo2 = pd.pivot_table(data=bogo_t, index='line-manager', columns='t', values='bogo %', aggfunc='mean').reset_index()

bogo = pd.merge(bogo1, bogo2, how='left', on='line-manager').fillna(0)
bogo = bogo.rename(columns={'line-manager': 'Name'})

######################################################################
########################## Diagnostic Sales ##########################
######################################################################

diagnostic_td_q = f"""
                select
                    sm."line-manager", 
                    (case 
                        when DATE("date") between DATE(date_trunc('month', current_date)) and DATE(dateadd(day,
                        -1,
                        current_date)) then 'MTD'
                        when DATE("date") between DATE(date_trunc('month', dateadd(month, -1, current_date))) and DATE(dateadd(day,
                        -1,
                        dateadd(month,
                        -1,
                        current_date))) then 'LMTD'
                        else 'remove'
                    end
                    ) "td",
                    sum("total-sales") as "sales"
                from
                    "{read_schema}"."diagnostic-visibility" dv
                left join "{read_schema}"."stores-master" sm on
                    sm.id = dv."store-id"
                where
                    "td" != 'remove'
                group by
                    sm."line-manager",
                    "td";
                """

diagnostic_t_q = f"""
                select
                    sm."line-manager", 
                    (case
                        when DATE("date") = DATE(dateadd(day,
                        -1,
                        current_date)) then 'T-1'
                        when DATE("date") = DATE(dateadd(day,
                        -2,
                        current_date)) then 'T-2'
                        when DATE("date") = DATE(dateadd(day,
                        -3,
                        current_date)) then 'T-3'
                    end) as "T",
                    sum("total-sales") as "sales"
                from
                    "{read_schema}"."diagnostic-visibility" dv
                left join "{read_schema}"."stores-master" sm on
                    sm.id = dv."store-id"
                where
                    "T" != 'remove'
                group by
                    sm."line-manager",
                    "T";
                """

diagnostic_td = rs_db.get_df(diagnostic_td_q)
diagnostic_t = rs_db.get_df(diagnostic_t_q)

diagnostic_td['line-manager'] = diagnostic_td['line-manager'].fillna('OPS/APP')
diagnostic_t['line-manager'] = diagnostic_t['line-manager'].fillna('OPS/APP')

diagnostic_td['sales'] = diagnostic_td['sales'].astype(float)
diagnostic_t['sales'] = diagnostic_t['sales'].astype(float)
diagnostic1 = pd.pivot_table(data=diagnostic_td, index='line-manager', columns='td', values='sales',
                             aggfunc='sum').reset_index()
diagnostic2 = pd.pivot_table(data=diagnostic_t, index='line-manager', columns='t', values='sales',
                             aggfunc='sum').reset_index()

diagnostic = pd.merge(diagnostic1, diagnostic2, how='left', on='line-manager').fillna(0)
diagnostic = diagnostic.rename(columns={'line-manager': 'Name'})

######################################################################
########################## PR A1 A2 ##################################
######################################################################

pr_q = f"""
            select
                pm."line-manager",
                doi."drug-grade",
                count(distinct "order-number") "PR Count",
                round(sum("selling-rate" * quantity), 2) "PR Value"
            from
                "{read_schema}"."patient-requests-metadata" pm
            inner join "{read_schema}"."drug-order-info" doi on
                pm."store-id" = doi."store-id"
                and pm."drug-id" = doi."drug-id"
            where
                doi."drug-grade" in ('A1', 'A2')
                and
                date(pm."created-at") = DATE(dateadd(day, -1, current_date))
                and "line-manager" is not null
            group by
                pm."line-manager",
                doi."drug-grade";
        """

pr = rs_db.get_df(pr_q)

pr['pr value'] = pr['pr value'].astype(float)

pr = pd.pivot_table(data=pr,
                    index='line-manager',
                    columns='drug-grade',
                    values=['pr count', 'pr value'], margins='sum', margins_name='Total').reset_index()
pr = pr.rename(columns={'line-manager': 'Name'})

######################################################################
########################## MIN Bases OOS A1 A2 B #####################
######################################################################

min_oos_q = f"""
            select
                sm."line-manager",
                x1."drug-grade",
                avg(case
                    when "total-quantity"<"min"
                    or "total-quantity" = 0 then 100.0
                    else 0.0
                end) "oos-min-count"
            from
                (
                select
                    "store-id",
                    "drug-id",
                    "drug-grade",
                    "min"
                from
                    "{read_schema}"."drug-order-info" doi
                where
                    "drug-grade" in ('A1', 'A2', 'B')
                    and "max" > 0) x1
            inner join (
                select
                    "store-id",
                    "drug-id",
                    sum(quantity) "total-quantity"
                from
                    "{read_schema}"."inventory-1" i
                group by
                    "store-id",
                    "drug-id") x2 on
                x1."store-id" = x2."store-id"
                and
                x1."drug-id" = x2."drug-id"
            left join "{read_schema}"."stores-master" sm on
                x1."store-id" = sm.id
            group by
                sm."line-manager",
                x1."drug-grade";
            """

min_oos = rs_db.get_df(min_oos_q)

min_oos['oos-min-count'] = min_oos['oos-min-count'].astype('float')
min_oos = pd.pivot_table(data=min_oos,
                         index='line-manager',
                         columns='drug-grade',
                         values=['oos-min-count']).reset_index()

min_oos = min_oos.rename(columns={'line-manager': 'Name'})

######################################################################
########################## PR FF Rate ################################
######################################################################

pr_ff_q = """
            select
                a."patient-id" as "patient-id",
                a."line-manager", 
                (a."month-created-at") as "month",
                (a."year-created-at") as "year",
                CURRENT_TIMESTAMP as "refreshed_at",
                a."store-name" as "store-name",
                a."drug-name" as "drug-name",
                case
                    when ((date_part(hour, a."created-at") = '23')
                    or (date_part(hour, a."created-at") < '14') )then '1stR'
                    else '2ndR'
                end as "Round",
                -- -- Fulfillment on invoice-- -- 
                case
                    when DATE(a."invoiced-at") is null then
                    'Pending'
                    -- FOFO
                    -- Sunday-Friday
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."invoiced-at") <= 0 then 'ontime'
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."invoiced-at") = 1
                    and date_part(hour, a."invoiced-at") <= 15 then 'ontime'
                    -- Saturday 
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."invoiced-at") <= 1 then 'ontime'
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."invoiced-at") = 2
                    and date_part(hour, a."invoiced-at") <= 15 then 'ontime'
                    -- COCO in Surat, Satara
                    -- Sunday-Friday
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") <= 0 then 'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 1
                    and date_part(hour, a."invoiced-at") <= 15 then 'ontime'
                    -- Friday,Saturday 
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") <= 1 then 'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 2
                    and date_part(hour, a."invoiced-at") <= 15 then 'ontime'
                    -- COCO Except Surat, Satara
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 0
                    and date_part(hour, a."invoiced-at") <= '21' then 
                        'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 0 then
                            'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 1
                    and date_part(hour, a."invoiced-at") <= '21' then
                                'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 0 then
                                    'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 1
                    and date_part(hour, a."invoiced-at") <= '16' then
                                        'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 0
                    and date_part(hour, a."invoiced-at") <= '21' then
                                            'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") <= 1 then
                                                'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 2
                    and date_part(hour, a."invoiced-at") <= '16' then
                                                    'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Sunday'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") <= 1 then
                                                        'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Sunday'
                    and DATEDIFF(day,
                    a."created-at",
                    a."invoiced-at") = 2
                    and date_part(hour, a."invoiced-at") <= '16' then
                                                            'ontime'
                    else
                                                            'delayed'
                end as "fullfilment on invoice",
                -- -- Fulfillment on dispatch-- --   
                case
                    when DATE(a."dispatched-at") is null then 'Pending'
                    -- FOFO
                    -- Sunday-Friday
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."dispatched-at") <= 0 then 'ontime'
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."dispatched-at") = 1
                    and date_part(hour, a."dispatched-at") <= 23 then 'ontime'
                    -- staurday
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."dispatched-at") <= 1 then 'ontime'
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."dispatched-at") = 2
                    and date_part(hour, a."dispatched-at") <= 23 then 'ontime'
                    -- COCO In Surat and Satara
                    -- sunday-friday
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") <= 0 then 'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 1
                    and date_part(hour, a."dispatched-at") <= 23 then 'ontime'
                    -- staurday
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") <= 1 then 'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 2
                    and date_part(hour, a."dispatched-at") <= 23 then 'ontime'
                    -- COCO Except Surat, Satara
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 0 then
                        'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 1
                    and date_part(hour, a."dispatched-at") <= '10' then
                            'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 0 then
                                'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 1 then
                                    'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 2
                    and date_part(hour, a."dispatched-at") <= '10' then
                                        'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 0 then
                                            'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 1
                    and date_part(hour, a."dispatched-at") <= '17' then
                                                'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 0 then
                                                    'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 1
                    and date_part(hour, a."dispatched-at") <= '10' then
                                                        'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") <= 1 then
                                                            'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 2
                    and date_part(hour, a."dispatched-at") <= '17' then
                                                                'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Sunday'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") <= 1 then
                                                                    'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" not in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Sunday'
                    and DATEDIFF(day,
                    a."created-at",
                    a."dispatched-at") = 2
                    and date_part(hour, a."dispatched-at") <= '17' then
                                                                        'ontime'
                    else
                                                                        'delayed'
                end as "fullfilment on dispatch",
                -- -- Fulfillment on delivery-- --                                          
                    case
                    when DATE(a."store-delivered-at") is null then
                    'Pending'
                    -- FOFO
                    -- Sunday-Thursday
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) not in ('Friday', 'Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."store-delivered-at") <= 1 then 'ontime'
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) not in ( 'Friday', 'Saturday' )
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."store-delivered-at") = 2
                    and date_part(hour, a."store-delivered-at") <= 23 then 'ontime'
                    -- Friday, staurday
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) in ('Friday', 'Saturday' )
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."store-delivered-at") <= 2 then 'ontime'
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) in ( 'Friday', 'Saturday' )
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."store-delivered-at") = 3
                    and date_part(hour, a."store-delivered-at") <= 23 then 'ontime'
                    -- COCO In Surat and Satara
                    -- sunday-friday
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") <= 1 then 'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 2
                    and date_part(hour, a."store-delivered-at") <= 23 then 'ontime'
                    -- staurday
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") <= 2 then 'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 3
                    and date_part(hour, a."store-delivered-at") <= 23 then 'ontime'
                    -- COCO Except Surat, Satara  
                    when date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 0 then
                        'ontime'
                    when date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 1
                    and date_part(hour, a."store-delivered-at") <= '11' then
                            'ontime'
                    when (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 0 then
                                'ontime'
                    when (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 1 then
                                    'ontime'
                    when (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 2
                    and date_part(hour, a."store-delivered-at") <= '11' then
                                        'ontime'
                    when date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 0 then
                                            'ontime'
                    when date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 1
                    and date_part(hour, a."store-delivered-at") <= '19' then
                                                'ontime'
                    when (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 0 then
                                                    'ontime'
                    when (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 1
                    and date_part(hour, a."store-delivered-at") <= '12' then
                                                        'ontime'
                    when (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") <= 1 then
                                                            'ontime'
                    when (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 2
                    and date_part(hour, a."store-delivered-at") <= '19' then
                                                                'ontime'
                    when (trim(' ' from to_char(a."created-at", 'Day'))) = 'Sunday'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") <= 1 then
                                                                    'ontime'
                    when (trim(' ' from to_char(a."created-at", 'Day'))) = 'Sunday'
                    and DATEDIFF(day,
                    a."created-at",
                    a."store-delivered-at") = 2
                    and date_part(hour, a."store-delivered-at") <= '19' then
                                                                        'ontime'
                    else
                                                                        'delayed'
                end as "fullfilment on delivery",
                -- -- Order Timing-- --                                      
                    case
                    when DATE(a."ordered-at") is null then 'not ordered'
                    -- FOFO
                    -- Sunday-Friday 
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."ordered-at") <= 0 then 'ontime'
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."ordered-at") = 0
                    and date_part(hour, a."ordered-at") <= 23 then 'ontime'
                    --  staurday
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."ordered-at") <= 0 then 'ontime'
                    when s."franchisee-id" != 1
                    and (trim(' ' from to_char(fofo_approved_at."presaved_approved_at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."ordered-at") = 1
                    and date_part(hour, a."ordered-at") <= 23 then 'ontime'
                    -- COCO In Surat and Satara
                    -- sunday-friday
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") <= 0 then 'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 0
                    and date_part(hour, a."ordered-at") <= 23 then 'ontime'
                    -- staurday
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") <= 1 then 'ontime'
                    when s."franchisee-id" = 1
                    and s."city-id" in (1018, 876)
                    and (trim(' ' from to_char(a."created-at", 'Day'))) in ('Saturday')
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 1
                    and date_part(hour, a."ordered-at") <= 23 then 'ontime'
                    -- COCO Except Surat, Satara 
                    when DATE(a."ordered-at") is not null
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 0
                    and date_part(hour, a."ordered-at") <= '15' then
                    'ontime'
                    when DATE(a."ordered-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday' , 'Sunday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 0 then
                        'ontime'
                    when DATE(a."ordered-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Saturday' , 'Sunday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 1
                    and date_part(hour, a."ordered-at") <= '15' then
                            'ontime'
                    when DATE(a."ordered-at") is not null
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 0 then
                                'ontime'
                    when DATE(a."ordered-at") is not null
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 1
                    and date_part(hour, a."ordered-at") <= '01' then
                                    'ontime'
                    when DATE(a."ordered-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 0
                    and date_part(hour, a."ordered-at") <= '15' then
                                        'ontime'
                    when DATE(a."ordered-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 0 then
                                            'ontime'
                    when DATE(a."ordered-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 1 then
                                                'ontime'
                    when DATE(a."ordered-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 2
                    and date_part(hour, a."ordered-at") <= '01' then
                                                    'ontime'
                    when DATE(a."ordered-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Sunday'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 0 then
                                                        'ontime'
                    when DATE(a."ordered-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Sunday'
                    and DATEDIFF(day,
                    a."created-at",
                    a."ordered-at") = 1
                    and date_part(hour, a."ordered-at") <= '01' then
                                                            'ontime'
                    else
                                                                'delayed'
                end as "ordered timing",
                -- -- Reorder Timimng-- -- 
                case
                    when DATE(a."re-ordered-at") is null then
                        'not reordered'
                    when date(a."re-ordered-at") is not null
                    and s."franchisee-id" = 1
                    and DATEDIFF(day,
                    a."created-at",
                    a."re-ordered-at") <= 1
                        then 'ontime'
                    when date(a."re-ordered-at") is not null
                    and s."franchisee-id" != 1
                    and DATEDIFF(day,
                    fofo_approved_at."presaved_approved_at",
                    a."re-ordered-at") <= 1
                            then 'ontime'
                    else 'delayed'
                end as "re-ordered timing",
                -- -- Completed Issue -- -- 
                case
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is null
                    and date_part(hour, a."created-at") <= '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."completed-at") = 0
                    and (date_part(hour, a."completed-at")) <= '21' then 
                    'completed-early'
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."completed-at") = 0 then
                        'completed-early'
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) not in ('Sunday' , 'Saturday')
                    and date_part(hour, a."created-at") > '23'
                    and DATEDIFF(day,
                    a."created-at",
                    a."completed-at") = 1
                    and (date_part(hour, a."completed-at")) <= '21' then
                            'completed-early'
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is not null
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."completed-at") = 0 then
                                'completed-early'
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is not null
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."completed-at") = 1
                    and (date_part(hour, a."completed-at")) <= '16' then 
                                    'completed-early'
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and DATEDIFF(day,
                    a."created-at",
                    a."completed-at") = 0
                    and date_part(hour, a."created-at") <= '14'
                    and (date_part(hour, a."completed-at")) <= '21' then
                                        'completed-early'
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."completed-at") <= 1 then
                                            'completed-early'
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Saturday'
                    and date_part(hour, a."created-at") > '14'
                    and DATEDIFF(day,
                    a."created-at",
                    a."completed-at") = 2
                    and (date_part(hour, a."completed-at")) <= '16' then
                                                'completed-early'
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is not null
                    and (trim(' ' from to_char(a."created-at", 'Day'))) = 'Sunday'
                    and DATEDIFF(day,
                    a."completed-at",
                    a."created-at") <= 1 then
                                                    'completed-early'
                    when DATE(a."invoiced-at") is null
                    and DATE(a."completed-at") is not null
                    and DATEDIFF(day,
                    a."created-at",
                    a."completed-at") = 2
                    and (date_part(hour, a."completed-at")) <= '16' then
                                                        'completed-early'
                    else
                                                        'no issue'
                end as "completed issues",
                a."sb-status" as "status",
                a."pso-requested-quantity" as "requested-quantity",
                a."quantity" as "quantity",
                a."required-quantity" as "required-quantity",
                DATE(a."created-at") as "created-at",
                DATE(a."ordered-at") as "ordered-at",
                DATE(a."invoiced-at") as "invoiced-at",
                DATE(a."dispatched-at") as "dispatched-at",
                DATE(a."received-at") as "received-at",
                DATE(a."completed-at") as "completed-at",
                DATE(dtm."delivered-at") as "delivered-at" ,
                a."created-at" as "created-time",
                a."ordered-at" as "ordered-time",
                a."invoiced-at" as "invoiced-time",
                a."dispatched-at" as "dispatch-time",
                dtm."delivered-at" as "delivered-time",
                a."completed-at" as "completed-time",
                a."decline-reason" as "decline reason",
                a."type",
                a."store-id",
                a."drug-id",
                a."company",
                a."franchisee-short-book",
                e."drug-grade",
                f."name" as "received distributor",
                case
                    when a."store-id" >= 146 then 'new'
                    else 'old'
                end as "store-type",
                j."forward-dc-id",
                ss."name" as "dc_name",
                a."store-delivered-at",
                case
                    when p."patient-category" != 'others' then 1
                    else 0
                end as premium_flag,
                a."completion-type" ,
                s."franchisee-id",
                s."city-id" ,
                fofo_approved_at."presaved_approved_at",
                zc."name" as "city-name",
                a."re-ordered-at"
            from
                "prod2-generico"."prod2-generico"."patient-requests-metadata" a
            left join
                "prod2-generico"."prod2-generico"."drug-order-info" e on
                e."store-id" = a."store-id"
                and e."drug-id" = a."drug-id"
            left join
                "prod2-generico"."prod2-generico"."distributors" f on
                NVL(a."ordered-distributor-id", 0) = f."id"
            left join
                (
                select
                    *
                from
                    "prod2-generico"."prod2-generico"."store-dc-mapping"
                where
                    "drug-type" = 'ethical') j on
                j."store-id" = a."store-id"
            left join
                "prod2-generico"."prod2-generico"."stores" ss on
                ss."id" = j."forward-dc-id"
            left join 
                "prod2-generico"."prod2-generico"."delivery-tracking-metadata" dtm
                    on
                dtm.id = a.id
            left join 
                "prod2-generico"."prod2-generico"."patients" p
                    on
                a."patient-id" = p.id
            left join "prod2-generico"."prod2-generico".stores s
                  on
                s.id = a."store-id"
            left join "prod2-generico"."prod2-generico"."zeno-city" zc on
                s."city-id" = zc.id
            left join (
                select
                                sbol."short-book-id" ,
                                min(sbol."created-at") as "presaved_approved_at"
                from
                                "prod2-generico"."prod2-generico"."short-book-order-logs" sbol
                left join "prod2-generico"."prod2-generico"."short-book-1" sb2 
                                on
                                sb2.id = sbol."short-book-id"
                left join "prod2-generico"."prod2-generico".stores s2 
                                on
                                s2.id = sb2."store-id"
                where
                                s2."franchisee-id" != 1
                    and sbol.status not in ('presaved', 'lost', 'failed', 'declined', 'deleted')
                group by
                                sbol."short-book-id"
                            )fofo_approved_at
                        on
                fofo_approved_at."short-book-id" = a."sb-id"
            where
                DATE(a."created-at") = DATE(dateadd(day, -2, current_date))
                and (a."quantity" > 0
                    or a."completion-type" = 'stock-transfer')
                and a."sb-status" not in ('deleted', 'presaved')
            """

pr_ff = rs_db.get_df(pr_ff_q)

pr_ff['ff_quntity'] = np.where(pr_ff['fullfilment on delivery'] == 'ontime', pr_ff['quantity'], 0)

pr_ff_rate = pr_ff.groupby(['store-id', 'line-manager'], as_index=False).agg({'ff_quntity': 'sum', 'quantity': 'sum'})
pr_ff_rate['ff_rate'] = pr_ff_rate['ff_quntity'] / pr_ff_rate['quantity']


def pr_ff_cat(x):
    if x < 0.75:
        return '<75%'
    if x <= 0.8:
        return '75-80%'
    else:
        return '80%+'


pr_ff_rate['ff_rat_cat'] = pr_ff_rate['ff_rate'].apply(pr_ff_cat)

ff_rate = pd.pivot_table(data=pr_ff_rate, index='line-manager', columns='ff_rat_cat', values='store-id',
                         aggfunc='nunique')

ff_rate = ff_rate[['80%+', '75-80%', '<75%']]

file_name = 'Daily Metrics.xlsx'
file_path = s3.write_df_to_excel(data={'BOGO': bogo,
                                       'Diagnostic Sales': diagnostic.round(),
                                       'PR A1 A2': pr.round(),
                                       'Min Based OOS': min_oos, 'PR FF': ff_rate
                                       }, file_name=file_name)

email = Email()
email.send_email_file(subject="Daily Report",
                      mail_body=f'Hey ! Here is your store daily metrics tracker report',
                      to_emails=email_to, file_uris=[], file_paths=[file_path])
