from re import I
from SyncAlgo.utils_function import round_marginals, create_df
from SyncAlgo.functions import process
from SyncAlgo.utils import *
import pandas as pd
import numpy as np
import multiprocessing
import dask.dataframe as dd
from datetime import datetime
import glob
import concurrent.futures as futures
from functools import partial
import os


def init_data(data_primary, population, len_pri, col_names):
    """
    : func      : initialize data of each aggragation unit
    : return    : individual [df]
    """

    individual = np.array([])
    individual_fea = np.array([])

    pointer=0
    primary_list=list(col_names.get_level_values(0))
    primary_list=sorted(set(primary_list), key=primary_list.index)

    for feature_value,length in zip(primary_list,len_pri):
        names=[]
        for name in col_names:
            if name[0]==feature_value:
                names.append(name[1])

        marginals_features = round_marginals(data_primary[pointer:pointer+length].reshape(1,-1), np.float64(population))
        feature_categories = create_df(marginals_features, np.array(names), population)

        if individual.size == 0:
            individual = feature_categories
            individual_fea = names
        else:
            individual = np.concatenate([individual, feature_categories], axis=1)
            individual_fea = np.append(individual_fea, names)

        pointer+=length

    # convert numpy to pandas
    individual = pd.DataFrame(individual)
    individual.columns = individual_fea

    return individual

def sync_cumulative(aggregation, data_primary, data,fea_list, len_pri, len_fea, col_names, cumulative, model_name, model_path):
    """
    : func      : generate synthetic i-lv data by sync_ algorithm for each geo area
    : return    : Synced individual data in current aggregation unit
    """
    
    code=aggregation[0]
    population= aggregation[1]
    print("Current unit:", code)
    
    models = {}
    model_names = [model_name+ '_' + str(x).zfill(2) for x in range(4, len(fea_list) + 4)]    

    # load models
    if len(glob.glob1(model_path, (model_name+'*.h5'))) == len(model_names):
        for model_name in model_names:
            models[model_name] = load_model(model_path, model_name)
    else:
        print("Number of models unmatched with number of features, please check the models directory")
        exit()

    
    individual = init_data(data_primary, population, len_pri, col_names)

    # generate synthetic i-lv data one-by-one
    for name, length in zip(model_names, len_fea):
        # main process
        counter = 0 
        individual = process(marginals_pd=pd.DataFrame(data[counter:length]).T,
                             model=models[name], individual_pd=individual,name=name,
                             cumulative=cumulative
                             )
        counter += length

    individual_condensed = prep_dem(individual, len_pri + len_fea)
    individual_condensed.insert(loc=0, column='agg_unit', value=code)

    return individual_condensed



def sync_non_cumulative(aggregation, data_primary, data,fea_list, len_pri, len_fea, col_names, cumulative, model_name, model_path):
    """
    : func      : generate synthetic i-lv data by sync_ algorithm for each geo area
    : return    : Synced individual data in current aggregation unit
    """
    
    code=aggregation[0]
    population= aggregation[1]
    print("Current unit:", code)
    
    models = {}
    model_names = [model_name+ '_' + str(x).zfill(2) for x in range(4, len(fea_list) + 4)]    

    # load models
    if len(glob.glob1(model_path, (model_name+'*.h5'))) == len(model_names):
        for model_name in model_names:
            models[model_name] = load_model(model_path, model_name)
    else:
        print("Number of models unmatched with number of features, please check the models directory")
        exit()
    
    individual = init_data(data_primary, population, len_pri, col_names)

    output={}
    # generate synthetic i-lv data one-by-one
    for name, length in zip(model_names, len_fea):
        # main process
        counter = 0 
        output[name] = process(marginals_pd=pd.DataFrame(data[counter:length]).T,
                             model=models[name], individual_pd=individual,name=name,
                             cumulative=cumulative
                             )
        counter += length

    individual = pd.concat([w for w in output.values()], axis=1)
    individual.insert(loc=0, column='agg_unit', value=code)

    return individual

