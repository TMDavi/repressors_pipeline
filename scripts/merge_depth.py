import pandas as pd
import argparse
import yaml
import os
# Load the config.yaml file
#with open("config.yaml", 'r') as f:
#    config = yaml.safe_load(f)

# Access the value
#workdir = config["workdir"]


#def get_70_depth(file_path):
#    """
#    Parses the depth file and returns a DataFrame with the relevant data.
#    """
#    df = pd.read_csv(file_path, sep='\t',header=None, skiprows=1, names=['contig','depth'])
#    df = df[df['depth'] > 0.7]  # Filter for depth greater than 70
#    return df

def parse_depth(files):
    df = pd.DataFrame()
    temp_df= pd.DataFrame()
    for file in files:
        #temp_df = get_70_depth(f"{workdir}/results/{sample}/mapped_reads/{sample}_depth.txt")
        temp_df = pd.read_csv(file, sep='\t', names=['contig_id','depth'])
        sample_name = os.path.basename(file).replace('_depth.tsv', '')

        temp_df = pd.DataFrame({
            'contig_id':temp_df['contig_id'],
            sample_name: temp_df['depth']
        })
        if df.empty:
            df = temp_df 
        else:
            df = pd.merge(df, temp_df, on='contig_id', how='outer')
    
    df = df.fillna(0)  # Fill NaN values with 0
    return df

def main():
    parser = argparse.ArgumentParser(description="Merge depth results into a single DataFrame")
    parser.add_argument('--files', type=str, nargs='+', required=True, help='List of depth files')
    parser.add_argument('--output', type=str, required=True, help='Output file path')
    args = parser.parse_args()

    df = parse_depth(args.files)
    df.to_csv(args.output, sep='\t', index=False)

if __name__ == "__main__":
    main()
