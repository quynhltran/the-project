## Quynh Tran
## CS 351

import pandas as pd
import numpy as np
import json
import mysql.connector


# String variables of create table commands

movies = "CREATE TABLE Movie ( budget int, homepage varchar(150), m_id int PRIMARY KEY, orginal_language VARCHAR(2),original_title VARCHAR(150),overview VARCHAR(1000),popularity float,release_date VARCHAR(20),revenue bigint, runtime varchar(50), status set('Released', 'Post Production', 'Rumored'),tagline VARCHAR(300),title VARCHAR(150),vote_avg float,vote_count int )"

genres = "CREATE TABLE genres (id smallint PRIMARY KEY, name varchar(50))"

keywords = "CREATE TABLE keywords (id int PRIMARY KEY , name varchar(50))"

prod_comp = "CREATE TABLE production_companies (name varchar(100), id bigint PRIMARY KEY)"

prod_coun = "CREATE TABLE production_countries (iso_3166_1 varchar(5) PRIMARY KEY, name varchar(50))"

language = "CREATE TABLE spoken_language (iso_639_1 varchar(5) PRIMARY KEY, name varchar(50))"

# join tables
link_genres = "CREATE TABLE genres_and_movie (m_id int, g_id smallint, foreign key(m_id) references Movie(m_id), foreign key(g_id) references genres(id), PRIMARY KEY(m_id, g_id))"

link_company = "CREATE TABLE company_and_movie (m_id int, c_id bigint, foreign key(m_id) references Movie(m_id), foreign key(c_id) references production_companies(id), PRIMARY KEY(m_id, c_id))"

link_key = "CREATE TABLE keyword_and_movie (m_id int, k_id int, foreign key(m_id) references Movie(m_id), foreign key(k_id) references keywords(id), PRIMARY KEY(m_id, k_id))"

link_coun ="CREATE TABLE country_and_movie (m_id int,c_id varchar(5),foreign key(m_id) references Movie(m_id), foreign key(c_id) references production_countries(iso_3166_1), PRIMARY KEY(m_id, c_id))"

link_lan = "CREATE TABLE language_and_movie (m_id int,l_id varchar(5),foreign key(m_id) references Movie(m_id),foreign key(l_id) references spoken_language(iso_639_1), PRIMARY KEY(m_id, l_id))"


# read the csv file as a dataframe
df = pd.DataFrame(pd.read_csv('movies.csv'))

# connect sql to python
def create_server_connection(host_name, user_name, user_password):
   
    connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password)
    return connection

# create a new database - drop it if already exists
def create_database(connection):
    q = "DROP DATABASE IF EXISTS hw5"
    query = "CREATE DATABASE hw5"
    cursor = connection.cursor()
    cursor.execute(q)
    cursor.execute(query)
 
# connect to the database that is just created above (hw5)   
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database=db_name)
    return connection 
     
create_database(create_server_connection('localhost','root', 'sp21cs351') )
db = create_db_connection('localhost', 'root', 'sp21cs351','hw5')

# create a cursor - make sure all queries get called with buffered
cursor = db.cursor(buffered = True)
cursor.execute('SET GLOBAL FOREIGN_KEY_CHECKS=0') # fix bug for join table insertion

def create_tables():
    ''' Create 11 tables and drop the existed ones'''
    cursor.execute("DROP TABLE IF EXISTS language_and_movie")
    cursor.execute("DROP TABLE IF EXISTS country_and_movie")
    cursor.execute("DROP TABLE IF EXISTS keyword_and_movie")
    cursor.execute("DROP TABLE IF EXISTS genres_and_movie")
    cursor.execute("DROP TABLE IF EXISTS company_and_movie")

    cursor.execute("DROP TABLE IF EXISTS production_companies")
    cursor.execute("DROP TABLE IF EXISTS genres")
    cursor.execute("DROP TABLE IF EXISTS keywords")
    cursor.execute("DROP TABLE IF EXISTS spoken_language")
    cursor.execute("DROP TABLE IF EXISTS production_countries")
    cursor.execute("DROP TABLE IF EXISTS Movie")

    cursor.execute(movies)
    cursor.execute(genres)
    cursor.execute(keywords)
    cursor.execute(prod_comp)
    cursor.execute(prod_coun)
    cursor.execute(language)

    cursor.execute(link_genres)
    cursor.execute(link_company)
    cursor.execute(link_key)
    cursor.execute(link_coun)
    cursor.execute(link_lan)
    
# get all columns needed for Movie table
movie_att = ["budget","homepage","id","original_language","original_title", "overview","popularity", "release_date","revenue","runtime","status","tagline","title","vote_average","vote_count"]
movie_df = df[movie_att]
movie_df = movie_df.fillna('null') # change NAN to null
list_id = df['id'] 

def create_dictionary(att):
    ''' Create a dictionary of all unique values of a column. This function takes att as a string of the column's name '''

    # read the column that is in json format
    s =  df[att].map(json.loads)
    s = s.fillna('null') # replace NAN with null
    keys = []
    values =[]
    dict_keys = []
    dict_values = []
    temp_val = []
    for row in range(0,len(df)): # for each tuple - l is a list of dictionaries
        l = s[row]
        for i in range(0,len(l)): # for each dictionary in the list
            temp_val = list(l[i].values()) # list of each key and value
            keys.append(temp_val[0]) 
            values.append(temp_val[1])

    # only append unique keys and values
    for i in keys:
        if i not in dict_keys:
            dict_keys.append(i)
    for i in values:
        if i not in dict_values:
            dict_values.append(i)
    diction = dict(zip(dict_keys, dict_values)) # create a dictionary of each key and value
    return diction

