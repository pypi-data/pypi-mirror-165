# Copyright 2022 Airwallex.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
import pydeequ
from pydeequ.analyzers import *

import sys
sys.path.append("..")

from vivqu.quality_check import *
from vivqu.visualize import *
from sender import *
from datetime import datetime, timedelta

from load import load_gcloud_bq

from vivqu.quality_check.verification import *
from vivqu.loader import *

NoDup = lambda name: (Uniqueness([name]), lambda x: x == 1, f"{name} has no Duplicate value")
NoNull = lambda name: (Completeness(name), lambda x: x == 1, f"{name} has no NULL value")

constraint_all = [
    NoDup("ID"),
    NoNull("Normalized_amount_USD"),
    NoNull("Transaction_Type_Raw"),
    NoNull("Transaction_Status_Raw"),
    NoNull("Datetime_created"),
    NoNull("Booking_account_ID"),
    NoNull("Booking_Legal_Entity_ID"),
    NoNull("Booking_Legal_Entity_Name_Local"),
    NoNull("Booking_Legal_Entity_Name_English"),
    NoNull("Booking_Legal_Entity_Owningentity"),
]

constraint_transdir_in = [
    NoNull("Beneficiary_internal_account_ID"),
    NoNull("Beneficiary_Legal_Entity_ID"),
    NoNull("Beneficiary_full_name"),
    NoNull("Beneficiary_type"),
    NoNull("Credit_amount_currency"),
]

constraint_transdir_out = [
    NoNull("Originator_internal_account_ID"),
    NoNull("Originator_Legal_Entitiy_ID"),
    NoNull("Originator_type"),
    NoNull("Originator_full_name"),
    NoNull("Original_amount_currency"),
]


column_dtype_checklist = [
    ("ID", str),
    ("Normalized_amount_USD", float),
    ("Transaction_Type_Raw", str),
    ("Transaction_Status_Raw", str),
    ("Datetime_created", "^[0-9]{4}-[0-9]{2}-[0-9]{2}"),
    ("Booking_account_ID", str),
    ("Booking_Legal_Entity_ID", str),
    ("Booking_Legal_Entity_Name_Local", str),
    ("Booking_Legal_Entity_Name_English", str),
    ("Booking_Legal_Entity_Owningentity", str),

    ("Beneficiary_internal_account_ID", str),
    ("Beneficiary_Legal_Entity_ID", str),
    ("Beneficiary_full_name", str),
    ("Beneficiary_type", str),
    ("Credit_amount_currency", str),

    ("Originator_internal_account_ID", str),
    ("Originator_Legal_Entitiy_ID", str),
    ("Originator_type", str),
    ("Originator_full_name", str),
    ("Original_amount_currency", str),
]

select_cols = [
    "ID",
    "Normalized_amount_USD",
    "Transaction_Type_Raw",
    "Transaction_Status_Raw",
    "Datetime_created",
    "Booking_account_ID",
    "Booking_Legal_Entity_ID",
    "Booking_Legal_Entity_Name_Local",
    "Booking_Legal_Entity_Name_English",
    "Booking_Legal_Entity_Owningentity",
    "Beneficiary_internal_account_ID",
    "Beneficiary_Legal_Entity_ID",
    "Beneficiary_full_name",
    "Beneficiary_type",
    "Credit_amount_currency",
    "Originator_internal_account_ID",
    "Originator_Legal_Entitiy_ID",
    "Originator_type",
    "Originator_full_name",
    "Original_amount_currency",
    "Transaction_Direction",
]


def get_period_data(start_date, end_date, select_cols=None, limit=None) -> pd.DataFrame:
    df = load_gcloud_bq(
        "awx-dw.dwa_risk.risk_unified_transactions",
        "Datetime_created",
        (f"{start_date}", f"{end_date}"),
        select_cols,
        limit
    )
    return df


def verify_all_constraints(
    verifier: Verifier, 
    df_all
):
    result = []
    result += verifier.verify(
        df_all, 
        constraint_all
    )
    result += verifier.verify(
        df_all[df_all["Transaction_Direction"] == "IN"], 
        constraint_transdir_in
    )
    result += verifier.verify(
        df_all[df_all["Transaction_Direction"] == "OUT"], 
        constraint_transdir_out
    )
    return result


