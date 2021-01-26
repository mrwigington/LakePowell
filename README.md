# Lake Powell Data

This repo contains software to download data regarding Lake Powell. Lake Powell is the second-largest man-made reservoir in the United States. Since the reservoir was created in 1963 annual surveys of fish populations and daily calculations of atmospheric and lake conditions have been collected. To facilitate the research being done with this data, we developed an application programming interface (API) to make the data easily accessible to everyone. This API pulls recent datasets for fish surveys and lake conditions. It also includes catch per unit effort (CPUE) calculations, graphing functions, and correlation of biotic data with lake conditions. Tutorials that show users how to use various elements of the package are available through Dr. Mark Belk at BYU.

## Installation

```
pip install lakepowell
```

or install from source

```
git pull https://github.com/mrwigington/LakePowell.git
cd LakePowell
pip install -e .
```

## Usage
```
import Fish_data
f = Fish_data.Fish()

fish_data = f.get_fish_data()
water_data = f.get_water_data()

# pandas data tables
print(fish_data.head())
print(fish_data.columns)
print(water_data.head())
```

[See the notebook example here](https://github.com/mrwigington/LakePowell/blob/master/.ipynb_checkpoints/data_descriptor-checkpoint.ipynb)

