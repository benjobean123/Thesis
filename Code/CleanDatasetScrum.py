import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import LabelEncoder
import re

xls3 = pd.ExcelFile("dataset/High_Functioning_Scrum_Communication_with_TSA.xlsx")
xls4 = pd.ExcelFile("dataset/Medium_Functioning_Scrum_Communication_with_TSA.xlsx")
pd.set_option('display.max_columns', None)


## Read in a sheet for each sheet in the excel for scrum simulations
# Read in the Scrum high functioning excel sheet
sims_3 = [pd.read_excel(xls3, sheet) for sheet in xls3.sheet_names]
metrics_3 = sims_3.pop(5) ## Remove the Metrics sheet from the dataframe
sim_names3 = xls3.sheet_names[1:]
#print(sims_3)




# Read in the Scrum high functioning excel sheet
sims_4 = [pd.read_excel(xls4, sheet) for sheet in xls4.sheet_names]
metrics_4 = sims_4.pop(5) ## Remove the Metrics sheet from the dataframe
sim_names4 = xls4.sheet_names[1:]



## Remove duplicate
def rn(df, suffix = '-duplicate-'):
    appendents = (suffix + df.groupby(level=0).cumcount().astype(str)).replace(suffix, '')
    return df.set_index(df.index + appendents)



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
  column_order = ['Name', 'Timestamp', 'Message', 'Sprint', 'TSA']
  sim_df = sim_df[column_order]


  
  return sim_df


def reorder_scrum_sims(sim_df):
  
  reordered_sims = {}
  reordered_sims[0]=pd.DataFrame(columns=sim_df[0].columns)
  reordered_sims[1]=pd.DataFrame(columns=sim_df[1].columns)
  reordered_sims[2]=pd.DataFrame(columns=sim_df[2].columns)
  reordered_sims[3]=pd.DataFrame(columns=sim_df[3].columns)

  for i in range(len(sim_df)):
    print(sim_df[i])
    ## Reorganize the sheets to separate Agile Ceremonies by sprint 
    # Create empty dataframes with the same columns
    sprint1 = pd.DataFrame(columns=sim_df[i].columns)
    sprint2 = pd.DataFrame(columns=sim_df[i].columns)
    sprint3 = pd.DataFrame(columns=sim_df[i].columns)
    sprint4 = pd.DataFrame(columns=sim_df[i].columns)
    
    # Check for what sprint the line belongs too
    # Loop through each row and add to the right dataframe
    for _, row in sim_df[i].iterrows():
        if row['Sprint'] == 1:
            sprint1 = pd.concat([sprint1, pd.DataFrame([row])], ignore_index=True)
        elif row['Sprint'] == 2:
            sprint2 = pd.concat([sprint2, pd.DataFrame([row])], ignore_index=True)
        elif row['Sprint'] == 3:
            sprint3 = pd.concat([sprint3, pd.DataFrame([row])], ignore_index=True)
        elif row['Sprint'] == 4:
            sprint4 = pd.concat([sprint4, pd.DataFrame([row])], ignore_index=True)
    
    #print(sprint1.shape)
    # Save the Sprints to another dataframe to create the simulations
    reordered_sims[0] = pd.concat([reordered_sims[0], sprint1], ignore_index=True)
    reordered_sims[1] = pd.concat([reordered_sims[1], sprint2], ignore_index=True)
    reordered_sims[2] = pd.concat([reordered_sims[2], sprint3], ignore_index=True)
    reordered_sims[3] = pd.concat([reordered_sims[3], sprint4], ignore_index=True)
        
  print(reordered_sims[0].shape)
  print(reordered_sims[1].shape)
  print(reordered_sims[2].shape)
  print(reordered_sims[3].shape)


  return reordered_sims

## Function to add all the simulations together
def add_sumulations(simulations_df):

  for i in range(len(sims_3_clean)):
    scrum_simulations[i + len(scrum_simulations)] = pd.DataFrame(columns=sims_3_clean[i].columns)
    scrum_simulations[i + len(scrum_simulations)] = pd.concat([scrum_simulations[i + len(scrum_simulations)], sims_3_clean[i]], ignore_index=True)
  
  return simulations_df


# clean the agile sims high functioning
sims_3_clean = sims_3
for i in range(len(sims_3)):
  try:
    sims_3_clean[i] = clean_sim_scrum_data(sims_3[i])
  except Exception as e:
    print("\n")
    #print(i, sim_names3[i], e)
    #print(sims_3[i])

# reorder the sim columns
sims_3_clean = reorder_scrum_sims(sims_3_clean)


# clean the agile sims medium functioning
sims_4_clean = sims_3
for i in range(len(sims_4)):
  try:
    sims_4_clean[sim_names4[i]] = clean_sim_scrum_data(sims_4[i])
  except Exception as e:
    print("\n")
    #print(i, sim_names4[i], e)
    #print(sims_4[i])

# reorder the sim columns
sims_4_clean = reorder_scrum_sims(sims_4_clean)

scrum_simulations = {}
print(len(scrum_simulations) + len(scrum_simulations[0]))

scrum_simulations = add_sumulations(sims_3_clean)
scrum_simulations = add_sumulations(sims_4_clean)

print(len(scrum_simulations) + len(scrum_simulations[0]))





## open the .pickle file and dump the clean data into it
with open("clean_data_scrum.pickle", 'wb') as handle:
    pickle.dump(sims_3_clean, handle, protocol=pickle.HIGHEST_PROTOCOL)