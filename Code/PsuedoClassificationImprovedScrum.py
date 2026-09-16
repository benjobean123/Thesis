import pandas as pd
from datetime import *
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.svm import SVC
import timeit
import numpy as np
import pickle




with open('clean_data_scrum.pickle', 'rb') as handle:
  data = pickle.load(handle)

sim_names = list(data.keys())
print("Sim Names")
print(len(sim_names))


clean_sims = [data[name] for name in sim_names]
#print(clean_sims)
# Median + Mode => 7 - 12
# Low: 7,8
# Med: 9, 10
# High: 11, 12
#sim_classifications = [['low', 'low', 'medium', 'medium', 'high', 'high'][int(sim['SA'].median() + sim['SA'].mode()[0]) - 7] for sim in clean_sims]
sim_classifications = [[1, 1, 2, 2, 3, 3][int(sim['TSA'].median() + sim['TSA'].mode()[0]) - 7] for sim in clean_sims]
sim_classifications = [2, 3, 3, 1, 1, 2, 3, 2]
print("Sim Classifications")
print(sim_classifications)
#print(sim_part_0_average_turn_taking)
day = date.today()
#print((lambda x: datetime.combine(day, x.iloc[-1]) - datetime.combine(day, x.iloc[0]))(clean_sims[0][clean_sims[0]['Simulation']==3]['Time'].sort_values()).seconds)


def calculate_average(sim, i):
  try:

    return 60 * len(sim[sim['Sprint']==i+1]) / (lambda x: datetime.combine(day, x.iloc[-1]) - datetime.combine(day, x.iloc[0]))(sim[sim['Sprint']==i+1]['Timestamp'].sort_values()).seconds
  except:
    return 0


sim_average_turn_taking = [
  sum([
    calculate_average(sim, i) for i in range(0, 8)
  ]) for sim in clean_sims
]

print("names")
print(sim_names[1])
sim_number_turns = [len(sim) for sim in clean_sims]
print("number of turns:")
print(sim_number_turns[0])
sim_turn_taking = [[len(sim[sim['Name'] == i+1])for sim in clean_sims] for i in range(0, 8)]
print("turn taking")
print(sim_turn_taking[0][0])
sim_player_sa = [[sim[sim['Name'] == i+1]['TSA'].dropna().mean() for sim in clean_sims] for i in range(0, 8)]
print("player tsa score")
print(sim_player_sa[0][0])
sim_player_sa_median = [[sim[sim['Name'] == i+1]['TSA'].median() for sim in clean_sims] for i in range(0, 8)]
print("median tsa score")
print(sim_player_sa_median[0][0])
sim_turn_taking_by_sa = [[len(sim[sim['TSA']==i]) for sim in clean_sims] for i in range(3, 7)]
print("turn taking by tsa")
print(sim_turn_taking_by_sa[0][0])

prediction_scrum_df = pd.DataFrame.from_dict(
  {
    'Name' : sim_names,
    'Number of Turns' : sim_number_turns,
    'Member 1 Turn Taking' : sim_turn_taking[0],
    'Member 2 Turn Taking' : sim_turn_taking[1],
    'Member 3 Turn Taking' : sim_turn_taking[2],
    'Member 4 Turn Taking' : sim_turn_taking[3],
    'Member 5 Turn Taking' : sim_turn_taking[4],
    'Member 6 Turn Taking' : sim_turn_taking[5],
    'Member 7 Turn Taking' : sim_turn_taking[6],
    'Member 8 Turn Taking' : sim_turn_taking[7],
    'Member 1 TSA Average' : sim_player_sa[0],
    'Member 2 TSA Average' : sim_player_sa[1],
    'Member 3 TSA Average' : sim_player_sa[2],
    'Member 4 TSA Average' : sim_player_sa[3],
    'Member 5 TSA Average' : sim_player_sa[4],
    'Member 6 TSA Average' : sim_player_sa[5],
    'Member 7 TSA Average' : sim_player_sa[6],
    'Member 8 TSA Average' : sim_player_sa[7],
    'Average Turn Taking' : sim_average_turn_taking,
    'TSA 3 Turn Taking': sim_turn_taking_by_sa[0],
    'TSA 4 Turn Taking': sim_turn_taking_by_sa[1],
    'TSA 5 Turn Taking': sim_turn_taking_by_sa[2],
    'TSA 6 Turn Taking': sim_turn_taking_by_sa[3],
    'Performance Rank': sim_classifications
  }
).fillna(0)

#temp = np.array(clean_sims.length)

## Dump the prediction_df file
with open("prediction_scrum_df.pickle", 'wb') as handle:
    pickle.dump(prediction_scrum_df, handle, protocol=pickle.HIGHEST_PROTOCOL)

