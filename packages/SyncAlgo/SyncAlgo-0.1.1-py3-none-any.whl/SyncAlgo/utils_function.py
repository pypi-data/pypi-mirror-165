import numpy as np

def shuffle_forward(array):
    """ shuffle array and record order """
    
    order = np.arange(len(array))
    np.random.shuffle(order)
    return np.array(array)[order], order

def shuffle_backward(array, order):
    """ undo shuffled array by given order """
    
    if array.shape[0] == 0:
        return array
    array_out = [0] * len(array)
    for i, j in enumerate(order):
        array_out[j] = array[i]
    return np.array(array_out)

def power_two(count):
    """ calculate nearest value of power of two by given input """
    
    power = 1
    while pow(2, power) <= count:
        power += 1
    return pow(2, power - 1)

def less_na(x, y):
    y = y[np.where(y!=-1)]
    if np.all(np.less_equal(x,y)):
        return True
    else:
        return False

def normalize(x):
    """ apply min-max normalization """
    
    x = np.nan_to_num(x)
    x = np.abs(x)
    return np.divide(x, np.sum(x))

def round_marginals(marginal, total):
    """
    : func            : convert prob. to population
    : marginal [list] : marginal information 
    : total    [int]  : total number of population 
    : return   [df]   : marginal_new
    """

    if np.sum(marginal) == 0:
        marginal += 1/marginal.shape[1]
    marginal_new = np.round(np.multiply(normalize(marginal), total))
    marginal_sum = int(np.sum(marginal_new))
    difference = np.abs(marginal_sum - int(total))

    if marginal_sum > total:
        while difference > 0:
            sample_prob = marginal_new
            sample_prob[np.where(marginal_new == 0)] = 0
            marginal_new -= np.random.multinomial(
                1, np.ravel(normalize(sample_prob)), size = 1)
            difference -= 1
    else:
        marginal_new += np.random.multinomial(
            difference, np.ravel(normalize(marginal)), size = 1)
        
    return marginal_new

def create_df(marginal, features, total):
    """ 
    : func            : create ethnicity table by random
    : marginal [list] : marginal information 
    : features [list] : column names of dataframe
    : total    [int]  : total number of population
    : return   [df]   :  ethnicity
    """

    ethnicity = np.zeros((total, len(features)))
    counter = 0

    for key, value in zip(features, marginal.T):
        if value[0] > 0:
            ethnicity_id = int(np.where(features == key)[0])
            ethnicity[counter:(counter + int(value[0])), ethnicity_id] = 1
            counter += int(value[0])
    return ethnicity

def create_age_gender_df(marginals, features, total, age_cols, gender_cols):
    """ 
    : func               : create age and gender table by random
    : marginals   [list] : marginal information
    : features    [list] : column names of dataframe 
    : total       [int]  : total number of population
    : age_cols    [list] : column names of age
    : gender_cols [list] : column names of gender
    : return      [df]   : age_gender_df 
    """

    age = np.zeros((total, len(age_cols)))
    gender = np.zeros((total, len(gender_cols)))

    counter = 0

    for key, value in zip(features, marginals.T):
        population = int(value[0])
        if population > 0:
            if 'FM' in key:
                gender_label = 0
                age_label = key.replace('FM', '')
            else:
                gender_label = 1
                age_label = key.replace('M', '')
            gender[counter:(counter + population), gender_label] = 1
            age_id = int(np.where(age_cols == age_label)[0])
            age[counter:(counter + population), age_id] = 1
            counter += population
            
    age_gender_df = np.concatenate((age, gender), axis=1), np.append(age_cols, gender_cols)
    return age_gender_df
