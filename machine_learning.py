import utilities as utils
from datetime import datetime
import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.svm import SVR
import matplotlib.pyplot as plt


start_time = datetime.now()
print("*"*10, "Process started @", start_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*50)

save_dir = "../../Output/"

imdb_dummies_df = pd.read_csv(save_dir + "imdb_dummies_df_2020_09_15.csv", sep="|")

print("imdb_dummies_df.shape :", imdb_dummies_df.shape)
cols = list(imdb_dummies_df.columns)
print("cols :", cols[:10])

plt.scatter(imdb_dummies_df["budget"], imdb_dummies_df["revenue"], marker="o", color="red")
plt.xlabel("Budget")
plt.ylabel("Revenue")
plt.savefig(save_dir + "/Budget_vs_Revenue.png")
# plt.show()

y = imdb_dummies_df["revenue"] / imdb_dummies_df["budget"]

imdb_dummies_df["startYear"] = imdb_dummies_df["startYear"].astype(int).astype(str)
imdb_dummies_df.drop(["primaryTitle", "originalTitle", "imdb_id", "revenue", "budget"], axis="columns", inplace=True)
imdb_dummies_df.set_index("tconst", inplace=True)
print(imdb_dummies_df[list(imdb_dummies_df.columns)[:5]].head())

X = imdb_dummies_df
features = list(X.columns)
print("len(features) :", len(features))
if "revenue" in features:
    print("revenue in features!")
# print("y :", y.head())
print("y.shape :", y.shape)
print("X.shape :", X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

corr_df = imdb_dummies_df.copy()
corr_df["profitability"] = imdb_dummies_df["revenue"] / imdb_dummies_df["budget"]
correlation_matrix = imdb_dummies_df.corr()
print("correlation_matrix.shape :", correlation_matrix.shape)


est = SVR()

# print("est.get_params().keys() ", est.get_params().keys())
# grid_dict = {"kernel": ["linear"],  # "linear", ‘poly’, ‘rbf’, ‘sigmoid’"
#              "degree": [1],
#              "C": [0.1],
#              "gamma": ["auto"]
#              }
# # grid_dict = {}
# grid = GridSearchCV(estimator=est,
#                     param_grid=grid_dict,
#                     scoring="r2",
#                     n_jobs=2,
#                     cv=5)

grid_dict = {"criterion": ["mse"],  # “mse”, “friedman_mse”, “mae”
             "random_state": [125]
             }
grid = GridSearchCV(estimator=RandomForestRegressor(),
                    param_grid=grid_dict,
                    scoring="r2",
                    n_jobs=-1,
                    cv=5)
print("grid :")
print(grid)

grid.fit(X_train, y_train)
best_params = grid.best_params_
print("best_params :", best_params)
feature_importances = grid.best_estimator_.feature_importances_
print("feature_importances :", feature_importances)
feature_importances_df = pd.DataFrame({"Feature_name": features, "Score": feature_importances})
feature_importances_df.sort_values("Score", ascending=False, inplace=True)
print("feature_importances_df :")
print(feature_importances_df.head(10))

y_pred = grid.predict(X_test)
score = grid.score(X_test, y_test)
print("score :", score)
mae = mean_absolute_error(y_true=y_test, y_pred=y_pred)
print("mae :", mae)

# shap_values = shap.TreeExplainer(grid).shap_values(X_train)
# shap.summary_plot(shap_values, X_train, plot_type="bar")

# fig, axes = plt.subplot()
plt.clf()
plt.scatter(y_pred, y_test, marker="o", color="blue")
plt.xlabel("Predicted Values")
plt.ylabel("Actual Values")
# plt.savefig(save_dir + "Predicted_vs_Actual.png")
plt.show()

end_time = datetime.now()
print("*"*10, "Process ended @", end_time.strftime("%d-%m-%Y, %H:%M:%S"), "*"*50)
duration = end_time - start_time
print("*"*10, "Duration -", duration, "*"*50)
