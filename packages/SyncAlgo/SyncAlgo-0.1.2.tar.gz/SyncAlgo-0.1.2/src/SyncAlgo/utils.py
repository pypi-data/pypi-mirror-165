from tensorflow.keras.models import model_from_json
import dask.dataframe as dd
from functools import partial
import multiprocessing
import pandas as pd
import os

def concat_csv(input_path, output_path):
    concat_list=[]

    filelist = [ f for f in os.listdir(input_path) if f.endswith(".csv") ]

    for input_csv in filelist:
        csv_path= os.path.join(input_path,input_csv)
        print(csv_path)
        csvresult = dd.read_csv(csv_path).compute()
        csvresult.reset_index(drop=True, inplace=True)
        concat_list.append(csvresult)

    concat_result = pd.concat(concat_list, axis=1)
    concat_result.to_csv(os.path.join(output_path ,'fea_concatenated.csv'), index=False)


def prep_dem(df, feature_lens):

    num_cols = len(df.columns.values)
    df.columns = [w for w in range(1, num_cols+1)]

    counter = 0
    converted = pd.DataFrame()
    for n in feature_lens:
        group = df.iloc[:, counter:(counter + n)]
        if n == 1:
            converted = pd.concat([converted, group.columns[0] + (group - 1) * -1], axis=1)
        else:
            converted = pd.concat([converted, group.idxmax(1)], axis=1)
        counter += n
    converted += 10011000
    return converted

def load_model(models_directory, var_name):
    """ load trained model """

    json_file = open(f'{models_directory}/{var_name}.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(f'{models_directory}/{var_name}.h5')
    return model

def count_files(directory):
    """ count number of files of given directory """

    total_csv_files = 0

    for base, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                total_csv_files += 1
    return total_csv_files


def store_df_row(path, include_first, row):
    """ partial function of split_df for multiprocessing """

    if include_first:
        row.tofile(path + str(row[0]) + '.csv', sep=",", format="%s")
    else:
        row[1:].tofile(path + str(row[0]) + '.csv', sep=",", format="%s")

def split_df(df, path, include_first=True):
    """ split data into many piece of csvs for multiprocessing """

    func = partial(store_df_row, path, include_first)
    multiprocessing.set_start_method('spawn', force=True)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map_async(func, df.values)
    pool.close()
    pool.join()

# def merge_csvs(postals, code):
#     """ merge many csvs into one """

#     li = []
#     for p in postals:
#         df = pd.read_csv(output_directory + code + '_' + p + '.csv', header=None)
#         li.append(df)
#     return pd.concat(li, axis=0, ignore_index=True)

