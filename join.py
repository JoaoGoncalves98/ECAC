import os
import sqlite3
import pandas as pd
from pandas import DataFrame
from sklearn.linear_model import LinearRegression


def fill_missing_data():
    heart = pd.read_csv ('district.csv', sep=';', header=0)
    heart.head()
    train = heart[~heart['no_of_commited_crimes_95'].str.contains('\?')]
    test = heart[heart['no_of_commited_crimes_95'].str.contains('\?')]
    x_train = train[train.columns.difference(['no_of_commited_crimes_95', 'unemploymant_rate_95', 'name', 'region'])]
    y_train = train.iloc[:,14]
    x_test = test[test.columns.difference(['no_of_commited_crimes_95', 'unemploymant_rate_95', 'name', 'region'])]
    y_test = test.iloc[:,14]

    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)[0]
    dictionary = {'\?':y_pred}
    heart.replace(dictionary, regex=True, inplace=True)
    return heart

def create_table_train(conn, c):
    c.execute('DROP TABLE IF EXISTS ALL_LOANS_TRAIN')
    c.execute('''CREATE TABLE ALL_LOANS_TRAIN
             (loan_id INTEGER PRIMARY KEY,
             account_id integer,
             date date, 
             amount integer, 
             duration integer, 
             payments integer, 
             number_trans integer,
             avg_bal integer,
             min_bal integer,
             max_bal integer,
             dist_id integer,
             dist_avg_salary integer,
             dist_crimes_95 integer,
             dist_crimes_96 integer,
             client_birth_year integer,
             status integer);''')
    conn.commit()

def create_table_test(conn, c):
    c.execute('DROP TABLE IF EXISTS ALL_LOANS_TEST')
    c.execute('''CREATE TABLE ALL_LOANS_TEST
             (loan_id INTEGER PRIMARY KEY,
             account_id integer,
             date date, 
             amount integer, 
             duration integer, 
             payments integer, 
             number_trans integer,
             avg_bal integer,
             min_bal integer,
             max_bal integer,
             dist_id integer,
             dist_avg_salary integer,
             dist_crimes_95 integer,
             dist_crimes_96 integer,
             client_birth_year integer,
             status integer);''')
    conn.commit()


def queries_train(c):

    c.execute('''
    CREATE VIEW IF NOT EXISTS trans_info AS 
    SELECT TRANS_TRAIN.account_id as account_id, COUNT(TRANS_TRAIN.account_id) as number_trans, CAST(AVG(TRANS_TRAIN.balance) as INTEGER) as avg_bal, CAST(MIN(TRANS_TRAIN.balance) as INTEGER) as min_bal, CAST(MAX(TRANS_TRAIN.balance) as INTEGER) as max_bal
    FROM TRANS_TRAIN
    GROUP BY TRANS_TRAIN.account_id
    ''')

    c.execute('''
    CREATE VIEW IF NOT EXISTS district_info AS 
    SELECT acc.account_id as account_id, dist.code as dist_id, dist.average_salary as dist_avg_salary, dist.no_of_commited_crimes_95 as dist_crimes_95, dist.no_of_commited_crimes_96 as dist_crimes_96 
    FROM ACCOUNT acc, DISTRICT dist
    WHERE acc.district_id=dist.code
    ''')

    c.execute('''
    CREATE VIEW IF NOT EXISTS client_info AS 
    SELECT DISP.account_id as account_id, CAST(SUBSTR(clt.birth_number,1,2) as INTEGER) as client_birth_year
    FROM CLIENT clt, DISP
    WHERE DISP.client_id=clt.client_id and DISP.type LIKE 'OWNER'
    ''')

    c.execute('''
    INSERT INTO ALL_LOANS_TRAIN (loan_id,account_id,date,amount,duration,payments,number_trans,avg_bal,min_bal,max_bal,dist_id,dist_avg_salary,dist_crimes_95,dist_crimes_96,client_birth_year,status) 
    SELECT DISTINCT lns.loan_id, lns.account_id, lns.date, lns.amount, lns.duration, lns.payments, trs.number_trans, trs.avg_bal, trs.min_bal, trs.max_bal, dis.dist_id, dis.dist_avg_salary, dis.dist_crimes_95, dis.dist_crimes_96, cli.client_birth_year, lns.status
    FROM LOANS_TRAIN lns, trans_info trs, district_info dis, client_info cli
    WHERE lns.account_id=trs.account_id AND lns.account_id=dis.account_id AND lns.account_id=cli.account_id
    ''')

    c.execute('''
    SELECT DISTINCT *
    FROM ALL_LOANS_TRAIN
    ''')

