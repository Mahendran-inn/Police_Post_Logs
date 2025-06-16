import pandas as pd
import streamlit as st


#Dataset path selection and copying
data= pd.read_csv("traffic_stops - traffic_stops_with_vehicle_number.csv")
df=data.copy()

#basic structure checks
    #df.dtypes -> find the types 
    #df.isnull().sum() -> find the null values


#fill the null values to structurize the data
mode_value = df['search_type'].mode()[0]
df['search_type']=df['search_type'].fillna(mode_value)

#insert the data in database
from sqlalchemy import create_engine

host= "localhost"
username= "postgres"
password= "njibhuvgy"
port= 5432
database= "Demo_database2"
engine_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
connection=create_engine(engine_string)
df.to_sql("Police_Post_Logs",connection,if_exists="replace")
print('Data loaded successfully.') #just confirmation whether above is executed or not



import psycopg2 #this will connect vs code with PostgreSQL

# Function to fetch data from PostgreSQL
def fetch_data(query):
    conn = psycopg2.connect(
        host= "localhost",
        user= "postgres",
        password= "njibhuvgy",
        port= 5432,
        database= "Demo_database2",
    )
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    #this line will show the column name
    colnames = [desc[0] for desc in cur.description]  # type: ignore
    cur.close()
    conn.close()
    #return results
    return pd.DataFrame(results, columns=colnames)

#page configuration for streamlit to view as dashboared
st.set_page_config(page_title="SecureCheck Police Dashboard", layout="wide")
st.title("SecureCheck: Police Check Post Digital Ledger")
st.markdown("Real-Time monitoring & Insights for Law Enforcement")

#it show full table
st.header("Police Logs Overview")
query='select * from "Police_Post_Logs" '
x=fetch_data(query)
#df.columns=['.','sl.no','stop_date','stop_time','country_name','driver_gender','driver_age_raw','driver_age','driver_race','violation_raw,violation','search_conducted','search_type','stop_outcome,is_arrested','stop_duration','drugs_related_stop','vehicle_number']
st.dataframe(x, use_container_width=True)

# advanced insights
st.header("📌Advanced Insights")


#this column for medium level question
col1,col2=st.columns(2)
with col1:
    st.header("Medium level")
    selected_query = st.selectbox('select any question',[
        "List the top 10 vehicles involved in drug-related stops",
        "Which vehicles were most frequently searched",
        "Which driver age group had the highest arrest rate",
        "What is the gender distribution of drivers stopped in each country",
        "Which race and gender combination has the highest search rate",
        "What time of day sees the most traffic stops",
        "What is the average stop duration for different violations",
        "Are stops during the night more likely to lead to arrests",
        "Which violations are most associated with searches or arrests",
        "Which violations are most common among younger drivers (<25)",
        "Is there a violation that rarely results in search or arrest",
        "Which countries report the highest rate of drug-related stops",
        "What is the arrest rate by country and violation",
        "Which country has the most stops with search conducted"]) 

