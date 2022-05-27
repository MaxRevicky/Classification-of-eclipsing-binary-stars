import os
from pathlib import Path
import pandas as pd
import numpy as np


if __name__ == '__main__':
    # create outfolder
    outfolder = 'results'
    Path(outfolder).mkdir(parents=True, exist_ok=True)
    source_folder = 'curves_rot_ell'

    files = []
    # for (dirpath, dirnames, filenames) in walk("scans_november_exploit"):
    for (dirpath, dirnames, filenames) in os.walk(source_folder):
        files.append((dirpath, filenames))

    print(files)

    all_rows = []
    for path, filenames in files:
        for filename in filenames:
            data = pd.read_csv(path + '\\' + filename, sep=" ", header=None)
            data.columns = ["a", "curve", "c"]
            one_row = (path, filename, data['curve'].tolist())
            all_rows.append(one_row)
            # print(one_row)

    # Create the dataframe
    df = pd.DataFrame(all_rows)
    df.columns = ["path", "filename", "curve"]

    print(df['path'].str)

    df['Type'] = np.where(df['path'].str.contains('\\\\ell'), '1', np.where(df['path'].str.contains('\\\\rot'), '0', '?'))


    df.to_csv('out.csv')

    print(df)
    
