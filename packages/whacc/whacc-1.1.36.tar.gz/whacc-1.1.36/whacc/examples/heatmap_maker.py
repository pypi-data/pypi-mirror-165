


import matplotlib.pyplot as plt
from tqdm.auto import tqdm
from imgaug import augmenters as iaa  # optional program to further augment data

from whacc import utils
import numpy as np
from whacc import image_tools, PoleTracking
from natsort import natsorted, ns
import pickle
import pandas as pd
import os
import copy
import seaborn as sns
from keras.preprocessing.image import ImageDataGenerator
import h5py

from whacc import utils, analysis
import h5py
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from pathlib import Path

from whacc import utils, image_tools, transfer_learning, analysis
from IPython.utils import io
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow import keras
from sklearn.utils import class_weight
import time
from pathlib import Path
import os
import copy
import numpy as np
from tensorflow.keras import applications
from pathlib import Path
import shutil
import zipfile
from datetime import datetime
import pytz
import json
from whacc import model_maker

from whacc.model_maker import *
import itertools

import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
import h5py
from whacc import image_tools
from whacc import utils
import copy
import time
import os
import pdb
import glob
from tqdm.contrib import tzip
import scipy.io as spio
import h5py
# from tqdm.notebook import tqdm
from matplotlib import cm

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.patches as mpatches
from scipy.signal import medfilt, medfilt2d
import cv2


def plot_segments_with_array_blocks(actual_h5_img_file, list_of_inds_to_plot, in_list_of_arrays=[], seg_num=0, border=4,
                                    height=20, img_width=61,
                                    color_numers_to_match=[0, 1, 2, 3, 4, 5], color_list=[0, .5, .2, .3, .75, .85],
                                    cmap_col='inferno', max_frames=40, min_frames=10):
    # apply max and min
    # in_list_of_arrays[0] needs to be the "true"" values
    if in_list_of_arrays == []:
        print('no input arrays, returning...')
        return
    color_dict = dict()
    cmap = cm.get_cmap(cmap_col)

    for i, k1 in enumerate(color_list):
        color_dict[i] = np.asarray(cmap(k1)[:-1]) * 255

    in_list_of_arrays = copy.deepcopy(in_list_of_arrays)

    # set/adjust size of the array
    inds = list(range(list_of_inds_to_plot[seg_num][0] - border, list_of_inds_to_plot[seg_num][-1] + 1 + border * 2))
    inds = inds[:max_frames]
    if len(inds) < min_frames:
        inds = np.arange(inds[0], inds[0] + min_frames)

    # get the image array with colored blocks
    for i, k in enumerate(in_list_of_arrays):
        k = k.astype(float)
        if i == 0:
            tmp1 = np.tile(np.repeat(k[inds], img_width, axis=0), (height, 1))
        else:
            tmp1 = np.vstack((tmp1, np.tile(np.repeat(k[inds], img_width, axis=0), (height, 1))))
    tmp1 = np.stack((tmp1,) * 3, axis=-1)

    for kk in color_numers_to_match:
        tmp3 = np.where(tmp1 == kk)
        for i1, i2 in zip(tmp3[0], tmp3[1]):
            tmp1[i1, i2, :] = color_dict[kk]

    tmp1 = tmp1.astype(int)
    with h5py.File(actual_h5_img_file, 'r') as h:
        tmp2 = image_tools.img_unstacker(h['images'][inds[0]:inds[-1] + 1], num_frames_wide=len(inds))
        print(tmp1.shape, tmp2.shape)
        tmp2 = np.vstack((tmp1, tmp2))
    return tmp2

def remap_array_to_color_channels(in_array, color_numers_to_match=None, color_list=[0, .5, .2, .3, .75, .85],
                                  cmap_col='inferno'):
    in_array = copy.deepcopy(in_array).astype(int)
    out_array = np.stack((in_array,) * 3, axis=-1)

    color_dict = dict()
    cmap = cm.get_cmap(cmap_col)
    if color_numers_to_match is None:
        color_numers_to_match = np.unique(in_array).astype(int)
        print(color_numers_to_match)

    for key, k1 in zip(color_numers_to_match, color_list):
        color_dict[key] = (np.asarray(cmap(k1)[:-1]) * 255).astype(int)
    for ii, kk in enumerate(color_numers_to_match):
        out_array[(in_array == kk).astype(bool)] = color_dict[kk]

    return out_array, color_dict


