import numpy as np 
import argparse
import logging
import heapq
import configparser
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit
import const
import multiprocessing as mp
import random
import time
from matplotlib import pyplot as plt

random.seed(0)
np.random.seed(0)

global_list = [0]*175

def init_logger():
    logger = logging.getLogger('kf')
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter(const.LOG_FORMAT)
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    return logger


### Parameters ###
r = 1000  #N/P

def read_conf(file):
    cf = configparser.ConfigParser()
    cf.read(file)  
    return dict(cf['default'])



def closed_world_acc(neighbors,y_test):
    global MON_SITE_NUM
    # logger.info('Calculate the accuracy...')
    p_c = [0] * MON_SITE_NUM
    tp_c = [0] * MON_SITE_NUM



    tp, p = 0, len(neighbors)
    for trueclass , neighbor in zip(y_test, neighbors):
        p_c[trueclass] += 1
        if len(set(neighbor)) == 1:
            guessclass = neighbor[0]
            if guessclass == trueclass:
                tp += 1
                tp_c[guessclass] += 1


    return tp/p, tp_c, p_c

def open_world_acc(neighbors, y_test,MON_SITE_NUM):
    # logger.info('Calculate the precision...')
    tp, wp, fp, p, n = 0, 0, 0, 0 ,0
    neighbors = np.array(neighbors)
    p += np.sum(y_test < MON_SITE_NUM)
    n += np.sum(y_test == MON_SITE_NUM)
    
    for trueclass, neighbor in zip(y_test,neighbors):
        if len(set(neighbor)) == 1:
            guessclass = neighbor[0]
            if guessclass != MON_SITE_NUM:
                if guessclass == trueclass:
                    tp += 1
                else:
                    if trueclass != MON_SITE_NUM: #is monitored site
                        wp += 1
                        # logger.info('Wrong positive:{},{}'.format(trueclass,neighbor))
                    else:
                        fp += 1
                        # logger.info('False positive:{},{}'.format(trueclass,neighbor))

    return tp,wp,fp,p,n
    
def kfingerprinting(X_train,X_test,y_train,y_test):
    # logger.info('training...')
    model = RandomForestClassifier(n_jobs=-1, n_estimators=1000, oob_score=True)
    model.fit(X_train, y_train)
#    M = model.predict(X_test)
    # for i in range(0,len(M)):
    #     x = M[i]
    #     label = str(Y_test[i][0])+'-'+str(Y_test[i][1])
    #     logger.info('%s: %s'%(str(label), str(x)))
    acc = model.score(X_test, y_test)
    logger.info('Accuracy = %.4f'%acc)
    train_leaf = model.apply(X_train)
    test_leaf = model.apply(X_test)
    
    #print(model.feature_importances_)

    for i in range(175):
        global_list[i] = global_list[i] + model.feature_importances_[i]

#    joblib.dump(model, 'dirty-trained-kf.pkl')
    return train_leaf, test_leaf

def get_neighbor(params):
    train_leaf, test_leaf, y_train, K = params[0],params[1], params[2], params[3]
    atile = np.tile(test_leaf, (train_leaf.shape[0],1))
    dists = np.sum(atile != train_leaf, axis = 1)
    k_neighbors = y_train[np.argsort(dists)[:K]]
    return k_neighbors

def parallel(train_leaf, test_leaf, y_train, K = 1, n_jobs = 10):
    train_leaves = [train_leaf]*len(test_leaf)
    y_train = [y_train]*len(test_leaf)
    Ks = [K] * len(test_leaf)
    pool = mp.Pool(n_jobs)
    neighbors = pool.map(get_neighbor, zip(train_leaves, test_leaf, y_train,Ks))
    return np.array(neighbors)

