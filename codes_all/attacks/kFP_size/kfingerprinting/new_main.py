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
    tag_names = "max_in_interarrival,max_out_interarrival,max_total_interarrival,avg_in_interarrival,avg_out_interarrival,avg_total_interarrival,std_in_interarrival,std_out_interarrival,std_total_interarrival,75th_percentile_in_interarrival,75th_percentile_out_interarrival,75th_percentile_total_interarrival,25th_percentile_in_times,50th_percentile_in_times,75th_percentile_in_times,100th_percentile_in_times,25th_percentile_out_times,50th_percentile_out_times,75th_percentile_out_times,100th_percentile_out_times,25th_percentile_total_times,50th_percentile_total_times,75th_percentile_total_times,100th_percentile_total_times,in_count,out_count,total_count,in_count_in_first30,out_count_in_first30,in_count_in_last30,out_count_in_last30,std_out_concentration,avg_out_concentration,avg_count_per_sec,std_count_per_sec,avg_order_in,avg_order_out,std_order_in,std_order_out,50th_out_concentration,50th_count_per_sec,min_count_per_sec,max_count_per_sec,max_out_concentrations,in_percentage,out_percentage,sum_alt_concentration,sum_alt_per_sec,sum_intertimestats,sum_timestats,sum_number_pkts,total_size,in_size,out_size,avg_total_size,avg_in_size,avg_out_size,var_total_size,var_in_size,var_out_size,std_total_size,std_in_size,std_out_size,max_in_size,max_out_size,,unknown_tag_0,unknown_tag_1,unknown_tag_2,unknown_tag_3,unknown_tag_4,unknown_tag_5,unknown_tag_6,unknown_tag_7,unknown_tag_8,unknown_tag_9,unknown_tag_10,unknown_tag_11,unknown_tag_12,unknown_tag_13,unknown_tag_14,unknown_tag_15,unknown_tag_16,unknown_tag_17,unknown_tag_18,unknown_tag_19,unknown_tag_20,unknown_tag_21,unknown_tag_22,unknown_tag_23,unknown_tag_24,unknown_tag_25,unknown_tag_26,unknown_tag_27,unknown_tag_28,unknown_tag_29,unknown_tag_30,unknown_tag_31,unknown_tag_32,unknown_tag_33,unknown_tag_34,unknown_tag_35,unknown_tag_36,unknown_tag_37,unknown_tag_38,unknown_tag_39,unknown_tag_40,unknown_tag_41,unknown_tag_42,unknown_tag_43,unknown_tag_44,unknown_tag_45,unknown_tag_46,unknown_tag_47,unknown_tag_48,unknown_tag_49,unknown_tag_50,unknown_tag_51,unknown_tag_52,unknown_tag_53,unknown_tag_54,unknown_tag_55,unknown_tag_56,unknown_tag_57,unknown_tag_58,unknown_tag_59,unknown_tag_60,unknown_tag_61,unknown_tag_62,unknown_tag_63,unknown_tag_64,unknown_tag_65,unknown_tag_66,unknown_tag_67,unknown_tag_68,unknown_tag_69,unknown_tag_70,unknown_tag_71,unknown_tag_72,unknown_tag_73,unknown_tag_74,unknown_tag_75,unknown_tag_76,unknown_tag_77,unknown_tag_78,unknown_tag_79,unknown_tag_80,unknown_tag_81,unknown_tag_82,unknown_tag_83,unknown_tag_84,unknown_tag_85,unknown_tag_86,unknown_tag_87,unknown_tag_88,unknown_tag_89,unknown_tag_90,unknown_tag_91,unknown_tag_92,unknown_tag_93,unknown_tag_94,unknown_tag_95,unknown_tag_96,unknown_tag_97,unknown_tag_98,unknown_tag_99,unknown_tag_100,unknown_tag_101,unknown_tag_102,unknown_tag_103,unknown_tag_104,unknown_tag_105,unknown_tag_106,unknown_tag_107,unknown_tag_108"
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
   

