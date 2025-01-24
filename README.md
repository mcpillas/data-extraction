# Earth Meteorite Landings Analysis

This project analyzes the Earth Meteorite Landings dataset provided by NASA. The analysis includes data fetching, cleaning, and visualization to gain insights into meteorite landings over time and their mass distribution.

## **Features**
- Fetches meteorite landing data from NASA's API.
- Cleans and preprocesses the dataset (handles missing values and converts data types).
- Analyzes key statistics:
  - Total number of meteorites.
  - Largest meteorite by mass.
  - Most frequent year for meteorite landings.
- Visualizes:
  - Meteorite counts per year (bar chart).
  - Mass distribution (histogram with optional log scale).
  - Relationship between meteorite mass and year (scatter plot with log scale).

## **Requirements**
The following Python libraries are required:
- `pandas`
- `numpy`
- `seaborn`
- `matplotlib`
- `requests`
- `notebook`

## **How to Use**
1. Clone this repository:

    `git clone <repository_url>`
    `cd <repository_folder>`

2. Install the required libraries:

    `sh setup_env.sh` or `./setup_env.ps1`

3. Run the Jupyter Notebook or Python script:
- **Jupyter Notebook**:
  Open the notebook in Jupyter and execute each cell step by step.
- **Python Script**:
  Run the script directly using:

  `python earth_metiorite_landings.py`

4. View the results:
- Key statistics will be printed in the terminal or notebook.
- Visualizations will be displayed inline (in Jupyter) or saved as `.png` files.

## **Visualizations**
The code generates the following visualizations:
1. **Meteorite Counts Per Year**: A bar chart showing the number of meteorites landed per year.
2. **Mass Distribution**: A histogram showing how meteorite masses are distributed, with a log scale for better visualization.
3. **Mass vs. Year**: A scatter plot showing the relationship between meteorite mass and year, with a log-scaled y-axis.

## **Customization**
You can customize the analysis by modifying filtering thresholds or visualization parameters directly in the code.

### Example Customizations:
- Change the range of years or masses to focus on a specific subset of data.
- Adjust bin sizes in histograms for finer granularity.

## **Dataset Source**
The dataset is fetched from NASA's API:
[Earth Meteorite Landings Dataset](https://data.nasa.gov/resource/y77d-th95.json)
