# © Copyright 2022 CERN. This software is distributed under the terms of 
# the GNU General Public Licence version 3 (GPL Version 3), copied verbatim 
# in the file "LICENCE.txt". In applying this licence, CERN does not waive 
# the privileges and immunities granted to it by virtue of its status as an 
# Intergovernmental Organization or submit itself to any jurisdiction.

from multiprocessing.context import _default_context
from turtle import color
from numpy import float64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from scipy import stats
from scipy import linalg
from datetime import datetime
import matplotlib.dates as mdates
from csv import DictReader

pd.set_option('display.width', None)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', None, 'display.max_columns', None)

# filename_all_data  = 'test_finde/transfer_broker_rx_all_transfers_1652599569.760289.txt.txt'
# filename_transfers = 'test_finde/transfer_broker_rx_CERN-PROD_TRIUMF-LCG2_1652599569.7602243.txt'
# filename_all_data = 'test_triumf/transfer_broker_tx_all_transfers_1652870285.0060742.txt'
# filename_transfers = 'test_triumf/transfer_broker_tx_TRIUMF-LCG2_CERN-PROD_1652870285.006065.txt'
# filename_all_data = 'test_triumf/transfer_broker_rx_all_transfers_1652870285.0061207.txt'
# filename_transfers = 'test_triumf/transfer_broker_rx_CERN-PROD_TRIUMF-LCG2_1652870285.0060718.txt'

filename_all_data = 'test_triumf_intermittent/transfer_broker_rx_all_transfers_1653902850.072492.txt'
filename_transfers = 'test_triumf_intermittent/transfer_broker_rx_CERN-PROD_TRIUMF-LCG2_1653902850.0724514.txt'
# filename_all_data = 'test_triumf_intermittent/transfer_broker_tx_all_transfers_1653902850.0724537.txt'
# filename_transfers = 'test_triumf_intermittent/transfer_broker_tx_TRIUMF-LCG2_CERN-PROD_1653902850.072444.txt'

dict_all_data  = pd.read_csv(filename_all_data,  delimiter = ',', header = None, names = ['Timestamp', 'Datetime', 'Source', 'Destination', 'Data [GB]', 'Throughput [Gbps]', 'Parallel transfers', 'Queued transfers']).to_dict()
dict_transfers = pd.read_csv(filename_transfers, delimiter = ',', header = None, names = ['Timestamp', 'Datetime', 'Source', 'Destination', 'Data [GB]', 'Throughput [Gbps]', 'Parallel transfers', 'Queued transfers']).to_dict()
df_all_data    = pd.DataFrame.from_dict(dict_all_data)
df_transfers   = pd.DataFrame.from_dict(dict_transfers)

# Function to format data
def format_data(df_data):
    # Format data
    df_data['Datetime']    = df_data['Datetime'].str.split('datetime:', expand = True)[1].astype(str)                     # Format datetime: 2022-05-15 01:20:05.848425  -> 2022-05-15 01:20:05.848425
    df_data['Datetime']    = df_data['Datetime'].str.replace('\..*', '', regex = True)                                    # Format datetime: 2022-05-15 01:20:05.848425  -> 2022-05-15 01:20:05
    df_data['Datetime']    = pd.to_datetime(df_data['Datetime'], format = '%Y/%m/%d %H:%M:%S')
    df_data['Data [GB]']   = df_data['Data [GB]'].str.split(' ', expand = True)[3].astype(float64)                        # Format data: data_gigabytes [GB]: 5.89805632 -> 5.89805632
    df_data['Timestamp']   = df_data['Timestamp'].str.split(' ', expand = True)[1].astype(int)                            # Format timestamp: timestamp: 1648645043578 [milliseconds] -> 1648645043578
    df_data['Queued transfers']     = df_data['Queued transfers'].str.split(' ', expand = True)[2].astype(int)            # Format queue: queued_transfers: 2126 -> 2126
    df_data['Throughput [Gbps]']    = df_data['Throughput [Gbps]'].str.split(' ', expand = True)[3].astype(float64)       # Format throughput: throughput_gigabits [Gb/s]: 5.89805632 -> 5.89805632
    df_data['Parallel transfers']   = df_data['Parallel transfers'].str.split(' ', expand = True)[2].astype(int)          # Format TCP transfers: parallel_transfers: 252 -> 252
    df_data.set_index(pd.DatetimeIndex(df_data['Datetime']), inplace = True)
    return df_data

