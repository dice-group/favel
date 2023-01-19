"""
Execute as 'python3 Analysis.py'
"""

from os import path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def loadPaths():
    paths = dict()
    favelPath = path.realpath(__file__)
    pathLst = favelPath.split('/')
    favelPath = "/".join(pathLst[:-2])
    
    paths["Overview"] = path.join(favelPath, "Evaluation/Overview.xlsx")
    paths["Analysis"] = path.join(favelPath, "Analysis/")
    return paths
    

def readOverview():
    return pd.read_excel(PATHS["Overview"])

def getBpdp(df):
    return df.loc[df['Dataset'] == "BPDP_Dataset"]

def getFactBench(df):
    return df.loc[df['Dataset'] == "factbench-clean"]

def getFavel(df):
    return df.loc[df['Dataset'] == "FinalDataset_Hard"]

def plotImprovement(df):
    """
    Boxplot of improvement over all experiments
    """
    plt.figure()
    df = df[["Improvement"]]
    plot = df.plot(kind="box", figsize=(3.5, 5.5))
    fig = plot.get_figure()
    fig.savefig(path.join(PATHS["Analysis"], "improvement.png"))

def plotPerformanceStdDev(df):
    """
    Scatter plot of standard deviation depending on performance
    """
    plt.figure()
    df = df[["Testing AUC-ROC Mean", "Testing AUC-ROC Std. Dev."]]
    plot = df.plot(x="Testing AUC-ROC Mean", y="Testing AUC-ROC Std. Dev.", kind="scatter")
    fig = plot.get_figure()
    fig.savefig(path.join(PATHS["Analysis"], "performance-stdDev.png"))
    
def plotMlAlgorithms(df):
    """
    Bar chart showing the best performance grouped by ML algorithm
    """
    plt.figure()
    df = df[["Testing AUC-ROC Mean", "ML Algorithm"]]
    gb = df.groupby(by="ML Algorithm")
    result = dict()
    for group in gb.groups.keys():
        result[group] = float(df.loc[gb.groups[group]][["Testing AUC-ROC Mean"]].max())
    series = pd.Series(result)
    plot = series.plot(kind='bar', ylabel="Best AUC-ROC Score", rot=10)
    fig = plot.get_figure()
    fig.savefig(path.join(PATHS["Analysis"], "performance-mlAlgorithm.png"))

def plotDataset(df):
    """
    Bar chart showing the best ensemble performance
    compared to the best single performance grouped by dataset
    """
    plt.figure()

    labels = []
    ensemble = []
    single = []

    # Get best ensemble and best single score for each dataset
    df = df[["Testing AUC-ROC Mean", "Dataset", "Best Single Score"]]
    gb = df.groupby(by="Dataset")
    for group in gb.groups.keys():
        e = float(df.loc[gb.groups[group]][["Testing AUC-ROC Mean"]].max())
        s = float(df.loc[gb.groups[group]][["Best Single Score"]].max())
        labels.append(group)
        ensemble.append(round(e, 4))
        single.append(round(s, 4))

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, ensemble, width, label='Men')
    rects2 = ax.bar(x + width/2, single, width, label='Women')
    ax.set_ylabel("AUC-ROC Score")
    ax.set_xticks(x, labels)
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    fig.savefig(path.join(PATHS["Analysis"], "performance-dataset.png"))

    
def analyzeBestN(df, N:int):
    """
    Scatter plot.
    For every combination of two datasets, take N best configurations for the first dataset,
    plot how they improve in the second dataset.
    """
    datasets = dict()
    datasets['bpdp'] = getBpdp(df)
    datasets['factBench'] = getFactBench(df)
    datasets['favel'] = getFavel(df)
    
    for key in datasets.keys():
        datasets[key].sort_values(by="Testing AUC-ROC Mean", ascending=False, inplace=True)
    
    primaryKey = ["ML Algorithm", "ML Parameters", "Normalizer", "Iterations", "Fact Validation Approaches"]
    
    result = {"Source Dataset": [], "Target Dataset": [], "Testing AUC-ROC Mean": [], "Improvement": []}
    for i in datasets.keys():
        for j in datasets.keys():
            if i != j:
                """
                Take N best configurations for dataset i.
                Look up these configurations for dataset j.
                """
                for index, row in datasets[i].head(n=N).iterrows():
                    tmp = _findRow(datasets[j], row, primaryKey)
                    if not tmp is None:
                        result["Source Dataset"].append(i)
                        result["Target Dataset"].append(j)
                        result["Testing AUC-ROC Mean"].append(tmp["Testing AUC-ROC Mean"])
                        result["Improvement"].append(tmp["Improvement"])
    
    plt.figure()
    result = pd.DataFrame(result)
    # Define colors
    colors = []
    for index, row in result.iterrows():
        if row["Source Dataset"] == "bpdp":
            colors.append('g')
        if row["Source Dataset"] == "factBench":
            colors.append('b')
        if row["Source Dataset"] == "favel":
            colors.append('r')
            
    # Plot results
    for key in result:
        plot = result.plot(kind="scatter", x="Target Dataset", y="Improvement", c=colors)
        fig = plot.get_figure()
        fig.savefig(path.join(PATHS["Analysis"], "nBest.png"))
        
