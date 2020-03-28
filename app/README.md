# Team NYC Carbon Emissions App

Team NYC's project is a dashboard that provides informative analytics on maritime traffic and CO2 emissions.

## Getting Started

### Running the app locally

First create a virtual environment with conda or venv inside a temp folder, then activate it.

```
virtualenv venv

# Windows
venv\Scripts\activate
# Or Linux
source venv/bin/activate

```

Clone the git repo, then install the requirements with pip

```

git clone https://github.gatech.edu/nzaker3/teamnyc-project
cd app
pip install -r requirements.txt

```

Run the app

```

python app.py

```


## Built With

- [Dash](https://dash.plot.ly/) - Main server and interactive components
- [Plotly Python](https://plot.ly/python/) - Used to create the interactive plots

