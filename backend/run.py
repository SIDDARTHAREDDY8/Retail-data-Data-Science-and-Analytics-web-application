from app import app
import pyodbc
from flask import jsonify, request, send_file
from datetime import datetime
import os
from flask import Flask
from flask_cors import CORS
import io
import base64
import csv
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report,roc_curve, roc_auc_score
from mlxtend.frequent_patterns import apriori, association_rules
from io import BytesIO
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import json



app = Flask(__name__)

CORS(app)

DB_SERVER = 'siddureddych.database.windows.net'  # Your server name
DB_DATABASE = 'retail-db'  # Your database name
DB_USERNAME = 'admin-1'  # Your username
DB_PASSWORD = 'Siddu@1139'

# Set allowed file extensions for file uploads
ALLOWED_EXTENSIONS = {'csv'}

# Database connection string (using the variables defined in the previous step)
def get_db_connection():
    connection_string = "Driver={ODBC Driver 18 for SQL Server};"+f'Server={DB_SERVER};' + f'Database={DB_DATABASE};'+f'UID={DB_USERNAME};'+f'PWD={DB_PASSWORD};'    
    conn = pyodbc.connect(connection_string)
    return conn

# Function to check the file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Root endpoint for testing
@app.route("/", methods=["GET"])
def root():
    return "Flask API for Household, Transaction, Product"


@app.route("/dashboard/insights", methods=["GET"])
def get_dashboard_insights():
    conn = get_db_connection()
    cursor = conn.cursor()

    group_by_field = request.args.get('group_by', 'age_range')

    if group_by_field not in ['age_range', 'income_range', 'children']:
        group_by_field = 'age_range'

    demographics_query = f"""
        SELECT 
            CAST({group_by_field} AS VARCHAR(255)) AS group_value, 
            COUNT(*) AS engagement_score
        FROM [500_households]
        JOIN [500_transactions] ON [500_households].hshd_num = [500_transactions].hshd_num
        GROUP BY CAST({group_by_field} AS VARCHAR(255))
    """

    cursor.execute(demographics_query)
    demographics_rows = cursor.fetchall()

    # Prepare the data for the chart
    demographics_data = [{
        "group_value": row[0].strip(),  
        "engagement_score": row[1]
    } for row in demographics_rows]

    cursor.close()
    conn.close()

    return jsonify({
        "demographics": demographics_data,
    })

@app.route("/dashboard/engagement_over_time", methods=["GET"])
def get_engagement_over_time():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get total units sold per year
    yearly_units_query = """
        SELECT YEAR(purchase) AS year, SUM(units) AS total_units
        FROM [500_transactions]
        GROUP BY YEAR(purchase)
        ORDER BY year
    """
    cursor.execute(yearly_units_query)
    yearly_units_rows = cursor.fetchall()

    # Process the data for the pie chart (yearly data)
    yearly_units_data = [{
        "year": row[0],
        "total_units": row[1]
    } for row in yearly_units_rows]

    # Get the available years
    available_years = [row[0] for row in yearly_units_rows]

    selected_year = request.args.get('year', available_years[0] if available_years else '2018')

    monthly_units_query = """
        SELECT MONTH(purchase) AS month, SUM(units) AS total_units
        FROM [500_transactions]
        WHERE YEAR(purchase) = ?
        GROUP BY MONTH(purchase)
        ORDER BY month
    """
    cursor.execute(monthly_units_query, (selected_year,))
    monthly_units_rows = cursor.fetchall()

    # Process the data for the bar chart (monthly data for selected year)
    monthly_units_data = [{
        "month": row[0],
        "total_units": row[1]
    } for row in monthly_units_rows]

    cursor.close()
    conn.close()

    return jsonify({
        "yearlyData": yearly_units_data,
        "monthlyData": monthly_units_data,
        "availableYears": available_years,
    })


@app.route("/data/<int:hshd_num>", methods=["GET"])
def get_merged_data(hshd_num):
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL Query to merge the three datasets using JOINs
    query = """
        SELECT 
            h.hshd_num, h.l, h.age_range, h.income_range, h.marital, h.homeowner, 
            h.hshd_composition, h.hh_size, h.children, 
            t.basket_num, t.purchase, t.spend, t.units, t.store_r, t.week_num, t.year, 
            p.product_num, p.department, p.commodity, p.brand_ty, p.natural_organic_flag
        FROM [500_households] h
        JOIN [500_transactions] t ON h.hshd_num = t.hshd_num
        LEFT JOIN [500_products] p ON t.product_num = p.product_num
        WHERE h.hshd_num = ?
    """
    
    cursor.execute(query, (hshd_num,))
    rows = cursor.fetchall()

    # Process the result into a list of dictionaries
    result = [{
        "hshd_num": row[0], 
        "l": row[1], 
        "age_range": row[2],
        "income_range": row[3], 
        "marital": row[4], 
        "homeowner": row[5],
        "hshd_composition": row[6], 
        "hh_size": row[7], 
        "children": row[8],
        "basket_num": row[9], 
        "purchase": row[10], 
        "spend": row[11], 
        "units": row[12], 
        "store_r": row[13], 
        "week_num": row[14], 
        "year": row[15], 
        "product_num": row[16], 
        "department": row[17],
        "commodity": row[18],
        "brand_ty": row[19],
        "natural_organic_flag": row[20]
    } for row in rows]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the merged data as JSON
    return jsonify(result)

