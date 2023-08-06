"""Utils useful for testing."""

import logging
import pandas as pd


logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def download_wine_quality_data() -> pd.DataFrame:
    """Read the wine-quality csv file from the URL."""
    csv_url = (
        "http://archive.ics.uci.edu/"
        "ml/machine-learning-databases/wine-quality/winequality-red.csv"
    )
    try:
        data = pd.read_csv(csv_url, sep=";")
    except ConnectionError as ecx:
        logger.exception(
            "Unable to download training & test CSV, "
            "check your internet connection. Error: %s",
            ecx,
        )
    return data


def remove_mean(data: pd.DataFrame, column: str = None) -> pd.DataFrame:
    """For the `column`, remove the mean. If column is None, remove for all."""
    if column is None:
        data -= data.mean(axis=0)
    else:
        data[column] -= data[column].mean()
    return data
