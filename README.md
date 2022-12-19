
# Web Application Dashboard on Law Enforcement Line of Duty Deaths USA

![Python](https://img.shields.io/badge/%20%20%20Programming%20Language-Python-blue)
![Libraries](https://img.shields.io/badge/%20%20%20Libraries%20Used%20For%20Web%20App-numpy--pandas--plotly--matplotlib--seaborn--scipy--streamlit%3D%3D1.15.2-brightgreen) 


This interactive web application dashboard provides user with the analysis on the Law Enforcement Line of Duty Deaths in USA from 1791 to 2022.

### It have two main sections ->
1. Human Unit -> This section provides all the analysis w.r.t Human police unit.
2. K9 Unit -> This section provides all the analysis w.r.t K9 police unit.


### Currently It has 5 features ->
1. Overall Analysis -> This feature gives an overall analysis by presenting top statistics and different types of visualizations.
2. Top Ten Deadly... -> This feature shows bar chart according to their deaths count. For example top ten deadly states, years, etc.
3. Death Tally -> This feature shows death tally according to the user selections like death tally on this year, month, state, etc.
4. State-Wise Analysis -> This feature shows different types of visualizations according to the selected state by the user.
5. Cartogram -> This feature shows a map of the USA and death count of each state on that map. User can select the year range.


## Run Locally ->

### Prerequisite:
1. Python 3.10 or greater.
2. Github account.
3. IDE [VS Code, Spyder, etc.].
4. Git CLI.

#### Clone the project

```bash
  git clone https://github.com/MayureshKoli45/web-application-dashboard-on-law-enforcement-line-of-duty-deaths-usa.git
```

#### Go to the project directory

```bash
  python3 -m venv /cloned-repo-path
```

#### Open your IDE and then activate venv.

#### Install dependencies

```bash
  pip install -r requirements.txt
```

#### Start the app locally

```bash
  streamlit run app.py
```


## Directories Description
1. image folder -> This directory contains and image of the USA flag which I have used in Web App.

2. main data files -> This directory contains 2 main csv files which are the source of this project.

3. preprocessed data -> Some features implementation required some data to be preprocessed so that it will reduce the load time of the web app. This directory contains some preprocessed csv files.

## Important Files Description
1. app.py -> This is main app file. To implement this webapp dashboard run this file.

2. human_unit.py -> This file contains the data manipulation and data visualization w.r.t police deaths of Human Unit. This file contains main functionalities of the webapp dashboard.

3. k9_unit.py -> This file contains the data manipulation and data visualization w.r.t police deaths of K9 Unit. This file contains main functionalities of the webapp dashboard.

4. helper.py -> This file contains all the helper functions.

## Feel free to connect with me  
1. Email :- kolimayuresh450@gmail.com
2. Linkedin :- https://www.linkedin.com/in/mayuresh45/
3. Kaggle :- https://www.kaggle.com/mayureshkoli


