from datetime import datetime
from typing import List, Union

import pandas as pd

from archimedes.data.common import get_api_base_url_v2
from archimedes.utils import get_end_date, get_start_date
from archimedes.utils.api_request import api
from archimedes.utils.split import get_queries_observation_json
from archimedes.utils.threaded_executor import execute_many
from archimedes.utils.utils import datetime_to_iso_format


def get_intraday_trades(
    price_areas: List[str] = None,
    start: Union[str, pd.Timestamp, datetime, None] = None,
    end: Union[str, pd.Timestamp, datetime, None] = None,
    *,
    access_token: str = None,
):
    """Get raw intraday trades from Archimedes Database

    This function can be used to fetch raw time series from the Archimedes Database
    without any post-processing.
    To see which series are available, use `list_ids()`.

    Example:
        >>> import archimedes
        >>> archimedes.get_intraday_trades(
        >>>     price_areas=["NO1",],
        >>>     start="2020-06-20T04:00:00+00:00",
        >>>     end="2020-06-20T09:00:00+00:00",
        >>> )
                              from_dt                      to_dt          series_id  price  volume                    trade_time buy_area sell_area                                         attributes
        0   2020-06-20T04:00:00+00:00  2020-06-20T05:00:00+00:00  NP/IntradayTrades   7.05     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 7.05, 'buy_area': 'OPX', 'currency':...
        1   2020-06-20T05:00:00+00:00  2020-06-20T06:00:00+00:00  NP/IntradayTrades   6.80     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 6.8, 'buy_area': 'OPX', 'currency': ...
        2   2020-06-20T06:00:00+00:00  2020-06-20T07:00:00+00:00  NP/IntradayTrades   7.75     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 7.75, 'buy_area': 'OPX', 'currency':...
        3   2020-06-20T07:00:00+00:00  2020-06-20T08:00:00+00:00  NP/IntradayTrades   1.70     0.1  2020-06-19T20:20:14.765+0000       FI       NO1  {'price': 1.7, 'buy_area': 'FI', 'currency': '...
        4   2020-06-20T07:00:00+00:00  2020-06-20T08:00:00+00:00  NP/IntradayTrades   8.30     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 8.3, 'buy_area': 'OPX', 'currency': ...
        5   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     2.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        6   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        7   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        8   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        9   2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     0.9  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        10  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        11  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     0.1  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        12  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        13  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        14  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     6.0  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        15  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   2.60     5.1  2020-06-19T20:19:56.057+0000      OPX       NO1  {'price': 2.6, 'buy_area': 'OPX', 'currency': ...
        16  2020-06-20T08:00:00+00:00  2020-06-20T09:00:00+00:00  NP/IntradayTrades   9.90     0.9  2020-06-19T15:55:24.817+0000      OPX       NO1  {'price': 9.9, 'buy_area': 'OPX', 'currency': ...

    Args:
        price_areas (List[str], optional): The price areas to pick, all price areas if None. Defaults to None.
        start (str, optional): The first datetime to fetch (inclusive). Returns all if None. Defaults to None.
        end (str, optional): The last datetime to fetch (exclusive). Returns all if None. Defaults to None.
        access_token (str, optional): None - access token for the API

    Returns:
        DataFrame with all the time series data

    Raises:
        HTTPError: If an HTTP error occurs when requesting the API.
        NoneAuth: If the user is unauthorized or if the authorization has expired.
    """  # pylint:disable=line-too-long

    if isinstance(price_areas, str):
        price_areas = [price_areas]

    start = datetime_to_iso_format(get_start_date(start))
    end = datetime_to_iso_format(get_end_date(end))

    queries = get_queries_observation_json(
        ["NP/IntradayTrades"],
        price_areas,
        start,
        end,
    )

    base_url = get_api_base_url_v2()

    params_array = [
        dict(
            url=f"{base_url}/observation_json/get",
            access_token=access_token,
            params=query,
        )
        for query in queries
    ]

    observation_data = execute_many(api.request, params_array)

    if len(observation_data) == 0:
        return pd.DataFrame(
            columns=[
                "from_dt",
                "to_dt",
                "series_id",
                "version",
                "price",
                "volume",
                "trade_time",
                "buy_area",
                "sell_area",
                "attributes",
            ]
        )
    observation_data = [
        {
            **i,
            "price": i["value"].get("price"),
            "volume": i["value"].get("quantity"),
            "trade_time": i["value"].get("trade_time"),
        }
        for i in observation_data
    ]
    observation_data = pd.DataFrame.from_dict(observation_data)

    # Extracting price area and series id
    observation_data[
        ["series_id1", "series_id2", "buy_area", "sell_area"]
    ] = observation_data["series_id"].str.split("/", 3, expand=True)
    observation_data["series_id"] = (
        observation_data["series_id1"] + "/" + observation_data["series_id2"]
    )
    observation_data["attributes"] = observation_data["value"]
    observation_data["attributes_str"] = observation_data["value"].astype(str)
    observation_data = observation_data.drop_duplicates(
        ["from_dt", "series_id", "attributes_str"]
    )
    observation_data = observation_data.drop(
        ["series_id1", "series_id2", "value", "version", "attributes_str"], axis=1
    )
    observation_data = observation_data.sort_values(by=["from_dt"]).reset_index(
        drop=True
    )

    return observation_data
