# from app import app
# import pyodbc
# from flask import jsonify, request

# # Database connection string (for pyodbc)
# def get_db_connection():
#     connection_string = (
#         f'DRIVER={{ODBC Driver 18 for SQL Server}};'
#         f'SERVER={DB_SERVER},1433;'
#         f'DATABASE={DB_DATABASE};'
#         f'UID={DB_USERNAME};'
#         f'PWD={DB_PASSWORD};'
#         f'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
#     )
#     conn = pyodbc.connect(connection_string)
#     return conn


# # Root endpoint for testing
# @app.route("/", methods=["GET"])
# def root():
#     return "Flask API for Household, Transaction, Product"


# # Endpoint to retrieve all households (using pyodbc)
# @app.route("/households", methods=["GET"])
# def get_households():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM households")
#     rows = cursor.fetchall()
    
#     result = [{"hshd_num": row[0], "loyalty": row[1], "age_range": row[2], 
#                "income_range": row[3], "marital_status": row[4], "homeowner": row[5],
#                "hshd_composition": row[6], "hshd_size": row[7], "children": row[8]} 
#               for row in rows]
    
#     cursor.close()
#     conn.close()
    
#     return jsonify(result)


# # Endpoint to retrieve a specific household by hshd_num
# @app.route("/household/<int:hshd_num>", methods=["GET"])
# def get_household(hshd_num):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM households WHERE hshd_num = ?", (hshd_num,))
#     row = cursor.fetchone()
    
#     if row:
#         result = {
#             "hshd_num": row[0], "loyalty": row[1], "age_range": row[2], 
#             "income_range": row[3], "marital_status": row[4], "homeowner": row[5],
#             "hshd_composition": row[6], "hshd_size": row[7], "children": row[8]
#         }
#     else:
#         result = {"message": "Household not found"}
    
#     cursor.close()
#     conn.close()
    
#     return jsonify(result)


# # Endpoint to retrieve all transactions (using pyodbc)
# @app.route("/transactions", methods=["GET"])
# def get_transactions():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM transactions")
#     rows = cursor.fetchall()
    
#     result = [{"basket_num": row[0], "hshd_num": row[1], "date": row[2], 
#                "spend": row[3], "units": row[4], "store": row[5], 
#                "region": row[6], "week_num": row[7], "year": row[8]} 
#               for row in rows]
    
#     cursor.close()
#     conn.close()
    
#     return jsonify(result)


# # Endpoint to retrieve a specific transaction by basket_num
# @app.route("/transaction/<int:basket_num>", methods=["GET"])
# def get_transaction(basket_num):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM transactions WHERE basket_num = ?", (basket_num,))
#     row = cursor.fetchone()
    
#     if row:
#         result = {
#             "basket_num": row[0], "hshd_num": row[1], "date": row[2], 
#             "spend": row[3], "units": row[4], "store": row[5], 
#             "region": row[6], "week_num": row[7], "year": row[8]
#         }
#     else:
#         result = {"message": "Transaction not found"}
    
#     cursor.close()
#     conn.close()
    
#     return jsonify(result)


# # Endpoint to retrieve all products (using pyodbc)
# @app.route("/products", methods=["GET"])
# def get_products():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM products")
#     rows = cursor.fetchall()
    
#     result = [{"product_num": row[0], "department": row[1], "commodity": row[2],
#                "brand_type": row[3], "natural_organic_flag": row[4]} 
#               for row in rows]
    
#     cursor.close()
#     conn.close()
    
#     return jsonify(result)


# # Endpoint to retrieve a specific product by product_num
# @app.route("/product/<int:product_num>", methods=["GET"])
# def get_product(product_num):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM products WHERE product_num = ?", (product_num,))
#     row = cursor.fetchone()
    
#     if row:
#         result = {
#             "product_num": row[0], "department": row[1], "commodity": row[2],
#             "brand_type": row[3], "natural_organic_flag": row[4]
#         }
#     else:
#         result = {"message": "Product not found"}
    
#     cursor.close()
#     conn.close()
    
#     return jsonify(result)