def foo_heatmap_with_critical_errors(real_bool, pred_bool, in_range, frame_nums, lines_thick=20, title_str='',
                                     figsize=(10, 10)):
    acc_percentage = ((pred_bool == real_bool) * 1).astype(float)
    acc_percentage[np.invert(in_range.astype(bool))] = np.nan
    acc_percentage = np.nanmean(acc_percentage)
    acc_percentage = str(np.round(acc_percentage * 100, 2)) + '%  '
    title_str = acc_percentage + title_str

    c_list = []
    for n in [2, 3, 4, 5, 8]:
        c_list.append(.0833 / 2 + n * .0833)

    max_ = np.max(frame_nums)
    x = np.zeros([len(frame_nums), int(max_)]) - 2

    d = real_bool - pred_bool
    d = d + (real_bool + pred_bool == 2) * 2  # TP = 2, TN = 0, FP = -1, FN = 1 ...... -2 pole out of range

    for i, (k1, k2) in enumerate(utils.loop_segments(frame_nums)):
        L = frame_nums[i]
        tmp1 = d[k1:k2]

        tmp1[in_range[k1:k2] == 0] = -2
        # in_range[k1:k2]
        x[i, :L] = tmp1

    x2, color_dict = remap_array_to_color_channels(x, color_numers_to_match=[0, 2, 1, -1, -2], color_list=c_list,
                                                   cmap_col='Paired')
    x2 = np.repeat(x2, lines_thick, axis=0)

    # get the color coded error type matrix
    a = analysis.error_analysis(real_bool, pred_bool, frame_num_array=frame_nums)
    d = copy.deepcopy(a.coded_array)
    d[d < 0] = -2
    d[d >= 4] = -2

    max_ = np.max(frame_nums)
    x = np.zeros([len(frame_nums), int(max_)]) - 2

    for i, (k1, k2) in enumerate(utils.loop_segments(frame_nums)):
        L = frame_nums[i]
        tmp1 = d[k1:k2]

        tmp1[in_range[k1:k2] == 0] = -2
        x[i, :L] = tmp1
    c_list = []
    for n in [1, 3, 4, 5, 8]:  # ['ghost', 'miss', 'join', 'split', nothing
        c_list.append(.1111 / 2 + n * .1111)
    x2_error_type, color_dict_error_type = remap_array_to_color_channels(x, color_numers_to_match=[0, 1, 2, 3, -2],
                                                                         color_list=c_list, cmap_col='Set1')
    print(np.nanmin(x2_error_type))
    x2_error_type = np.repeat(x2_error_type, lines_thick, axis=0)

    for i, (k1, k2) in enumerate(utils.loop_segments([10, 10] * len(
            frame_nums))):  # nan out certain regions so that we can leave those to be filled in with actual heatmap
        if (i % 2) != 0:
            x2_error_type[k1:k2] = color_dict_error_type[-2]

    x3 = copy.deepcopy(x2).astype(int)
    inds = x2_error_type != color_dict_error_type[-2]
    x3[inds] = x2_error_type[inds]
    plt.figure(figsize=figsize)
    plt.imshow(x3)

    # LEGEND
    all_labels = ['TN', 'TP', 'FN', 'FP', 'pole down']
    patches = []
    for i, ii in zip(color_dict, all_labels):
        c = color_dict[i] / 255
        patches.append(mpatches.Patch(color=c, label=ii))
    all_labels = ['ghost', 'miss', 'join', 'split']
    for i, ii in zip(color_dict_error_type, all_labels):
        c = color_dict_error_type[i] / 255
        patches.append(mpatches.Patch(color=c, label=ii))
    plt.legend(handles=patches, bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0, fontsize=15, prop={'size': 6})
    plt.title(title_str, fontsize=20)

    return x3


