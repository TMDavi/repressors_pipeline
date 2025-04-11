import pandas as pd
import argparse
import os 

def mergeDataFrame(filelist):

    df = pd.DataFrame({
        'contig_id':[],
        'Mapped':[]
    })
    temp_df= pd.DataFrame()
    for file in filelist:
        temp_df = pd.read_csv(file, sep='\t',names=['contig_id','length','Mapped','Unmapped'])
        sample_name = os.path.basename(file).replace('_vs_DNA_repressor_sorted.idxstats', '')

        temp_df = pd.DataFrame({
            'contig_id':temp_df['contig_id'],
            sample_name: temp_df['Mapped']
        })
        if df.empty:
            df = temp_df 
        else:
            df = pd.merge(df, temp_df, on='contig_id', how='outer')
    return df
    


def main():
    parser = argparse.ArgumentParser(description="Merge idxstats files into a single DataFrame")
    parser.add_argument('--files', type=str, nargs='+', required=True, help='List of idxstats files')
    parser.add_argument('--output', type=str, required=True, help='Output file path')
    args = parser.parse_args()

    df = mergeDataFrame(args.files)
    df.to_csv(args.output, sep='\t', index=False)

if __name__ == "__main__":
    main()