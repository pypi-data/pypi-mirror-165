# ESPN-Statsguru-Scraper


## Introduction

An easy-to-use python scraper to pull all-time cricket statistics from ESPN Cricinfo.


## Prerequisites

### Python requirements

* You need to install Python with version 3.4 or more. You can find the latest version of Python at https://www.python.org/downloads/

* Install the library as follows.

```
pip install espncricket
```

## How to run the code

```
import espncricket.ESPN as ESPN

df = ESPN().get_score()
print(df.head())
```

### By default it returns Test batting statistics for men only.
### But, you can also tweak following parameters to get custom results of your own choice.

* match_type='ODI_Women'
* data_type='bowling'
* view_type="series"
* number_of_pages=10

```

ESPN_object = ESPN(match_type='ODI_Women', data_type='bowling', view_type="series")
odi_batting_scores_for_women_per_series_with_10_pages_only = ESPN_object.get_score(number_of_pages)
```

* After successful execution, a pandas dataframe object is returned.


## License Information

Please refer "LICENSE" file to know the license details.
Before reusing the code, please take a written permission from me.
You can contact me at sanketpatole1994@outlook.com