# Additional routes (updated to use square brackets for table names)
@app.route("/households", methods=["GET"])
def get_households():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Use square brackets to reference table names starting with numbers
    cursor.execute("SELECT * FROM [500_households]")
    rows = cursor.fetchall()
    
    result = [{"hshd_num": row[0], "l": row[1], "age_range": row[2], 
               "income_range": row[3], "marital": row[4], "homeowner": row[5],
               "hshd_composition": row[6], "hh_size": row[7], "children": row[8]} 
              for row in rows]
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

# Further endpoints also need to be updated for any table name starting with a number
@app.route("/household/<int:hshd_num>", methods=["GET"])
def get_household(hshd_num):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Correct SQL query using square brackets
    cursor.execute("SELECT * FROM [500_households] WHERE hshd_num = ?", (hshd_num,))
    rows = cursor.fetchall()
    
    if rows:
        result = [{"hshd_num": row[0], "l": row[1], "age_range": row[2], "income_range": row[4], "marital": row[3], "homeowner": row[5], "hshd_composition": row[6], "hh_size": row[7], "children": row[8]} for row in rows]
    else:
        result = {"message": "Household not found"}
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

# Similarly, update other routes that query tables with names starting with numbers
@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM [500_transactions]")
    rows = cursor.fetchall()
    
    result = [{"product_num": row[0], "basket_num": row[1], "hshd_num": row[2], 
               "purchase": row[3], "spend": row[4], "units": row[5], 
               "store_r": row[6], "week_num": row[7], "year": row[8]} 
              for row in rows]
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

@app.route("/transaction/<int:hshd_num>", methods=["GET"])
def get_transaction(hshd_num):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [500_transactions] WHERE hshd_num = ?", (hshd_num,))
    rows = cursor.fetchall()
    
    if rows:
        result = [{"product_num": row[3], "basket_num": row[0], "hshd_num": row[1], "purchase": row[2], "spend": row[4], "units": row[5], "store_r": row[6], "week_num": row[7], "year": row[8]} for row in rows]
    else:
        result = {"message": "Transaction not found"}
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

@app.route("/products", methods=["GET"])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM [500_products]")
    rows = cursor.fetchall()
    
    result = [{"product_num": row[0], "department": row[1], "commodity": row[2],
               "brand_ty": row[3], "natural_organic_flag": row[4]} 
              for row in rows]
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

# Example endpoint to fetch a specific product by product_num
@app.route("/product/<int:product_num>", methods=["GET"])
def get_product(product_num):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM [500_products] WHERE product_num = ?", (product_num,))
    row = cursor.fetchone()
    
    if row:
        result = {
            "product_num": row[0], "department": row[1], "commodity": row[2],
            "brand_ty": row[3], "natural_organic_flag": row[4]
        }
    else:
        result = {"message": "Product not found"}
    
    cursor.close()
    conn.close()
    
    return jsonify(result)

ALLOWED_EXTENSIONS = {'csv'}

# Path for saving the graphs
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# Ensure the static folder exists
os.makedirs(STATIC_FOLDER, exist_ok=True)


# Function to check the file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Expected columns and data types for validation
expected_household_columns = [
    "hshd_num", "l", "age_range", "income_range", "marital", 
    "homeowner", "hshd_composition", "hh_size", "children"
]
expected_household_data_types = {
    "hshd_num": int,
    "l": int,
    "age_range": str,
    "income_range": str,
    "marital": str,
    "homeowner": str,
    "hshd_composition": str,
    "hh_size": int,
    "children": int
}

expected_transaction_columns = [
    "basket_num", "hshd_num", "purchase", "spend", "units", 
    "store_r", "week_num", "year"
]
expected_transaction_data_types = {
    "basket_num": int,
    "hshd_num": int,
    "purchase": str,
    "spend": float,
    "units": int,
    "store_r": str,
    "week_num": int,
    "year": int
}

expected_product_columns = [
    "product_num", "department", "commodity", "brand_ty", 
    "natural_organic_flag"
]
expected_product_data_types = {
    "product_num": int,
    "department": str,
    "commodity": str,
    "brand_ty": str,
    "natural_organic_flag": str
}



