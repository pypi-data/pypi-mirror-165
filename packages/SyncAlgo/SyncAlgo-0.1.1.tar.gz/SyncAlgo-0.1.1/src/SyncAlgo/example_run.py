import multiprocessing
import DataTraining
import DataSync

if __name__ == '__main__': 

    # Cumulative example
    data_file = "dem_filled.csv"
    init_features = [
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    [16],
                    [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
                    ]
    feature_list = [
                    [32, 33, 34, 35, 36, 37, 38, 39, 40],
                    [41, 42, 43, 44],
                    [45, 46, 47, 48, 49, 50, 51, 52],
                    [53, 54, 55, 56, 57, 58],
                    [59, 60, 61, 62, 63, 64],
                    [65, 66, 67, 68, 69],
                    [70],
                    [72],
                    [74],
                    [76, 77, 78, 79, 80],
                    [81],
                    [83, 84, 85, 86, 87],
                    [88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107],
                    [108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126],
                    ]

    agg_units="geo.csv" 
    model_name='dem'
    path='/home/ubuntu/arima/SynC/data/'
    num_epoch=1
    num_sample=5
    num_cpu=multiprocessing.cpu_count()
    multi=True
    cumulative=False
    save=True

    DataTraining.train_data(data_file, init_features, feature_list, \
                                model_name, path= path, num_epoch=num_epoch,cumulative=cumulative)

    # # Non-cumulative Sync.
    dem_df =  DataSync.sync_agg(data_file, agg_units, init_features, feature_list, \
                model_name, path=path,  num_sample=num_sample, \
                num_cpu=num_cpu, multi=multi, cumulative=cumulative, save=save)



    # Non cumulative example
    data_file= 'dem_filled.csv'
    init_features=[
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    [16],
                    [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
                    [32, 33, 34, 35, 36, 37, 38, 39, 40],
                    [41, 42, 43, 44],
                    [45, 46, 47, 48, 49, 50, 51, 52],
                    [53, 54, 55, 56, 57, 58],
                    [59, 60, 61, 62, 63, 64],
                    [65, 66, 67, 68, 69],
                    [70],
                    [72],
                    [74],
                    [76, 77, 78, 79, 80],
                    [81],
                    [83, 84, 85, 86, 87],
                    [88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107],
                    [108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126],
                    ]
    feature_list= [[127],[129],[131],[133],[135],[137],[139],[141],[143],[145],[147],[149],[155]]

    model_name= 'psy'
    agg_units="geo.csv" 

    cumulative=False

    DataTraining.train_data(data_file, init_features, feature_list, \
                                model_name, path= path, num_epoch=num_epoch,cumulative=cumulative)

    # Non-cumulative Sync.
    psy_df =  DataSync.sync_agg(data_file, agg_units, init_features, feature_list, \
                model_name, path=path,  num_sample=num_sample, \
                num_cpu=num_cpu, multi=multi, cumulative=cumulative, save=save)