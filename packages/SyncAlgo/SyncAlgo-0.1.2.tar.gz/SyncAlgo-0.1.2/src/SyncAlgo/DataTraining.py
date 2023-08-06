from SyncAlgo.functions import train_model
from SyncAlgo.utils import *
import pandas as pd
import dask.dataframe as dd
import os

def train_sync(data_primary,data,num_epoch,model_name,cumulative,model_path):
    """
    : func        : train the prediction model of sync algorithm
    : draw [bool] : decide whether to draw figures or not
    : return      : none
    """

    train_data_init = []
    for _ , feature_value in data_primary.items():
        train_data_init.append(feature_value)

    train_data = pd.concat(train_data_init, axis=1)

    for i, fea_infer in enumerate(data):

        train_model(train_data, data[fea_infer], 
                                   model_name + '_' + str(i + 4).zfill(2), 
                                   epoch=num_epoch,
                                   models_directory=model_path)
        if cumulative:
            train_data = pd.concat([train_data, data[fea_infer]], axis=1)
    # if cumulative:
    #     train_data.to_csv(output_file, index=False)


def train_data(feature_file, init_features, feature_list, model_name='dem', num_epoch=3, cumulative = True, path=''):
    '''
    feature_file: The data file contains aggregation level features for both training and predicting.
    init_feaures  : list of list contains the column names of each feature in primary data
    feature_list  : list of list contains the column names of each feature in rest of data
    model_name: name of models saved to local model directory, saved as [model_name]_0x.h5
    num_epoch: number of epoches for training the model.
    cumulative: training cumulatively is using current predicted column data as training data for next column
    path : path to data files, default as "../data"
    return: none, model files will be created under model directory
    '''

    total_feature_length=[]
    data_primary = {}
    data = {}

    if path == '':
        print("Please specify the correct data path.")
        exit()
    else:
        feature_file = os.path.join(path, feature_file)
        model_path = path + '/../models/'

    flat_list = [str(item) for sublist in (init_features + feature_list) for item in sublist]

    features = dd.read_csv(feature_file,usecols =flat_list)[flat_list].compute()
    features.reset_index(drop=True, inplace=True)

    init_names= [[str(j) for j in i] for i in init_features]
    feature_names = [[str(j) for j in i] for i in feature_list]

    for index, fea_infer in enumerate(init_names):
        data_primary[index] = features.filter(items = fea_infer)
        total_feature_length.append(len(fea_infer))

    for index, fea_infer in enumerate(feature_names):
        data[index] = features.filter(items = fea_infer)
        total_feature_length.append(len(fea_infer))

    # train sync algorithm
    print("TRAIN MODE")
    train_sync(data_primary, data, num_epoch, model_name, cumulative, model_path)
    # Save log to file
    # logs.to_csv(filepath + 'training_log.csv', index=False)

