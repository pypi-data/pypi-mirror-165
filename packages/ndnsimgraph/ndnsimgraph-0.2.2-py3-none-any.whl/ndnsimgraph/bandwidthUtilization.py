"""
实现带宽利用率计算
"""
import math

from .throughput import ThroughputExtractBase, Throughput, NodeThroughput
from .common import GraphBase, ExportBase, NodeItem
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.legend import Legend
from matplotlib.patches import Patch
import matplotlib.ticker as mticker


class BandWidthUtilizationItem:
    """
    带宽利用率条目
    label => R1-R2
    nodeName => R1
    faceId => 271
    bandwidth => 100
    """

    def __init__(self, label: str, ticker: str, nodeName: str, faceId: int,
                 bandwidth: float, x: [float], y: [float]):
        self.label = label
        self.ticker = ticker
        self.nodeName = nodeName
        self.faceId = faceId
        self.bandwidth = bandwidth
        self.x = x
        self.y = y
        self.value = np.mean([item / bandwidth for item in y])


class BandwidthUtilizationExtractBase(ThroughputExtractBase):
    def __init__(self, throughput: Throughput):
        ThroughputExtractBase.__init__(self, throughput)
        self.bandwidth = 100


class BandwidthUtilizationGraph(BandwidthUtilizationExtractBase, GraphBase):
    """
    一个用于实现绘制带宽利用率图的类
    """

    def __init__(self, throughput: Throughput):
        GraphBase.__init__(self)
        BandwidthUtilizationExtractBase.__init__(self, throughput)
        self.totalWidth = 1
        self.figSize = (10, 7)  # 图的大小
        self.edgecolor = "black"  # 边缘颜色
        self.totalWidth = 0.8
        self.fig = None
        self.ax = None
        self.items: [BandWidthUtilizationItem] = []

    def xlim(self, *args, **kwargs):
        self.ax.set_xlim(*args, **kwargs)
        return self

    def ylim(self, *args, **kwargs):
        plt.ylim(*args, **kwargs)
        return self

    def xticks(self, ticks=None, labels=None, **kwargs):
        plt.xticks(ticks, labels, **kwargs)
        return self

    def title(self, label, fontdict=None, loc=None, pad=None, **kwargs):
        # self.ax.title(label, fontdict=fontdict, loc=loc, pad=pad, **kwargs)
        return self

    def legend(self, *args, **kwargs):
        handles, labels = self.ax.get_legend_handles_labels()
        self.ax.legend(handles, labels, *args, **kwargs)
        return self

    # def categoryLegend(self, facecolor='white', *args, loc='upper left', **kwargs):
    #     categories, patches = [], []
    #     for dtc in self.deliveryTimeCollections:
    #         categories.append(dtc.collectionName)
    #         patches.append(Patch(facecolor=facecolor, edgecolor=self.edgecolor, hatch=dtc.hatch))
    #     if "frameon" not in kwargs:
    #         kwargs["frameon"] = False
    #     leg = Legend(self.ax, patches, categories, *args, loc=loc, **kwargs)
    #     self.ax.add_artist(leg)
    #     return self

    def append(self, label: str, ticker: str, nodeName: str, faceId: int, bandwidth: float):
        """
        添加一个带宽利用率记录
        :param label:           dsccp
        :param ticker:          R1-R2
        :param nodeName:        R1
        :param faceId:          271
        :param bandwidth:       10
        :return:
        """
        node = self.getNode(nodeName)
        if not node:
            print("not exist node: ", node)
            return self
        x, y = self.getX(node, faceId), self.getY(node, faceId)
        self.items.append(BandWidthUtilizationItem(label, ticker, nodeName, faceId, bandwidth, x, y))
        return self

    def doDraw(self):
        """
        绘制带宽利用率对比图
        :return:
        """
        links, maxSize = dict(), 0
        colors, hatchs = dict(), dict()
        for item in self.items:
            if item.label not in links:
                links[item.label] = [item]
            else:
                links[item.label].append(item)
            if item.label not in colors:
                colors[item.label] = self.autoSelectColor()
                self.currentUsedColor[colors[item.label]] = item.label
            if item.label not in hatchs:
                hatchs[item.label] = self.autoSelectHatch()
            maxSize = max(maxSize, len(links[item.label]))

        xStart = np.arange(maxSize)
        total_width, n = self.totalWidth, len(links)
        width = total_width / n
        xStart = xStart - ((n - 1) * width / 2)

        self.fig, self.ax = plt.subplots(figsize=self.figSize)
        offsetX, isFirst = 0, True
        firstLabel = None
        for label in links:
            items = links[label]
            if firstLabel is None:
                firstLabel = label

            self.ax.bar(xStart + offsetX, [item.value for item in items], width=width, color=colors[label],
                        edgecolor=self.edgecolor,
                        label=items[0].label,
                        hatch=hatchs[label])
            offsetX += width

        consumers = [item.ticker for item in links[firstLabel]]
        print(consumers)
        xticklabels, nextTarget = [], 0
        ticks_loc = self.ax.get_xticks().tolist()
        for v in ticks_loc:
            if math.isclose(v, nextTarget, rel_tol=1e-5) and nextTarget < len(consumers):
                xticklabels.append(consumers[nextTarget])
                nextTarget += 1
            else:
                xticklabels.append("")
        print(ticks_loc)
        self.ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
        self.ax.set_xticklabels(xticklabels)
        return self

    def innerParse(self, inputFile: str):
        self.throughput = Throughput.parse(inputFile)
        return self

    @staticmethod
    def parse(inputFile: str):
        return BandwidthUtilizationGraph(Throughput.parse(inputFile))
