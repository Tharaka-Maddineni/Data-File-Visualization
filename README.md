# Visualize-CSV
Visualize-CSV is a web application where users can get insights of any .csv extension data file regardless of file structure. Also, usercs can upload any new data source (only .csv extension files).

Insights: 
          1. max/min/sum operation of particular column and
          2. can plot graph between any 2 columns based on selection.


## How to run the app.
1. Either fork or download the app and open the folder in any IDE or CLI.
2. Install all the dependencies mentioned in the requirements.txt file.
3. Start the web server using `python application.py` in the terminal/CLI or run the application in the IDE.
4. The app will be served at http://localhost:5000/.
5. Go to http://localhost:5000/ in your browser and select required fields and get results.


## How to upload
1. Go to Data Tab.
2. Create or download any sample data source (.csv extension) from internet or by using MS Excel and save it in desired folder.
3. Click on choose file option to browse and select required file from your local system.
4. Click on upload button to get the file uploaded.


## How to compute
1. Go to Plot Tab.
2. Select available data file from drop down.
3. Select any one of the column from above selected data file.
4. Select any one operation (MAX/MIN/SUM) and click on compute the operation on selected data file column.


## How to Plot the graph
1. Go to Plot Tab.
2. Select available data file from drop down.
3. Select any one of the column from above selected data file in column1.
4. Select any one of the column from above selected data file in column2.
5. Click on Plot button to plot the graph.

## Future Features
==> Availability of multiple formats (.txt, .xls)

## Dependencies
- Python 3.6
- flask
- pandas
- psycopg2


## What the application service looks like
1. Home Page
![alt_text](https://github.com/tharakmaddineni17/Data-Source-Insights/blob/main/Home.png)
2. Data Page
![alt_text](https://github.com/tharakmaddineni17/Data-Source-Insights/blob/main/Data_Page.png)
3. Plot Page
![alt_text](https://github.com/tharakmaddineni17/Data-Source-Insights/blob/main/Plot.png)
