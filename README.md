# My Project Title: Police_Post_Logs
   
what are the libraries i used to complete my project:
      1.PANDAS 
      2.SQLALCHEMY 
      3.PSYCOPG2
      4.STREAMLIT

first we need to create virtual environment to initiate the installation process and activate using some command
    i.To activate virtual environment, write in terminal (.venv/Scripts.activate) and press enter`
    ii.After it activated, using pip install option install all above mention libraries

**Why pandas**: PANDAS is a powerfull library in python to read and manipulate data, here i used pandas to read the csv file
Example: 
    pip install pandas -> using this command we install pandas 
    import pandas as pd -> this can use to import pandas library with alias name "pd"
    data=pd.read_csv("path of file") -> using this line we can store the data in a variable named as "data"

# basic structure checks:
    using some functions we can find the null values, dublicate values, datatype conversion
    after finding all these we need to handle all these and make a copy of cleaned data set
    df=data.copy()

**Why SQLAlchemy**: SQLALCHEMY is used to send the bulk data to Database. it will automatically create Table schemas and insert the values accordingly
    Example:
              from sqlalchemy import create_engine -> this line import the sqlqlchemy
              (import create_engine will help to push the data to database)
              host= "hostname"
              username= "username"
              password= "password"
              port= portname
              database= "databasename"
              engine_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
              connection=create_engine(engine_string) -> this line creates a connection
              df.to_sql("tablename",connection,if_exists="replace",index=False or True) ->to replace with existing table

**Why psycopg2**: PSYCOPG2 also helps us to connect our "vs code and postgrsql". it specifically used to fetch the result from database table
    Example:
              connection = psycopg2.connect(
                  host='enter postgresql host name',
                  username='enter postgresql username',
                  password='enter postgresql password',
                  port='enter postgresql port',
                  database='enter database_name' # this will connect a database 
                  ) 
              mediator=connection.cursor() -> cursor is a tool to connect python and postgrsql 
              mediator.execute()
              mediator.fetchall() -> used to fetch the result from database table

**Why Streamlit**: STREAMLIT is used to diplay the content in the backend likely in a website dashboared. It has many functions to create a dashboared             
