import pyodbc
import pandas as pd
import warnings
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.tree import DecisionTreeClassifier, export_text

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
conn_str = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=.\SQLEXPRESS;"
    r"DATABASE=oel;"
    r"Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("Successfully connected to the 'oel' Star Schema database on .\\SQLEXPRESS\n")
except Exception as e:
    print(f"Primary connection failed: {e}")
    print("Attempting fallback connection to localhost...")
    conn_str = conn_str.replace(".\\SQLEXPRESS", "localhost")
    conn = pyodbc.connect(conn_str)


print(" PART 1: ASSOCIATION MINING FROM 'FACT_SALES' & 'DIM_PRODUCT'")

query_basket = """
select 
    f.customer_key, 
    f.time_key, 
    p.product_name 
from fact_sales f 
inner join dim_product p on f.product_key = p.product_key
"""

df_basket_raw = pd.read_sql(query_basket, conn)

df_basket_raw["transaction_id"] = (
    df_basket_raw["customer_key"].astype(str)
    + "_"
    + df_basket_raw["time_key"].astype(str)
)

basket = (
    pd.crosstab(df_basket_raw["transaction_id"], df_basket_raw["product_name"])
    .map(lambda x: x > 0)
    .astype(bool)
)

print("\nExtracted One-Hot Encoded Basket from Star Schema ")
print(basket)

frequent_itemsets = apriori(basket, min_support=0.3, use_colnames=True)
print("\nFrequent Itemsets from SQL Server ")
print(frequent_itemsets)


if not frequent_itemsets.empty and max(frequent_itemsets["itemsets"].apply(len)) > 1:
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
    print("\nGenerated Association Rules from SQL Server ")
    print(rules[["antecedents", "consequents", "support", "confidence", "lift"]])
else:
    print("\nNo frequent itemsets with multiple items found to generate rules.")


print("\n")
print(" PART 2: CLASSIFICATION FROM 'FACT_SALES' & 'DIM_CUSTOMER'")

query_cust = """
select 
    c.country, 
    c.segment, 
    sum(f.sales_amount) as total_spent
from fact_sales f
inner join dim_customer c on f.customer_key = c.customer_key
group by f.customer_key, c.country, c.segment
"""

df_cust_raw = pd.read_sql(query_cust, conn)

df_cust_raw["is_premium_segment"] = df_cust_raw["segment"].map(
    lambda x: 1 if x == "Premium" else 0
)
df_cust_raw["is_usa"] = df_cust_raw["country"].map(lambda x: 1 if x == "USA" else 0)

df_cust_raw["is_high_spender"] = df_cust_raw["total_spent"].map(
    lambda x: 1 if x > 500.00 else 0
)

print("\nExtracted Customer Profiles for Classification ")
print(df_cust_raw[["country", "segment", "total_spent", "is_high_spender"]])

X = df_cust_raw[["is_premium_segment", "is_usa"]]
y = df_cust_raw["is_high_spender"]

clf = DecisionTreeClassifier(max_depth=2, random_state=42)
clf.fit(X, y)

tree_rules = export_text(clf, feature_names=["Is_Premium_Segment", "Is_USA"])
print("\n--- Generated Decision Tree Rules from Star Schema ---")
print(tree_rules)

new_test = pd.DataFrame([[0, 1]], columns=["is_premium_segment", "is_usa"])
prediction = clf.predict(new_test)
print(f"Prediction for standard segment customer from the USA:")
print(f" -> Will be a High Spender: {'YES' if prediction[0] == 1 else 'NO'}")

conn.close()