def generate_msg(result):
    idx = 0
    msg = ""
    for constr in constraint_all:
        if result[idx] == True:
            msg += f"[Success] {constr[2]}\n"
        else:
            msg += f"[Failed]  {constr[2]}\n"
        idx += 1

    for constr in constraint_transdir_in:
        if result[idx] == True:
            msg += f"[Success] {constr[2]}\n"
        else:
            msg += f"[Failed]  {constr[2]}\n"
        idx += 1

    for constr in constraint_transdir_out:
        if result[idx] == True:
            msg += f"[Success] {constr[2]}\n"
        else:
            msg += f"[Failed]  {constr[2]}\n"
        idx += 1
    return msg


if __name__ == "__main__":
    # create spark session and create checker and verifier
    spark_session = (
        SparkSession.builder
        .config("spark.jars.packages", pydeequ.deequ_maven_coord)
        .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
        .getOrCreate()
        )
    checker = QualityChecker(spark_session)
    verifier = Verifier(checker)

    # select columns in check_list
    # select_cols = [col_name for (col_name, _dtype) in column_dtype_checklist]
    yesterday_str = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')
    df_all = get_period_data(yesterday_str, yesterday_str, select_cols)
    # df_all.to_csv(yesterday_str + ".csv")
    df_all = pd.read_csv("../example/test-2022-08-30.csv")[select_cols]

    # check if all values in specific columns have right type
    new_df, error_df, error_dict = \
        verifier.check_type(df_all, column_dtype_checklist, "ID")

    # new_df.to_csv("new_df.csv", index=False)
    error_df.to_csv("error_df.csv", index=False)
    with open("error_dict.json", "w") as fp:
        fp.write(json.dumps(error_dict, indent=4))
    
    result = verify_all_constraints(verifier, new_df)
    msg = generate_msg(result)
    print(msg)

# normal_titles = [
#         "ID","Booking_account_ID","Booking_Legal_Entity_ID","Booking_Legal_Entity_Name_Local","Booking_Legal_Entity_Name_English",
#         "Booking_Legal_Entity_Owningentity","Booking_account_Owner_Org_Level","Transaction_Domain","Transaction_Type_Raw","Transaction_Direction",
#         "Originator_internal_account_ID","Originator_Legal_Entitiy_ID","Beneficiary_internal_account_ID","Beneficiary_Legal_Entity_ID",
#         "Transaction_Status_Raw","Datetime_created","Transaction_method","Transaction_moneyhouse","Transaction_ID","Transaction_reference",
#         "Transaction_reason","Credit_amount_USD","Credit_amount_currency","Credit_amount_orig_ccy","Credit_Inverse_USD","Original_amount_USD",
#         "Original_amount_currency","Original_amount_orig_ccy","Original_Inverse_USD","Originator_full_name","Originator_standardized_full_name",
#         "Originator_cleansed_full_name","Originator_type","Originator_country","Originator_address","Originator_bank_country","Originator_bank_name",
#         "Originator_external_bank_account_number","Originator_card_scheme","Originator_Card_BIN","Originator_Card_last_4_digits","Originator_card_type",
#         "Originator_card_Fingerprint","Originator_category_code","Beneficiary_full_name",      "Beneficiary_type",
#         "Beneficiary_Country","Beneficiary_address","Beneficiary_bank_country","Beneficiary_bank_name","Beneficiary_external_Bank_Account_Number",
#         "Beneficiary_IBAN","Beneficiary_card_scheme","Beneficiary_Card_BIN","Beneficiary_Card_last_4_digits",        "Beneficiary_card_Fingerprint",
#         "Beneficiary_category_code","GTPN_inChannelWhiteList","GTPN_sameClientSign","GlobalAccountId",
#         "PA_providerOriginalResponseCode","ISS_Request_authcode","ISS_i2c_transaction_id","Normalized_amount_USD","Realtime_RFI","Realtime_result"
# ]

# empty_titles = [
#         "Beneficiary_standardized_full_name",
#         "Beneficiary_card_type"
# ]