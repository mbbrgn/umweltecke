#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pyarrow.csv as csv


def hnd_read_csv(
    filename, n_header_lines=9, date_format="%Y-%m-%d", date_col_string="Datum"
):
    table = csv.read_csv(
        filename,
        read_options=csv.ReadOptions(
            use_threads=True,
            skip_rows=n_header_lines,
        ),
        parse_options=csv.ParseOptions(delimiter=";", quote_char='"'),
        convert_options=csv.ConvertOptions(decimal_point=","),
    )

    df = table.to_pandas()
    for date in (n for n in df.columns if date_col_string in n):
        # if not isinstance np.datetime[ns] TODO
        df[date] = pd.to_datetime(df[date], format=date_format)
    return df


def dwd_read_csv(filename, date_format="%Y%m%d", date_col_string="MESS_DATUM"):
    table = csv.read_csv(
        filename,
        read_options=csv.ReadOptions(
            use_threads=True,
            skip_rows=0,
        ),
        parse_options=csv.ParseOptions(delimiter=";"),  # , quote_char='"'),
        convert_options=csv.ConvertOptions(
            decimal_point=".",
            strings_can_be_null=True,
            # does not work, why ever, replace below again
            null_values=["  -999" " -999", "-999"],
            # column_types={"MESS_DATUM": pa.string()},
            # timestamp_parsers=[date_format], # not working
        ),
    )

    df = table.to_pandas().replace(-999, float("nan"))
    df.columns = [k.strip() for k in df.columns]
    for date in (n for n in df.columns if date_col_string in n):
        df[date] = pd.to_datetime(df[date], format=date_format)
    return df
