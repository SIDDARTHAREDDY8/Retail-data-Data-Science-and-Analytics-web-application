import pandas as pd
from app import db
from app.models import Transaction, Household, Product

def get_data_from_db(hshd_num):
    # Fetch data for the given hshd_num
    household_data = Household.query.filter_by(hshd_num=hshd_num).first()
    transactions = Transaction.query.filter_by(hshd_num=hshd_num).all()
    products = Product.query.all()
    
    # Convert to DataFrames for easy manipulation
    transaction_df = pd.DataFrame([t.__dict__ for t in transactions])
    household_df = pd.DataFrame([household_data.__dict__] if household_data else [])
    
    # Example: Join data (this may need to be adjusted depending on the model)
    data = pd.merge(transaction_df, household_df, on="hshd_num")
    return data.to_dict(orient='records')
