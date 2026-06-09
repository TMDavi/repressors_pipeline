import pandas as pd
import os
import argparse

def get_coverage(file):
    df = pd.read_csv(file, sep='\t', names=['gene','depth', 'nbases', 'length','fraction'])
    df = df[df['depth']>0]
    df = df[df['gene'] != 'genome']
    df = df.drop(columns=['depth', 'fraction'])
    df = df.groupby(['gene','length'])['nbases'].sum()
    df = df.to_frame()
    df.reset_index(inplace=True)
    df['coverage'] = df['nbases'] / df['length']
    df = df.drop(columns=['nbases', 'length'])
    return df

def parse_coverage(filelist):
    df = pd.DataFrame()
    temp_df = pd.DataFrame()
    for file in filelist:
        temp_df = get_coverage(file)
        sample_name = os.path.basename(file).replace('_coverage.tsv', '')
        temp_df = pd.DataFrame({
            'contig_id':temp_df['gene'],
            sample_name: temp_df['coverage']
        })
        if df.empty:
            df = temp_df
        else:
            df = pd.merge(df, temp_df, on='contig_id', how='outer')
    df = df.fillna(0)  # Fill NaN values with 0
    return df

def main():
    parser = argparse.ArgumentParser(description="Merge coverage files into a single DataFrame")
    parser.add_argument('--files', type=str, nargs='+', required=True, help='List of coverage files')
    parser.add_argument('--output', type=str, required=True, help='Output file path')
    args = parser.parse_args()

    df = parse_coverage(args.files)
    df.to_csv(args.output, sep='\t', index=False)

if __name__ == "__main__":
    main()
