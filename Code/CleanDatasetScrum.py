import pandas as pd
import pickle
from numpy import nan
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

  ## Reorganize the sheets to separate Agile Ceremonies by sprint 
  # Check for what sprint the line belongs too
  for line in sim_df['Sprint']:
    # If sprint 1, add the line to the new sim file
    match line:
      case '1':
        sprint1 = pd.concat([sprint1, pd.sim_df([line])])
      case '2':
        sprint2 = pd.concat([sprint2, pd.sim_df([line])])
      case '3':
        sprint3 = pd.concat([sprint2, pd.sim_df([line])])
      case '4':
        sprint4 = pd.concat([sprint2, pd.sim_df([line])])
    
  print(sprint1)
  

  return sim_df

clean_scrum_sims = {}


# clean the agile sims high functioning
for i in range(len(sims_3)):
  try:
    clean_scrum_sims[sim_names3[i]] = clean_sim_scrum_data(sims_3[i])
  except Exception as e:
    print("\n")
    #print(i, sim_names3[i], e)
    #print(sims_3[i])

# clean the agile sims high functioning
for i in range(len(sims_4)):
  try:
    clean_scrum_sims[sim_names4[i]] = clean_sim_scrum_data(sims_4[i])
  except Exception as e:
    print("\n")
    #print(i, sim_names4[i], e)
    #print(sims_4[i])



## open the .pickle file and dump the clean data into it
with open("clean_data_scrum.pickle", 'wb') as handle:
    pickle.dump(clean_scrum_sims, handle, protocol=pickle.HIGHEST_PROTOCOL)