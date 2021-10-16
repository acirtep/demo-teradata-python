import pandas as pd

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', None)  # or 199

input_file = "/usr/src/app/demo_data/index_2011_1000.csv"

df_index_2011 = pd.read_csv(input_file)
print(f"Datatypes:\n{df_index_2011.dtypes} \n\n")
print(f"DF counts:\n{df_index_2011.count()} \n\n")
for column in df_index_2011.select_dtypes(["object"]).columns:
    print(f"{column} has max length \
        {df_index_2011[column].str.len().max()}")

column_list = list(df_index_2011.columns)

import giraffez
td_connection = {
    "host": "",
    "username": "",
    "password": ""
}

"""
Create table based on the description of the data
INT64 = BIGINT
OBJECT = VARCHAR
"""

create_ddl = "create multiset table demo_teradata_python.index_2011_1000(\
    RETURN_ID         BIGINT, \
    FILING_TYPE      VARCHAR(5), \
    EIN               BIGINT, \
    TAX_PERIOD        BIGINT, \
    SUB_DATE         VARCHAR(22), \
    TAXPAYER_NAME    VARCHAR(100), \
    RETURN_TYPE      VARCHAR(5), \
    DLN               BIGINT, \
    OBJECT_ID         BIGINT)"

with giraffez.Cmd(**td_connection) as cmd:
    cmd.execute(create_ddl)
    show_ddl = cmd.execute("SHOW TABLE demo_teradata_python.index_2011_1000")
    print(list(show_ddl))

with giraffez.Cmd(**td_connection) as cmd:
    cmd.insert(
        table_name="demo_teradata_python.index_2011_1000",
        fields=column_list,
        rows=input_file,
        delimiter=",",
    )

export_file = "/usr/src/app/demo_data/index_2011_agg.json"
with giraffez.BulkExport('demo_teradata_python.index_2011_agg', **td_connection) as export:
    with open(export_file, "w") as f:
        for row in export.to_json():
            f.write(row)

import json
with open(export_file) as json_file:
    data = json.load(json_file)