h5 = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1pUteMEgx37rAyqujJWxVN9-ywFAqaxhF/WhACC_PROCESSING_FOLDER/Finished_Sessions/Session1_FINISHED/Session1/AH1179X23052021x1_final_combined.h5'
h5 = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1pUteMEgx37rAyqujJWxVN9-ywFAqaxhF/WhACC_PROCESSING_FOLDER/Finished_Sessions/Session21_FINISHED/Session21/AH1184X08062021x21_final_combined.h5'
# h5 = '/Users/phil/Desktop/SAMSONS_TEST_SESSIONS/TESTING_SAMSONS_MP4S_FINISHED/AH1179X01062021x14_final_combined.h5'
####################################
####################################a
model_list = utils.get_files('/Users/phil/Desktop/model_saves', '*.pkl')
model_list = model_list[-3:]
utils.foo_predict_mods(model_list, h5)
####################################
####################################
utils.lister_it(utils.print_h5_keys(h5, 1, 0), 'YHAT__')
labels_key = 'sess21_4perTrial_withOUT_sess1_OG_in_valData_V1'
labels_key = 'sess21_4perTrial_with_sess1_OG_NOTin_valData_V1'
labels_key = 'sess21_4perTrial_with_sess1_OG_in_valData_V1'
pred_bool_temp = image_tools.get_h5_key_and_concatenate(h5, labels_key)
contacts_samson_curated_for_transfer_learning_220707 = image_tools.get_h5_key_and_concatenate(h5, 'contacts_samson_curated_for_transfer_learning_220707')
labels = image_tools.get_h5_key_and_concatenate(h5, 'labels')
frame_nums = image_tools.get_h5_key_and_concatenate(h5, 'frame_nums')
locations_x_y = np.asarray(image_tools.get_h5_key_and_concatenate(h5, 'locations_x_y'))
x_loca_all = locations_x_y[1500::3000, 0]
loc_x_sort_inds = np.argsort(x_loca_all)
################################################
""" SET THHE SOURCE OF THE LABELS YOU ARE DRAWING FROM MAKE SURE TO ADJUST MODEL IND ACCORDINGLY"""
threshold = .4
lines_thick = 20
kernel_size = 11
test_mood = False

if test_mood:### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP### TEMP
    pred_bool_smoothed = medfilt(copy.deepcopy(pred_bool_temp).flatten(), kernel_size=kernel_size)
    pred_bool_smoothed = (pred_bool_smoothed>threshold)*1

    real_bool = pred_bool_smoothed
    in_range = np.ones_like(pred_bool_temp)
else:
    pred_bool_smoothed = medfilt(copy.deepcopy(pred_bool_temp).flatten(), kernel_size=kernel_size)
    pred_bool_smoothed = (pred_bool_smoothed>threshold)*1

    in_range = 1*(contacts_samson_curated_for_transfer_learning_220707!=-1)

    real_bool = contacts_samson_curated_for_transfer_learning_220707
    real_bool[np.invert(in_range.astype(bool))] = -1
    real_bool = 1*(real_bool==1)



a = analysis.error_analysis(real_bool, pred_bool_smoothed, frame_nums)
ind = 0
x = a.all_errors_sorted[ind][0]
error_type = a.all_error_type_sorted[ind]

for i, (k1, k2) in enumerate(utils.loop_segments(frame_nums)):
    if k1 <= x < k2:
        print('trial num', i, error_type)
        y_line = i * lines_thick - lines_thick
        x_line = x - k1 - 1
        break

# x2 = foo_heatmap_with_critical_errors(real_bool, pred_bool_smoothed, in_range, frame_nums.astype(int), title_str='')


# tmp3 = plot_segments_with_array_blocks(h5, [[100]], in_list_of_arrays=[real_bool, pred_bool_smoothed],
#                                        seg_num=0,
#                                        color_numers_to_match=[0, 1], color_list=[0, .5], cmap_col='nipy_spectral',
#                                        max_frames=20, min_frames=20)

x2 = foo_heatmap_with_critical_errors(real_bool, pred_bool_smoothed, in_range, frame_nums.astype(int), title_str='')

tmp1 = []
for k in range(10):
    tmp1.append(x2[10+k::10, :, :])

plt.imshow(tmp1[0], interpolation='nearest', aspect='auto')
x4 = []
# fig, ax = plt.subplots(1, 2, sharex=True, gridspec_kw={'height_ratios': [10, 1]})
# fig, ax = plt.subplots(1, 2)
for k in loc_x_sort_inds:
    kk = k*lines_thick
    tmp1 = x2[kk:kk+lines_thick, :, :]
    if not np.all(np.unique(tmp1) == [178, 202, 214]):
        # if k in [0, 1, 2, 3]:
        #     tmp1 = np.ones_like(tmp1)*20
        x4.append(tmp1)

x4 = np.vstack(x4)
plt.figure()
plt.imshow(x4[0::20, :, :], interpolation='nearest', aspect='auto')

plt.plot(np.sort(x_loca_all))