def create_dict(att):
    ''' Create a dictionary of all values in a column with corresponding keys and values'''
    s =  df[att].map(json.loads)
    s = s.fillna('null')
    dic = {}
    keys = []
    values =[]
    temp_val = []

    for row in range(0, len(df)): # read tuple
        l = s[row]
        for i in range(0,len(l)): # each dictionary in the tuple
            temp_val = list(l[i].values())
            keys.append(temp_val[0])
            dic[temp_val[0]] = temp_val[1] 
    return dic

def join_dict(att):
    ''' Create a dictionary for join tables that have foreign keys reference to other tables'''

    s =  df[att].map(json.loads)
    s = s.fillna('null')
    keys = []
    diction = {}
    for row in range(0,len(df)): # each row
        l = s[row]
        keys = [] # reset the list of keys
        for i in range(0,len(l)):
            temp_val = list(l[i].values())
            if att == 'production_companies': # switch the order
                keys.append(temp_val[1])
            else:
                keys.append(temp_val[0])
        diction[list_id[row]]= keys # each key can have a list of values
    return diction

def insert_to_tables():
    ''' Iterate through each row of the dataframe, get the values, insert them to the correct relations, and commit the changes '''

    for i,row in movie_df.iterrows():
        cursor.execute("INSERT INTO hw5.Movie VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", tuple(row))
        db.commit()

    for (key, value) in create_dictionary('genres').items():
        sql = "INSERT INTO hw5.genres (id, name) VALUES (%s, %s)"
        cursor.execute(sql, (key, value))
        db.commit()

    for (key, value) in create_dictionary('keywords').items():
        sql = "INSERT INTO hw5.keywords (id, name) VALUES (%s, %s)"
        cursor.execute(sql, (key, value))
        db.commit()

    for (key, value) in create_dict('production_companies').items():
        sql = "INSERT INTO hw5.production_companies(name, id) VALUES (%s, %s)"
        cursor.execute(sql, (key, value))
        db.commit()


    for (key, value) in create_dict('production_countries').items():
        sql = "INSERT INTO hw5.production_countries(iso_3166_1, name) VALUES (%s, %s)"
        cursor.execute(sql, (key, value))
        db.commit()

    for (key, value) in create_dictionary('spoken_languages').items():
        sql = "INSERT INTO hw5.spoken_language(iso_639_1, name) VALUES (%s, %s)"
        cursor.execute(sql, (key, value))
        db.commit()

    for key,val in join_dict('genres').items():
        for i in val:
            sql = "INSERT INTO hw5.genres_and_movie(m_id,g_id) VALUES (%s, %s)"
            cursor.execute(sql, (int(key), i))
            db.commit()

    for key,val in join_dict('keywords').items():
        for i in val:
            sql = "INSERT INTO hw5.keyword_and_movie(m_id,k_id) VALUES (%s, %s)"
            cursor.execute(sql, (int(key), i))
            db.commit()

    for (key, value) in join_dict('production_countries').items():
        for i in value:
            sql = "INSERT INTO hw5.country_and_movie(m_id, c_id) VALUES (%s, %s)"
            cursor.execute(sql, (int(key), i))
            db.commit()

    for (key, value) in join_dict('spoken_languages').items():
        for i in value:
            sql = "INSERT INTO hw5.language_and_movie(m_id, l_id) VALUES (%s, %s)"
            cursor.execute(sql, (int(key), i))
            db.commit()

    for (key, val) in join_dict('production_companies').items():
        for i in val:
            sql = "INSERT INTO hw5.company_and_movie(m_id,c_id) VALUES (%s, %s)"
            cursor.execute(sql, (int(key), i))
            db.commit()

def query(question_num):
    ''' All commands for Part 2- Query'''

    if question_num == 1:
        q = "SELECT AVG(budget) FROM Movie"

    if question_num ==2:
        q = "SELECT Movie.original_title, production_companies.name AS 'Production Company'  FROM Movie INNER JOIN company_and_movie ON Movie.m_id =company_and_movie.m_id INNER JOIN production_companies ON company_and_movie.c_id = production_companies.id INNER JOIN country_and_movie ON Movie.m_id = country_and_movie.m_id INNER JOIN production_countries ON country_and_movie.c_id = production_countries.iso_3166_1 WHERE iso_3166_1= 'US' limit 5 "
       
    if question_num ==3:
        q = "SELECT original_title,revenue FROM Movie ORDER BY revenue DESC limit 5"

    if question_num ==4:
        q = "SELECT Movie.original_title, GROUP_CONCAT(genres.name) FROM Movie JOIN genres_and_movie ON Movie.m_id = genres_and_movie.m_id JOIN genres ON genres_and_movie.g_id = genres.id WHERE Movie.m_id IN (SELECT Movie.m_id  FROM Movie  INNER JOIN genres_and_movie  ON Movie.m_id = genres_and_movie.m_id  INNER JOIN genres ON genres_and_movie.g_id = genres.id WHERE genres.name = 'Science Fiction' or genres.name = 'Mystery'  GROUP BY(Movie.original_title) HAVING COUNT(*) =2)  GROUP BY(Movie.original_title) limit 5"
        cursor.execute("SET SESSION sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))")

    if question_num ==5:
        q = "SELECT original_title, popularity FROM Movie WHERE popularity > (SELECT avg(popularity) FROM Movie) LIMIT 5 "

    cursor.execute(q)
    result = cursor.fetchall()
    # print the results from the queries
    for row in result:
        print(row)
  

if __name__ == '__main__':
    create_tables()
    insert_to_tables()

    for i in [1,2,3,4,5]:
        query(i)

