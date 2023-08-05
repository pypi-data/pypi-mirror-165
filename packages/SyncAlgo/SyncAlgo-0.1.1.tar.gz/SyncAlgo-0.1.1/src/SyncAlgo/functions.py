from tensorflow.keras.layers import Dense, Activation, BatchNormalization
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from scipy.stats import rankdata
import tensorflow as tf
import multiprocessing
import pandas as pd
import numpy as np
import logging
import os

from SyncAlgo.utils_function import power_two, shuffle_forward, shuffle_backward, \
    round_marginals, less_na

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
pd.options.mode.chained_assignment = None
# key = names.key

seed_value = 123
tf.random.set_seed(seed_value)
train_opt = 'nadam'
train_loss = 'kullback_leibler_divergence'

def build_model(x_train, x_val, y_train, y_val):
    """ build tensorflow model """
    
    model = Sequential()
    model.add(Dense(units=max(int(power_two(len(x_train.columns))/1),8), input_dim=len(x_train.columns)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dense(units=max(int(power_two(len(x_train.columns))/2),4), activation='relu'))
    
    if (not isinstance(y_train, pd.Series) and len(y_train.columns) > 1):
        print('Training Multi Categorical Model')
        model.add(BatchNormalization())
        model.add(Dense(units=len(y_train.columns), activation='softmax'))
        model.compile(optimizer=train_opt, loss=train_loss, metrics=['accuracy'])
    else:
        print('Training Single Categorical Model')
        model.add(Dense(units=max(int(power_two(len(x_train.columns))/4),2), activation='relu'))
        model.add(Dense(units=max(int(power_two(len(x_train.columns))/8),2), activation='relu'))
        model.add(BatchNormalization())
        model.add(Dense(units = 1, activation = 'sigmoid'))
        model.compile(optimizer='nadam', loss='binary_crossentropy', metrics=['mean_absolute_error'])
    
    return model

def train_model(x, y, var_name, epoch=10, models_directory=''):
    """ 
    train prediction model 
    save best model
    return logging results
    """
    
    print("Training", var_name)
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.3, random_state=seed_value)
    model = build_model(x_train, x_val, y_train, y_val)
    
    checkpoint_filepath = f'{models_directory}/{var_name}.h5'
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
                                filepath=checkpoint_filepath,
                                save_weights_only=True,
                                monitor='val_loss',
                                mode='min',
                                save_best_only=True)
        
    log = model.fit(x_train, y_train, batch_size=1024, epochs=epoch, verbose=2,
                        validation_data=(x_val, y_val), 
                        use_multiprocessing=True, workers=multiprocessing.cpu_count())
    
    model.save_weights(checkpoint_filepath)
    model_json = model.to_json()
    with open(f'{models_directory}/{var_name}.json', "w") as json_file:
        json_file.write(model_json)
    
    print(log)
    print(var_name, 'trained')

def match_marginals(rank_mat, normalize_marginals):

    output_records = np.zeros((rank_mat.shape))
    tracker = normalize_marginals.copy().reshape(-1)
    num_row = rank_mat.shape[0]

    rank_mat[:, tracker == 0] = -1

    for i in range(num_row):
        row = rank_mat[i, :]
        min_id = np.argmin(np.where(row > 0, row, np.inf))

        if row[min_id] <= tracker[min_id]:
            output_records[i, min_id] = 1
            tracker[min_id] -= 1
            rank_mat[i, :] = -1
    
    rank_mat[:, tracker == 0] = -1

    if np.all(tracker == 0):
        return output_records

    tracker, rank_mat, output_records = assign_to_ranks(
        tracker, rank_mat, output_records)
    
    counter = 0
    while not np.all(tracker == 0):
        tracker, rank_mat, output_records = assign_to_ranks(
            tracker, rank_mat, output_records)
        counter += 1
        if counter > 5:
            break
        
    return output_records

def assign_to_ranks(tracker, rank_mat, output_records):
    """
    : func                : assign results to each attribute of each row
    : tracker        [np] : track how many quota left for each attribute
    : rank_mat       [np] : ranking results of prediction
    : output_records [np] : output matrix
    : return              : tracker [np], ori_rank_mat [np], output_records [np]
    """ 
    
    ori_rank_mat = rank_mat.copy()
    
    # sort the array
    num_target_col = len(tracker[tracker != 0])
    sort_col_ary = np.argsort(np.where(tracker > 0, tracker, np.inf))[:num_target_col]

    # iterate each column
    for target_col_ind in sort_col_ary:

        temp = ori_rank_mat[:,target_col_ind]
        output_ind = np.argsort(np.where(temp > 0, temp, np.inf))
        rank_mat = ori_rank_mat[output_ind]

        # iterate each row
        num_target_row = len(temp[temp > 0])
        for j in range(num_target_row):
          
            if not np.all(rank_mat[j,:] == -1) and \
                less_na(rank_mat[j, target_col_ind], \
                                   np.delete(rank_mat[j], target_col_ind)):
                output_records[output_ind[j], target_col_ind] = 1
                tracker[target_col_ind] -= 1
                rank_mat[j, :] = -1
                ori_rank_mat[output_ind[j], :] = -1
                if tracker[target_col_ind] == 0:
                    rank_mat[:, target_col_ind] = -1
                    ori_rank_mat[:, target_col_ind] = -1
                    break
                
    return tracker, ori_rank_mat, output_records

def process(marginals_pd, model, individual_pd,name,
            # index=None, data_type='categorical',gender=False, conditional_dem_index=None,
            cumulative=False):

    marginals_np = marginals_pd.to_numpy()
    marginals_fea = marginals_pd.columns.values
    individual_np = individual_pd.to_numpy()
    individual_fea = individual_pd.columns.values

    predictions_np = model.predict(individual_np)
    noise_func = lambda x: np.random.uniform(0.9, 1.1) * x
    predictions_np = noise_func(predictions_np)  

    if predictions_np.shape[1] > 1:
        predictions_np, order = shuffle_forward(predictions_np)
        
        rank_mat_np = len(predictions_np) + 1 - rankdata(predictions_np, method='ordinal', axis = 0).astype(np.float)
        normalize_marginals_np = round_marginals(marginals_np, np.float64(len(rank_mat_np)))
        entry_np = match_marginals(rank_mat_np, normalize_marginals_np)
        
        entry_np = shuffle_backward(entry_np, order)
        
        entry_pd = pd.DataFrame(entry_np)
        entry_pd.columns = marginals_fea
    else:
        total = int(np.round(marginals_np*len(individual_np)))
        entry_np = np.zeros((predictions_np.shape))
        entry_pd = pd.DataFrame(entry_np)
        entry_pd.columns = marginals_fea
        predictions_pd = pd.DataFrame(predictions_np)
        entry_pd[(predictions_pd.rank(ascending = False) <= total).values] = 1

    if cumulative:
        if not type(entry_pd) == pd.core.frame.DataFrame:
            print('error')
        return pd.concat([individual_pd, entry_pd], axis=1)
    else:
        return entry_pd.astype(int)
