import urllib.request
import zipfile

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00360/AirQualityUCI.zip"
hf = "fhdkfj"

urllib.request.urlretrieve(url, "air.zip")
with zipfile.ZipFile("air.zip") as z:
  z.extractall(".")
print("Done!")

