import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(
  os.path.dirname(os.path.abspath(__file__)),
  'database',
  'customer_history.db'
)

def init_database():
  os.makedirs(os.path.dirname(DB_PATH),
  exist_ok=True)
  conn = sqlite3.connect(DB_PATH)
  c = conn.cursor()

  c.execute('''CREATE TABLE IF NOT EXISTS
  customers(
  customer_id TEXT PRIMARY KEY, name TEXT, phone TEXT, email TEXT,
  created_date TEXT, last_updated TEXT, aon REAL, avg_arpu REAL, is_high_value INTEGER, is_roaming INTEGER, notes TEXT)''')


  c.execute('''CREATE TABLE IF NOT EXISTS predictions(
  pred_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id TEXT, prediction_date TEXT, churn_probability REAL, risk_level TEXT,
  arpu_6 REAL, arpu_7 REAL, arpu_8 REAL, og_6 REAL, og_7 REAL, og_8 REAL, ic_6 REAL, ic_7 REAL, ic_8 REAL,
  reach_6 REAL, rech_7 REAL, reach_8 REAL, rnum_6 REAL, rnum_7 REAL, rnum_8 REAL, top_reason TEXT )''')

  c.execute('''CREATE TABLE IF NOT EXISTS offers(
  offer_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id TEXT, pred_id INTEGER,
  offer_date TEXT, offer_type TEXT, offer_details TEXT, action_taken TEXT,
  timeline TEXT, offered_by TEXT)''')

  c.execute('''CREATE TABLE IF NOT EXISTS outcomes(outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id TEXT, offer_id INTEGER, outcome_date TEXT, customer_response TEXT, offer_accepted INTEGER,
  churn_risk_reduced INTEGER, customer_active INTEGER, follow_prob REAL,
  notes TEXT)''')

  conn.commit()
  conn.close()

def add_customer(customer_id, name="", phone="", email="", aon=0, avg_rpu=0, is_high_value=0, is_roaming=0, notes=""):
  conn = sqlite3.connect(DB_PATH)
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  conn.cursor().execute(
    '''INSERT OR REPLACE INTO customers VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
    (customer_id, name, phone, email, now, aon, avg_arpu, is_high_value, is_roaming, notes))
  conn.commit()
  conn.close()

def save_prediction(customer_id,probability,risk_level,data,top_reason=""):
  conn = sqlite3.connect(DB_PATH)
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  c = conn.cursor()
  c.execute('''INSERT INTO predictions(customer_id, prediction_date, churn_probability,
  risk_level, arpu_6, arpu_7, arpu_8, og_6, og_7, og_8, ic_6, ic_7, ic_8,
  reach_6, rech_7, reach_8, rnum_6, rnum_7, rnum_8, top_reason)VALUES(?,?,?)''',
  (customer_id, now, probability, risk_level, data.get('arpu_6',0),
  data.get('arpu_7, 0'), data.get('arpu_8', 0),data.get('total_og_mou_6',0), data.get('total_og_mou_7', 0),
  data.get('total_og_mou_8',0), data.get('total_ic_mou_6',0), data.get('total_ic_mou_7',0), data.get('total_ic_mou_8',0),
  data.get('total_rech_amt_6',0), data.get('total_rech_amt_7',0), data.get('total_rech_amt_8',0), top_reason))

  pred_id = c.lastrowid
  conn.commit()
  conn.close()
  return pred_id

def save_offer(customer_id, pred_id, offer_type, offer_details, action_taken, timeline, offered_by="System"):
  conn = sqlite3.connect(DB_PATH)
  now= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  c=conn.cursor()
  c.execute('''INSERT INTO offers(customer_id, pred_id,
  offer_date, offer_type, offer_details, action_taken,
  timeline, offered_by)VALUES(???????)''',
  (customer_id, pred_id, now, offer_type, offer_details, action_taken, timeline, offered_by))

  offer_id= c. lastrowid
  conn.commit()
  conn.close()
  return offer_id

def save_coutcome(customer_id, offer_id, customer_response, offer_accepted, churn_risk_reduced, customer_active, follow_prob=None, notes=""):
  conn = sqlite3.connect(DB_PATH)
  now = datetime.noe().strftime("%Y-%m-%d %H:%M:%S")
  conn.cursor().execute(
    '''INSERT INTO outcomes(customer_id, offer_id, outcome_date, customer_response, offer_accepted,
  churn_risk_reduced, customer_active, follow_prob, notes)VALUES(?????????)''',
  (customer_id, offer_id, now, customer_response, offer_accepted, churn_risk_reduced, customer_active, follow_prob, notes))

  conn.commit()
  conn.close()

  def get_customer_history(customer_id):
    conn = sqlite3.connect(DB_PATH)
    data = {
      'customer': pd.read_sql_query(
        "SELECT * FROM customers where customer_id=?",
        conn, params=(customer_id,)),
      'predictions': pd.read_sql_query(
        "select * from predictions  where customer_id=? order by prediction_data DESC",
        conn, params=(customer_id,)),
      'offers': pd.read_sql_query("select * from offers where customer_id=? order by offer_date DESC",
      conn, params=(customer_id,)),
      'outcomes': pd.read_sql_query(
        "select * from ooutcomes where customer_id=? order by outcome_date DESC",
        conn, params=(customer_id,))
}    
    conn.close()
    return data 