import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Constants
DATA_URL = "https://data.nasa.gov/resource/y77d-th95.json"

# Function to fetch data from the API
def fetch_data(url):
    """
    Fetch JSON data from the provided URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        list: A list of dictionaries containing the dataset.
                Returns an empty list if the request fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to clean and preprocess the data
def clean_data(data):
    """
    Convert JSON data to a Pandas DataFrame and clean it.

    - Handles missing values.
    - Converts columns to appropriate data types.
    - Extracts the year from datetime values.

    Args:
        data (list): A list of dictionaries representing the dataset.

    Returns:
        pd.DataFrame: A cleaned DataFrame with valid `mass` and `year` columns.
                      Returns an empty DataFrame if critical columns are missing.
    """
    # Load data into a DataFrame
    df = pd.DataFrame(data)

    # Ensure critical columns exist in the dataset
    if 'mass' not in df.columns or 'year' not in df.columns:
        print("Critical columns ('mass', 'year') are missing from the dataset.")
        return pd.DataFrame()

    # Handle missing or malformed data
    df['mass'] = pd.to_numeric(df['mass'], errors='coerce')  # Convert mass to float, set invalid values to NaN
    df['year'] = pd.to_datetime(df['year'], errors='coerce')  # Convert year to datetime, set invalid values to NaT

    # Drop rows with missing critical values (mass or year)
    df = df.dropna(subset=['mass', 'year'])

    # Extract only the year part from the datetime column for analysis
    df['year'] = df['year'].dt.year

    return df

# Function to analyze the dataset
def analyze_data(df):
    """
    Analyze the dataset to extract key insights.

    - Counts total entries.
    - Finds the most massive meteorite.
    - Identifies the most frequent year of meteorite landings.

    Args:
        df (pd.DataFrame): The cleaned DataFrame.

    Returns:
        dict: A dictionary containing:
              - total_entries (int): Total number of entries in the dataset.
              - most_massive_name (str): Name of the most massive meteorite.
              - most_massive_mass (float): Mass of the most massive meteorite.
              - most_frequent_year (int): Year with the most meteorite landings.
              - most_frequent_count (int): Number of landings in that year.
    """
    results = {}

    # Total number of entries
    results['total_entries'] = len(df)

    # Most massive meteorite
    most_massive = df.loc[df['mass'].idxmax()]
    results['most_massive_name'] = most_massive['name']
    results['most_massive_mass'] = most_massive['mass']

    # Most frequent year
    most_frequent_year = df['year'].value_counts().idxmax()
    most_frequent_count = df['year'].value_counts().max()
    results['most_frequent_year'] = most_frequent_year
    results['most_frequent_count'] = most_frequent_count

    return results

# Function to visualize the dataset
def visualize_data(df):
    """
    Create visualizations for better understanding of the dataset.

    - Bar chart: Meteorite counts per year.
    - Histogram: Distribution of meteorite masses.
    - Scatter plot: Mass vs. Year.

    Args:
        df (pd.DataFrame): The cleaned DataFrame.

    Saves:
        meteorite_counts_per_year.png: Bar chart showing counts per year.
        meteorite_mass_distribution.png: Histogram showing mass distribution.
        scatter_mass_vs_year.png: Scatter plot of mass vs. year.
   """
    # Bar chart: Meteorite counts per year
    plt.figure(figsize=(12, 6))
    sns.countplot(x='year',
                    data=df,
                    palette='viridis',
                    hue='year',
                    legend=False,
                    order=sorted(df['year'].unique()))
    # Show every 5th year as a label
    years = sorted(df['year'].unique())
    tick_positions = range(0, len(years), 5)
    tick_labels = [years[i] for i in tick_positions]
    plt.xticks(ticks=tick_positions,
                labels=tick_labels,
                rotation=45,
                ha='right')
    plt.title('Meteorite Counts Per Year')
    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('meteorite_counts_per_year.png')

    # Histogram: Distribution of meteorite masses (log-scaled)
    plt.figure(figsize=(12, 6))
    filtered_df = df[df['mass'] <= 100000]
    sns.histplot(filtered_df['mass'], bins=100, kde=True, color='blue')
    mean_mass = filtered_df['mass'].mean()
    median_mass = filtered_df['mass'].median()
    plt.axvline(mean_mass, color='red', linestyle='--', label=f'Mean: {mean_mass:.2f}g')
    plt.axvline(median_mass, color='green', linestyle='--', label=f'Median: {median_mass:.2f}g')
    plt.legend()
    plt.xscale('log')
    plt.title('Log-Scaled Distribution of Meteorite Masses (Filtered)')
    plt.xlabel('Mass (log scale)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig('meteorite_mass_distribution.png')

    # Scatter plot: Mass vs. Year (log-scaled)
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='year', y='mass', data=df, alpha=0.7, color='red')
    plt.title('Meteorite Mass vs. Year')
    plt.xlabel('Year')
    plt.ylabel('Mass (grams)')
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig("meteorite_scatter_mass_vs_year.png")

# Main function to orchestrate the task
def earth_meteorite_landing_data_handling():
    """
    Main function to orchestrate fetching, cleaning, analyzing,
    and visualizing the Earth Meteorite Landings dataset.
    """
    print("Fetching data...")
    raw_data = fetch_data(DATA_URL)
    if not raw_data:
        print("No data was fetched. Exiting.")
        return

    print("Cleaning data...")
    df = clean_data(raw_data)
    if df.empty:
        print("The dataset is empty after cleaning. Exiting.")
        return

    print("Analyzing data...")
    results = analyze_data(df)

    print("\nResults:")
    print(f"Total Entries: {results['total_entries']}")
    print(f"Most Massive Meteorite: {results['most_massive_name']} ({results['most_massive_mass']} grams)")
    print(f"Most Frequent Year: {results['most_frequent_year']} ({results['most_frequent_count']} occurrences)")
    print("\nCreating visualizations...")
    visualize_data(df)

if __name__ == "__main__":
    earth_meteorite_landing_data_handling()
