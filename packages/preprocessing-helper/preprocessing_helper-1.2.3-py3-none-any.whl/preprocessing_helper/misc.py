import logging
import numpy as np
import pandas as pd
from typing import Any, Callable, List
import re
# List all files in a database
# List all files matching a certain pattern


logger = logging.getLogger("preprocessing_helper")

def flatten_mutli_index(input_df_cols:List)->List:
    """Flattens a hierachichal pandas index

    Args:
        input_df_cols (List): List type object of hierachical indices

    Returns:
        List: Flatten list of indexes where the index names are concatonated 
        by _
    """
    input_df_cols = [re.sub("_$", "", '_'.join(col).strip()) 
                     for col in input_df_cols]
    return input_df_cols
    

def pd_safe_merge(input_df_1:pd.DataFrame, input_df_2:pd.DataFrame, *args, 
                  raise_exception:bool=False, **kwargs)->pd.DataFrame:
    """Wrapper for pandas merge but raises a warning (and optionally an 
    exception) when the row counts have been altered by the merge

    Args:
        input_df_1 (pd.DataFrame): Input dataframe whichh requires merging. 
        This dataframe will be used as the basis for the row counts
        input_df_2 (pd.DataFrame): Input dataframe whichh requires merging. 
        raise_exception (bool, optional): Indicator determining whether an 
        exception should be raised if the row counts don't match. Defaults to 
        False.

    Raises:
        Exception: Raised when the row counts don't match and raise_exception 
        is True

    Returns:
        pd.DataFrame: pandas data frame with input_df_1 and input_df_2 joined
    """
    pre_join_shape = input_df_1.shape[0]
    out_df = pd.merge(input_df_1, input_df_2, *args, **kwargs)
    if pre_join_shape != out_df.shape[0]:
        warn_msg = "Join has altered the shape of input_df_1."
        logger.warning(warn_msg)
        info_msg = "input_df_1 shape: {}, input_df_2 shape: {}, out_df shape: {}".format(
            input_df_1.shape[0], input_df_2.shape[0], out_df.shape[0])
        logger.info(info_msg)
        if raise_exception:
            raise Exception(warn_msg+" "+info_msg)
    else:
        pass
    return out_df


def flatten_lst(input_lst:List[Any], recursive:bool=True)->List[Any]:
    """Function for flattening a list containing lists

    Args:
        input_lst (List[Any]): Input list to flatten
        recursive (bool, optional): If true the function will recursively 
        flatten lists within the input list else only the first layer of lists
        will be flattened. Defaults to True.

    Returns:
        List[Any]: A flattened version of the input_lst
    """
    output_lst = []
    for sub_lst in input_lst:
        if isinstance(sub_lst, list):
            if recursive:
                sub_lst = flatten_lst(sub_lst)
            output_lst = output_lst + sub_lst
        else:
            output_lst.append(sub_lst)
    return output_lst


def pd_agg_percentile(n:int, nan:str="ignore")->Callable:
    """Function to generate percentile values in the pandas aggregate function
    us as follows:
        column.agg([np.sum, np.mean, np.std, np.median,
                     np.var, np.min, np.max, percentile(50), percentile(95)])

    Args:
        n (int): Integer between 0 and 100, defining the percentile of interest
        nan (str, optional): Option to "ignore" nans or "include" nans. If 
        "include" is selected and nans are present, the percentile_ will return 
        nans. Defaults to "ignore".

    Returns:
        Callable: Chosen percentile function, with name based on the percentile 
        of interest. This can then be evaluated in the pandas agg function
    """
    fnk_lkp = {
        "include":np.percentile,
        "ignore":np.nanpercentile
    }
    def percentile_(x):
        return fnk_lkp[nan](x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_