# The upload endpoint
@app.route("/upload", methods=["POST"])
def upload_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    
    files = request.files.getlist('file')

    if len(files) > 3:
        return jsonify({"error": "You can upload a maximum of 3 datasets."}), 400
        

    # Prepare DataFrames for uploaded files
    datasets = {
        "households": None,
        "transactions": None,
        "products": None
    }

    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))

            # Read the CSV file
            data = pd.read_csv(os.path.join('uploads', filename))

            # Replace missing values with None (SQL NULL equivalent)
            data = data.where(pd.notnull(data), None)

            if 'hshd_num' in data.columns:  # Household dataset
                datasets["households"] = data
            elif 'basket_num' in data.columns:  # Transaction dataset
                datasets["transactions"] = data
            elif 'product_num' in data.columns:  # Product dataset
                datasets["products"] = data
            else:
                return jsonify({"error": f"Invalid file columns in {filename}"}), 400
                

    # Database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Household Validation
    if datasets["households"] is not None:
        data = datasets["households"]
        if not all(col in data.columns for col in expected_household_columns):
            return jsonify({"error": "Household dataset column names do not match the expected schema."}), 400
            
        # for col, expected_type in expected_household_data_types.items():
        #     if not all(isinstance(val, expected_type) for val in data[col]):
        #         return jsonify({"error": f"Invalid data type in column: {col} for household dataset."}), 400
                
        # Check data types for each column and handle missing values
        for col in expected_household_columns:
            if col in data.columns and not all(isinstance(val, str) if isinstance(data[col][0], str) else isinstance(val, int) for val in data[col]):
                return jsonify({"error": f"Invalid data type in column: {col} for household dataset."}), 400
        
        cursor.execute("DELETE FROM [500_households]")  # Clear existing data
        for index, row in data.iterrows():
            insert_query = """
            INSERT INTO [500_households] (hshd_num, l, age_range, income_range, marital, homeowner, 
                                          hshd_composition, hh_size, children)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, tuple(row))

    # Transaction Validation
    if datasets["transactions"] is not None:
        data = datasets["transactions"]
        if not all(col in data.columns for col in expected_transaction_columns):
            return jsonify({"error": "Transaction dataset column names do not match the expected schema."}), 400
            
        # for col, expected_type in expected_transaction_data_types.items():
        #     if not all(isinstance(val, expected_type) for val in data[col]):
        #         return jsonify({"error": f"Invalid data type in column: {col} for transaction dataset."}), 400
                
        # Check data types for each column and handle missing values
        for col in expected_transaction_columns:
            if col in data.columns and not all(isinstance(val, str) if isinstance(data[col][0], str) else isinstance(val, int) for val in data[col]):
                return jsonify({"error": f"Invalid data type in column: {col} for transaction dataset."}), 400
        
        
        cursor.execute("DELETE FROM [500_transactions]")  # Clear existing data
        for index, row in data.iterrows():
            insert_query = """
            INSERT INTO [500_transactions] (basket_num, hshd_num, purchase, spend, units, 
                                            store_r, week_num, year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, tuple(row))

    # Product Validation
    if datasets["products"] is not None:
        data = datasets["products"]
        if not all(col in data.columns for col in expected_product_columns):
            return jsonify({"error": "Product dataset column names do not match the expected schema."}), 400
            
        # for col, expected_type in expected_product_data_types.items():
        #     if not all(isinstance(val, expected_type) for val in data[col]):
        #         return jsonify({"error": f"Invalid data type in column: {col} for product dataset."}), 400
                
        # Check data types for each column and handle missing values
        for col in expected_product_columns:
            if col in data.columns and not all(isinstance(val, str) if isinstance(data[col][0], str) else isinstance(val, int) for val in data[col]):
                return jsonify({"error": f"Invalid data type in column: {col} for product dataset."}), 400
        
        
        cursor.execute("DELETE FROM [500_products]")  # Clear existing data
        for index, row in data.iterrows():
            insert_query = """
            INSERT INTO [500_products] (product_num, department, commodity, brand_ty, natural_organic_flag)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, tuple(row))

    # Handle missing datasets (default original datasets if any dataset is missing)
    if datasets["households"] is None:
        # Set default households dataset here if necessary
        pass
    if datasets["transactions"] is None:
        # Set default transactions dataset here if necessary
        pass
    if datasets["products"] is None:
        # Set default products dataset here if necessary
        pass

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Data uploaded and processed successfully"}), 200
# Additional routes (updated to use square brackets for table names)


# Convert the generated plot to base64-encoded string
def get_image_base64(image_data):
    buffered = BytesIO()
    image_data.savefig(buffered, format="png")
    buffered.seek(0)
    return base64.b64encode(buffered.read()).decode("utf-8")

import calendar

@app.route("/dashboard/churn_prediction", methods=["GET"])
def get_churn_prediction_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the user selections from the frontend (with default to 'All')
    department = request.args.get('department', 'All')
    commodity = request.args.get('commodity', 'All')
    brand_type = request.args.get('brand_type', 'All')
    organic_flag = request.args.get('organic_flag', 'All')

    # Start building the query
    query = """
        SELECT 
            t.purchase,  -- Daily date
            SUM(t.spend) AS total_spend,
            p.department,
            p.commodity,
            p.brand_ty,
            p.natural_organic_flag
        FROM [500_transactions] t
        JOIN [500_products] p ON t.product_num = p.product_num
        WHERE 1=1
    """
    
    # Add conditions based on the selected filters
    if department != 'All':
        query += f" AND p.department = '{department}'"
    if commodity != 'All':
        query += f" AND p.commodity = '{commodity}'"
    if brand_type != 'All':
        query += f" AND p.brand_ty = '{brand_type}'"
    if organic_flag != 'All':
        query += f" AND p.natural_organic_flag = '{organic_flag}'"
    
    # Group by exact date to get daily data
    query += """
        GROUP BY t.purchase, p.department, p.commodity, p.brand_ty, p.natural_organic_flag
        ORDER BY t.purchase
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    # Process the data into a format we can use for the frontend
    result_data = [{
        "purchase": row[0],  # Exact date of purchase
        "total_spend": row[1],  # Total spend for the day
        "department": row[2],
        "commodity": row[3],
        "brand_ty": row[4],
        "natural_organic_flag": row[5],
        "month_name": calendar.month_name[row[0].month],  # Month name from the date
    } for row in rows]

    cursor.close()
    conn.close()

    return jsonify(result_data)


