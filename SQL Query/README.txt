A single Python file: test_run.py

This project is about data normalization and creating SQL query


Call create_tables() to create 11 relations
     insert_to_tables() to have data inserted into 11 relations
     query(question_num) with question_num is an int to run the query and have output printed out 


All functions included:
	- create_server_connection(host_name, user_name, user_password) : create connection with the server with customizable host_name, user_name, user_password
	- create_database(connection): create a new database and drop the existed one
	- create_db_connection(host_name, user_name, user_password, db_name): connect to the database just created (hw5)
	- create_dictionary(att),  create_dict(att), join_dict(att) : format data in to dictionary before inserting it to relations
	- create_tables()
	- insert_to_tables()
	- query(question_num)



	
	
