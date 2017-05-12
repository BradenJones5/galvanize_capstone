import pandas as pd


def extract_names_from_detail_col(detail_string):
    '''
    input: takes in a string description of 1 play
    output: extracts the names in that play
    '''

    return ' '.join([word for word in detail_string.split()[:2] if word[0].isupper()])

def get_qb_names(details):
    '''
    input: pandas series
    output: return a set of unique qb names
    '''
    return details.apply(extract_names_from_detail_col)

def filter_qb_rb_plays(df):
    '''
    input: dataframe
    output: filtered dataframe for pass, run, and special teams plays only
    '''
    mask = filter(lambda x: len(x.split()) == 2, df.qb_names)
    return df[df.qb_names.isin(mask)]

def create_flag_for_plays(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass play, 0 otherwise
    '''
    return details.apply(lambda x: 1 if 'pass' in x.split() else 0)

def create_short_right_complete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was completed to the right for
    short yardage
    '''
    short_right_complete = ['short', 'right', 'complete']
    return details.apply(lambda x: 1 if all(word in x.split() for word in short_right_complete) else 0)

def create_short_left_complete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was completed to the left for
    short yardage
    '''
    short_left_complete = ['short', 'left', 'complete']
    return details.apply(lambda x: 1 if all(word in x.split() for word in short_left_complete) else 0)

def create_deep_left_complete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was completed to the left for
    long yardage
    '''
    deep_left_complete = ['deep', 'left', 'complete']
    return details.apply(lambda x: 1 if all(word in x.split() for word in deep_left_complete) else 0)

def create_deep_right_complete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was completed to the right for
    long yardage
    '''
    deep_right_complete = ['deep', 'right', 'complete']
    return details.apply(lambda x: 1 if all(word in x.split() for word in deep_right_complete) else 0)

def create_short_middle_complete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was completed to the middle for
    short yardage
    '''
    short_middle_complete = ['short', 'middle', 'complete']
    return details.apply(lambda x: 1 if all(word in x.split() for word in short_middle_complete) else 0)

def create_deep_middle_complete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was completed to the middle for
    long yardage
    '''
    deep_middle_complete = ['deep', 'middle', 'complete']
    return details.apply(lambda x: 1 if all(word in x.split() for word in deep_middle_complete) else 0)

def get_data(filename):
    data = pd.read_csv('2016_season.csv')
    data['qb_names'] = get_qb_names(data.Detail)
    data = filter_qb_rb_plays(data)
    data['_passplay_flag'] = create_flag_for_plays(data.Detail)
    data = data[data._passplay_flag == 1]
    data['short_right_complete'] = create_short_right_complete_col(data.Detail)
    data['short_left_complete'] = create_short_left_complete_col(data.Detail)
    data['deep_left_complete'] = create_deep_left_complete_col(data.Detail)
    data['deep_right_complete'] = create_deep_right_complete_col(data.Detail)
    data['short_middle_complete'] = create_short_middle_complete_col(data.Detail)
    data['deep_middle_complete'] = create_deep_middle_complete_col(data.Detail)
    features = ['short_right_complete','short_left_complete','deep_left_complete',
                'deep_right_complete','short_middle_complete','deep_middle_complete',
                '_passplay_flag']
    subset_df = data.groupby('qb_names')[features].sum()
    mask = subset_df['_passplay_flag'] > 100
    subset_df = subset_df[mask]
    for feature in features[:-1]:
        subset_df[feature] = subset_df[feature] * 1.0 / subset_df['_passplay_flag']
    feature_matrix = subset_df.iloc[:,:-1].values
    return subset_df, feature_matrix

if __name__ == '__main__':
    subset_df, feature_matrix = get_data('2016_season.csv')
