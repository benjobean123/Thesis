import pandas as pd
import pickle
from numpy import nan
from IPython.display import display
from sklearn.preprocessing import LabelEncoder
import re

xls1 = pd.ExcelFile("dataset/discourse_analysis_one.xlsx")
xls2 = pd.ExcelFile("dataset/discourse_analysis_two.xlsx")
xls3 = pd.ExcelFile("dataset/High_Functioning_Scrum_Communication_Final_v5.xlsx")
xls4 = pd.ExcelFile("dataset/Medium_Functioning_Scrum_Communication_Final_v5.xlsx")


## Read in a sheet with no expected header for each sheet in the excel for intial simulations
# Read in the simulation 1 excel sheet
sims_1 = [pd.read_excel(xls1, sheet, header=None) for sheet in xls1.sheet_names]
sims_1.pop(0) # remove the metadata sheet

# Read in the simulation 2 excel sheet
sims_2 = [pd.read_excel(xls2, sheet) for sheet in xls2.sheet_names]
sims_2.pop(0) # remove the metadata sheet

## Combine the different simulation list and their names
sims = sims_1 + sims_2
sim_names = xls1.sheet_names[1:] + xls2.sheet_names[1:]

## Read in a sheet for each sheet in the excel for scrum simulations
# Read in the Scrum high functioning excel sheet
sims_3 = [pd.read_excel(xls3, sheet) for sheet in xls3.sheet_names]
metrics_3 = sims_3.pop(5) ## Remove the Metrics sheet from the dataframe
sim_names3 = xls3.sheet_names[1:]

# Read in the Scrum high functioning excel sheet
sims_4 = [pd.read_excel(xls4, sheet) for sheet in xls4.sheet_names]
metrics_4 = sims_4.pop(5) ## Remove the Metrics sheet from the dataframe
sim_names4 = xls4.sheet_names[1:]



## Remove duplicate
def rn(df, suffix = '-duplicate-'):
    appendents = (suffix + df.groupby(level=0).cumcount().astype(str)).replace(suffix, '')
    return df.set_index(df.index + appendents)

## Function to clean each excel sheet dataframe
def clean_sim_data(sim_df):
  # Label coulmns
  sim_df = sim_df.rename(columns={0:"Turn Taking", 1:"Time", 2:"Total", 3:"Simulation", 4:"SA Team"})

  # Drops any rows with empty values in the turn taking coulumn
  sim_df = sim_df[sim_df["Turn Taking"].notna()]

  # Drops any coulumns past 5
  sim_df = sim_df.drop(columns=sim_df.columns.values[5:])

  # Format all the values in the SA team coulumn to "[" + str(x) + "]"
  sim_df['SA Team'] = sim_df['SA Team'].apply(lambda x: eval("[" + str(x) + "]"))

  try:
    # If there are multiple SA, split them into two columns
    sa = sim_df.iloc[:,4].apply(lambda x : pd.Series(x).dropna()).merge(sim_df, left_index = True, right_index = True)

    # Drop all the rows that only have one SA rating or are NAN
    sa_two = sa[sa[1].notna()].drop(columns=[0]).rename(columns={1:"SA"})
    sim_df = sa.drop(columns=[1]).rename(columns={0:"SA"})
    
    # Merge the copies back into one DataFrame
    sim_df = pd.concat([sim_df, sa_two])
  except:
    # If there's no item with multiple SA values in the trial, it'll throw an error, so move on
    sim_df['SA'] = sim_df['SA Team'].apply(lambda x: eval(str(x))[0])
  
  sim_df = sim_df.drop(columns=["SA Team"])

  if not sim_df.index.is_unique:
    #print(sim_df.index.duplicated())
    #input()
    sim_df = sim_df.set_index(pd.Series(range(0, len(sim_df))))

  return sim_df



## Function to clean each Agile excel sheet dataframe
def clean_sim_scrum_data(sim_df):
  
  # Remove the unneeded Date and Role columns
  sim_df = sim_df.drop(columns=["Date", "Role"])


  # Encode the names to numbers
  team_names = {
    'Eli': 1, 
    'Jin': 2, 
    'Lena': 3, 
    'Maya': 4, 
    'Noah': 5, 
    'Raj': 6, 
    'Sofia': 7, 
    'Zara': 8
  }
  sim_df['Name'] = sim_df['Name'].map(team_names)


  # Remove the names from the chat logs
  sim_df['Message'] = sim_df['Message'].str.replace(r'^[^:]*:', '', regex=True)

  # Reorder the columns
  column_order = ['Name', 'Timestamp', 'Message', 'Sprint']
  sim_df = sim_df[column_order]

  pd.set_option('display.max_columns', None)
  #print(sim_df)
  

  return sim_df

clean_scrum_sims = {}
clean_sims = {}

# clean the Firefighting sims
for i in range(len(sims)):
  try:
    ## clean the dataset
    clean_sims[sim_names[i]] = clean_sim_data(sims[i])
  except Exception as e:
    print("Hello World")
    #print(i, sim_names[i], e)
    #print(sims[i])

# clean the agile sims high functioning
for i in range(len(sims_3)):
  try:
    clean_scrum_sims[sim_names3[i]] = clean_sim_scrum_data(sims_3[i])
  except Exception as e:
    print("\n")
    print(i, sim_names3[i], e)
    print(sims_3[i])

# clean the agile sims high functioning
for i in range(len(sims_4)):
  try:
    clean_scrum_sims[sim_names4[i]] = clean_sim_scrum_data(sims_4[i])
  except Exception as e:
    print("\n")
    print(i, sim_names4[i], e)
    print(sims_4[i])


#print(clean_scrum_sims[sim_names3[1]])

## open the .pickle file and dump the clean data into it
with open("clean_data.pickle", 'wb') as handle:
    pickle.dump(clean_sims, handle, protocol=pickle.HIGHEST_PROTOCOL)