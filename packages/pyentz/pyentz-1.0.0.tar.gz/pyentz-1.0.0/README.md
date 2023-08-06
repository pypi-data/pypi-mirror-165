# Custom data wrangling functions.

### This package is built for data scientists/analysts who needs to clean data, and train machine learning / AI models alot. The features in it are critical for Xgboost and Lightgbm models.

### Example usage:

1. As a function:

```python
from pyentz import check_high_corr
list = check_high_corr(df, 0.7)

Return:
["price", "items_sold"]


```


2. Other functions:
    1. inspect_data
    2. inspect_data2
    3. get_cat_col
    4. plot_distribution
    5. check_skew
    6. up_sample
    7. check_high_corr