def queries_test(c):
    c.execute('''
    CREATE VIEW trans_info AS 
    SELECT TRANS_TEST.account_id as account_id, COUNT(TRANS_TEST.account_id) as number_trans, CAST(AVG(TRANS_TEST.balance) as INTEGER) as avg_bal, CAST(MIN(TRANS_TEST.balance) as INTEGER) as min_bal, CAST(MAX(TRANS_TEST.balance) as INTEGER) as max_bal
    FROM TRANS_TEST
    GROUP BY TRANS_TEST.account_id
    ''')

    c.execute('''
    CREATE VIEW IF NOT EXISTS district_info AS 
    SELECT acc.account_id as account_id, dist.code as dist_id, dist.average_salary as dist_avg_salary, dist.no_of_commited_crimes_95 as dist_crimes_95, dist.no_of_commited_crimes_96 as dist_crimes_96 
    FROM ACCOUNT acc, DISTRICT dist
    WHERE acc.district_id=dist.code
    ''')

    c.execute('''
    CREATE VIEW IF NOT EXISTS client_info AS 
    SELECT DISP.account_id as account_id, CAST(SUBSTR(clt.birth_number,1,2) as INTEGER) as client_birth_year
    FROM CLIENT clt, DISP
    WHERE DISP.client_id=clt.client_id and DISP.type LIKE 'OWNER'
    ''')

    c.execute('''
    INSERT INTO ALL_LOANS_TEST (loan_id,account_id,date,amount,duration,payments,number_trans,avg_bal,min_bal,max_bal,dist_id,dist_avg_salary,dist_crimes_95,dist_crimes_96,client_birth_year,status) 
    SELECT DISTINCT lns.loan_id, lns.account_id, lns.date, lns.amount, lns.duration, lns.payments, trs.number_trans, trs.avg_bal, trs.min_bal, trs.max_bal, dis.dist_id, dis.dist_avg_salary, dis.dist_crimes_95, dis.dist_crimes_96, cli.client_birth_year, lns.status
    FROM LOANS_TEST lns, trans_info trs, district_info dis, client_info cli
    WHERE lns.account_id=trs.account_id AND lns.account_id=dis.account_id AND lns.account_id=cli.account_id
    ''')
    
    c.execute('''
    SELECT DISTINCT *
    FROM ALL_LOANS_TEST
    ''')


def convert_train():
    conn = sqlite3.connect('LoansTrain.db')  
    c = conn.cursor()
    create_table_train(conn, c)

    read_loans = pd.read_csv ('loan_train.csv', sep=';')
    read_loans.head()
    read_loans.to_sql('LOANS_TRAIN', conn, if_exists='append', index = False)

    read_trans = pd.read_csv ('trans_train.csv', sep=';')
    read_trans.head()
    read_trans.to_sql('TRANS_TRAIN', conn, if_exists='append', index = False)

    read_acc = pd.read_csv ('account.csv', sep=';')
    read_acc.head()
    read_acc.to_sql('ACCOUNT', conn, if_exists='append', index = False)

    read_clients = pd.read_csv ('client.csv', sep=';')
    read_clients.head()
    read_clients.to_sql('CLIENT', conn, if_exists='append', index = False)

    read_disp = pd.read_csv ('disp.csv', sep=';')
    read_disp.head()
    read_disp.to_sql('DISP', conn, if_exists='append', index = False)

    read_dist = fill_missing_data()
    read_dist.to_sql('DISTRICT', conn, if_exists='append', index = False)
    

    queries_train(c)

    df = DataFrame(c.fetchall(), columns=['loan_id','account_id','date','amount','duration','payments','number_trans','avg_bal','min_bal','max_bal','dist_id','dist_avg_salary','dist_crimes_95','dist_crimes_96','client_birth_year','status'])
    export_csv = df.to_csv ('gerado_train.csv', index = None, header=True)


def convert_test():
    conn = sqlite3.connect('LoansTest.db')  
    c = conn.cursor()
    create_table_test(conn, c)

    read_loans = pd.read_csv ('loan_test.csv', sep=';')
    read_loans.head()
    read_loans.to_sql('LOANS_TEST', conn, if_exists='append', index = False)

    read_trans = pd.read_csv ('trans_test.csv', sep=';')
    read_trans.head()
    read_trans.to_sql('TRANS_TEST', conn, if_exists='append', index = False)

    read_acc = pd.read_csv ('account.csv', sep=';')
    read_acc.head()
    read_acc.to_sql('ACCOUNT', conn, if_exists='append', index = False)

    read_clients = pd.read_csv ('client.csv', sep=';')
    read_clients.head()
    read_clients.to_sql('CLIENT', conn, if_exists='append', index = False)

    read_disp = pd.read_csv ('disp.csv', sep=';')
    read_disp.head()
    read_disp.to_sql('DISP', conn, if_exists='append', index = False)

    read_dist = fill_missing_data()
    read_dist.to_sql('DISTRICT', conn, if_exists='append', index = False)

    queries_test(c)

    df = DataFrame(c.fetchall(), columns=['loan_id','account_id','date','amount','duration','payments','number_trans','avg_bal','min_bal','max_bal','dist_id','dist_avg_salary','dist_crimes_95','dist_crimes_96','client_birth_year','status'])
    export_csv = df.to_csv ('gerado_test.csv', index = None, header=True)
# ___________________________________________________________________________________________________________________-


os.chdir('data')

convert_train()
os.remove("LoansTrain.db")

convert_test()
os.remove("LoansTest.db")