import pandas as pd
import psycopg2



class PostGreSQL:
    def __init__(self, host, port, dbname, user, password):
        """
        This function sets the database parameters
        """
        try:
            self.host = host
            self.port = port
            self.dbname = dbname
            self.user = user
            self.password = password
            self.connection_string = "host=%s port=%s dbname=%s user=%s password=%s" % (self.host, self.port, self.dbname, self.user, self.password)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initiation process\n" + str(e))
    
    def createDatabase(self, database_name):
        """
        This function to create a database inside the PostGreSQLserver
        """
        try:
            # get connection and cursor
            cursor,connection = self.createCursor()

            # Check if the table already exists
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{}';".format(database_name))

            check = cursor.fetchone()

            # Query to create a database
            create_database_query = "CREATE DATABASE %s;" %(database_name)

            # Execure the query to create a database named xVectorLabs_DB
            if not check:
                cursor.execute(create_database_query)            

            # Commit the transaction
            connection.commit()

            # Close the cursor
            self.closeCursor(cursor)
        
            # Close the connection
            self.closeConnection(connection)
            
        except Exception as e:
            raise Exception(f'Something went wrong while creating a database in PostGreSQL server', str(e))
    
    def createMasterTable(self):
        """
        This function is to create a Master Table named dataset_names which contains all the uploaded csv file names.
        """
        try:

            # query to create database table dataset_names
            create_table_query = """CREATE SEQUENCE dataset_names_id_seq;
                                    CREATE TABLE dataset_names (
	                                        id integer NOT NULL PRIMARY KEY DEFAULT nextval('dataset_names_id_seq'),
	                                        dataset text
                                            );
                                    ALTER SEQUENCE dataset_names_id_seq
                                    OWNED BY dataset_names.id;
                                """

            # get connection and cursor
            cursor,connection = self.createCursor()

            cursor.execute("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name = 'dataset_names');")

            # Flag to check if master table is exists or not.
            check = cursor.fetchone()

            # Cursor executing the creation of dataset_names table query
            if not check:
                cursor.execute(create_table_query)

            # Commit the transaction
            connection.commit()

            # Close the cursor
            self.closeCursor(cursor)
        
            # Close the connection
            self.closeConnection(connection)

        except Exception as e:
            raise Exception(f"(createMasterTable): Something went wrong when creating Master table: dataset_names", str(e))
    
    def createConnection(self):
        """
        This function creates and establishes the connection between database and application
        """
        try:
            connection = psycopg2.connect(self.connection_string)
            return connection
        except Exception as e:
            raise Exception("(createConnection): Something went wrong on creation of connection \n" + str(e))
    
    def closeConnection(self, connection):
        """
        This function closes the connection of db
        """
        try:
            connection.close()
        except Exception as e:
            raise Exception(f"Something went wrong on closing connection\n", str(e))
        
    def createCursor(self):
        """
        This function created the cursor to execute databse queries
        """
        try:
            connection = self.createConnection()
            cursor = connection.cursor()
            return cursor,connection
        except Exception as e:
            raise Exception(f"(createCursor): Something went wrong on creation of cursor\n"+str(e))
    
    def closeCursor(self, cursor):
        """
        This function closes the cursor object
        """
        try:
            cursor.close()
        except Exception as e:
            raise Exception(f"(closeCursor): Something went wrong on closing cursor\n"+str(e))
    
    def fetch_datasets(self):
        """
        This function used to fetch all table names from postgres database
        """
        try:
            # query to select only table names from postgres to display on data page
            # table_query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
            table_query =  "select * from dataset_names;"

            # Creating cursor
            cursor,connection = self.createCursor()

            # Cursor executing the query
            cursor.execute(table_query)

            # fetching all data from cursor and storing into datasets variable
            datasets = cursor.fetchall()

            # Commit the transaction
            connection.commit()

            # Close the cursor
            self.closeCursor(cursor)
            
            # Close the connection
            self.closeConnection(connection)

            # returning datasets 
            return datasets
        except Exception as e:
            raise Exception(f"Something went wrong while fetching table names\n" + str(e))

    def createTable(self, tablename, table_column_string):
        """
        This function drop table if already exists and 
        create new table with given tablename and table_column_string
        """
        try:
            drop_table_query = "drop table if exists %s" % ( tablename )
            
            create_table_query = "create table %s (%s)" % ( tablename, table_column_string )

            # Creating cursor
            cursor,connection = self.createCursor()

            # Cursor executing table drop query
            cursor.execute(drop_table_query)

            # Cursor executing the table creation query
            cursor.execute(create_table_query)

            # Commit the transaction
            connection.commit()

            # Close the cursor
            self.closeCursor(cursor)
            
            # Close the connection
            self.closeConnection(connection)
        
        except Exception as e:
            raise Exception(f"Something went wrong on creating table\n" + str(e))
    
    def upload_to_DB(self, tablename, my_file):
        """
        This function copies data from csv file to database table
        """
        try:
            # Upload table content and records to database
            copy_query = """COPY %s FROM STDIN WITH
                        CSV
                        HEADER
                        DELIMITER AS ',';
                    """ 
            # Grant access to table
            grant_query = "grant select on table %s to public;" %tablename

            #----- insert dateset into dataset_names table
            dataset_name_query = """
                                INSERT INTO dataset_names (dataset)
                                SELECT * FROM (SELECT '%s') AS tmp
                                WHERE NOT EXISTS (
                                    SELECT dataset FROM dataset_names where dataset = '%s'
                                ) LIMIT 1;                                
                             """ % (tablename, tablename)

            # get connection and cursor
            cursor,connection = self.createCursor()

            # Cursor executing the copy query
            cursor.copy_expert(sql = copy_query %tablename, file = my_file)

            # Cursor executing the dataset insert into master table query
            cursor.execute(dataset_name_query)

            # Cursor executing the grant query
            cursor.execute(grant_query)

            # Commit the transaction
            connection.commit()

            # Close the cursor
            self.closeCursor(cursor)
        
            # Close the connection
            self.closeConnection(connection)

        except Exception as e:
            raise Exception(f"Something went wrong on uploading tablename to database\n" + str(e))
    
    def getTableName(self, id):
        """
        This function is to get table name from master table dataset_names based on id passed as argument.
        """
        try:
            # get connection and cursor
            cursor,connection = self.createCursor()
            
            # query to fetch all table name from given dataset table by passing id
            table_name_query = "select dataset from dataset_names where dataset_names.id = {}".format(int(id))

            # Cursor executing table_name query
            cursor.execute(table_name_query)
            
            # Extracting table name from cursor 
            table_name = cursor.fetchall()

            # Commit the transaction
            connection.commit()

            # Close the cursor
            self.closeCursor(cursor)
        
            # Close the connection
            self.closeConnection(connection)

            # Returning table name back to called function
            return table_name[0][0]
        except Exception as e:
            raise Exception(f'(getTableName): Something went wrong on fetching table name from dataset_names', str(e))
    
    def fetch_table_columns(self, tablename):

        """
        This function is used to fetch table columns from database table based on given tablename. 
        """
        try:
            # get connection and cursor
            cursor,connection = self.createCursor()
            
            # query to fetch all column names from given table
            tablename = tablename.lower()
            col_query = "SELECT column_name from information_schema.columns where table_name = '%s';" % (tablename)

            # Cursor executing table_name query
            cursor.execute(col_query)
            
            # Extracting table name from cursor 
            columns = cursor.fetchall()

            # Commit the transaction
            connection.commit()

            # Close the cursor
            self.closeCursor(cursor)
        
            # Close the connection
            self.closeConnection(connection)

            # Returning table column names back to called function    
            column_names = []
            for col in columns:
                column_names.append(col[0])

            return column_names

        except Exception as e:
            raise Exception(f'(fetch_table_columns): Something went wrong on fetching table column names from database', str(e))
    
    def fetch_data(self, table_name, column_name):
        """
        This function is to fetch data-records from table name and column name
        """
        try:
            # get connection and cursor
            cursor,connection = self.createCursor()

            # query to fetch all tables(datasets) from database

            ### ---- change query to fetch data from dataset_names
            #query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
            query = "select {} from {};".format(column_name, table_name)

            # Executing query
            cursor.execute(query)

            # Extracting data from cursor
            cursor_data = cursor.fetchall()

            # Commit the transaction
            connection.commit()

            # Close the cursor
            self.closeCursor(cursor)
        
            # Close the connection
            self.closeConnection(connection)

            # fetchall tables and store it into datasets
            records_data = []
            for data in cursor_data:
                records_data.append(data[0])
            return records_data

        except Exception as e:
            raise Exception(f'(fetch_data): Something went wrong while fetching data from database', str(e))

    def fetch_column_with_data(self, tablename):
        """
        This function is to fetch data-records from table name and column name
        """
        try:
            # get connection and cursor
            cursor,connection = self.createCursor()
            
            # query to fetch column names from given tablename
            col_query = "SELECT column_name from information_schema.columns where table_name = '{}';".format(tablename)
            
            # Cursor executing col_query
            cursor.execute(col_query)

            # Extracting column data from cursor
            columns_data = cursor.fetchall()

            data = []
            data.append(columns_data)
        
            # query to fetch records of limit 25 from given tablename
            data_query = "select * from %s limit 25;" %(tablename)

            # Cursor executing data_query
            cursor.execute(data_query)
        
            # fetchall tables and store it into datasets
            records_data = cursor.fetchall()

            data.append(records_data)
    

            # Commit the transaction
            connection.commit()

            # Close the cursor
            self.closeCursor(cursor)
        
            # Close the connection
            self.closeConnection(connection)

            return data

        except Exception as e:
            raise Exception(f'(fetch_column_with_data): Something went wrong while fetching the data from database', str(e))

    def compute(self, table_name, column_name, operation_name):
        try:

            # Fetch_data function return list of column records
            data = self.fetch_data(table_name, column_name)

            # Computation
            if operation_name.upper() == "MAX":
                return max(data)

            elif operation_name.upper() == "MIN":
                return min(data)

            elif operation_name.upper() == "SUM":
                return sum(data)

        except Exception as e:
            raise Exception(f'(compute): Something went wrong on computing data', str(e))
