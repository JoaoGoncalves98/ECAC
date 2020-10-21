import os
import sqlite3
import pandas as pd
from pandas import DataFrame

def create_table_train(conn, c):
    c.execute('DROP TABLE IF EXISTS ALL_LOANS_TRAIN')
    c.execute('''CREATE TABLE ALL_LOANS_TRAIN
             (loan_id INTEGER PRIMARY KEY,
             account_id integer,
             date text, 
             amount integer, 
             duration integer, 
             payments integer, 
             number_trans integer,
             avg_bal integer,
             status integer);''')
    conn.commit()

def create_table_test(conn, c):
    c.execute('DROP TABLE IF EXISTS ALL_LOANS_TEST')
    c.execute('''CREATE TABLE ALL_LOANS_TEST
             (loan_id INTEGER PRIMARY KEY,
             account_id integer,
             date text, 
             amount integer, 
             duration integer, 
             payments integer, 
             number_trans integer,
             avg_bal integer,
             status integer);''')
    conn.commit()


def queries_train(c):
    c.execute('''
    INSERT INTO ALL_LOANS_TRAIN (loan_id,account_id,date,amount,duration,payments,number_trans,avg_bal,status) 
    SELECT DISTINCT lns.loan_id, lns.account_id, lns.date, lns.amount, lns.duration, lns.payments, COUNT(TRANS_TRAIN.account_id), CAST(AVG(TRANS_TRAIN.balance) as INTEGER), lns.status
    FROM LOANS_TRAIN lns
    LEFT JOIN TRANS_TRAIN ON TRANS_TRAIN.account_id = lns.account_id
    GROUP BY TRANS_TRAIN.account_id;
    ''')

    c.execute('''
    SELECT DISTINCT *
    FROM ALL_LOANS_TRAIN
    ''')

def queries_test(c):
    c.execute('''
    INSERT INTO ALL_LOANS_TEST (loan_id,account_id,date,amount,duration,payments,number_trans,avg_bal,status) 
    SELECT DISTINCT lns.loan_id, lns.account_id, lns.date, lns.amount, lns.duration, lns.payments, COUNT(TRANS_TEST.account_id), CAST(AVG(TRANS_TEST.balance) as INTEGER), lns.status
    FROM LOANS_TEST lns
    LEFT JOIN TRANS_TEST ON TRANS_TEST.account_id = lns.account_id
    GROUP BY TRANS_TEST.account_id;
    ''')
    
    c.execute('''
    SELECT DISTINCT *
    FROM ALL_LOANS_TEST
    ''')


def convert_train():
    conn = sqlite3.connect('LoansTrain.db')  
    c = conn.cursor()
    create_table_train(conn, c)

    os.chdir('data')
    read_loans = pd.read_csv ('loan_train.csv', sep=';')
    read_loans.head()
    read_loans.to_sql('LOANS_TRAIN', conn, if_exists='append', index = False)

    read_trans = pd.read_csv ('trans_train.csv', sep=';')
    read_trans.head()
    read_trans.to_sql('TRANS_TRAIN', conn, if_exists='append', index = False)
    os.chdir('..')

    queries_train(c)

    df = DataFrame(c.fetchall(), columns=['loan_id','account_id','date','amount','duration','payments','number_trans','avg_bal','status'])
    export_csv = df.to_csv ('gerado_train.csv', index = None, header=True)


def convert_test():
    conn = sqlite3.connect('LoansTest.db')  
    c = conn.cursor()
    create_table_test(conn, c)

    os.chdir('data')
    read_loans = pd.read_csv ('loan_test.csv', sep=';')
    read_loans.head()
    read_loans.to_sql('LOANS_TEST', conn, if_exists='append', index = False)

    read_trans = pd.read_csv ('trans_test.csv', sep=';')
    read_trans.head()
    read_trans.to_sql('TRANS_TEST', conn, if_exists='append', index = False)
    os.chdir('..')


    queries_test(c)

    df = DataFrame(c.fetchall(), columns=['loan_id','account_id','date','amount','duration','payments','number_trans','avg_bal','status'])
    export_csv = df.to_csv ('gerado_test.csv', index = None, header=True)
# ___________________________________________________________________________________________________________________-


convert_train()
os.remove("LoansTrain.db")

convert_test()
os.remove("LoansTest.db")