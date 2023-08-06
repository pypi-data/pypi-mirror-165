import numpy as np

"""
Dictionary writing code, relies on base list zip procedure. 
Ensure that this is launched and run before anything that may interfere with this base python function. 
"""

def norm_dict(scale):
    """
    Generates dictionary of value and label for use within mapper2
    Used for non-transformed variables
    :param scale: input raw values that you wish to use as labels
    :return: returns dictionary associating value and a label
    """
    i = scale.copy()
    labels = [str(i) for i in i]
    values = list(i)
    return dict(zip(labels, values))

def log1p_dict(scale):
    """
    Generates dictionary of value and label for use within mapper 2
    Used for dependent variables that have been log1 transformed
    :param scale: input raw values that you wish to use as labels
    :return: returns dictionary associating value and a label, value is log1p transformation of input
    """
    i = scale.copy()
    labels = [str(i) for i in i]
    values = list(np.log1p(i))
    return dict(zip(labels, values))

def log2p_dict(scale):
    """
    Generates dictionary of value and label for use within mapper 2
    Used for dependent variables that have been log1 transformed twice
    :param scale: input raw values that you wish to use as labels
    :return: returns dictionary associating value and a label, value is log1p transformation twice of input
       """
    i = scale.copy()
    labels = [str(i) for i in i]
    values = list(np.log1p(np.log1p(i)))
    return dict(zip(labels, values))

"""
Standard dictionary stored for ease of access
Now available in 3K and 10K format for standard scale
"""
standard_scale_1p_2p= [0, 1, 3, 10, 30, 100, 300, 1000, 3000]
standard_scale = [0,100,300,1000,3000]

dictionary_stand = norm_dict(standard_scale)
dictionary_stand_1p = log1p_dict(standard_scale_1p_2p)
dictionary_stand_2p = log2p_dict(standard_scale_1p_2p)

standard_scale_1p_2p_10k= [0, 1, 3, 10, 30, 100, 300, 1000, 3000, 10000]
standard_scale_10k = [0,100,300,1000,3000,10000]

dictionary_stand_10k = norm_dict(standard_scale_10k)
dictionary_stand_1p_10k = log1p_dict(standard_scale_1p_2p_10k)
dictionary_stand_2p_10k = log2p_dict(standard_scale_1p_2p_10k)


"""
Scale for dichotomous output from 0 to 1 
"""
dichotomous_scale_0_1 = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
dictionary_dichotomous_stand = norm_dict(dichotomous_scale_0_1)

#takes a variable name in string form and determines which dictionary to use
def find_the_dictionary(string, dictionary_0, dictionary_log1, dictionary_log2):
    if string.startswith('ln1'):
        output = dictionary_log1
        name = 'log_transformed_dictionary'
    elif string.startswith('ln2'):
        output = dictionary_log2
        name = 'log2_transformed_dictionary'
    else:
        output = dictionary_0
        name = 'non_transformed_dictionary'
    return {name:output}