# # Endpoint to create a new household (using pyodbc)
# @app.route("/household", methods=["POST"])
# def create_household():
#     data = request.get_json()
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute(
#         "INSERT INTO households (loyalty, age_range, income_range, marital_status, homeowner, hshd_composition, hshd_size, children) "
#         "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#         (data["loyalty"], data["age_range"], data["income_range"], data["marital_status"], 
#          data["homeowner"], data["hshd_composition"], data["hshd_size"], data["children"])
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return jsonify({"message": "Household created"}), 201


# # Endpoint to create a new transaction (using pyodbc)
# @app.route("/transaction", methods=["POST"])
# def create_transaction():
#     data = request.get_json()
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute(
#         "INSERT INTO transactions (hshd_num, date, spend, units, store, region, week_num, year) "
#         "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#         (data["hshd_num"], data["date"], data["spend"], data["units"], data["store"], 
#          data["region"], data["week_num"], data["year"])
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return jsonify({"message": "Transaction created"}), 201


# # Endpoint to create a new product (using pyodbc)
# @app.route("/product", methods=["POST"])
# def create_product():
#     data = request.get_json()
#     conn = get_db_connection()
#     cursor = conn.cursor()
    
#     cursor.execute(
#         "INSERT INTO products (department, commodity, brand_type, natural_organic_flag) "
#         "VALUES (?, ?, ?, ?)",
#         (data["department"], data["commodity"], data["brand_type"], data["natural_organic_flag"])
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return jsonify({"message": "Product created"}), 201



from app import app
import pyodbc
from flask import jsonify, request
from datetime import datetime
from app.models import Household, Transaction, Product

# Database connection string (using the variables defined in the previous step)
def get_db_connection():
    connection_string = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={DB_SERVER},1433;'  # Add the port (1433 is default for SQL Server)
        f'DATABASE={DB_DATABASE};'
        f'UID={DB_USERNAME};'
        f'PWD={DB_PASSWORD};'
        f'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    )
    conn = pyodbc.connect(connection_string)
    return conn


# Root endpoint for testing
@app.route("/", methods=["GET"])
def root():
    return "Flask API for Household, Transaction, Product"

@app.route("/data", methods=["GET"])
def get_data():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to fetch the first 10 rows from the 500_households table
    cursor.execute("SELECT TOP 10 * FROM 500_households")
    rows = cursor.fetchall()

    # Prepare the response data
    result = [{
        "hshd_num": row[0], 
        "l": row[1], 
        "age_range": row[2],
        "income_range": row[3], 
        "marital": row[4], 
        "homeowner": row[5],
        "hshd_composition": row[6], 
        "hh_size": row[7], 
        "children": row[8]
    } for row in rows]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Return the data as JSON
    return jsonify(result)

# Endpoint to retrieve specific data (e.g., Household) with limit and offset
@app.route("/data/<int:id>", methods=["GET"])
def get_data_by_id(id):
    # Extract limit and offset from query parameters
    # limit = request.args.get('limit', default=10, type=int)
    # offset = request.args.get('offset', default=0, type=int)

    # Example of querying the database with `id`, `limit`, and `offset`
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to fetch the record by ID (you can adjust this as per your needs)
    # cursor.execute(f"SELECT * FROM 500_households WHERE hshd_num = {id} LIMIT {limit} OFFSET {offset}")
    cursor.execute(f"SELECT * FROM 500_households WHERE hshd_num = {id}")

    rows = cursor.fetchall()

    result = [{"hshd_num": row[0], "l": row[1], "age_range": row[2], 
               "income_range": row[3], "marital": row[4], "homeowner": row[5],
               "hshd_composition": row[6], "hh_size": row[7], "children": row[8]} 
              for row in rows]

    cursor.close()
    conn.close()

    return jsonify(result)



# Endpoint to retrieve all households
@app.route("/households", methods=["GET"])
def get_households():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 500_households")
    rows = cursor.fetchall()
    
    result = [{"hshd_num": row[0], "l": row[1], "age_range": row[2], 
               "income_range": row[3], "marital": row[4], "homeowner": row[5],
               "hshd_composition": row[6], "hh_size": row[7], "children": row[8]} 
              for row in rows]
    
    cursor.close()
    conn.close()
    
    return jsonify(result)


# Endpoint to retrieve a specific household by hshd_num
@app.route("/household/<int:hshd_num>", methods=["GET"])
def get_household(hshd_num):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [500_households] WHERE hshd_num = ?", (hshd_num,))
    row = cursor.fetchone()
    print("household", row)
    if row:
        result = {
            "hshd_num": row[0], "l": row[1], "age_range": row[2], 
            "income_range": row[3], "marital": row[4], "homeowner": row[5],
            "hshd_composition": row[6], "hh_size": row[7], "children": row[8]
        }
    else:
        result = {"message": "Household not found"}
    
    cursor.close()
    conn.close()
    
    return jsonify(result)


# Endpoint to retrieve all transactions
@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 500_transactions")
    rows = cursor.fetchall()
    
    result = [{"product_num": row[0], "basket_num": row[1], "hshd_num": row[2], 
               "purchase": row[3], "spend": row[4], "units": row[5], 
               "store_r": row[6], "week_num": row[7], "year": row[8]} 
              for row in rows]
    
    cursor.close()
    conn.close()
    
    return jsonify(result)


# Endpoint to retrieve a specific transaction by basket_num
@app.route("/transaction/<int:basket_num>", methods=["GET"])
def get_transaction(basket_num):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 500_transactions WHERE basket_num = ?", (basket_num,))
    row = cursor.fetchone()
    
    if row:
        result = {
            "product_num": row[0], "basket_num": row[1], "hshd_num": row[2], 
            "purchase": row[3], "spend": row[4], "units": row[5], 
            "store_r": row[6], "week_num": row[7], "year": row[8]
        }
    else:
        result = {"message": "Transaction not found"}
    
    cursor.close()
    conn.close()
    
    return jsonify(result)


# Endpoint to retrieve all products
@app.route("/products", methods=["GET"])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 500_products")
    rows = cursor.fetchall()
    
    result = [{"product_num": row[0], "department": row[1], "commodity": row[2],
               "brand_ty": row[3], "natural_organic_flag": row[4]} 
              for row in rows]
    
    cursor.close()
    conn.close()
    
    return jsonify(result)


# Endpoint to retrieve a specific product by product_num
@app.route("/product/<int:product_num>", methods=["GET"])
def get_product(product_num):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM 500_products WHERE product_num = ?", (product_num,))
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


# Endpoint to create a new household
@app.route("/household", methods=["POST"])
def create_household():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO 500_households (l, age_range, income_range, marital, homeowner, hshd_composition, hh_size, children) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (data["l"], data["age_range"], data["income_range"], data["marital"], 
         data["homeowner"], data["hshd_composition"], data["hh_size"], data["children"])
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Household created"}), 201