# Corresponding SQL queries for each question
queries = {
    'List the top 10 vehicles involved in drug-related stops':'select vehicle_number, count(*) as stop_count from "Police_Post_Logs" where drugs_related_stop = True group by vehicle_number order by stop_count desc limit 10',
    'Which vehicles were most frequently searched':'select vehicle_number, count(*) as search_count from "Police_Post_Logs" where search_conducted = True group by vehicle_number order by search_count desc limit 10',
    'Which driver age group had the highest arrest rate':'select driver_age, count(*) as highest_arrest from "Police_Post_Logs" where is_arrested=True group by driver_age order by highest_arrest desc limit 10',
    'What is the gender distribution of drivers stopped in each country':'select country_name, driver_gender, count(*) as stop_count from "Police_Post_Logs" group by country_name, driver_gender order by country_name, stop_count desc',
    'Which race and gender combination has the highest search rate':'select driver_race,driver_gender, count(*) as search_rate from "Police_Post_Logs" group by driver_race,driver_gender order by search_rate desc limit 10',
    'What time of day sees the most traffic stops':'select extract(hour from (stop_date || ' ' || stop_time)::timestamp)::int as hour_of_day,count(*) as stop_count from "Police_Post_Logs" group by hour_of_day order by stop_count desc',
    'What is the average stop duration for different violations':'''with mapped as (select violation,case stop_duration
      WHEN '0-15 Min'  THEN 7.5
      WHEN '16-30 Min' THEN 24
      WHEN '30+ Min'   THEN 45
      ELSE NULL
    END::numeric AS duration_minutes FROM "Police_Post_Logs")
select violation, ROUND(avg(duration_minutes), 2) as avg_stop_duration,count(*) as num_stops
from mapped where duration_minutes IS NOT NULL group by violation order by avg_stop_duration desc''',
    'Are stops during the night more likely to lead to arrests':'''with timed as (select
    CASE
      WHEN EXTRACT(HOUR FROM stop_time::time)::int BETWEEN 6 AND 17 THEN 'Day'
      ELSE 'Night'
    END AS period,
    is_arrested
  from "Police_Post_Logs")
select period,ROUND(avg(is_arrested::int)::numeric, 4) as arrest_rate,
  count(*) as stops from timed group by period''',
    'Which violations are most associated with searches or arrests':'''SELECT
  violation,
  ROUND(AVG(search_conducted::int)::numeric, 4) AS search_rate,
  ROUND(AVG(is_arrested::int)::numeric, 4) AS arrest_rate,
  COUNT(*) AS total_stops
FROM "Police_Post_Logs"
GROUP BY violation
ORDER BY search_rate DESC, arrest_rate DESC
LIMIT 10''',
    'Which violations are most common among younger drivers (<25)':'select violation,count(*) as stop_count from "Police_Post_Logs" where driver_age < 25 group by violation order by stop_count desc limit 10',
    'Is there a violation that rarely results in search or arrest':'''SELECT
  violation,
  ROUND(AVG(search_conducted::int)::numeric, 4) AS search_rate,
  ROUND(AVG(is_arrested::int)::numeric, 4) AS arrest_rate,
  COUNT(*) AS total_stops
FROM "Police_Post_Logs"
GROUP BY violation
HAVING AVG(search_conducted::int) < 0.05
   AND AVG(is_arrested::int) < 0.05
ORDER BY total_stops DESC''',
    'Which countries report the highest rate of drug-related stops':'''SELECT
  country_name,
  ROUND(AVG(drugs_related_stop::int)::numeric, 4) AS drug_stop_rate,
  COUNT(*) AS total_stops
FROM "Police_Post_Logs"
GROUP BY country_name
ORDER BY drug_stop_rate DESC
LIMIT 10''',
    'What is the arrest rate by country and violation':'''SELECT
  country_name,
  violation,
  ROUND(AVG(is_arrested::int)::numeric, 4) AS arrest_rate,
  COUNT(*) AS total_stops
FROM "Police_Post_Logs"
GROUP BY country_name, violation
ORDER BY country_name, arrest_rate DESC''',
    'Which country has the most stops with search conducted':'''SELECT
  country_name,
  COUNT(*) AS search_stops
FROM "Police_Post_Logs"
WHERE search_conducted = TRUE
GROUP BY country_name
ORDER BY search_stops DESC
LIMIT 1'''}

if st.button("Run to execute"):
    result=fetch_data(queries[selected_query])
    #st.write(result)
     #this will convert them as database and display
    df_result = pd.DataFrame(result)
    answer=st.dataframe(df_result)
 

#this column for complex level question
col3,col4=st.columns(2)
with col3:
    st.header("Complex level")
    complex_query = st.selectbox('select any question',[
        "Yearly Breakdown of Stops and Arrests by Country",
        "Driver Violation Trends Based on Age and Race",
        "Time Period Analysis of Stops (Joining with Date Functions),Number of Stops by Year,Month, Hour of the Day",
        "Violations with High Search and Arrest Rates",
        "Driver Demographics by Country (Age, Gender, and Race)",
        "Top 5 Violations with Highest Arrest Rates"]) 

