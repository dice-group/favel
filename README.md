FAVEL
=
<i>Fact Validation Ensemble Learner</i>

The vision of this project is to explore the possibility to train a supervised machine learning algorithm based on the results of several fact validation approaches.

To achieve this vision this project offers:
* A software which can automatically
    1. Validate a dataset on multiple fact validation approaches
    2. Use the results of the fact validation approaches to train a supervised machine learning algorithm
    3. Validate the dataset on the trained machine learning model
* Two datasets that can be used for evaluation

# Structure of the Repository

- [**Analysis**](Analysis): Simple script to plot diagrams based on the data in [**Evaluation/Overview**](Evaluation/Overview.xlsx)
- [**Evaluation**](Evaluation): The software saves results to this directory. It also contains preliminaries results of our experiments.
- [**Datasets**](Datasets): Dataset with simple example.  You can find the documentation [**here**](Datasets/README.md).  
- [**Software**](Software): Software for exploring the vision

# Installation
<details><summary> </summary>

```
git clone https://github.com/dice-group/favel.git
conda create -n "favel" python=3.7
conda activate favel
cd favel
pip install -r requirements.txt
```
or 
```
git clone https://github.com/dice-group/favel.git
virtualenv -p python3.7 favel
source favel/bin/activate
cd favel
pip install -r requirements.txt
```
</details>

# Usage

<details><summary> </summary>

* To conduct an experiment with the software execute the following steps:
    1. Create a directory inside the Evaluation directory.\
        The name of the directory is the name of the experiment \
        Example: ```favel/Evaluation/experiment42```
    2. Create a configuration file ```favel.conf``` inside the experiment directory. \
        The configuration file defines the set of fact validation approaches and the machine learning algorithm. \
        A basic configuration file is can be found [**here**](Evaluation/example/favel.conf). \
        For more advanced configuration options look [**here**](Software/MLService/README.md). \
        Example: ```favel/Evaluation/experiment42/favel.conf```
    3. Execute the software. \
        For the software to be able to use fact validation approaches, these approaches might have to be started manually. \
        An exaustive description how to run the software can be found in the following section. \
        Results will be saved to the [**favel/Evaluation/**](Evaluation) directory. \
        Example: ```python3 favel/Software/Favel.py -d favel/FinalDataset_Hard -e experiment42```

</details>

## How to run

```
python3 Software/Favel.py [options]
```

### Options

<details><summary> </summary>

* ```-e EXPERIMENT, --experiment EXPERIMENT``` name of the experiment, corresponds with the name of the experiment folder in the ```Evaluation``` directory
* ```-b EXPERIMENT, --batch EXPERIMENT``` name of the experiment, corresponds with the name of the experiment folder in the ```Evaluation``` directory.
Experiment will be run in batch mode, meaning that an experiment will be executed with every subset of the specified set of fact validation approaches.
* ```-d DATA, --data DATA``` path to the dataset to validate
* ```-w, --write``` write everything to disk. If this flag is set, all possible outputs are written to disk. This includes models, normalizers, predicate encoders, and dataframes.
If the flag is not set, only the overview is written to disk.
* ```-c, --containers```Automatically Start/Stop containers that encapsulate the fact validation approaches.
* ```-a, --automl``` To use the autoML system instead of the manual algorithm selection.

</details>


## How to test

```
python3 -m unittest
```

## How to run using pre-computed fact-validation approaches veracity scores
<details><summary> </summary>
    
* First activate the environment using the command specified above. 
* FAVEL_ALL_RESULTS.zip file contains the precomputed veracity scores from individual approaches. 
* Unzip this file and run the following command to execute experiments.
* You can change the input config file in the Evaluations/eval001 folder.

```
unzip FAVEL_ALL_RESULTS.zip
python3 Software/Favel.py -e eval001 -d FAVEL_ALL_RESULTS/FaVEL/input/ -w -a
```

Each experiment can take up to 3 hours depending upon no. of iterations in the input config file.

</details>

# Additional Resources

## Datasets

More informations about included datasets [here](Datasets)
<!-- * [FactBench](https://github.com/dice-group/favel/FactBench-Dataset_2022)
* [BPDP](https://github.com/dice-group/favel/BPDP-Dataset_2022)
* [Favel](https://github.com/dice-group/favel/favel/tree/main/Favel_Dataset)
* [Favel-hard](https://github.com/dice-group/favel/favel/tree/main/FinalDataset_Hard) -->

## Fact Validation Approaches
* <https://github.com/saschaTrippel/knowledgestream> offers multiple algorithms
<!-- * <https://github.com/palaniappan1/COPAAL> offers COPAAL -->



## How to cite
If you find our work useful in your research, please consider citing the paper:
```
@inproceedings{10.1007/978-3-031-77792-9_13,
author = {Qudus, Umair and Pekarou, Franck Lionel Tatkeu and Silva, Ana Alexandra Morim da and R\"{o}der, Michael and Ngomo, Axel-Cyrille Ngonga},
title = {FaVEL: Fact Validation Ensemble Learning},
year = {2024},
isbn = {978-3-031-77791-2},
publisher = {Springer-Verlag},
address = {Berlin, Heidelberg},
url = {https://doi.org/10.1007/978-3-031-77792-9_13},
doi = {10.1007/978-3-031-77792-9_13},
abstract = {Validating assertions before adding them to a knowledge graph is an essential part of its creation and maintenance. Due to the sheer size of knowledge graphs, automatic fact-checking approaches have been developed. These approaches rely on reference knowledge to decide whether a given assertion is correct. Recent hybrid approaches achieve good results by including several knowledge sources. However, it is often impractical to provide a sheer quantity of textual knowledge or generate embedding models to leverage these hybrid approaches. We present FaVEL, an approach that uses algorithm selection and ensemble learning to amalgamate several existing fact-checking approaches that rely solely on a reference knowledge graph and, hence, use fewer resources than current hybrid approaches. For our evaluation, we create updated versions of two existing datasets and a new dataset dubbed FaVEL-DS. Our evaluation compares our approach to 15 fact-checking approaches—including the state-of-the-art approach HybridFC—on 3 datasets. Our results demonstrate that FaVEL outperforms all other approaches significantly by at least 0.04 in terms of the area under the ROC curve. Our source code, datasets, and evaluation results are open-source and can be found at .},
booktitle = {Knowledge Engineering and Knowledge Management: 24th International Conference, EKAW 2024, Amsterdam, The Netherlands, November 26–28, 2024, Proceedings},
pages = {209–225},
numpages = {17},
keywords = {fact checking, ensemble learning, transfer learning, knowledge management},
location = {Amsterdam, The Netherlands}
}
```

## Acknowledgements
his  work  is  part  of  a  project  that  has  received  funding  from  the  Euro-pean Union’s Horizon 2020 research and innovation programme (Marie Skodowska-Curie, No.860801), the German Federal Ministry of Education and Research (BMBF) within the projectNEBULA (13N16364), the Ministry of Culture and Science of North Rhine-Westphalia (MKWNRW) within the project SAIL (NW21-059D).
