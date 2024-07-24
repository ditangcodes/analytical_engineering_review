import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
def load_data(file_path):
    return pd.read_csv(file_path)

# Function to create summary statistics table
def create_summary_statistics(data):
    print(data.describe())

# Function to create a bar chart for missing data by column
def plot_missing_data(data):
    missing_data = data.isnull().sum()
    missing_percentage = (missing_data / len(data)) * 100

    plt.figure(figsize=(10, 6))
    missing_data.plot(kind='bar')
    plt.title('Missing Data by Column')
    plt.xlabel('Column Name')
    plt.ylabel('Number of Missing Values')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('missing_data_by_column.png')
    plt.show()

# Function to create a bar chart for average claim size by cover type
def plot_average_claim_size_by_cover(data):
    average_claim_size = data.groupby('cover')['incurred'].mean()

    plt.figure(figsize=(10, 6))
    average_claim_size.plot(kind='bar')
    plt.title('Average Claim Size by Cover Type')
    plt.xlabel('Cover Type')
    plt.ylabel('Average Claim Size')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('average_claim_size_by_cover.png')
    plt.show()

# Function to create a box plot for claim size distribution by vehicle use
def plot_claim_size_distribution_by_vehicle_use(data):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='vehicle_use', y='incurred', data=data)
    plt.title('Claim Size Distribution by Vehicle Use')
    plt.xlabel('Vehicle Use')
    plt.ylabel('Claim Size')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('claim_size_distribution_by_vehicle_use.png')
    plt.show()

# Function to create a scatter plot for claim size vs. vehicle value
def plot_claim_size_vs_vehicle_value(data):
    plt.figure(figsize=(10, 6))
    plt.scatter(data['rounded_vehicle_value'], data['incurred'])
    plt.title('Claim Size vs. Vehicle Value')
    plt.xlabel('Vehicle Value')
    plt.ylabel('Claim Size')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('claim_size_vs_vehicle_value.png')
    plt.show()

# Function to create a correlation heatmap
def plot_correlation_heatmap(data):
    correlation_matrix = data[['vehicle_value', 'vehicle_annual_mileage', 'vehicle_age', 'years_held_licence', 'incurred']].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png')
    plt.show()

# Function to create a pie chart for policy distribution by entitlement
def plot_policy_distribution_by_entitlement(data):
    entitlement_distribution = data['entitlement'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(entitlement_distribution, labels=entitlement_distribution.index, autopct='%1.1f%%', startangle=140)
    plt.title('Policy Distribution by Entitlement')
    plt.tight_layout()
    plt.savefig('policy_distribution_by_entitlement.png')
    plt.show()

# Main function to execute all visualizations
def main():
    file_path = '../src/transformed_policies.csv'
    data = load_data(file_path)

    create_summary_statistics(data)
    plot_missing_data(data)
    plot_average_claim_size_by_cover(data)
    plot_claim_size_distribution_by_vehicle_use(data)
    plot_claim_size_vs_vehicle_value(data)
    plot_correlation_heatmap(data)
    plot_policy_distribution_by_entitlement(data)

if __name__ == "__main__":
    main()
