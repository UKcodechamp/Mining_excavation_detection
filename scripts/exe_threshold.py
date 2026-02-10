import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV with reference index statistics
df = pd.read_csv("outputs/index_statistics_table.csv")

# Indices to consider
indices = ["NDVI","MNDWI","BSI","CBI","BAEI"]

# Dictionary to store selected thresholds
thresholds = {}

for idx in indices:
    plt.figure(figsize=(6,4))
    
    # Plot histogram
    sns.histplot(df[df['Index']==idx], x='Mean', hue='Class', bins=20, kde=True, palette=['blue','orange'], alpha=0.6)
    plt.title(f'{idx} - Pit (1) vs Non-pit (0)')
    plt.xlabel('Index value')
    plt.ylabel('Frequency')
    plt.show()
    
    # Extract pit (class 1) and non-pit (class 0) values
    pit_vals = df[(df['Index']==idx) & (df['Class']==1)]['Mean']
    nonpit_vals = df[(df['Index']==idx) & (df['Class']==0)]['Mean']
    
    # Percentile-based thresholds:
    # Lower-bound: 10th percentile of pits
    # Upper-bound: 90th percentile of non-pits
    pit_low = pit_vals.quantile(0.10)
    nonpit_high = nonpit_vals.quantile(0.90)
    
    # Select threshold conservatively: avoid false positives
    if pit_low > nonpit_high:
        threshold = (pit_low + nonpit_high)/2  # mid-point if they don’t overlap
    else:
        threshold = pit_low  # otherwise, use 10th percentile of pit
    
    thresholds[idx] = threshold
    print(f"{idx}: pit 10th percentile = {pit_low:.3f}, non-pit 90th percentile = {nonpit_high:.3f}, selected threshold = {threshold:.3f}")

# Final thresholds dictionary
print("\nSuggested thresholds for detection:")
for k,v in thresholds.items():
    print(f"{k}: {v:.3f}")
