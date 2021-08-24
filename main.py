from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy
import src.service as service
import pandas as pd


app = Flask(__name__)
# enable debugging mode
app.config["DEBUG"] = True

UPLOAD_FOLDER = 'file'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
app.config['UPLOAD_FILE'] =  'orders.csv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:my_password@orders_db_1/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
  

# Root URL
@app.route('/')
def index():
    db.create_all()  
    return render_template('index.html')


@app.route('/display', methods=['GET'])
def display():
     return render_template('display.html', data=getData())


@app.route('/error', methods=['GET'])
def error(message):
     return render_template('error.html', data=message)


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get uploaded file
      uploaded_file = request.files['file']
      app.logger.info('Received file')
      if (uploaded_file.filename != '') & (uploaded_file.filename.endswith('.csv')) :
           file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FILE'])
           uploaded_file.save(file_path)
           #Parse file
           parseCSV(file_path)
      else:
        return error('Wrong file extention. Please upload a .csv file')
      return redirect(url_for('display'))


class OrderItems(db.Model):
    __tablename__ = 'order_items'
    region = db.Column('region', db.Text)
    country = db.Column('country', db.Text)
    itemType = db.Column('item_type', db.Text)
    salesChannel = db.Column('sales_channel', db.Text)
    orderPriority = db.Column('order_priority', db.Text)
    orderDate = db.Column('order_date', db.Date)
    orderId = db.Column('order_id', db.Integer, primary_key=True)
    shipDate = db.Column('ship_date', db.Date)
    unitsSold = db.Column('units_sold', db.Integer)
    unitPrice = db.Column('unit_price', db.Float)
    unitCost = db.Column('unit_cost', db.Float)
    totalRevenue = db.Column('total_revenue', db.Float)
    totalCost = db.Column('total_cost', db.Float)
    totalProfit = db.Column('total_profit', db.Float)
    nric = db.Column('nric', db.Text)


def parseCSV(filePath):
      app.logger.info('Start parsing')
      # CVS Column Names
      col_names = ['Region','Country','Item Type','Sales Channel','Order Priority','Order Date','Order ID','Ship Date','Units Sold','Unit Price','Unit Cost','Total Revenue','Total Cost','Total Profit']
      data_types = {'Region':str,'Country':str,'Item Type':str,'Sales Channel':str,'Order Priority':str,'Order Date':str,'Order ID':int,'Ship Date':str,'Units Sold':int,'Unit Price':float,'Unit Cost':float,'Total Revenue':float,'Total Cost':float,'Total Profit':float}
      # Parse file with pandas
      csvData = pd.read_csv(filePath,names=col_names, header=None, skiprows=1, dtype=data_types)
      app.logger.info('Start Validation')
      csvData = service.validateDF(csvData)
      app.logger.info('Validation Completed')
      #deleting data before inserting data from new file
      OrderItems.query.delete()
      app.logger.info('Generate nric')
      order_items_array = []
      for i,row in csvData.iterrows():
            #print(i,row['Region'],row['Country'],row['Item Type'],row['Sales Channel'],row['Order Priority'],row['Order Date'],
            #row['Order ID'],row['Ship Date'],row['Units Sold'],row['Unit Price'],row['Unit Cost'],row['Total Revenue'],row['Total Cost'],row['Total Profit'],)
            new_order_item = OrderItems(
                    region = row['Region'],
                    country = row['Country'],
                    itemType = row['Item Type'],
                    salesChannel = row['Sales Channel'],
                    orderPriority = row['Order Priority'],
                    orderDate = row['Order Date'],
                    orderId = row['Order ID'],
                    shipDate = row['Ship Date'],
                    unitsSold = row['Units Sold'],
                    unitPrice = row['Unit Price'],
                    unitCost = row['Unit Cost'],
                    totalRevenue = row['Total Revenue'],
                    totalCost = row['Total Cost'],
                    totalProfit = row['Total Profit'],
                    nric = service.get_random_nric()
                )
            order_items_array.append(new_order_item)
      app.logger.info('Data Ready for insertion')
      db.session.add_all(order_items_array)
      app.logger.info('Data Inserted')
      db.session.commit()
      app.logger.info('DB Commit done')


def getData():
    ROWS_PER_PAGE = 8
    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    app.logger.info('Start Fetching records')
    orders = OrderItems.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    app.logger.info('Records Fetched')
    return orders


if (__name__ == "__main__"):
     app.run(port = 5000, host='0.0.0.0')