# Function to plot data XY Graph
def generate_plots(axis, data, ylabel, x_xticks_datetime, title, color, fig, stats):
    x_axis = np.linspace(0, data.shape[0]-1, num = data.shape[0])
    axis.plot(x_xticks_datetime, data, color = color, linewidth = 2, zorder = 1)
    # if color == 'tab:orange': axis.fill_between(x_xticks_datetime, 0, data, where = data, color = color, alpha = 0.2)
    if stats:
        axis.scatter(x_xticks_datetime, data, color = color, marker = '.', zorder = 1, s = 2)
        axis.axhline(data.mean(), color = color, linestyle = '-.', linewidth = 1, zorder = 1, label = 'Mean = ' + str(round(data.mean(), 2))) # Mean value
        # Statistics: Linear Regression
        linear_regression = linregress(x_axis, data)
        m = linear_regression.slope
        b = linear_regression.intercept
        axis.plot(x_xticks_datetime, m*x_axis+b, color = 'xkcd:tan', linewidth = 1, zorder = 1, label = 'Linear regresion: \n$y = mx + b \longrightarrow m = $' + str(round(m, 2)) + '$, b = $' + str(round(b, 2)))
        # Statistics: Linear Least-Squares
        # Compute least-squares solution to equation Ax = b.
        # Compute a vector x such that the 2-norm |b - A x| is minimized
        # https://docs.scipy.org/doc/scipy/tutorial/stats.html
        # https://docs.scipy.org/doc/scipy/tutorial/linalg.html
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lstsq.html
        M = x_axis[:, np.newaxis]**[0, 2]      # Fit a quadratic polynomial of the form y = a + b*x**2 to data. We first form the “design matrix” M, with a constant column of 1s and a column containing x**2
        p, res, rnk, s = linalg.lstsq(M, data) # Find the least-squares solution to M.dot(p) = y, where p is a vector with length 2 that holds the parameters a and b
        yy = p[0] + p[1]*x_axis**2             # y = a + b*x**2
        axis.plot(x_xticks_datetime, yy, color = 'xkcd:lightblue', linewidth = 1, zorder = 1, label = 'Linear least-squares: \n$y = a + bx^2 \longrightarrow a = $' + str(round(p[0], 2)) + '$, b = $' + str(round(p[1], 2)))
        # Title, legend, ylabel, grid and xticks labels
        fig.suptitle(title)
        axis.grid(axis = 'x', linestyle = ':')
        axis.set_ylabel(ylabel)
        axis.legend(loc = 'upper right', fontsize = 6)
        # Date format in x-axis
        format = mdates.DateFormatter('%d/%m/%Y\n%H:%M:%S')
        axis.xaxis.set_major_formatter(format)

# Function to plot threshold values
def generate_plots_threshold(axis, df_all_data, str_data, color, threshold):
    df_data = df_all_data[df_all_data[str_data] > threshold]
    axis.scatter(df_data['Datetime'], df_data[str_data], color = color, linewidth = 2, marker = '.', zorder = 2)

# Main function
def main():
    # Format data
    df_all = format_data(df_all_data)
    df_trf = format_data(df_transfers)
    # Fill with NaN the datetime where there were no transfers [remove lines while plotting discontinuities]
    list_transfers_datetime = df_trf['Datetime'].to_list()
    df_not_transfers = df_all[~df_all['Datetime'].isin(list_transfers_datetime)]['Datetime']
    df_trf = pd.concat([df_trf, df_not_transfers])
    df_trf = df_trf.sort_index()
    # Plot data
    fig, axs = plt.subplots(4, 1)
    generate_plots(axs[0], df_all['Data [GB]'], 'Amount of Data [GB]', df_all['Datetime'], 'CERN - TRIUMF', 'tab:blue',   fig, True)
    generate_plots(axs[0], df_trf['Data [GB]'], 'Amount of Data [GB]', df_trf['Datetime'], 'CERN - TRIUMF', 'tab:orange', fig, False)
    generate_plots(axs[1], df_all['Throughput [Gbps]'],  'Throughput [Gbps]',  df_all['Datetime'], 'CERN - TRIUMF', 'tab:blue',   fig, True)
    generate_plots(axs[1], df_trf['Throughput [Gbps]'],  'Throughput [Gbps]',  df_trf['Datetime'], 'CERN - TRIUMF', 'tab:orange', fig, False)
    generate_plots(axs[2], df_all['Parallel transfers'], 'Parallel transfers', df_all['Datetime'], 'CERN - TRIUMF', 'tab:blue',   fig, True)
    generate_plots(axs[2], df_trf['Parallel transfers'], 'Parallel transfers', df_trf['Datetime'], 'CERN - TRIUMF', 'tab:orange', fig, False)
    generate_plots(axs[3], df_all['Queued transfers'], 'Queued transfers', df_all['Datetime'], 'CERN - TRIUMF', 'tab:blue',   fig, True)
    generate_plots(axs[3], df_trf['Queued transfers'], 'Queued transfers', df_trf['Datetime'], 'CERN - TRIUMF', 'tab:orange', fig, False)
    # Plot thresholds
    generate_plots_threshold(axs[0], df_all, 'Data [GB]', 'red', 20)
    generate_plots_threshold(axs[1], df_all, 'Throughput [Gbps]',  'red', 20)
    generate_plots_threshold(axs[2], df_all, 'Parallel transfers', 'red', 200)
    generate_plots_threshold(axs[3], df_all, 'Queued transfers',   'red', 3500)
    # Share x-axis and remove space between them
    axs[3].get_shared_x_axes().join(axs[3], axs[2], axs[1], axs[0])
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()

main()
