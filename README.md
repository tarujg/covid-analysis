# Life in a pandemic - what has changed in San Diego

## How to run

Create a folder in the project root called `data/` and download these files and place them in respective folders

| Aspect        | Source                                          | Place In     | Link                                                  |
|---------------|-------------------------------------------------|-----------------|-------------------------------------------------------|
| Air Quality   | San Diego Air Quality Control District Database | In-memory       | http://jtimmer.digitalspacemail17.net/data/           |
| Economy       | City of San Diego Open Data                     | data/econ/      | https://data.sandiego.gov/datasets/business-listings/ |
| Energy Usage  | San Diego Gas & Electric Company                | data/sdge/      | https://energydata.sdge.com/                          |
| Road Accidents | Moosavi et al. (Ohio State University)          | data/accidents/ | https://smoosavi.org/datasets/us_accidents            |
| Mobility      | Google Community Mobility Report                | data/mobility/  | https://www.google.com/covid19/mobility/              |


To run the analysis notebook
```bash
$ git clone https://github.com/tarujg/covid-analysis.git
$ cd covid-analysis/
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ python
>>> import src
```

## Motivation
It’s clear that the outbreak of COVID-19 changed people’s lives everywhere especially in social and economic aspects. People prefer to stay at home rather than go out. Online shoppings becomes more popular but real stores encounter slumps. We would like to find the changes before and after COVID-19 in different aspects and the correlations between them.

## Directory Structure
```raw
├── README.md
└── data
    └── econ
        └── sd_businesses_active_since08_datasd_v1.csv
    └── mobility
        └── Region_Mobility_Report_CSVs
    
└── notebooks
    └── plots.ipynb
└── src
    └── accidents # modules for traffic-data analysis
        ├── accidents_data.py
        └── accidents_graph.py
    └── air_quality  # modules for air quality analysis
        ├── air_quality_analysis.py
        └── air_quality_graph.py
    └── econ         # modules for economy analysis
        ├── data.py
        └── fbpf.py
    └── mobility     # modules for mobility analysis
        └── data.py
    └── sdge         # modules for energy usage analysis
        └── data.py

```
## External Libraries
```raw
fbprophet
matplotlib
numpy
pandas
```
