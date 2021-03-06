def scale_data_total_passatt(dataframe):
    '''
    input: dataframe
    output: return numpy matrix with features standardized by total pass attempts
    thoughout one season
    '''
    for feature in dataframe.iloc[:,2:14:2].columns:
        dataframe[feature] = dataframe[feature] * 1.0 / dataframe['_passplay_flag']

    return dataframe.iloc[:,2:14:2].values

def scale_data_total_comp(dataframe):
    '''
    input: dataframe
    output: return numpy matrix with features standardized by total pass completions
    throughout one season
    '''
    dataframe['total_comps'] = dataframe.iloc[:,2:14:2].sum(axis=1)
    for feature in dataframe.iloc[:,2:14:2].columns:
        dataframe[feature] = dataframe[feature] * 1.0 / dataframe['total_comps']

    return dataframe.iloc[:,2:14:2].values

def get_scaled_feature_matrix(dataframe):
    '''
    input: dataframe
    output: return numpy matrix with features standardized by comp percentage for each
    feature
    '''
    for comp, inc in zip(dataframe.iloc[:,2:14:2].columns, dataframe.iloc[:,3:14:2].columns):
        dataframe[comp] = dataframe[comp] * 1.0 / (dataframe[comp] + dataframe[inc])

    return dataframe.iloc[:,2:14:2].values

def scale_conversion(dataframe):
    '''
    input: dataframe
    output: return numpy array with scaled 3rd conversion rate
    '''
    dataframe['comp_percent'] = dataframe.iloc[:,-2] / (dataframe.iloc[:,-1].values + dataframe.iloc[:,-2].values)