# real_bool = real_bool[:3000*100]
# pred_bool_smoothed = pred_bool_smoothed[:3000*100]
h5_images = '/Volumes/GoogleDrive-114825029448473821206/.shortcut-targets-by-id/1pUteMEgx37rAyqujJWxVN9-ywFAqaxhF/WhACC_PROCESSING_FOLDER/Session1_FINISHED_MP4s/Session1/image_frames.h5'
tmp3 = plot_segments_with_array_blocks(h5_images, [[10]], in_list_of_arrays=[real_bool, pred_bool_smoothed],
                                       seg_num=0,img_width=71,
                                       color_numers_to_match=[0, 1], color_list=[0, .5], cmap_col='nipy_spectral',
                                       max_frames=20, min_frames=20)



# tmp1 = image_tools.get_h5_key_and_concatenate(h5_images, 'labels')
# tmp1.shape

new_shape = (x2.shape[1], np.round((x2.shape[1] / tmp3.shape[1]) * tmp3.shape[0]).astype(int))
tmp3 = cv2.resize(tmp3.astype('float32'), new_shape)

x3 = np.vstack((x2, tmp3.astype(int)))

fig1 = plt.figure(figsize=[15, 10])
img_1 = plt.imshow(x3)
plt.tight_layout()

marker_point, = plt.plot(x_line, y_line, 'vk', markersize=5)
marker_point.set_ydata(0)
marker_point.set_xdata(0)


def onclick(event):
    # global ix, iy, lines_thick, marker_point, real_bool_tmp, pred_bool_tmp, x2, img_1, frame_nums
    ix, iy = event.xdata - lines_thick, event.ydata - lines_thick

    print('x = %d, y = %d' % (ix, iy))

    # global coords
    # coords.append((ix, iy))
    #
    # if len(coords) == 2:
    #     fig.canvas.mpl_disconnect(cid)
    # foo(frame_nums, lines_thick, x)
    x3 = np.round(ix)
    trial = int(np.floor(iy / lines_thick))
    y3 = np.sum(frame_nums[:trial + 1])
    ind = int(x3 + y3)
    marker_point.set_ydata(trial * lines_thick)
    marker_point.set_xdata(x3)
    print(x3, y3)

    # tmp3 = plot_segments_with_array_blocks(h5_file_IMG, [[ind]], in_list_of_arrays=[real_bool_tmp, pred_bool_tmp],
    #                                        seg_num=0,
    #                                        color_numers_to_match=[0, 1], color_list=[0, .5], cmap_col='nipy_spectral',
    #                                        max_frames=20, min_frames=20)
    tmp3 = plot_segments_with_array_blocks(h5_images, [[ind]], in_list_of_arrays=[real_bool, pred_bool_smoothed],
                                       seg_num=0,img_width=71,
                                       color_numers_to_match=[0, 1], color_list=[0, .5], cmap_col='nipy_spectral',
                                       max_frames=20, min_frames=20)
    new_shape = (x2.shape[1], np.round((x2.shape[1] / tmp3.shape[1]) * tmp3.shape[0]).astype(int))
    tmp3 = cv2.resize(tmp3.astype('float32'), new_shape)

    x3 = np.vstack((x2, tmp3.astype(int)))
    img_1.set_data(x3)
    # marker_point, = plt.plot(ix, iy-lines_thick, '+k', markersize=5)
    # return coords


fig = plt.gcf()
cid = fig.canvas.mpl_connect('button_press_event', onclick)

_ = plt.text(50, 1317, 'Real\nPred', fontsize=5, color='w')

plt.figure()
_ = plt.hist(pred_bool_temp, 100)


#
#
# a = analysis.error_analysis(1*(real_bool==1), 1*(pred_bool_smoothed==1), frame_num_array=frame_nums.astype(int))
# # pred_bool = copy.deepcopy(pred_bool_smoothed)
# # pred_bool[np.invert(in_range.astype(bool))] = -1
# x2 = foo_heatmap_with_critical_errors(real_bool, pred_bool_smoothed, in_range, frame_nums, title_str='median smoothed')


for i, (i1, i2) in enumerate(utils.loop_segments(frame_nums)):
    ii = i*lines_thick
    x = pd.Series(pred_bool_temp[i1:i2])
    tmp1 = np.argmax(x.rolling(window=10).std())
    plt.plot(tmp1,ii, '.k')


yhat = 'array of predicitons output fomr model'
from scipy.signal import medfilt
yhat_smoothed = medfilt(copy.deepcopy(yhat), 7)
yhat_smoothed = 1*(yhat_smoothed>.5)
utils.overwrite_h5_key()







tmp1 = np.linspace(0, 1, 311)*1000
tmp2 = np.round(tmp1)
plt.plot(tmp2, '.')



