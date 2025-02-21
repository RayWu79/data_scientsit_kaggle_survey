import pandas as pd
import sqlite3

connection = sqlite3.connect("data/kaggle_survey.db")
sql_query = """
SELECT surveyed_in,
       question_type,
       response,
       response_count
  FROM aggregated_responses
 WHERE (question_index = 'Q29A' AND surveyed_in = 2020)
    OR (question_index = 'Q32A' AND surveyed_in = 2021)
    OR (question_index = 'Q35' AND surveyed_in = 2022)
 ORDER BY surveyed_in,
          response_count DESC;
"""
response_counts = pd.read_sql(sql_query, con=connection)
connection.close()
print(response_counts)