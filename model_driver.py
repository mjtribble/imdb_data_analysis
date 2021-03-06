"""
Created on November 14, 2017
@author: Melody Tribble & Xuying Wang

"""
import regression
import correlation
import classification
import pandas as pd
import pymysql


# This class holds all the queries and data cleaning functionality for each question.
class Query:
    def __init__(self):
        self.cursor = self.config.cursor()

    # This will execute query 1 and call the Pearson's Correlation function
    # Q1: Do the number of parts an actor works on increase, decrease or stay the same with age?
    def query_1(self):

        # grabs the name, title, release date, and birth year, with a limit of 3000 records.
        query1 = ("SELECT  Name, Primary_title, Release_date, Birth_year "
                  "FROM TEMP_DirectorActor, TITLE, PERSON "
                  "WHERE Movie_title = Primary_title "
                  "AND Actor1_name = Name "
                  "AND NOT Actor1_name = '' "
                  "AND NOT Movie_title = '' "
                  "AND NOT Release_date = '' "
                  "AND NOT Release_date = '\\N' "
                  "AND NOT Birth_year= '' "
                  "AND NOT Birth_year= '\\N' "
                  "LIMIT 3000 ")

        # Run the query
        self.cursor.execute(query1)

        # This will hold the query results
        query1_dict = {}

        # Creates a dictionary where the key a person's age, and the value is count of roles for that age
        for (Actor1_name, Movie_title, Release_date, Birth_year) in self.cursor:
            # tries to calculate the age based on query results and count the number of roles per age.
            try:
                # calculate the age
                age = int(Release_date) - int(Birth_year)

                # remove ages 80+
                if age > 80: continue

                # if the age is already in the dictionary increment the count
                if age in query1_dict:
                    query1_dict[age] += 1

                # if the age is not already in the dictionary add a new dict. item
                else:
                    query1_dict.update({age: 1})

            # This will catch an exception if either year values cannot be converted to an int.
            except ValueError:
                continue

        # Analyse data with Pearson's Correlation Coefficient
        correlation.Pearson(query1_dict)

    # This will execute query 2 and call the Linear Regression function
    # Q2: As a movie's budget increases do the sales also continuously increase
    def query_2(self):

        # This selects the total gross and budget for a movie
        query2 = ("SELECT Total_gross , Budget "
                  "FROM MOVIE, TITLE "
                  "WHERE TM_const=T_const "
                  "AND NOT Total_gross=0 "
                  "AND NOT Budget=0 "
                  "ORDER BY Budget "
                  )

        # execute the query
        self.cursor.execute(query2)

        # store query results here
        raw_data_2 = []

        # adds query results to the list
        for response in self.cursor:
            raw_data_2.append(response)

        # creates a data frame with the list
        df_2 = pd.DataFrame(raw_data_2, columns=("Gross", "Budget"))

        # Analyses data with Linear Regression
        regression.LRegression(df_2)

    # This will execute query 3 and call the KNN function
    # Q3: Can we predict a genre based on the actor and director of a film?
    def query_3(self):

        # pulls the genre and actor/director's unique name ids for each title
        query3 = ('SELECT Genre, ACTOR_N_const, DIRECTOR_N_const '
                  'FROM ACTOR_HAS_ROLE_IN_TITLE AS a, TITLE_GENRE, DIRECTOR_DIRECTS_A_TITLE AS d '
                  'WHERE a.TITLE_T_const = TG_const '
                  'AND a.TITLE_T_const = d.TITLE_T_const '
                  'AND d.TITLE_T_const= TG_const '
                  )

        # execute query
        self.cursor.execute(query3)

        # This dictionary holds each genre as a key
        # with list integers that correspond to an actor or director as the value
        query3_dict = {}

        for (Genre, ACTOR_N_const, DIRECTOR_N_const) in self.cursor:

            # remove the first 4 characters of the name id so that only numbers remain
            actor_name = ACTOR_N_const[4:]
            director_name = DIRECTOR_N_const[4:]

            # if the genre already exists in the dictionary, add the two id's to the list
            if Genre in query3_dict:
                query3_dict[Genre].append(int(actor_name))
                query3_dict[Genre].append(int(director_name))

            # if the genre doesn't already exist in the dictionary start a new entry
            else:
                query3_dict.update({Genre: [int(actor_name), int(director_name)]})

        # send the data to be processed by the K-NearestNeighbor function
        classification.KNN(query3_dict)

    # This will execute query 4 and call the Spearman Rank function
    # Q4: Is there a correlation between a movie's country and budget
    def query_4(self):

        # This collects the country and budget for each movie
        query4 = ("SELECT Country, Budget "
                  "FROM MOVIE, MOVIE_COUNTRIES, TITLE "
                  "WHERE TM_const = T_const "
                  "AND TC_const = T_const "
                  "ORDER BY Budget "
                  )

        # execute query
        self.cursor.execute(query4)

        # lists to hold country and budget data
        country_l = []
        budget_l = []

        # this holds the key for each countries numerical code
        options = {'USA': 0,
                   'UK': 1,
                   'Mexico': 2,
                   'France': 3,
                   'South Korea': 4,
                   'Canada': 5,
                   'Germany': 6,
                   'Australia': 7,
                   'Hong Kong': 8,
                   'China': 9,
                   'Spain': 10,
                   'Japan': 11,
                   'New Zealand': 12
                   }

        # convert into a list for printing
        options_l = []
        c = []
        b = []
        for key in options:
            options_l.append((key, options[key]))
            c.append(key)
            b.append(options[key])

        # adds data into respective lists
        for (Country, Budget) in self.cursor:

            # skip data if the budget is zero or the country is "New Line"
            if Budget == 0 or Country == 'New Line':
                continue
            # converts the country string into a unique integer
            country_int = options[Country]

            country_l.append(country_int)
            budget_l.append(Budget)

        data = country_l, budget_l

        # Analyse with Spearman Rank
        correlation.SpearmanRank(data)

    # This will execute query 5 and call the Naive Bayes function
    # Q5: Can we predict a director based release date, duration, imdb score?
    def query_5(self):
        # query5 = ("SELECT DISTINCT Keyword, Director_name "
        #           "FROM MOVIE_KEYWORD, TEMP_DirectorActor, TITLE "
        #           "WHERE T_const = TK_const "
        #           "AND Primary_title = Movie_title "
        query5 = ("SELECT DISTINCT Keywords, Director_name, Movie_title "
                  "FROM TEMP_DirectorActor "
                  "WHERE Director_name = 'Steven Spielberg' "
                  # "OR Director_name = 'Tim Burton' "
                  # "OR Director_name = 'Baz Luhrmann' "
                  # "OR Director_name = 'Darren Aronofsky' "
                  # "OR Director_name = 'George Lucas' "
                  # "OR Director_name = 'Spike Jonze' "
                  # "OR Director_name = 'David Fincher' "
                  # "OR Director_name = 'Guillermo del Toro' "
                  # "OR Director_name = 'Quentin Tarantino' "
                  "OR Director_name = 'Spike Lee' "
                  # "OR Director_name = 'Gus Van Sant' "
                  "OR Director_name = 'Woody Allen' "
                  # "OR Director_name = 'Alfred Hitchcock' "
                  # "OR Director_name = 'Sofia Coppola' "
                  # "OR Director_name = 'John Hughes' "
                  # "OR Director_name = 'Tyler Perry' "
                  # "OR Director_name = 'John Singleton' "
                  "OR Director_name = 'Martin Scorsese' ")

        self.cursor.execute(query5)

        query5_dict = {}

        for (Keyword, Director_name, title) in self.cursor:
            keyword = Keyword.split('|')
            if Director_name in query5_dict:
                for k in keyword:
                    query5_dict[Director_name].append(k)
            else:
                query5_dict.update({Director_name: keyword})

        classification.NaiveBase(query5_dict)

    def end_query(self):
        self.config.close()

if __name__ == '__main__':
    print('Starting Application')
    q = Query()
    q.query_1()
    q.query_2()
    q.query_3()
    q.query_4()
    q.query_5()
    q.end_query()
