import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from sklearn.utils import resample



######################## Inspect data ########################
##############################################################
def inspect_data(df: str) -> pd.DataFrame:
    """This function inspect data type, unique values, the amount of unique values, null amount, percentage of null.
    e.g. `inspect_data(df)`

    Args:
        df (pandas.core.frame): The name of the dataframe, e.g. `dfA`

    Returns:
        dataframe: A dataframe of summary with dType, unique amount, uniques, null amount, null percentage.
    """
    return pd.DataFrame(
        {
            "data_type": df.dtypes,
            "unique_amount": df.apply(lambda x:len(x.unique()), axis=0),
            "uniques": df.apply(lambda x:x.unique(), axis=0),
            "missing_amount": df.apply(lambda x: x.isnull().sum(), axis=0),
            "missing_percent": df.apply(lambda x: x.isnull().sum() * 100 / len(x))
        }
    )




######################## Inspect data 2 ########################
##############################################################
def inspect_data2(df: str) -> pd.DataFrame:
    """This function inspect unique values, missing values.
    e.g. `inspect_data(df)`

    Args:
        df (pandas.core.frame): The name of the dataframe, e.g. `dfA`

    Returns:
        dataframe: A dataframe of summary with percentage of null amount, and unique.
    """
    
    # missing values
    total_missing = df.isnull().sum().sort_values(ascending = False)
    percent_missing = (df.isnull().sum()/df.isnull().count()*100).sort_values(ascending = False)
    missing = pd.concat([total_missing, percent_missing], axis=1, keys=['total', 'percent'])
    
    #unique values 
    total_data = df.count()
    tt = pd.DataFrame(total_data)
    tt.columns = ['total']
    uniques = []
    for col in df.columns:
        unique = df[col].nunique()
        uniques.append(unique)
    tt['uniques'] = uniques
    unique = tt 
    return pd.concat([missing, unique], axis=1, keys=['missing', 'unique'])




######################## Get cat col ########################
##############################################################
def get_cat_col(df: str):
    """Get the categorical column names, and numerical column names.
    e.g. `cat, num = get_cat_col(df)`


    Args:
        data (pandas.core.frame): The name of the dataframe, e.g. `dfA`

    Returns:
        cat, num: A list of categorical column names, and a list of numerical column names.
    """

    num = list(df._get_numeric_data().columns)
    cat = [cat for cat in  df.columns if cat not in (num)]
    print(f"numerical features : {num}\ntotal numerical : {len(num)}\n\ncategorical features : {cat}\n total categorical: {len(cat)}")
    return cat , num





######################## plot distribution ########################
##############################################################
def plot_distribution(df:str , col_list:str):
    """ This function will plot the distribution of features with seaborn, and pyplt.
    e.g. `plot_distribution(df, list)`

    Args:
        df (str): The name of the dataframe, e.g. `dfA`
        col_list (str): a list of numeric col. Get it with `list(dfA._get_numeric_data().columns)`.
    """
    list_size = len(col_list)
    m = len(col_list)//2 +1
    n = 2
    if list_size > 2:
        fig , ax = plt.subplots(m , n,figsize=(20,24))
        for i , c in enumerate(col_list):
            if i< m:
                sns.histplot(data=df , x = c  , ax= ax[i,0] ) 
                ax[i,0].axvline(df[c].median(),color='r', linestyle=':')
                ax[i,0].axvline(np.mean(df[c]),color='b', linestyle='-')

            else :
                sns.histplot(data=df , x = c , ax= ax[i-m,1] )
                ax[i-m,1].axvline(df[c].median(),color='r', linestyle=':')
                ax[i-m,1].axvline(np.mean(df[c]),color='b', linestyle='-')
    else:
        print("Error: the dataframe has only one col to be plot. \nThis function needs 2 or more numerical columns to work.")




######################## check skew ########################
##############################################################

def check_skew(df:str):
    """returns kurtosis, and skewness of an observation. e.g. `check_skew(df.colA)`

    Args:
        col (str): A column name of a dataframe, e.g. `df.colA`

    Returns: Same as df.col.skew()

    """
    df.plot.box(figsize=(5,5), rot=90)
    if stats.kurtosis(df) > 0:
        print(f"The column has a skinny-tall bell, Kurtosis={round(stats.kurtosis(df),2)}." + '\n')
    elif stats.kurtosis(df) < 0:
        print(f"The column has a fat-bottom bell, Kurtosis={round(stats.kurtosis(df),2)}." + '\n')
    elif stats.kurtosis(df) == 1:
        print(f"The column has a normal bell, Kurtosis={round(stats.kurtosis(df),2)}." + '\n')

    if stats.skew(df) > 0:
        print(f"The column has a heavy head, skewness={round(stats.skew(df),2)}." + '\n')
    elif stats.skew(df) < 0:
        print(f"The column has a heavy tail, skewness={round(stats.skew(df),2)}." + '\n')
    elif stats.skew(df) == 1:
        print(f"The column has an evenly spread tail, skewness={round(stats.skew(df),2)}." + '\n')



######################## Upsample ########################
##############################################################
def up_sample(df:str, ycol:str) -> pd.DataFrame:
    """return a datarame after upsampling the target ycol. e.g. `up_sample(df, "ycol")`

    Args:
        df (str): The name of the dataframe, e.g. `dfA`

        ycol (str): The name of the target col, or Y col, e.g. `target`

    Returns:
        A datarame after upsampling the target ycol. 
    """

    # find out the name and quanitty of the majority of the targets
    maj_name = df[ycol].value_counts().sort_values(ascending=False).index[0]
    maj_amt = df[ycol].value_counts().sort_values(ascending=False).iloc[0]
    # and make a df of the majority
    df_majority = df[(df[ycol] == maj_name)] 

    # get the list of minority targets:
    all_target_list = list(df[ycol].unique())
    majority_list = []
    majority_list.append(maj_name)

    # this dict will hold all re-sampled df
    df_dict = {}

    # a for loop of all targets, minus the majority
    # = [i for i in A if i not in B]
    for i in set(all_target_list).difference(majority_list):
        _df = df[df[ycol] == i]
        df_dict[i] = resample(_df,
                            replace = True,
                            n_samples = maj_amt,
                            random_state = 42)


    # Convert a dict of minority classes dataframes into one big df, and drop the key of the dictionary, and the indexes during concat
    new_df = pd.concat(df_dict, axis=0).reset_index().iloc[:,2:]


    # Combine majority class with upsampled minority classes
    upsampled_df = pd.concat([new_df, df_majority]).reset_index(drop=True)

    return upsampled_df




######################## Check high correlation ########################
##############################################################
def check_high_corr (df:str, corr_value:float):
    """Check dimensions with high correlation as specified in the 2nd param.
    e.g. `check_high_corr(df, 0.7)`


    Args:
        df (str): The name of the dataframe, e.g. `dfA`
        corr_value (float): e.g. 0.8, 0.6...

    Returns:
        This function will return a list of paired dimensions with correlation higher than the 2nd param.
    """
    corr_matrix = df.corr().abs()
    # this numpy is the coordinates corr_matrix>0.8
    high_corr_var=np.where(corr_matrix>corr_value) 
    high_corr_var=[(corr_matrix.columns[x],corr_matrix.columns[y]) for x,y in zip(*high_corr_var) if x!=y and x<y]
    return high_corr_var

