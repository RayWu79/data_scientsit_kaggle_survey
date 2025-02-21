import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# function to plot the horizontal bars of questions from kaggle survey every year
def plot_horizontal_bars(sql_query: str, fig_name: str, shareyaxis: bool=False):
    connection = sqlite3.connect("data/kaggle_survey.db")
    response_counts = pd.read_sql(sql_query, con=connection)
    connection.close()
    fig, ax = plt.subplots(ncols=3, figsize=(32, 8), sharey=shareyaxis)
    survey_years = [2020, 2021, 2022]
    for i in range(len(survey_years)):
        survey_year = survey_years[i]
        response_counts_year = response_counts[response_counts["surveyed_in"] == survey_year]
        y = response_counts_year["response"].values
        width = response_counts_year["response_count"].values
        ax[i].barh(y, width)
        ax[i].set_title(f"{survey_year}")
    plt.tight_layout()
    fig.savefig(f"{fig_name}.png")

# Select any activities that make up an important part of your role at work:
sql_query_activaties = """
SELECT surveyed_in,
       question_type,
       response,
       response_count
  FROM aggregated_responses
 WHERE (question_index = 'Q23' AND surveyed_in = 2020)
    OR (question_index = 'Q24' AND surveyed_in = 2021)
    OR (question_index = 'Q28' AND surveyed_in = 2022)
 ORDER BY surveyed_in,
          response_count;
"""

# Which of the following ML algorithms do you use on a regular basis? 
sql_query_algorithms = """
SELECT surveyed_in,
       question_type,
       response,
       response_count
  FROM aggregated_responses
 WHERE (question_index = 'Q17' AND surveyed_in IN (2020, 2021))
    OR (question_index = 'Q18' AND surveyed_in = 2022)
 ORDER BY surveyed_in,
          response_count;
"""

# Which of the following big data products (relational databases, data warehouses, data lakes, or similar) do you use on a regular basis? 
sql_query_big_data_products = """
SELECT surveyed_in,
       question_type,
       response,
       response_count
  FROM aggregated_responses
 WHERE (question_index = 'Q29A' AND surveyed_in = 2020)
    OR (question_index = 'Q32A' AND surveyed_in = 2021)
    OR (question_index = 'Q35' AND surveyed_in = 2022)
 ORDER BY surveyed_in,
          response_count;
"""

# What programming languages do you use on a regular basis? 
sql_query_programming_languages = """
SELECT surveyed_in,
       question_type,
       response,
       response_count
  FROM aggregated_responses
 WHERE (question_index = 'Q7' AND surveyed_in IN (2020, 2021))
    OR (question_index = 'Q12' AND surveyed_in = 2022)
 ORDER BY surveyed_in,
          response_count;
"""

# Select the title most similar to your current role 
sql_query_role_titles = """
SELECT surveyed_in,
       question_type,
       response,
       response_count
  FROM aggregated_responses
 WHERE (question_index = 'Q5' AND surveyed_in IN (2020, 2021))
    OR (question_index = 'Q23' AND surveyed_in = 2022)
 ORDER BY surveyed_in,
          response_count;
"""

# What data visualization libraries or tools do you use on a regular basis?
sql_query_visualization_libraries = """
SELECT surveyed_in,
       question_type,
       response,
       response_count
  FROM aggregated_responses
 WHERE (question_index = 'Q14' AND surveyed_in IN (2020, 2021))
    OR (question_index = 'Q15' AND surveyed_in = 2022)
 ORDER BY surveyed_in,
          response_count;
"""

# Plot every questions
plot_horizontal_bars(sql_query_activaties, "data_scientist_job_activaties", shareyaxis=True)
plot_horizontal_bars(sql_query_algorithms, "data_scientist_job_ML_algorithms")
plot_horizontal_bars(sql_query_big_data_products, "data_scientist_job_big_data_products")
plot_horizontal_bars(sql_query_programming_languages, "data_scientist_job_programming_languages")
plot_horizontal_bars(sql_query_role_titles, "data_scientist_job_role_titles")
plot_horizontal_bars(sql_query_visualization_libraries, "data_scientist_job_visualization_libraries")