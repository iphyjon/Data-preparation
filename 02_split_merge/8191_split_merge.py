#########################################################
# The merge data was split into two in cloudcompare     #
# Here we load the two files and drop duplicates        #
# Then save to .txt files                               #
#########################################################

# Import Libraries
import pandas as pd
import numpy as np

# Dict classification

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
# Load data

path = "D:/Ifeanyi/for_preprocessing/Cloudcompare_split/"
name = "8191_merge_part1.txt"

# Column mapping 
col_map = {0: "X", 1: "Y",2: "Z", 3: "R", 4: "G", 5: "B", 6: "I", 7: "L"}
# Columnames
col_name = ["X", "Y", "Z", "I", "R", "G", "B", "L"]

# Read data into python
df = pd.read_csv(path + name, delimiter=' ', header = None)
# Rename columns and change the column order
df = df.rename(columns = col_map).reindex(columns = col_name)

# Round columns "X", "Y", "Z" to 3 decimals
df["X"] = round(df["X"], 3)
df["Y"] = round(df["Y"], 3)
df["Z"] = round(df["Z"], 3)

# Now drop duplicate rows
df_dup = df.drop_duplicates()

# Save output
outdir = "D:/Ifeanyi/for_preprocessing/Duplicatesdrop_round3/8191_part1.txt"
df_dup.to_csv(outdir, header = False, index = False, sep = " ")


# Repeat same process for the second part
# Part 2
path = "D:/Ifeanyi/for_preprocessing/Cloudcompare_split/"
name = "8191_merge_part2.txt"

col_map = {0: "X", 1: "Y",2: "Z", 3: "R", 4: "G", 5: "B", 6: "I", 7: "L"}
col_name = ["X", "Y", "Z", "I", "R", "G", "B", "L"]


df1 = pd.read_csv(path + name, delimiter=' ', header = None)
df1 = df1.rename(columns = col_map).reindex(columns = col_name)

df1["X"] = round(df1["X"], 3)
df1["Y"] = round(df1["Y"], 3)
df1["Z"] = round(df1["Z"], 3)

df1_dup = df1.drop_duplicates()

# file = ["8187", "8196", "8191_finished", "8193_finished"]
outdir = "D:/Ifeanyi/for_preprocessing/Duplicatesdrop_round3/8191_part2.txt"
df1_dup.to_csv(outdir, header = False, index = False, sep = " ")

# Get the total number of point for each class
# Part 1
points = {}
for key, val in class_id.items():
    num  = len(df1_dup[df1_dup.L == val])
    points[key] = num
    df_points = pd.DataFrame(points, index = [8191])
    print("{} == {} ".format(key, num))

# Part 2
points1 = {}
for key, val in class_id.items():
    num  = len(df_dup[df_dup.L == val])
    points1[key] = num
    df_points1 = pd.DataFrame(points1, index = [8191])
    print("{} == {} ".format(key, num))

# Add both dataframes together (Part1 and Part2)
df_total = df_points1.add(df_points, fill_value=0)
# Save this as .xlsx for future reference
df_total.to_excel("D:/Ifeanyi/Total_points/8196_new_totalpoints.xlsx")

# Get respons(labels) and features and save as .txt file
label = df_dup["L"].values
part1 = df_dup[["X", "Y", "Z", "I", "R", "G", "B"]]
# save response
out_lab = "D:/Ifeanyi/for_preprocessing/8191_part1_labels.txt"
np.savetxt(out_lab, label)
# save features
out_feat = "D:/Ifeanyi/for_preprocessing/8191_part1_features.txt"
part1.to_csv(out_feat, header = False, index = False, sep = " ")

# Part 2
label2 = df1_dup["L"].values
out_lab2 = "D:/Ifeanyi/for_preprocessing/8191_part2_labels.txt"
np.savetxt(out_lab2, label2)
##
part2 = df1_dup[["X", "Y", "Z", "I", "R", "G", "B"]]
out_feat2 = "D:/Ifeanyi/for_preprocessing/8191_part2_features.txt"
part2.to_csv(out_feat2, header = False, index = False, sep = " ")

##############################################################################################