y = prediction_scrum_df['Performance Rank']
x = prediction_scrum_df.drop(columns=['Performance Rank', 'Name'])

print("y")
print(y)
print("x")
print(x)

temp = np.array(clean_sims)

print("prediction_scrum_df")
print(prediction_scrum_df)

X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.25, random_state=2)


rgr_tree = DecisionTreeRegressor(random_state=22).fit(X_train, Y_train)

Y_pred = rgr_tree.predict(X_test)

print('\n\n[ANOVA Decision Tree]')
print("Time:", timeit.timeit('rgr_tree.predict(X_test)', globals=globals(), number=1000)/1000)
print("R2 Score:", metrics.r2_score(Y_test, Y_pred))
print("Mean Squared Error:", metrics.mean_squared_error(Y_test, Y_pred))
print("Mean Absolute Error:", metrics.mean_absolute_error(Y_test, Y_pred))

print("[Feature Importances]")
importance = rgr_tree.feature_importances_
for i, v in enumerate(importance):
  print(f"{x.columns[i]}:\t\t{v}")



clf_tree = DecisionTreeClassifier(random_state=21).fit(X_train, Y_train)
Y_pred = clf_tree.predict(X_test)

print("\n\n[Decision Tree Classifier]")
print("Time:", timeit.timeit('clf_tree.predict(X_test)', globals=globals(), number=1000)/1000)

print("Accuracy:", metrics.accuracy_score(Y_test, Y_pred))
print("Confusion Matrix:\n",metrics.confusion_matrix(Y_test, Y_pred))

print("[Feature Importances]")
importance = clf_tree.feature_importances_
for i, v in enumerate(importance):
  print(f"{x.columns[i]}:\t\t{v}")

print("\n")







clf = RandomForestClassifier(random_state=2).fit(X_train, Y_train)
Y_pred = clf.predict(X_test)

print("\n\n[Random Forest Classifier]")
print("Time:", timeit.timeit('clf.predict(X_test)', globals=globals(), number=1000)/1000)

print("Accuracy:", metrics.accuracy_score(Y_test, Y_pred))
print("Confusion Matrix:\n",metrics.confusion_matrix(Y_test, Y_pred))

print("[Feature Importances]")
importance = clf.feature_importances_
for i, v in enumerate(importance):
  print(f"{x.columns[i]}:\t\t{v}")







test = SelectKBest(score_func=f_classif, k=5)
fit = test.fit(X_train, Y_train)
print("\n\n[ANOVA F Value Feature Scores]") 
# summarize scores
for s in fit.scores_:
  print("\t\t", s)
print(fit.get_feature_names_out())




rgr_tree = RandomForestRegressor(random_state=22).fit(X_train, Y_train)
Y_pred = rgr_tree.predict(X_test)
print('\n\n[Random Forest Regressor]')
print("Time:", timeit.timeit('rgr_tree.predict(X_test)', globals=globals(), number=1000)/1000)
print("R2 Score:", metrics.r2_score(Y_test, Y_pred))
print("Mean Squared Error:", metrics.mean_squared_error(Y_test, Y_pred))
print("Mean Absolute Error:", metrics.mean_absolute_error(Y_test, Y_pred))

print("[Feature Importances]")
importance = rgr_tree.feature_importances_
for i, v in enumerate(importance):
  print(f"{x.columns[i]}:\t\t{v}")



clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
clf.fit(X_train, Y_train)
print("\n\n[SVM Classifier]")
print("Time:", timeit.timeit('clf.predict(X_test)', globals=globals(), number=1000)/1000)
print(clf.score(X_test, Y_test))

test = SelectKBest(score_func=f_classif, k=5)
fit = test.fit(X_train, Y_train)

kx_train = fit.transform(X_train)
ky_train = Y_train
kx_test = fit.transform(X_test)
ky_test = Y_test

clf.fit(kx_train, ky_train)
print("\n\n[SVM Classifier - K Best]")
print("Time:", timeit.timeit('clf.predict(kx_test)', globals=globals(), number=1000)/1000)
print(clf.score(kx_test, ky_test))


clf = MLPClassifier(random_state=2)
clf.fit(X_train, Y_train)
print("\n\n[MLP Classifier - Adam]")
print("Time:", timeit.timeit('clf.predict(X_test)', globals=globals(), number=1000)/1000)
print(clf.score(X_test, Y_test))


clf = MLPClassifier(solver="lbfgs", random_state=2)
clf.fit(X_train, Y_train)
print("\n\n[MLP Classifier - LBFGS]")
print("Time:", timeit.timeit('clf.predict(X_test)', globals=globals(), number=1000)/1000)
print(clf.score(X_test, Y_test))