if __name__ == '__main__':
    global MON_SITE_NUM
    '''initialize logger'''
    logger = init_logger()
    '''read config'''
    parser = argparse.ArgumentParser(description='k-FP attack')
    parser.add_argument('feature_path',
                        metavar='<feature path>',
                        help='Path to the directory of the extracted features')
    args = parser.parse_args()
    
    '''read config file'''
    cf = read_conf(const.confdir)
    MON_SITE_NUM = int(cf['monitored_site_num'])
    MON_INST_NUM = int(cf['monitored_inst_num'])
    if cf['open_world'] == '1':
        UNMON_SITE_NUM = int(cf['unmonitored_site_num'])
        OPEN_WORLD = 1
    else:
        OPEN_WORLD = 0
    
    # logger.info('loading data...')
    dic = np.load(args.feature_path,allow_pickle=True).item()

    X = np.array(dic['feature'])
    Y = np.array(dic['label'])
    y = np.array([label[0] for label in Y])

    if not OPEN_WORLD:
        X = X[y<MON_SITE_NUM]
        y = y[y<MON_SITE_NUM]
     #   print(X.shape, y.shape)
    #here just want to save the model 
    # train_leaf, test_leaf = kfingerprinting(X,X[:1],y, y[:1])
    # np.save('dirty_tor_leaf.npy',train_leaf)
    

    tp_of_cls = np.array([0]*MON_SITE_NUM)
    p_of_cls = np.array([0]*MON_SITE_NUM)
    sss = StratifiedShuffleSplit(n_splits=10, test_size=0.1, random_state=0)
    reports = []
    start_time = time.time()
    folder_num = 1
    for train_index, test_index in sss.split(X,y):
        # logger.info('Testing fold %d'%folder_num)
        # folder_num += 1 
        # if folder_num > 2:
        #     break
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]  
        train_leaf, test_leaf = kfingerprinting(X_train,X_test,y_train, y_test)
        neighbors  = parallel(train_leaf, test_leaf, y_train, 3)
        if OPEN_WORLD:
            tp,wp,fp,p,n = open_world_acc(neighbors,y_test,MON_SITE_NUM)
            reports.append(( tp,wp,fp,p,n))

        else:
            result, tp_c, p_c = closed_world_acc(neighbors,y_test)
            print(result)
            reports.append(result)
            tp_of_cls += np.array(tp_c)
            p_of_cls += np.array(p_c)
    #        print(tp_of_cls[:5])
    if OPEN_WORLD:
        tps ,wps, fps, ps, ns = 0, 0, 0, 0, 0
        for report in reports:
            tps += report[0]
            wps += report[1]
            fps += report[2]
            ps  += report[3]
            ns  += report[4]
        print("{},{},{},{},{}".format(tps, wps, fps, ps, ns))
    else:
        print(np.array(reports).mean())
        
        for i in range(MON_SITE_NUM):
            if p_of_cls[i] == 0:
                continue
     #       print("{}, {}/{} = {:.2f}".format(i, tp_of_cls[i],p_of_cls[i],tp_of_cls[i]/p_of_cls[i]))


    for i in range(175):
        global_list[i] = global_list[i]/10

    dataset_name = args.feature_path.split('/')[1].split('.')[0]
    tag_names = "max_in_interarrival,max_out_interarrival,max_total_interarrival,avg_in_interarrival,avg_out_interarrival,avg_total_interarrival,std_in_interarrival,std_out_interarrival,std_total_interarrival,75th_percentile_in_interarrival,75th_percentile_out_interarrival,75th_percentile_total_interarrival,25th_percentile_in_times,50th_percentile_in_times,75th_percentile_in_times,100th_percentile_in_times,25th_percentile_out_times,50th_percentile_out_times,75th_percentile_out_times,100th_percentile_out_times,25th_percentile_total_times,50th_percentile_total_times,75th_percentile_total_times,100th_percentile_total_times,in_count,out_count,total_count,in_count_in_first30,out_count_in_first30,in_count_in_last30,out_count_in_last30,std_out_concentration,avg_out_concentration,avg_count_per_sec,std_count_per_sec,avg_order_in,avg_order_out,std_order_in,std_order_out,50th_out_concentration,50th_count_per_sec,min_count_per_sec,max_count_per_sec,max_out_concentrations,in_percentage,out_percentage,sum_alt_concentration,sum_alt_per_sec,sum_intertimestats,sum_timestats,sum_number_pkts,altconc_1,altconc_2,altconc_3,altconc_4,altconc_5,altconc_6,altconc_7,altconc_8,altconc_9,altconc_10,altconc_11,altconc_12,altconc_13,altconc_14,altconc_15,altconc_16,altconc_17,altconc_18,altconc_19,altconc_20,altconc_21,altconc_22,altconc_23,altconc_24,altconc_25,altconc_26,altconc_27,altconc_28,altconc_29,altconc_30,altconc_31,altconc_32,altconc_33,altconc_34,altconc_35,altconc_36,altconc_37,altconc_38,altconc_39,altconc_40,altconc_41,altconc_42,altconc_43,altconc_44,altconc_45,altconc_46,altconc_47,altconc_48,altconc_49,altconc_50,altconc_51,altconc_52,altconc_53,altconc_54,altconc_55,altconc_56,altconc_57,altconc_58,altconc_59,altconc_60,altconc_61,altconc_62,altconc_63,altconc_64,altconc_65,altconc_66,altconc_67,altconc_68,altconc_69,altconc_70,altconc_71,alt_per_sec_1,alt_per_sec_2,alt_per_sec_3,alt_per_sec_4,alt_per_sec_5,alt_per_sec_6,alt_per_sec_7,alt_per_sec_8,alt_per_sec_9,alt_per_sec_10,alt_per_sec_11,alt_per_sec_12,alt_per_sec_13,alt_per_sec_14,alt_per_sec_15,alt_per_sec_16,alt_per_sec_17,alt_per_sec_18,alt_per_sec_19,alt_per_sec_20,alt_per_sec_21,unknown_1,unknown_2,unknown_3,unknown_4,unknown_5,unknown_6,unknown_7,unknown_8,unknown_9,unknown_10,unknown_11,unknown_12,unknown_13,unknown_14,unknown_15,unknown_16,unknown_17,unknown_18,unknown_19,unknown_20,unknown_21,unknown_22,unknown_23,unknown_24,unknown_25,unknown_26,unknown_27,unknown_28,unknown_29,unknown_30,unknown_31,unknown_32"
    feature_names = np.array(tag_names.split(','))
    temp_global_list = np.array(global_list)
    sorted_idx = temp_global_list.argsort()
    fname20 = feature_names[sorted_idx][-20:]
    model20 = temp_global_list[sorted_idx][-20:]
    figure, axis = plt.subplots()
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    figure.set_figheight(40)
    figure.set_figwidth(16)
    #figure.suptitle(f'feature importance', fontsize=16)
    #axis.barh(fname20,model20)
    axis.barh(fname20, model20, height=0.5)  # Adjust the height as needed
    axis.tick_params(axis='y', labelsize=10)  # Adjust the label size as needed
    axis.tick_params(axis='x', labelsize=10)
    #plt.tight_layout()
    plt.xlabel("Random Forest Feature Importance")
    plt.ylabel("Features")
    plt.show()
    plt.draw()
    figure.savefig(dataset_name + "_feature_importance.png")
    # if not OPEN_WORLD:
    #     print(np.array(reports).mean())

   #    print(neighbors)
       # logger.info('tp:%d, wp:%d, fp:%d, p:%d, n:%d'%(tp, wp, fp, p, n))
    #    try:
    #        r_precision = tp*n / (tp*n+wp*n+r*p*fp)
    #    except:
    #        r_precision = 0.0
    #    # logger.info('%d-Precision is %.4f'%(r, r_precision))
   

