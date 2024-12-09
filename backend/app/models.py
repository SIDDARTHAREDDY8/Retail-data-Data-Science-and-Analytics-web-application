from app import db

class Household(db.Model):
    __tablename__ = '500_households'
    hshd_num = db.Column(db.Integer, primary_key=True)
    l = db.Column(db.String(50))
    age_range = db.Column(db.String(50))
    income_range = db.Column(db.String(50))
    marital = db.Column(db.String(50))
    homeowner = db.Column(db.String(50))
    hshd_composition = db.Column(db.String(50))
    hh_size = db.Column(db.Integer)
    children = db.Column(db.Integer)

    def __repr__(self):
        return f"<Household {self.hshd_num}>"

class Transaction(db.Model):
    __tablename__ = '500_transactions'
    product_num = db.Column(db.Integer, primary_key=True)
    basket_num = db.Column(db.Integer)
    hshd_num = db.Column(db.Integer, db.ForeignKey('500_households.hshd_num'))
    purchase = db.Column(db.Date)
    spend = db.Column(db.Float)
    units = db.Column(db.Integer)
    store_r = db.Column(db.String(50))
    # region = db.Column(db.String(50))
    week_num = db.Column(db.Integer)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"<Transaction {self.basket_num}>"

class Product(db.Model):
    __tablename__ = '500_products'
    product_num = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50))
    commodity = db.Column(db.String(50))
    brand_ty = db.Column(db.String(50))
    natural_organic_flag = db.Column(db.String(50))

    def __repr__(self):
        return f"<Product {self.product_num}>"
