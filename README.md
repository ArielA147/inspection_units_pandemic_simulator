# Inspection Units Pandemic Simulator
A spatio-temporal simulator for pandemic spread with the inspection units pandemic intervention model.
Details about the relevant theory and methods can be found in our [paper](add-here-later).

## Abstract 
Pandemics are a source of extensive mortality, economic impairment, and dramatic social fluctuation.
Once a pandemic occurs, policymakers are faced with the highly challenging task of controlling it over time and space. 
In this article, we propose a novel Pandemic Intervention Policy (PIP) that relies on the strategic deployment of Inspection Units (IUs). 
These IUs are allocated in the environment, represented as a graph, and sample individuals who pass through the same node. 
If a sampled individual is identified as infected, she is extracted from the environment until she recovers (or dies). 
We provide a realistic simulation-based evaluation of the Influenza A pathogen using both synthetic and real-world data. 
Our results demonstrate potential significant benefits of the proposed PIP in mitigating a pandemic spread which can complement other standard policies such as social distancing and mask-wearing.

## Prerequisites
- Python         3.7
- numpy          1.18.1
- matplotlib     3.2.2
- pandas         1.1.5

These can be found in the **requirements.txt** and easly installed using the "pip install requirements.txt" command in your terminal. 


## Citation

If you use parts of the code in this repository for your own research purposes, please cite:

@article{alexi2022,
	title={A Security Games Inspired Approach for Distributed Controlling Of Pandemic Spread},
	author={Alexi, A. and Rosenfeld, A. and Lazebnik, T.},
	journal={TBD},
	year={2022}
}

## Dependencies

This project uses Python 3.7.
To create a virtual environment and install the project dependencies, you can run the following commands:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage 

1. Clone the repo
2. Install the '**requirements.txt**' file (pip install requirements.txt)
3. Put the relevant data in the "data" folder.
4. Run the '**main.py**' file (python main.py or python3 main.py)
5. Checkout the results in the "results" folder.
