import requests
from pathlib import Path 
import tarfile
import io
import pandas as pd
from typing import IO, cast

url = "https://github.com/ageron/data/raw/main/housing.tgz"
response = requests.get(url)


if response.status_code == 200:
    with tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz") as housing_tarball:
        housing_csv_bytes = housing_tarball.extractfile("housing/housing.csv")

        housing_csv_bytes = cast(IO[bytes], housing_csv_bytes)

        housing_df: pd.DataFrame = pd.read_csv(housing_csv_bytes)
else:
    print("Failed to download the data.")


folder_path = Path("data")
Path(folder_path).mkdir(parents=True, exist_ok=True)
housing_df.to_parquet(f"{folder_path}/housing.parquet", compression="zstd", index=False)