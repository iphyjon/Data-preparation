# Import Libraries
import pandas as pd
import numpy as np
import glob

# Set data type 
d_type = {0: np.float64, 1: np.float64, 2: np.float64, 3: np.int32, 4: np.int32, 5: np.int32, 6: np.float64}

#########################################################
# Dict for classification                               #
#########################################################
class_id = dict()
class_id["Building"]             = 6
class_id["Bikes"]                = 69
class_id["CarsandTrucks"]        = 64
class_id["HighVegetation"]       = 5
class_id["Lamps"]                = 81
class_id["LowVegetation"]        = 3
class_id["ManMadeterrain"]       = 90
class_id["NaturalTerrain"]       = 2
class_id["Person"]               = 100
class_id["RemainingHardSpace"]   = 82
class_id["Road"]                 = 11
class_id["StreetSigns"]          = 80
class_id["Tram"]                 = 68
class_id["TrashCan"]             = 70
class_id["TramLine"]             = 111
class_id["Unclassified"]         = 1
class_id["UtilityTramLine"]      = 112
class_id["Bench"]                = 87
class_id["Fence"]                = 88
class_id["Other"]                = 120
###############################################################




def check_dtype(fname):
    """
    This function checks for .txt files that has str and float data types in the dataframe
    
    Args
    fname: folder name - str to the folder path that needs to be check
    
    Returns: 
    returns a list containing the paths to the .txt files with str and float data types 
    
    """
    fn = "D:/Ifeanyi/no_nan_values/" + fname + "/" # File path to the location of 3D point cloud data 
    
    names = ['CarsandTrucks', 'Building', 'TrashCan', 'Tram', 'LowVegetation', 'Bikes', 'HighVegetation', 'Person', 
         'StreetSigns', 'Road', 'Lamps', 'TramLine', 'ManMadeterrain', 'NaturalTerrain', 'Unclassified', 
         'UtilityTramLine', 'RemainingHardSpace', 'Bench', 'Fence', 'Other']
    
    file_ = []
    
    for name in names:
        for path in glob.glob(fn + name + "/*.txt"):
            df = pd.read_csv(path, delimiter=' ', header = None,usecols = [0,1,2,3,4,5,6], dtype = d_type)
            if type(df.loc[0][1]) == str:
                file_.append(path)
                
    return file_

check_dtype("8196")                
#############################################################################


def fixnan(df):
    """
    This function arranges the dataframe to the right format if it shifted to the right.
    
    Args
    df: Panda dataframe
    
    Returns: 
    returns a pandas dataframe with the right format. 
    
    """
    df1 = df[df[6].notnull()].dropna(axis = 1)
    df2 = df[df[9].notnull()].dropna(axis = 1).reindex(columns = [0,1,2,3,4,5,9,8,10]).rename(columns = {9:6, 8:7, 10:8})
    main_df = pd.concat([df1, df2], ignore_index = True)
    main_df = main_df.drop([7,8], axis = 1)
    return main_df

#################################################################################

def merge(fname):
    """
    This function loops through all the .txt files available in the file path provided 
    and merges them together in a pandas dataframe.
    
    Args
    fname: folder name - str to the folder path that needs to be read into python
    
    Returns: 
    returns a pandas dataframe. 
    
    """
    fn = "D:/Ifeanyi/no_nan_values/" + fname + "/"
    cols = {0: "X", 1: "Y",2: "Z",3:"R",4:"G",5:"B",6:"I"}

    merge_df = {}
    
    for keys, values in class_id.items():
        df = {}
        for path in glob.glob(fn + keys + "/*.txt"):
            
            if pd.read_csv(path, delimiter=' ', header = None, usecols = [0,1,2,3,4,5,6])[6].isnull().sum() != 0:
                df[path] = fixnan(pd.read_csv(path, delimiter=' ', header = None))
            else:
                df[path] = pd.read_csv(path, delimiter=' ', header = None, usecols = [0,1,2,3,4,5,6])

            data = pd.concat(df.values(), ignore_index = True)
            data = data.rename(columns = cols).reindex(columns = ["X", "Y", "Z", "I", "R", "G", "B"])
            data = data.drop_duplicates()
            data = data.assign(L = values)


            merge_df[keys] = data
        merge_data = pd.concat(merge_df.values(), ignore_index = True)
    
    return merge_data
###################################################################################################
# Run the function and save the output file as .txt or .csv in the right folder
outdir = "D:/Ifeanyi/for_preprocessing/8196_merge.csv"
out_txt = "D:/Ifeanyi/for_preprocessing/8196_merge.txt"

df = merge("8196")
df.to_csv(outdir, header = False, index = False)
df.to_csv(out_txt, header = False, index = False, sep = " ")

#####################################################################################################