from mlxtend.preprocessing import TransactionEncoder

# @app.route("/dashboard/basket_analysis", methods=["GET"])
# def basket_analysis():
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # SQL query to retrieve transactions
#     query = """
#         SELECT t.basket_num, t.product_num
#         FROM [500_transactions] t
#         JOIN [500_products] p ON t.product_num = p.product_num
#     """
#     cursor.execute(query)
#     rows = cursor.fetchall()

#     transactions = {}
#     for row in rows:
#         basket_num, product_num = row
#         if basket_num not in transactions:
#             transactions[basket_num] = []
#         transactions[basket_num].append(product_num)

#     cursor.close()
#     conn.close()

#     # Convert the transactions into a format suitable for apriori
#     te = TransactionEncoder()
#     te_ary = te.fit(transactions.values()).transform(transactions.values())
#     df = pd.DataFrame(te_ary, columns=te.columns_)

#     print("Df",df)

#     # Apply Apriori Algorithm to get frequent itemsets
#     frequent_itemsets = apriori(df, min_support=0.0001, use_colnames=True)

#     print("frequent datasets", frequent_itemsets)
#     # Generate association rules from frequent itemsets
#     # rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1, num_itemsets=10)
#     if not frequent_itemsets.empty:
#         rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
#     else:
#         rules = pd.DataFrame() 
#     # Return the rules as a JSON response
#     return jsonify(rules.to_dict(orient="records"))

@app.route("/dashboard/basket_analysis", methods=["GET"])
def basket_analysis():
    # Step 1: Query transaction data
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT t.basket_num, t.product_num, p.department, p.commodity, p.brand_ty, p.natural_organic_flag, t.spend
        FROM [500_transactions] t
        JOIN [500_products] p ON t.product_num = p.product_num
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    # Step 2: Prepare the data for supervised learning
    data = []
    for row in rows:
        basket_num = row[0]
        product_num = row[1]
        department = row[2]
        commodity = row[3]
        brand_ty = row[4]
        natural_organic_flag = row[5]
        spend = row[6]

        data.append([basket_num, product_num, department, commodity, brand_ty, natural_organic_flag, spend])

    df = pd.DataFrame(data, columns=['basket_num', 'product_num', 'department', 'commodity', 'brand_ty', 'natural_organic_flag', 'spend'])

    # Step 3: One-hot encode categorical columns
    df = pd.get_dummies(df, columns=['department', 'commodity', 'brand_ty', 'natural_organic_flag'])

    # Group by basket_num and sum product features (each product purchase is represented as a binary feature)
    X = df.groupby('basket_num').sum()

    # Target: Total spend for each basket
    y = df.groupby('basket_num')['spend'].sum()

    # Step 4: Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 5: Train the Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Step 6: Predict and evaluate the model
    y_pred = model.predict(X_test)

    # Step 7: Calculate performance metrics (R^2 and MSE)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    return jsonify({
        "r2_score": r2,
        "mse": mse,
        "predictions": y_pred.tolist(),
        "actuals": y_test.tolist()
    })


if __name__ == "__main__":
    app.run(debug=True)

