import numpy as np
def liveability_scoring(scores, cols, weights):
    """Takes score data, list of weights and column names, return the total liveability score based on the weights"""
    # check the validation of weight list
    if len(weights) != len(cols):
        return np.nan
    if sum(weights) != 1:
        return np.nan
    
    # initialize the values
    scores["total_liveability_score"] = 0

    # calculate the total liveability
    for i, rows in scores.iterrows():
        list_sum = 0
        for n in range(0, len(cols)):
            if not np.isnan(scores.loc[i, cols[n]]):
                list_sum = list_sum + (scores.loc[i, cols[n]]*weights[n])
        scores.loc[i, "total_liveability_score"] = list_sum
    return scores