# Corresponding SQL queries for each question
complex_queries = {
    'Yearly Breakdown of Stops and Arrests by Country':'''SELECT
  country_name,
  EXTRACT(YEAR FROM stop_date::date) AS year,
  COUNT(*) AS total_stops,
  SUM(is_arrested::int) AS arrests,
  ROUND(100.0 * SUM(is_arrested::int)/COUNT(*), 2) AS arrest_pct
FROM "Police_Post_Logs"
GROUP BY country_name, year
ORDER BY country_name, year''',
    'Driver Violation Trends Based on Age and Race':'''SELECT
  driver_race,
  CASE
    WHEN driver_age < 18 THEN '<18'
    WHEN driver_age BETWEEN 18 AND 24 THEN '18-24'
    WHEN driver_age BETWEEN 25 AND 34 THEN '25-34'
    ELSE '35+'
  END AS driver_age,
  violation,
  COUNT(*) AS stop_count,
  ROW_NUMBER() OVER (
    PARTITION BY driver_race, driver_age
    ORDER BY COUNT(*) DESC
  ) AS rank
FROM "Police_Post_Logs"
GROUP BY driver_race, driver_age, violation
HAVING COUNT(*) > 50
ORDER BY driver_race, driver_age, rank''',
    'Time Period Analysis of Stops (Joining with Date Functions),Number of Stops by Year,Month, Hour of the Day':'''SELECT
  EXTRACT(YEAR FROM stop_date::date)::int AS year,
  EXTRACT(MONTH FROM stop_date::date)::int AS month,
  EXTRACT(HOUR FROM stop_time::time)::int AS hour,
  COUNT(*) AS stop_count
FROM "Police_Post_Logs"
GROUP BY year, month, hour
ORDER BY year, month, hour''',
    'Violations with High Search and Arrest Rates':'''WITH stats AS (
  SELECT
    violation,
    AVG(is_arrested::int) AS arrest_rate,
    COUNT(*) AS total_stops
  FROM "Police_Post_Logs"
  GROUP BY violation
)
SELECT violation, arrest_rate, total_stops
FROM stats
WHERE total_stops > 50
ORDER BY arrest_rate DESC
LIMIT 5''',
    'Driver Demographics by Country (Age, Gender, and Race)':'''SELECT
  country_name,
  driver_race,
  driver_gender,
  ROUND(AVG(driver_age)::numeric, 1) AS avg_age,
  COUNT(*) AS total_stops
FROM "Police_Post_Logs"
GROUP BY country_name, driver_race, driver_gender
ORDER BY country_name, total_stops DESC''',
    'Top 5 Violations with Highest Arrest Rates':'''WITH violation_stats AS (
  SELECT
    violation,
    COUNT(*) AS total_stops,
    SUM(is_arrested::int) AS total_arrests,
    AVG(is_arrested::int)::numeric AS arrest_rate
  FROM "Police_Post_Logs"
  GROUP BY violation
  HAVING COUNT(*) > 20  -- ensures statistically significant sample (optional)
),
ranked AS (
  SELECT
    violation,
    total_stops,
    total_arrests,
    ROUND(arrest_rate, 4) AS arrest_rate,
    ROW_NUMBER() OVER (ORDER BY arrest_rate DESC) AS rn
  FROM violation_stats
)
SELECT
  violation,
  total_stops,
  total_arrests,
  arrest_rate
FROM ranked
WHERE rn <= 5'''
}

if st.button("Fly to query"):
    complex_result=fetch_data(complex_queries[complex_query])
    #st.write(result)
     #this will convert them as database and display
    df_complex_result = pd.DataFrame(complex_result) 
    complex_answer=st.dataframe(df_complex_result)



#creating form
st.header('New PoliceLog Form')
with st.form('Log_Form'):
    stop_date=st.date_input('stop date')
    stop_time=st.time_input('stop time')
    country_name=st.selectbox('country name',['Canada','India','USA'])
    driver_gender=st.selectbox('driver gender',['male','female'])
    driver_age=st.number_input('driver age',min_value=18,max_value=100)
    driver_race=st.selectbox('driver race',['Asian','Black','Hispanic','White','other'])
    search_conducted=st.selectbox('was a search conducted?',['0','1'])
    search_type=st.selectbox('search type',['Vehicle search','Frisk'])
    stop_duration= st.selectbox('stop duration',df['stop_duration'].dropna().unique())
    drugs_related_stop=st.selectbox('was it drug related?',['0','1'])
    vehicle_number=st.text_input('vehicle number')
    timestamp=pd.Timestamp.now()

    submitted=st.form_submit_button('Result')

    if submitted:
        filtered_data=df[
            (df['driver_gender']==driver_gender)&
            (df['driver_age']==driver_age)&
            (df['search_conducted']==int(search_conducted))&
            (df['stop_duration']==stop_duration)&
            (df['drugs_related_stop']==int(drugs_related_stop))        
        ]

st.markdown(f""" 
Your Search Result: A {driver_age} year-old {driver_gender} driver in {country_name} was stopped 
{'for drugs-related case' if drugs_related_stop == '1' else 'for regular security check'} 
at {stop_time.strftime('%I:%M %p')} on {stop_date} . The stop lasted for {stop_duration}
""")
