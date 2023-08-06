#REPLENV: /Users/therimalaya/.pyvenv/pysimrel/bin/activate

from pysimrel.utilities import *
from pysimrel.pysimrel import *
from functools import reduce
from dataclasses import dataclass, field
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def plot_true_coef(obj):
    row, col = sobj.properties.sigma.shape
    gap_idx = sobj.n_resp
    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(row, col, figure=fig)
    ax1 = fig.add_subplot(gs[:gap_idx,:gap_idx])
    ax1.imshow(sobj.covariances.cov_ww)
    # ax[0,1].imshow(sobj.covariances.cov_zw.T)
    # ax[1,0].imshow(sobj.covariances.cov_zw)
    # ax[1,1].imshow(sobj.covariances.cov_zz)
    plt.show()

sobj = Simrel()
plot_true_coef(sobj)


