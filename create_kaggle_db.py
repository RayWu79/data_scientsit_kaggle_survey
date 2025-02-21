import pandas as pd
import string
import sqlite3

class CreateKaggleDB():
    def __init__(self):
        self.survey_years = [2020, 2021, 2022]
        self.df_dict = dict()

        for survey_year in self.survey_years:
            file_path = f"data/kaggle_survey_{survey_year}_responses.csv"
            df = pd.read_csv(file_path, low_memory=False, skiprows=[1])
            df = df.iloc[:, 1:]
            self.df_dict[survey_year, "responses"] = df
            df = pd.read_csv(file_path, nrows=1)
            questions_descriptions = df.values.ravel() # make One-dimensional array
            questions_descriptions = questions_descriptions[1:]
            self.df_dict[survey_year, "question_descriptions"] = questions_descriptions

    def tidy_2020_2021(self, survey_year: int) -> tuple:
        question_indexes, question_types, question_descriptions = [], [], []
        column_names = self.df_dict[survey_year, "responses"].columns
        descriptions = self.df_dict[survey_year, "question_descriptions"]
        for column_name, description in zip(column_names, descriptions):
            column_name_split = column_name.split("_")
            description_split = description.split(" - ")
            if len(column_name_split) == 1:
                question_index = column_name_split[0]
                question_indexes.append(question_index)
                question_types.append("Multiple choice")
                question_descriptions.append(description_split[0])
            else:
                if column_name_split[1] in string.ascii_uppercase:
                    question_index = column_name_split[0] + column_name_split[1]
                    question_indexes.append(question_index)
                else:
                    question_index = column_name_split[0]
                    question_indexes.append(question_index)
                question_types.append("Multiple selection")
                question_descriptions.append(description_split[0])

        question_df = pd.DataFrame()
        question_df["question_index"] = question_indexes
        question_df["question_type"] = question_types
        question_df["question_description"] = question_descriptions
        question_df["surveyed_in"] = survey_year
        question_df = question_df.groupby(["question_index", "question_type", "question_description", "surveyed_in"]).count().reset_index()

        response_df = self.df_dict[survey_year, "responses"]
        response_df.columns = question_indexes
        response_df_reset_index = response_df.reset_index()
        response_df_melted = pd.melt(response_df_reset_index, id_vars="index", var_name="question_index")

        response_df_melted["responded_in"] = survey_year
        response_df_melted = response_df_melted.rename(columns={"index":"respondent_id"})
        response_df_melted = response_df_melted.rename(columns={"value": "response"})
        response_df_melted = response_df_melted.dropna().reset_index(drop=True)
        return question_df, response_df_melted

    def tidy_2022(self, survey_year: int) -> tuple:
        question_indexes, question_types, question_descriptions = [], [], []
        column_names = self.df_dict[survey_year, "responses"].columns
        descriptions = self.df_dict[survey_year, "question_descriptions"]
        for column_name, description in zip(column_names, descriptions):
            column_name_split = column_name.split("_")
            description_split = description.split(" - ")
            if len(column_name_split) == 1:
                question_types.append("Multiple choice")
            else:
                question_types.append("Multiple selection")
            question_indexes.append(column_name_split[0])
            question_descriptions.append(description_split[0])

        question_df = pd.DataFrame()
        question_df["question_index"] = question_indexes
        question_df["question_type"] = question_types
        question_df["question_description"] = question_descriptions
        question_df["surveyed_in"] = survey_year
        question_df = question_df.groupby(["question_index", "question_type", "question_description", "surveyed_in"]).count().reset_index()

        response_df = self.df_dict[survey_year, "responses"]
        response_df.columns = question_indexes
        response_df_reset_index = response_df.reset_index()
        response_df_melted = pd.melt(response_df_reset_index, id_vars="index", var_name="question_index")
        response_df_melted["responded_in"] = survey_year
        response_df_melted = response_df_melted.rename(columns={"index":"respondent_id"})
        response_df_melted = response_df_melted.rename(columns={"value": "response"})
        response_df_melted = response_df_melted.dropna().reset_index(drop=True)
        return question_df, response_df_melted
    
    def create_database(self):
        question_df = pd.DataFrame()
        response_df = pd.DataFrame()
        for survey_year in self.survey_years:
            if survey_year == 2022:
                q_df, r_df = self.tidy_2022(survey_year)
            else:
                q_df, r_df = self.tidy_2020_2021(survey_year)
            question_df = pd.concat([question_df, q_df], ignore_index=True)
            response_df = pd.concat([response_df, r_df], ignore_index=True)
        connection = sqlite3.connect("data/kaggle_survey.db")
        question_df.to_sql("questions", con=connection, if_exists="replace", index=False)
        response_df.to_sql("responses", con=connection, if_exists="replace", index=False)
        cur = connection.cursor()
        drop_view_sql = """DROP VIEW IF EXISTS aggregated_responses"""
        create_view_sql = """
        CREATE VIEW aggregated_responses AS
        SELECT questions.surveyed_in,
               questions.question_index,
               questions.question_type,
               questions.question_description,
               responses.response,
               COUNT(responses.respondent_id) AS response_count
          FROM questions
          JOIN responses
            ON questions.question_index = responses.question_index
           AND questions.surveyed_in = responses.responded_in
         GROUP BY questions.surveyed_in,
                  questions.question_index,
                  responses.response;
        """
        cur.execute(drop_view_sql)
        cur.execute(create_view_sql)
        connection.close()
create_kaggle_survey_db = CreateKaggleDB()
create_kaggle_survey_db.create_database()