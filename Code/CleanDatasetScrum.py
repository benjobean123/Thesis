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
highFunctioningDF = [pd.read_excel(xls3, sheet) for sheet in xls3.sheet_names]
highFunctioningMetrics = highFunctioningDF.pop(5) ## Remove the Metrics sheet from the dataframe
print(highFunctioningMetrics)
highFunctioningDFNames = xls3.sheet_names[1:]
#print(highFunctioningDF)




# Read in the Scrum high functioning excel sheet
mediumFunctioningDF = [pd.read_excel(xls4, sheet) for sheet in xls4.sheet_names]
mediumFunctioningMetrics = mediumFunctioningDF.pop(5) ## Remove the Metrics sheet from the dataframe
print(highFunctioningMetrics)
medFunctioningDFNames = xls4.sheet_names[1:]



## Remove duplicate
def rn(df, suffix = '-duplicate-'):
    appendents = (suffix + df.groupby(level=0).cumcount().astype(str)).replace(suffix, '')
    return df.set_index(df.index + appendents)



## Function to clean each Agile excel sheet dataframe
def clean_sim_scrum_data(simDF):
  
  # Remove the unneeded Date and Role columns
  simDF = simDF.drop(columns=["Date", "Role"])


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

  simDF['Name'] = simDF['Name'].map(team_names)


  # Remove the names from the chat logs
  simDF['Message'] = simDF['Message'].str.replace(r'^[^:]*:', '', regex=True)

  # Reorder the columns
  column_order = ['Name', 'Timestamp', 'Message', 'Sprint', 'TSA']
  simDF = simDF[column_order]


  
  return simDF


def reorder_scrum_sims(simDF):
  
  reordered_sims = {}
  reordered_sims[0]=pd.DataFrame(columns=simDF[0].columns)
  reordered_sims[1]=pd.DataFrame(columns=simDF[1].columns)
  reordered_sims[2]=pd.DataFrame(columns=simDF[2].columns)
  reordered_sims[3]=pd.DataFrame(columns=simDF[3].columns)

  for i in range(len(simDF)):
    print(simDF[i])
    ## Reorganize the sheets to separate Agile Ceremonies by sprint 
    # Create empty dataframes with the same columns
    sprint1 = pd.DataFrame(columns=simDF[i].columns)
    sprint2 = pd.DataFrame(columns=simDF[i].columns)
    sprint3 = pd.DataFrame(columns=simDF[i].columns)
    sprint4 = pd.DataFrame(columns=simDF[i].columns)
    
    # Check for what sprint the line belongs too
    # Loop through each row and add to the right dataframe
    for _, row in simDF[i].iterrows():
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
# def add_simulations(simulations_df):
#     key = len(scrumSimulations)
#     new_entries = {key + i: df.copy() for i, df in enumerate(sims_3_clean)}
#     scrumSimulations.update(new_entries)
#     return simulations_df

def add_simulations(simulationsDF):
  key=len(scrumSimulations)
  for i in range(len(simulationsDF)):
    print(scrumSimulations)
    scrumSimulations[i + key] = pd.DataFrame(columns=simulationsDF[i].columns)
    scrumSimulations[i + key] = pd.concat([scrumSimulations[i + key], simulationsDF[i]], ignore_index=True)
  
  return scrumSimulations

def assign_performance_rank(simDF, performanceMetrics):
  print("entering performance rank\n")
  ## Assign a Scrum performance rank to the dataframe

  # 1 = Low Functioning
  # 2 = Med Functioning
  # 3 = High Functioning

  for i in performanceMetrics:
    print(performanceMetrics[i])
  

  performace_level="high"

  performance_map = {
      "low": 1,
      "medium": 2,
      "high": 3
  }

  simDF = simDF.copy()

  simDF["Performance Rank"] = performance_map[performace_level.lower()]


# clean the agile sims high functioning
highFunctioningDFClean = highFunctioningDF
for i in range(len(highFunctioningDF)):
  try:
    highFunctioningDFClean[i] = clean_sim_scrum_data(highFunctioningDF[i])
  except Exception as e:
    print("\n")
    #print(i, sim_names3[i], e)
    #print(sims_3[i])

# reorder the sim columns
highFunctioningDFClean = reorder_scrum_sims(highFunctioningDFClean)

highFunctioningDFClean = assign_performance_rank(highFunctioningDFClean, highFunctioningMetrics)
#print(highFunctioningDFClean)


# clean the agile sims medium functioning
mediumFunctioningDFClean = mediumFunctioningDF
for i in range(len(mediumFunctioningDF)):
  try:
    mediumFunctioningDFClean[medFunctioningDFNames[i]] = clean_sim_scrum_data(mediumFunctioningDF[i])
  except Exception as e:
    print("\n")
    #print(i, medFunctioningDFNames[i], e)
    #print(sims_4[i])

# reorder the sim columns
mediumFunctioningDFClean = reorder_scrum_sims(mediumFunctioningDFClean)

scrumSimulations = {}

scrumSimulations = add_simulations(highFunctioningDFClean)
scrumSimulations = add_simulations(mediumFunctioningDFClean)








## open the .pickle file and dump the clean data into it
with open("clean_data_scrum.pickle", 'wb') as handle:
    pickle.dump(scrumSimulations, handle, protocol=pickle.HIGHEST_PROTOCOL)