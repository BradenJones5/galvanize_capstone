import pandas as pd
def scale_conversion(dataframe):
    '''
    input: dataframe
    output: return numpy array with scaled 3rd conversion rate
    '''
    dataframe['comp_percent'] = dataframe.iloc[:,-2] / (dataframe.iloc[:,-1].values + dataframe.iloc[:,-2].values)

def get_3rd_down_conversions(dataframe):
    '''
    input: dataframe
    output: return pandas series 1 if the team converted on third down, 0 otherwise
    '''
    temp =dataframe[dataframe['Down'] == 3.0]
    convert = (temp.yardage > temp.ToGo).astype(int)
    not_convert = pd.get_dummies(convert)[0]
    temp['convert'] = pd.Series(convert)
    temp['not_convert'] = pd.Series(not_convert)
    return temp

def extract_yard(string_description):
    '''
    input: a string description for 1 play
    output: an integer of the yardage on each play, 0 otherwise
    '''
    yardage =[]
    for word in string_description.split():
        if word.isdigit():
            yardage.append(int(word))
    if not yardage:
        return 0
    else:
        return yardage[0]

def create_yardage_column(details):
    '''
    input: pandas series
    output: a pandas series containing the yardage
    '''
    return details.apply(extract_yard)

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

def get_year_column_from_link(data):
    '''
    input: pandas series containing the link extension to each games boxscore
    output: extract the year from that link and return a new column
    '''
    return data.apply(lambda x: x[11:15])

def create_short_right_incomplete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was incomplete in the direction of short
    and to the right
    '''
    short_right_incomplete = ['short', 'right', 'incomplete']
    return details.apply(lambda x : 1 if all(word in x.split() for word in short_right_incomplete) else 0)

def create_short_left_incomplete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was incomplete in the direction of short
    and to the left
    '''
    short_left_incomplete = ['short', 'left', 'incomplete']
    return details.apply(lambda x : 1 if all(word in x.split() for word in short_left_incomplete) else 0)

def create_deep_left_incomplete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was incomplete in the direction of deep
    and to the left
    '''
    deep_left_incomplete = ['deep', 'left', 'incomplete']
    return details.apply(lambda x : 1 if all(word in x.split() for word in deep_left_incomplete) else 0)

def create_deep_right_incomplete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was incomplete in the direction of deep
    and to the right
    '''
    deep_right_incomplete = ['deep', 'right', 'incomplete']
    return details.apply(lambda x : 1 if all(word in x.split() for word in deep_right_incomplete) else 0)

def create_short_middle_incomplete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was incomplete in the direction of short
    and to the middle of the field
    '''
    short_middle_incomplete = ['short', 'middle', 'incomplete']
    return details.apply(lambda x : 1 if all(word in x.split() for word in short_middle_incomplete) else 0)

def create_deep_middle_incomplete_col(details):
    '''
    input: pandas series of play descriptions
    output: pandas series indicating 1 if a pass was incomplete in the direction of deep
    and to the middle of the field
    '''
    deep_middle_incomplete = ['deep', 'middle', 'incomplete']
    return details.apply(lambda x : 1 if all(word in x.split() for word in deep_middle_incomplete) else 0)

def get_feature_matrix(dataframe):
    '''
    input: pandas dataframe
    output: returns a dataframe consisting of engineered features
    '''
    features = ['short_right_complete', 'short_right_incomplete',
                'short_left_complete',' short_left_incomplete','deep_left_complete',
                'deep_left_incomplete','deep_right_complete','deep_right_incomplete',
                'short_middle_complete', 'short_middle_incomplete','deep_middle_complete',
                'deep_middle_incomplete','yardage','_passplay_flag']

    functions = [create_short_right_complete_col, create_short_right_incomplete_col,
                create_short_left_complete_col, create_short_left_incomplete_col,
                create_deep_left_complete_col, create_deep_left_incomplete_col,
                create_deep_right_complete_col, create_deep_left_incomplete_col,
                create_short_middle_complete_col, create_deep_left_incomplete_col,
                create_deep_middle_complete_col, create_deep_middle_incomplete_col,
                create_yardage_column,]

    for feature, function in zip(features[:-1], functions):
        dataframe[feature] = function(dataframe.Detail)

    return dataframe, features

def get_scaled_feature_matrix(dataframe):
    '''
    input: dataframe
    output: return numpy matrix of scaled feature variables
    '''
    for comp, inc in zip(dataframe.iloc[:,2::2].columns, dataframe.iloc[:,3::2].columns):

        dataframe[comp] = dataframe[comp] * 1.0 / (dataframe[comp] + dataframe[inc])

    return dataframe.iloc[:,2::2].values

def get_data(filename):
    data = pd.read_csv(filename)
    data['year'] = get_year_column_from_link(data['date'])
    data['year'] = data['year'].astype(int)
    data = data[data['year']  >= 2006]
    data['Detail'] = data['Detail'].astype(str)
    data['qb_names'] = get_qb_names(data.Detail)
    data = filter_qb_rb_plays(data)
    data['_passplay_flag'] = create_flag_for_plays(data.Detail)
    data = data[data._passplay_flag == 1]
    data, features = get_feature_matrix(data)
    copy = data.copy()
    copy = get_3rd_down_conversions(copy)

    data = pd.merge(data, copy[['Unnamed: 0','convert','not_convert']],how = 'left', left_on='Unnamed: 0', right_on = 'Unnamed: 0')
    data['convert'].fillna(0, inplace=True)
    data['not_convert'].fillna(0, inplace=True)


    features.append('convert')
    features.append('not_convert')
    data = data.groupby(['qb_names','year'])[features].sum().reset_index()

    mask = data['_passplay_flag'] > 350
    data = data[mask]
    scale_conversion(data)

    return data

if __name__ == '__main__':
    subset_df= get_data('all_seasons.csv')
