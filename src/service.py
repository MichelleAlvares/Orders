from random import randint
import pandas as pd
import random

multipliers = {0:2, 1:7, 2:6, 3:5, 4:4, 5:3, 6:2}
singaporean = {0:'J', 1:'Z', 2:'I', 3:'H', 4:'G', 5:'F', 6:'E', 7:'D', 8:'C', 9:'B', 10:'A'}
foreigner = {0:'X', 1:'W', 2:'U', 3:'T', 4:'R', 5:'Q', 6:'P', 7:'N', 8:'M', 9:'L', 10:'K'}
onlyLetters = "^[^-\s*#!ˆ()@$%_,./\'\\\][a-zA-Z\'\s-]+$"
floatCheck = "^[0-9.]+$"
integerCheck = "^[0-9]+$"
orderPriorityList = ['M', 'H', 'L', 'C']
salesChannels = ['Online', 'Offline']
stringCols = ['Region','Country']
dateCols = ['Order Date','Ship Date']
floatCols = ['Unit Price','Unit Cost','Total Revenue','Total Cost','Total Profit']
intCols = ['Order ID','Units Sold']

def validateDF(df):
    df = dropEmptyData(df)
    df = validateStrings(stringCols, df)
    df = validateDate(dateCols, df)
    df = validateNumbers(floatCols, df, floatCheck)
    df = validateNumbers(intCols, df, integerCheck)
    df = df.loc[df['Sales Channel'].isin(salesChannels)]
    df = df.loc[df['Order Priority'].isin(orderPriorityList)]
    return dropEmptyData(df)


def dropEmptyData(df):
    return df.dropna(axis=0, how="any", thresh=None, subset=None, inplace=False)

def validateStrings(cols, df):
    for col in cols:
        df = df.loc[df[col].str.contains(onlyLetters)]
    return df

def validateDate(cols, df):
    for col in cols:
        df[col] = pd.to_datetime(df[col], errors='coerce', format="%m/%d/%Y")
    return df

def validateNumbers(cols, df, exp):
    for col in cols:
        df = df.loc[df[col].astype(str).str.contains(exp)]
    return df

def get_random_nric():
    return appendLastChar(random.choice('STFG'), str(random_number()))


def random_number():
    start = 10**(7-1)
    end = (10**7)-1
    return randint(start, end)


def appendLastChar(firstLetter, num):
    sum = 0
    remainder = 0
    for i in range (len(str(num))):
        sum += multipliers.get(i) * int(str(num)[i])
    if firstLetter in ['T', 'G']:
        sum += 4

    remainder = sum % 11

    if firstLetter in ['F', 'G']:
        return firstLetter + str(num) + foreigner.get(remainder)
    else:
        return firstLetter + str(num) + singaporean.get(remainder)