from pathlib import Path
from typing import Union

import pandas as pd


def _parse_datetime_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Finds datetime columns in the DataFrame and converts them to datetime

    Args:
        df: pandas.DataFrame
    Returns:
        :class:`pandas.DataFrame` with datetime columns converted according to standard
        AEMO
        format
    """
    dt_cols = {
        "DATETIME",
        "EFFECTIVEDATE",
        "INTERVAL_DATETIME",
        "RUN_DATETIME",
        "AUTHORISEDDATE",
        "LASTCHANGED",
        "VERSION_DATETIME",
        "DAY",
        "PUBLISH_DATETIME",
        "LATEST_OFFER_DATETIME",
        "STARTDATE",
        "ENDDATE",
        "PERIOD_ENDING",
        "GENCONID_EFFECTIVEDATE",
        "BIDSETTLEMENTDATE",
        "SETTLEMENTDATE",
        "OFFERDATE",
    }
    dt_cols_present = dt_cols.intersection(set(df.columns.tolist()))
    dt_format = "%Y/%m/%d %H:%M:%S"
    for col in dt_cols_present:
        df.loc[:, col] = pd.to_datetime(df[col], format=dt_format)
    return df


def _parse_id_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Finds relevant ID columns in the DataFrame and converts them to cateogries

    Args:
        df: pandas.DataFrame
    Returns:
        :class:`pandas.DataFrame` with ID columns converted to categories
    """
    id_cols = {
        "CONSTRAINTID",
        "INTERCONNECTORID",
        "DUID",
        "CONNECTIONPOINTID",
        "PARTICIPANTID",
        "EXPORTGENCONID",
        "IMPORTGENCONID",
        "REGIONID",
    }
    id_cols_present = id_cols.intersection(set(df.columns.tolist()))
    for col in id_cols_present:
        df.loc[:, col] = df[col].astype("category")
    return df


def _parse_predispatch_seq_no(df: pd.DataFrame) -> pd.DataFrame:
    """Parses `PREDISPATCHSEQNO` as datetime and adds `PREDISPATCH_RUN_DATETIME`

    Args:
        df: pandas.DataFrame
    Returns:
        :class:`pandas.DataFrame` with additional column `PREDISPATCH_RUN_DATETIME`
    """
    df["PREDISPATCHSEQNO"] = df["PREDISPATCHSEQNO"].astype(int).astype(str)
    parsed = df["PREDISPATCHSEQNO"].str.extract(r"^([0-9]{8})([0-9]{2})$")
    year_month_day = pd.to_datetime(parsed[0], format="%Y%m%d")
    hour_min = ((parsed[1].astype(int) - 1) * pd.Timedelta(minutes=30)).add(
        pd.Timedelta(hours=4, minutes=30)
    )
    df["PREDISPATCH_RUN_DATETIME"] = year_month_day + hour_min  # type: ignore
    return df


def clean_forecast_csv(filepath_or_buffer: Union[str, Path]) -> pd.DataFrame:
    """Given a forecast csv filepath or buffer, reads and cleans the forecast csv.

    Cleans artefacts in the forecast csv files.

    Args:
        filepath_or_buffer: As for :func:`pandas.read_csv`
    Returns:
        Cleaned :class:`pandas.DataFrame` with forecast data
    """
    # skip AEMO metadata
    df = pd.read_csv(filepath_or_buffer, skiprows=1, low_memory=False)
    # remove end of report line
    df = df.iloc[0:-1, :]
    drop_cols = df.columns.tolist()[0:4]
    df = df.drop(drop_cols, axis="columns")
    df = _parse_datetime_cols(df)
    df = _parse_id_cols(df)
    if "PREDISPATCHSEQNO" in df.columns:
        df = _parse_predispatch_seq_no(df)
    return df
