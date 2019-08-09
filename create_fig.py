#!/usr/bin/python3
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys



def data_cleaning(clean):
    clean = clean[1]
    fig_df = pd.read_csv(clean)



    ax1 = plt.subplot(131)
    ax1.hist(fig_df['Pulse'], np.linspace(30, 150, 100), alpha=0.5, label='Charted VS')
    ax1.hist(fig_df['hr'], np.linspace(30, 150, 100), alpha=0.5, label='ECG',color = "red")
    ax1.set_title('Heart Rate')
    ax1.set_xlabel("Beats/Min")
    ax1.set_ylabel('Count')
    ax1.set_xlim([30, 150])


    ax2 = plt.subplot(132)
    ax2.hist(fig_df['Resp'], np.linspace(10, 40, 30), alpha=0.5, label='Charted VS')
    ax2.hist(fig_df['edrk'], np.linspace(10, 40, 30), alpha=0.5, label='ECG',color = "red")
    ax2.set_xlabel('Breaths/Min')
    ax2.set_title('Resp Rate')
    ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.subplots_adjust(left=None, bottom=None, right=3, top=None, wspace=None, hspace=None)
    plt.savefig('figure.png',bbox_inches='tight')



if __name__ == '__main__':
    data_cleaning(sys.argv)
