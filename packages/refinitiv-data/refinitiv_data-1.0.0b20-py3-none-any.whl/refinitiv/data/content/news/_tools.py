from typing import Callable, List, TYPE_CHECKING, Union

import pandas as pd

from ..._tools._dataframe import convert_str_to_datetime
from ...eikon._tools import tz_replacer

if TYPE_CHECKING:
    from ._data_classes import Headline, HeadlineUDF


def news_build_df_udf(content_data, **kwargs) -> pd.DataFrame:
    columns = ["versionCreated", "text", "storyId", "sourceCode"]

    raw_headlines = content_data.get("headlines", [])
    index = [
        convert_str_to_datetime(tz_replacer(raw_headline["firstCreated"]))
        for raw_headline in raw_headlines
    ]

    data = [
        [raw_headline[column] for column in columns] for raw_headline in raw_headlines
    ]
    if data:
        df = pd.DataFrame(
            data=data,
            index=index,
            columns=columns,
        )
        df = df.convert_dtypes()

    else:
        df = pd.DataFrame([], index, columns)

    return df


def news_build_df_rdp(raw: dict, **kwargs) -> pd.DataFrame:
    columns = ["versionCreated", "text", "storyId", "sourceCode"]

    if isinstance(raw, list):
        content_data = []

        for i in raw:
            content_data.extend(i["data"])

    else:
        content_data = raw["data"]

    index = [
        convert_str_to_datetime(
            tz_replacer(headline["newsItem"]["itemMeta"]["firstCreated"]["$"])
        )
        for headline in content_data
    ]

    data = []

    for headline_data in content_data:
        news_item = headline_data.get("newsItem", dict())
        item_meta = news_item.get("itemMeta", {})
        info_sources = news_item["contentMeta"]["infoSource"]
        info_source = next(
            (
                item["_qcode"]
                for item in info_sources
                if item["_role"] == "sRole:source"
            ),
            None,
        )
        version_created = convert_str_to_datetime(item_meta["versionCreated"]["$"])
        data.append(
            [
                version_created,
                item_meta["title"][0]["$"],
                headline_data["storyId"],
                info_source,
            ]
        )
    if data:
        df = pd.DataFrame(
            data=data,
            index=index,
            columns=columns,
        )
        df = df.convert_dtypes()

    else:
        df = pd.DataFrame([], columns=columns)

    return df


def _get_text_from_story(story: dict) -> str:
    news_item = story.get("newsItem", dict())
    content_set = news_item.get("contentSet", dict())
    inline_data = content_set.get("inlineData", [dict()])
    return inline_data[0].get("$")


def _get_headline_from_story(story: dict) -> str:
    news_item = story.get("newsItem", dict())
    content_meta = news_item.get("contentMeta", dict())
    headline = content_meta.get("headline", [dict()])
    return headline[0].get("$")


def get_headlines(
    raw: dict,
    build_headline: Callable[[dict], Union["Headline", "HeadlineUDF"]],
    limit: int,
) -> List[Union["Headline", "HeadlineUDF"]]:
    headlines = []

    if isinstance(raw, list):

        data = []
        for i in raw:
            data.extend(i.get("data", i.get("headlines", [])))

    else:
        data = raw.get("data", raw.get("headlines", []))

    for datum in data:
        headline = build_headline(datum)
        headlines.append(headline)

    headlines = headlines[:limit]
    return headlines
