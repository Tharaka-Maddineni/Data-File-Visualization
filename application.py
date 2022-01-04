import pandas as pd
from flask import (Flask, after_this_request, json, jsonify, render_template, request, url_for)
from DBOperations import PostGreSQL 

ALLOWED_EXTS = {'.csv'}

app = Flask(__name__)

# Database connectivity parameters
host = '127.0.0.1'
dbname = 'xVectorLabs_DB'
user = 'postgres'
password = 'Walker1510'

# Creating PostGreSQL database object
db_object = PostGreSQL(host, dbname, user, password)


# # Create Own Data Base
# own_database_name = 'xVector'
# db.createDatabase(own_database_name)

# Creating PostGreSQL database object
# db_object = PostGreSQL(host, port, own_database_name, user, password)


# Creation of master table to store all csv data file names.
db_object.createMasterTable()


# ENV = 'dev'
# if ENV == 'dev':
#     app.debug = True
# else:
#     app.debug = False


def check_file(filename):
    return '.' in filename and filename.split('.',1)[1].lower() in ALLOWED_EXTS

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/data')
def data_page():
    try:
        datasets = db_object.fetch_datasets()
        return render_template('data.html', datasets = datasets)

    except Exception as e:
        raise Exception(f'Unable to perform database connection, please check database credentials', str(e))

@app.route('/dataset', methods = ["POST","GET"])
def upload():
    if request.method == "POST":
        try:
            if 'file' not in request.files:
                error = "File not available"
                return render_template('data.html', error = error)
            file = request.files['file']
            filename = file.filename

            if filename == "" or filename is None:
                error = "Filename is empty"
                return render_template('data.html', error = error)

            # if check_file(filename) == False:
            #     error = "This file format is not allowed"
            #     return render_template('data.html', error = error)
            
            #file = request.form.get('file')
            #csv_filename = file.filename
            try:
                df = pd.read_csv(file)
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding="utf-8", engine='python')

            # Clean table names
            #     remove all white spaces
            #     replace -, /, \\, $ with _
            clean_tbl_name = str(filename).replace(" ","_").replace("?","").replace("-","_")\
                             .replace(r"/","_").replace("\\","_").replace("%","")\
                             .replace(")","").replace(r"(","").replace("$","")

            # Clean column names
            #     remove all white spaces
            #     replace -, /, \\, $ with _
            df.columns = [x.replace(" ","_").replace("?","").replace("-","_")\
                             .replace("/","_").replace("\\","_").replace("%","")\
                             .replace(")","").replace(r"(","").replace("$","") for x in df.columns]


            # remove .csv extension from clean_tbl_name
            table_name = '{}'.format(clean_tbl_name.split('.')[0])

            # replacement dictionary that maps pandas datatypes to sql dtypes
            replacements = {
                'object' : 'varchar',
                'float64' : 'float',
                'int64' : 'int',
                'datetime64' : 'timestamp',
                'timedelta64[ns]' : 'varchar'
                }

            # Table schema
            table_column_string = ", ".join("{} {}".format(n, d) for (n,d) in zip(df.columns, df.dtypes.replace(replacements)))

            # Creating a table
            db_object.createTable(table_name, table_column_string)

            # Insert values to table
            # Save df to csv
            df.to_csv(filename, header=df.columns, index=False, encoding="utf-8")

            # Open csv file
            my_file = open(filename)

            # Upload to db
            db_object.upload_to_DB(table_name, my_file)

            # Fetch datasets and display in data.html
            try:
                datasets = db_object.fetch_datasets()
                return render_template('data.html', datasets = datasets)

            except Exception as e:
                raise Exception(f'Unable to perform database connection, please check database credentials', str(e))
        

        except Exception as e:
            raise Exception(f'Something went wrong while accessing given csv file', str(e))

    elif request.method == "GET":
        try:
            datasets = db_object.fetch_datasets()
            return render_template('data.html', datasets = datasets)

        except Exception as e:
            raise Exception(f'Unable to perform database connection, please check database credentials', str(e))


@app.route('/plot')
def plot_page():
    try:
        datasets = db_object.fetch_datasets()
        return render_template('plot.html', datasets = datasets)

    except Exception as e:
        raise Exception(f'Unable to perform database connection, please check database credentials', str(e))


@app.route('/dataset/:<id>/compute', methods = ['POST','GET'])
def computation(id):
    if request.method == 'POST':
        try:
            tablename = db_object.getTableName(id).lower()
            column = request.form['columns']
            operation = request.form['operations']
            result_value = db_object.compute(tablename, column, operation)
            jsonResp = {}
            jsonResp['result_value'] = result_value
            return jsonResp
        
        except Exception as e:
            raise Exception(f"Something went wrong while accessing data from POST request", str(e))

    if request.method == 'GET':
        try:    
            # from javascript, passing dataset (tablename) as id
            @after_this_request
            def add_header(response):
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response
            tablename = db_object.getTableName(id)
            jsonResp = {}
            jsonResp[tablename]= db_object.fetch_table_columns(tablename)
            return jsonResp
        
        except Exception as e:
            raise Exception(f"Something went wrong while sending data to get request", str(e))


@app.route('/dataset/:<id>/plot', methods = ['GET'])
def plot(id):
    if request.method == 'GET':
        try:
            # from javascript, passing dataset (tablename) as id
            @after_this_request
            def add_header(response):
                response.headers['Access-Control-Allow-Origin'] = "*"
                return response
            tablename = db_object.getTableName(id)
            jsonResp = {}
            data = db_object.fetch_column_with_data(tablename)
            columns = data[0]
            records = data[1]
            dic1 = {}
            for i in range(0,len(columns)):
                column_wise_data = []
                for data in records:
                    column_wise_data.append(data[i])
                dic1[columns[i][0]] = column_wise_data
                jsonResp[tablename] = dic1

            return jsonResp
        
        except Exception as e:
            raise Exception(f"(Something went wromg while sending data back to GET request)", str(e))


if __name__ == "__main__":
    app.run()