def analyzeUniversalConfig(df):
    """
    Scatter plot.
    """
    datasets = dict()
    datasets['bpdp'] = getBpdp(df)
    datasets['factBench'] = getFactBench(df)
    datasets['favel'] = getFavel(df)
    
    # Sort the datasets by performance
    for key in datasets.keys():
        datasets[key].sort_values(by="Testing AUC-ROC Mean", ascending=False, inplace=True)
    
    primaryKey = ["ML Algorithm", "ML Parameters", "Normalizer", "Iterations", "Fact Validation Approaches"]
    
    result = {"Source Dataset": [], "Target Dataset": [], "Testing AUC-ROC Mean": [], "Improvement": []}
    for i in datasets.keys():
        for j in datasets.keys():
            if i != j:
                """
                Take N best configurations for dataset i.
                Look up these configurations for dataset j.
                """
                for index, row in datasets[i].iterrows():
                    if row["Improvement"] <= 0:
                        break
                    tmp = _findRow(datasets[j], row, primaryKey)
                    if not tmp is None and tmp["Improvement"] > 0:
                        result["Source Dataset"].append(i)
                        result["Target Dataset"].append(j)
                        result["Testing AUC-ROC Mean"].append(tmp["Testing AUC-ROC Mean"])
                        result["Improvement"].append(tmp["Improvement"])
    
    plt.figure()
    result = pd.DataFrame(result)
    # Define colors
    colors = []
    for index, row in result.iterrows():
        if row["Source Dataset"] == "bpdp":
            colors.append('g')
        if row["Source Dataset"] == "factBench":
            colors.append('b')
        if row["Source Dataset"] == "favel":
            colors.append('r')
            
    # Plot results
    for key in result:
        plot = result.plot(kind="scatter", x="Target Dataset", y="Improvement", c=colors)
        fig = plot.get_figure()
        fig.savefig(path.join(PATHS["Analysis"], "universalConfig.png"))

def _findRow(df, row, keys):
    result = dict()
    for key in keys:
        result[key] = set(df.index[df[key] == row[key]].tolist())

    intersect = None
    for key in keys:
        if intersect is None:
            intersect = result[key]
        else:
            intersect &= result[key]
    
    for i in intersect:
        return df.loc[i]
    
PATHS = loadPaths()

df = readOverview()
# plotImprovement(df)
# plotPerformanceStdDev(df)
# plotMlAlgorithms(df)
# plotDataset(df)
# analyzeBestN(df, 5)
analyzeUniversalConfig(df)
