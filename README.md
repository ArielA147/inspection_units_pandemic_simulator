# Inspection Units Pandemic Simulator
A spatio-temporal simulator for pandemic spread with the inspection units pandemic intervention model.
Details about the relevant theory and methods can be found in our [paper](https://onlinelibrary.wiley.com/doi/abs/10.1002/adts.202200631).

## Abstract 
Pandemics are a source of extensive mortality, economic impairment, and dramatic social fluctuation.
Once a pandemic occurs, policymakers are faced with the highly challenging task of controlling it over time and space. 
In this article, we propose a novel Pandemic Intervention Policy (PIP) that relies on the strategic deployment of Inspection Units (IUs). 
These IUs are allocated in the environment, represented as a graph, and sample individuals who pass through the same node. 
If a sampled individual is identified as infected, she is extracted from the environment until she recovers (or dies). 
We provide a realistic simulation-based evaluation of the Influenza A pathogen using both synthetic and real-world data. 
Our results demonstrate potential significant benefits of the proposed PIP in mitigating a pandemic spread which can complement other standard policies such as social distancing and mask-wearing.

## Implementation Details
In order to simulate the proposed model, we used the agent-based simulation (Macal, 2010; Ciatto et al., 2020) where each 
agent in the population is defined using a timed finite state machine (Alagar and Periyasamy, 2011) such that it stores
the agent’s current epidemiological state, location on the graph (as the node’s identification
value), if the individual wears a mask or not, and the time passed from the last epidemiological
status changed. In addition, the spatial component of the model is represented using a graph
G = (V, E) where each node has a unique identification value and edges has an source
and target nodes alongside a weight (0 < w \in R).
From the implementation point of view, the simulation is developed using the Python program-
ming language (version 3.7.5) with the object oriented programming approach. Specifically,
the simulation is governed by a class called Simulation that contains the Population (a class that
wrappers a list of Agent objects), a Graph that represents the spatial component of the model,
a value that indicates the maximum number of steps in time the simulation, a walk policy, and
a PIP. The walk policy is a function that gets a Population and Graph objects and returns the
new positions of the agents by updating their ”location” property. The PIP is a function that
gets a Population and Graph objects and returns the new epidemiological states of the agents.
At the beginning of the simulation (t = 0), the population of agents assigns a location to each
agent on the graph in random or based or pre-defined logic. Afterward, at each time 1 <= t <= T
where T >> 1 is the maximum number of steps allowed to be performed by the simulator, four
actions taking place: 1) an SEIRD logic as described by (Lazebnik et al. 2021), 2) the population moves on the graph
by applying the walk policy function, 3) applying the social distance or inspection units pandemic
intervention policies using the PIP function, and 4) storing the model’s state in the form of the
epidemiological states’ distribution.

## Code structure
Following the Object Oriented Programming (OOP) approach, we use a pure-OOP style in this project.
Thus, we would describe below the responsibility of each class and file in the project:
1. **agent.py** - a single agent in the population, implemented as a timed finite state machine. 
2. **edge.py** - an edge of a graph, has source, target, and weight (weight not used in this version).
3. **epidemiological_state.py** - Enum for the SEIRD epidemiological states.
4. **find_best_ui_config.py** - a static class that implement two ways to find the best IU allocation given a population and a graph.
5. **graph.py** - a simple graph class implemented by a list of nodes and edges.
6. **multi_sim.py** - a simple wrapper class with single function to run the same simulation multiple times and extract a wanted information.
7. **node.py** - a node of a graph, has only an ID property.
8. **plotter.py** - a static class that contains all the plotting logic of the project.
9. **population.py** - a wrapper class to the agent class holding a list of agents.
10. **seird_parms.py** - a global parameters for the simulation.
11. **sim.py** - the central class of the project, holding all the logic for the simulation itself.
12. **sim_generator.py** - a class that responsible to generate *Simulator* objects with a given properties.   
13. **main.py** - a class to run several experiments on the simulation, designed to give new users a better idea of the scope and possibilities of the proposed simulator.
14. **paper.py** - a class that runs all the experiments needed to generate the results shown in the paper. 

In addition, several walks and IU PIP strategies are implemented and can be found in the walks/ and pips/ folders, respectively. 

## Citation

If you use parts of the code in this repository for your own research purposes, please cite:

@article{alexi2022,
	title={A Security Games Inspired Approach for Distributed Controlling Of Pandemic Spread},
	author={Alexi, A. and Rosenfeld, A. and Lazebnik, T.},
	journal={TBD},
	year={2022}
}

## Contact
* Ariel Alexi - [email](mailto:ariel.147@gmail.com) | [LinkedInֿ](https://www.linkedin.com/in/ariel-alexi/)
* Ariel Rosenfeld - [email](mailto:ariel.rosenfeld@biu.ac.il) | [LinkedInֿ](https://www.linkedin.com/in/ariel-rosenfeld-575051114/)
* Teddy Lazebnik - [email](mailto:t.lazebnik@ucl.ac.uk) | [LinkedInֿ](https://www.linkedin.com/in/teddy-lazebnik/)

## Usage 
1. Clone the repo
2. Install the '**requirements.txt**' file (pip install requirements.txt)
3. Put the relevant data in the "data" folder.
4. Run the '**main.py**' file ('python main.py' or 'python3 main.py')
5. Checkout the results in the "results" folder.

### Paper's results
In order to re-produce the paper's results, just run the '**paper.py**' file ('python paper.py' or 'python3 paper.py').
Please make sure that both the virtual environment of Python and the dependencies are installed beforehand.

## Dependencies

This project uses Python 3.7.
To create a virtual environment and install the project dependencies, you can run the following commands:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Prerequisites
- Python         3.7
- numpy          1.18.1
- matplotlib     3.2.2
- pandas         1.1.5

These can be found in the **requirements.txt** and easily installed using the "pip install requirements.txt" command in your terminal. 

## Contributing
We would love you to contribute to this project, pull requests are very welcome! Please send us an email with your suggestions or requests...

## Bug Reports
Report [here]("https://github.com/teddy4445/ga_physics/issues"). Guaranteed reply as fast as we can :)

