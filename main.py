import os
import json
import shutil
import random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)    # TF > 1.12
#tf.logging.set_verbosity(tf.logging.ERROR)
from warnings import simplefilter

# Seed for reproducibility of results
seed = 1337
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)

from datasets.Movielens import Movielens
from binGANMF import BinGANMF
from EnGANMF import EncoderGANMF
from Base.Evaluation.Evaluator import EvaluatorHoldout

# Supress Tensorflow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['KMP_WARNINGS'] = '0'
simplefilter(action='ignore', category=UserWarning)
simplefilter(action='ignore', category=FutureWarning)

use_gpu = False
verbose = False
only_build = False
transposed = False

if not use_gpu:
    os.environ['CUDA_VISIBLE_DEVICES'] = ''

reader =  Movielens(version='100K', split_ratio=[0.6, 0.2, 0.2], use_local=True, implicit=True, verbose=False, seed=seed)

URM_train = reader.get_URM_train(transposed=transposed)
URM_validation = reader.get_URM_validation(transposed=transposed)
URM_test = reader.get_URM_test(transposed=transposed)
print(URM_train)
evaluator = EvaluatorHoldout(URM_test, [5, 20], exclude_seen=True)
evaluatorValidation = EvaluatorHoldout(URM_validation, [5], exclude_seen=True)

gan = BinGANMF(URM_train, mode='user')

_,epoch_metrics = gan.fit(num_factors=10,
        d_layers=5,
        d_nodes=128,
        d_hidden_act='linear',
        d_reg=1e-4,
        g_reg=0,
        epochs=500,
        batch_size=32,
        g_lr=1e-3,
        d_lr=1e-3,
        d_steps=1,
        g_steps=1,
        recon_coefficient=0.05,
        allow_worse=5,
        freq=5,
        validation_evaluator=evaluatorValidation,
        sample_every=10,
        validation_set=URM_validation)
#
# #print(epoch_metrics)
def plot_roc_auc_per_epoch(epoch_metrics):
    epoch_numbers = []
    roc_auc_values = []
    i = 1
    for epoch_dict in epoch_metrics:
        epoch_number = list(epoch_dict.keys())[0]
        roc_auc_value = epoch_dict[epoch_number]['RMSE']
        epoch_numbers.append(i)
        roc_auc_values.append(roc_auc_value)
        i = i +1
    # Plotting the ROC AUC values
    plt.plot(epoch_numbers, roc_auc_values, marker='o')
    plt.xlabel('Epoch')
    plt.ylabel('ROC AUC')
    plt.title('ROC AUC per Epoch')
    plt.show()

plot_roc_auc_per_epoch(epoch_metrics)
if not only_build:
    results_dic, results_run_string = evaluator.evaluateRecommender(gan)
    print(results_run_string)

    map_folder = os.path.join('plots', gan.RECOMMENDER_NAME, 'MAP_' + str(results_dic[5]['MAP'])[:7])
    if os.path.exists(map_folder):
        shutil.rmtree(map_folder)
    shutil.move(src=gan.logsdir, dst=map_folder)
