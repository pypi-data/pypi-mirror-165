# REPLENV: ~/.pyvenv/pysimrel/bin/activate

from pysimrel.pysimrel import Simrel
from pysimrel.simrelplot import plot_true_coef
import numpy as np
import matplotlib.pyplot as plt

sim_obj = Simrel()
ax = plt.plot(sim_obj.properties.beta, markers="o")
plt.axhline(y=0, linestyle="--", color="k")
plt.show()
