from unittest import result
import src.service as service
import unittest
import pandas as pd

dict = {'Region':['*rr(', 'Middle East and North Africa','Vietnam&', 'Europe', "'Europe"],
'Country':['Haiti', 'Nicaragua','Turkmenistan','United Kingdom','United Kingdom'],'Item Type':['Fruits','ûther','Electronics', 'Appliance','Miscellaneous'],
'Sales Channel':['Online', 'Offline', 'POS', 'Online', 'Online'],
'Order Priority':['Z','M','L','C','C'],'Order Date':['30/13/2020','12/14/2020','9/31/2017','9/7/2018','9/7/2018'],'Order ID':[112222,3333333,444444,555555,765656],
'Ship Date':['11/12/2020','11/14/2020','9/2/2017','9/7/2018','11/14/2020'],
'Units Sold':[400,910,25,1000,1000],'Unit Price':[7.9,66.9,5000,700,89],'Unit Cost':[5.5,6.6,4999,599,88.0],'Total Revenue':[5000,600.9,504.78,99.46,8.0],
'Total Cost':[5000,666,7777,3.44,5.5],'Total Profit':[34,543,665,82.3,688]}


class mytest(unittest.TestCase):

    def test_1_appendLastCharTest(self):
        result = service.appendLastChar('T', 2363210)
        self.assertEqual(result, 'T2363210H')
        result = service.appendLastChar('G', 1081324)
        self.assertEqual(result, 'G1081324M')
        result = service.appendLastChar('F', 7203999)
        self.assertEqual(result, 'F7203999T')
        result = service.appendLastChar('S', 9319325)
        self.assertEqual(result, 'S9319325C')


    def test_2_validateDF(self):
        df = pd.DataFrame(dict)
        result = service.validateDF(df)
        self.assertEqual(result['Region'].iloc[1], 'Europe')
        self.assertEqual(len(result), 2)

    def test_3_validateDate(self):
        df = pd.DataFrame(dict['Order Date'], columns=['Order Date'])
        result = service.dropEmptyData(service.validateDate(['Order Date'], df))
        self.assertEqual(len(result), 3)

    def test_4_validateFloat(self):
        df = pd.DataFrame(dict['Unit Cost'], columns=['Unit Cost'])
        result = service.dropEmptyData(service.validateNumbers(['Unit Cost'], df, "^[0-9.]+$"))
        self.assertEqual(len(result), 5)
        df = pd.DataFrame([3,4,5,6], columns=['Unit Cost'])
        result = service.dropEmptyData(service.validateNumbers(['Unit Cost'], df, "^[0-9.]+$"))
        self.assertEqual(len(result), 4)
    
    def test_5_validateFloat(self):
        df = pd.DataFrame(dict['Units Sold'], columns=['Units Sold'])
        result = service.dropEmptyData(service.validateNumbers(['Units Sold'], df, "^[0-9]+$"))
        self.assertEqual(len(result), 5)
        df = pd.DataFrame([3.7,4,5,6], columns=['Unit Cost'])
        result = service.dropEmptyData(service.validateNumbers(['Unit Cost'], df, "^[0-9]+$"))
        self.assertEqual(len(result), 0)

    def test_6_sales_cahnnel(self):
        df = pd.DataFrame(dict['Sales Channel'], columns=['Sales Channel'])
        result = df.loc[df['Sales Channel'].isin(['Online','Offline'])]
        self.assertTrue((result['Sales Channel'].iloc[2] == 'Online') | (result['Sales Channel'].iloc[2] == 'Offline'))

    def test_7_sales_cahnnel(self):
        df = pd.DataFrame(dict['Order Priority'], columns=['Order Priority'])
        result = df.loc[df['Order Priority'].isin(['M','L', 'C', 'H'])]
        self.assertTrue((result['Order Priority'].iloc[0] == 'M' ) | (result['Order Priority'].iloc[0] == 'L') | (result['Order Priority'].iloc[0] == 'C') | (result['Order Priority'].iloc[0] == 'H'))

if __name__=='__main__':
    unittest.main()