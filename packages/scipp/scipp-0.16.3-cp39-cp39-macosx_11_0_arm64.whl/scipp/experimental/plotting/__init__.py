# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Scipp contributors (https://github.com/scipp)

# flake8: noqa E402, F401

import matplotlib.pyplot as plt

plt.ioff()

from .plot import Plot
from .model import Node, show_graph, node, input_node
from .figure import Figure
from . import widgets
from .wrappers import plot