def main_infer(aggregation, data_primary, data, fea_list, len_pri, len_fea, \
               num_cpu, model_name, model_path, multi=True, cumulative= True):
    """
    : func               : main function of generate prediction
    : aggregation  [df]  : dataframe of aggregation csv file
    : data_primary [df]  : dataframe of data used as model predicting source
    : data       [df]    : dataframe of data used as individual data training source
    : fea_list   [list]  : string list contains names of feature
    : len_pri    [list]  : int list contains lengths of each feature in primary data
    : len_fea    [list]  : int list contains lengths of each feature in the rest of data
    : return             : none
    """
    
    agg_columns = aggregation.columns.values
    unit_name = agg_columns[0]

    start = datetime.now()
    print("START: \t", start)

    if multi:
        if cumulative:
            with futures.ProcessPoolExecutor(max_workers=num_cpu) as executor:
                results=executor.map(
                    partial(sync_cumulative, fea_list=fea_list, \
                        len_pri=len_pri, len_fea=len_fea, col_names=data_primary.columns, cumulative = cumulative, model_name=model_name, model_path=model_path),
                        aggregation.values, data_primary.values, data.values
                    )
                
            concated = pd.concat(results, axis=0)
        else:
            with futures.ProcessPoolExecutor(max_workers=num_cpu) as executor:
                results=executor.map(
                    partial(sync_non_cumulative, fea_list=fea_list, \
                        len_pri=len_pri, len_fea=len_fea, col_names=data_primary.columns, cumulative = cumulative, model_name=model_name, model_path=model_path),
                        aggregation.values, data_primary.values, data.values
                    )
                
            concated = pd.concat(results, axis=0)

    # singleprocessing
    else:
        print("="*10, "Singleprocessing", "="*10)
        if cumulative:
            results = []
            for cur_geo in aggregation[unit_name]:
                print(cur_geo)
                results.append(sync_cumulative(fea_list, len_pri, len_fea, data_primary.columns, cumulative, model_name, model_path,
                            aggregation.values, data_primary.values, data.values)
                )
            concated = pd.DataFrame(results)
        else:
            
            results = []
            for cur_geo in aggregation[unit_name]:
                print(cur_geo)
                results.append(sync_non_cumulative(fea_list, len_pri, len_fea, data_primary.columns, cumulative, model_name, model_path,
                            aggregation.values, data_primary.values, data.values)
                )
            concated = pd.DataFrame(results)

    end = datetime.now()
    print("END: \t", end)
    print("Duration: \t", (end-start).seconds, "s")
    
    return concated



def sync_agg(feature_file, agg_units, init_features, feature_list, \
            model_name='dem', path='', num_sample=-1, \
             num_cpu=multiprocessing.cpu_count(), multi=True, cumulative =True, save=True):
    """
    : agg_units     : aggragation csv file name: [aggregation unit, size]
    : init_feaures  : list of list contains the column names of each feature in primary data
    : feature_list  : list of list contains the column names of each feature in rest of data
    : path          : path to data files, default as "../data"
    : num_sample    : number of sampling geo area
    : num_cpu       : number of cpu assigned for multiprocessing
    : multi         : multiprocessing or singleprocessing
    : cumulative    : Sync cumulatively or non-cumulatively
    : return        : none, csv file with synced individual data as output
    """

    data_primary = {}
    data = {}
    len_prims=[]
    len_features=[]
    
    if path == '':
        print("Please specify the correct data path.")
        exit()
    else:
        aggregation_file=os.path.join(path,agg_units)
        feature_file=os.path.join(path, feature_file)
        model_path = path + '/../models/'

    flat_list = [str(item) for sublist in (init_features + feature_list) for item in sublist]


    aggregation = dd.read_csv(aggregation_file).compute()
    aggregation.reset_index(drop=True, inplace=True)
    features = dd.read_csv(feature_file,usecols =flat_list)[flat_list].compute()
    features.reset_index(drop=True, inplace=True)

    init_names= [[str(j) for j in i] for i in init_features]
    feature_names = [[str(j) for j in i] for i in feature_list]

    for index, fea_infer in enumerate(init_names):
        data_primary[index] = features.filter(items = fea_infer)
        len_prims.append(len(fea_infer))
    condata_primary= pd.concat(data_primary,axis=1)

    for index, fea_infer in enumerate(feature_names):
        data[index] = features.filter(items = fea_infer)
        len_features.append(len(fea_infer))
    condata = pd.concat(data,axis=1)

    # sample the data file for test purpose
    if num_sample != -1:
        aggregation = aggregation.iloc[:num_sample, :]
        condata = condata.iloc[:num_sample, :]
        condata_primary = condata_primary.iloc[:num_sample, :]

    # generate i-lv prediction results
    print("INFER MODE")
    size = aggregation.shape[0]
    chunk_current = 0
    df_list=[]

    # split the file into smaller chunks to periodically release memory.
    while(chunk_current<size):
        chunk_size = num_cpu*2000
        next_chunk=chunk_current + chunk_size
        df_list.append(main_infer(aggregation.iloc[chunk_current:next_chunk,:], condata_primary.iloc[chunk_current:next_chunk,:], condata.iloc[chunk_current:next_chunk,:], feature_list, \
                len_prims, len_features, num_cpu, model_name, model_path,
                multi, cumulative))
        chunk_current += chunk_size

    # Clean model files
    models = glob.glob(f'{model_path}*')
    for model in models:
        os.remove(model)

    # final result concatenated.
    final_df = pd.concat(df_list)

    if save:
        final_df.to_csv(path +'individual_'+model_name+'.csv', index=False)
    return final_df