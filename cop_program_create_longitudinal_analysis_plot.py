import pandas as pd
import sqlite3

connection = sqlite3.connect("data/kaggle_survey.db")
sql_query = """
SELECT surveyed_in,
       question_type,
       response,
       response_count
  FROM aggregated_responses
 WHERE (question_index = 'Q7' AND surveyed_in IN (2020, 2021))
    OR (question_index = 'Q12' AND surveyed_in = 2022)
 ORDER BY surveyed_in,
          response_count DESC;
"""
response_counts = pd.read_sql(sql_query, con=connection)
connection.close()
print(response_counts)
print(response_counts.shape)