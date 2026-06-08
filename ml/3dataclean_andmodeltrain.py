import pandas as pd
import numpy as np
from scipy import stats #z score module
np.random.seed(42)
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error , r2_score,root_mean_squared_error
import matplotlib.pyplot as plt 

n = 50

data = {
    "Engine_Size": np.random.uniform(1.0, 4.5, n),   # liters
    "Horsepower": np.random.randint(70, 300, n),
    "Age": np.random.randint(1, 15, n),
    "Mileage": np.random.randint(10000, 200000, n),
    "Brand_Value": np.random.randint(1, 5, n)  # 1=low brand, 5=high brand
}

df = pd.DataFrame(data)

# Price formula (realistic logic)
df["Price"] = (
    df["Engine_Size"] * 500000 +
    df["Horsepower"] * 10000 -
    df["Age"] * 80000 -
    df["Mileage"] * 5 +
    df["Brand_Value"] * 300000
)

# print(df)
#part1 : 

# averagePrice 
averagePrice  = np.mean(df["Price"]) 
print(f"the average price is : {averagePrice}")
print()

#top 5 most expensive car  df.nlargest(value,name)
top5 = df.sort_values("Price",ascending=False).head(5) 
print(f"top 5 expensive car is :\n {top5}")
print()

# Age > 10 भएका कारहरूको average price निकाल।
AgeGreaterThan10  = df[df["Age"] > 10]["Price"].mean()
print(f"The car age > 10 average  price are : \n {AgeGreaterThan10}")
print()

# Brand_Value अनुसार groupby गरेर average price निकाल।
brandValueBy= df.groupby("Brand_Value")["Price"].mean() 
print(F"The brand value by average price is \n : {brandValueBy}")
print()

# Correlation matrix निकाल।
correlection  = df.corr(numeric_only=True)
print(f"the correlation matrix is : {correlection}")
print()


#part2  : 
# Mileage column normalize गर।
mileage_normalize = (df["Mileage"] - np.min(df["Mileage"]))/ (np.max(df["Mileage"] - np.min(df["Mileage"])))
print(f"The normalized mileage is : \n {mileage_normalize}")


# Z-score निकाल Horsepower को।
# zScore = stats.zscore(df["Horsepower"])NUMPY TYPE CHECK
df["Horsepower"] = stats.zscore(df["Horsepower"])
print(f"the z score of horsepower is : \n {df}")

#  manual feature scaling गर।
feature_cols = ["Engine_Size", "Horsepower", "Age", "Mileage", "Brand_Value"]
df[feature_cols] = (df[feature_cols] - df[feature_cols].min())/ (df[feature_cols].max() - df[feature_cols].min())

print("manual feature scaling (first 5 rows):")
print(df)

# 75th percentile price निकाल।
p75 = np.percentile(df["Price"],75) 
print(f"75 percentile price is : {p75}")


# Outlier detect गर (IQR method use गरेर)।
Q1 = df["Price"].quantile(0.25)
Q3 = df["Price"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["Price"] < lower_bound) | (df["Price"] > upper_bound)]

print(f"Price IQR lower bound: {lower_bound}")
print(f"Price IQR upper bound: {upper_bound}")
print("Outliers based on IQR:")
print(outliers)
print(f"Total outliers: {len(outliers)}")


# Part 3: Machine Learning (Advanced Linear Regression)  
# features and target  
X  = df[ ["Engine_Size", "Horsepower", "Age", "Mileage", "Brand_Value"]]
y  = df["Price"]


#data split  
X_train, X_test , y_train ,y_test = train_test_split(X,y , test_size=0.2 , random_state=42)

#train the model 
model = LinearRegression()
model.fit(X_train,y_train)

#predict model and mse and r2 score 
y_pred  = model.predict(X_test)
print(f"the predict value is : {y_pred}")
print(f"The acutal value is {y_test}")
print(f"the mse is : {mean_squared_error(y_test,y_pred)}") 
print(f"The r2 score is : {r2_score(y_test,y_pred)}")


# intercept 
print(f"The intercept is : {model.intercept_}")
print(f"the Root mean square is {root_mean_squared_error(y_test,y_pred)}")


plt.scatter(y_test,y_pred)
plt.xlabel("Actual Price")  
plt.ylabel("Predicted Price")  
plt.title("Actual vs Predicted Price")
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')  # Line for perfect predictions
plt.show()