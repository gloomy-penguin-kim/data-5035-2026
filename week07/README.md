# How to run 

In Snowflake, just associate the Python Notebook with an engine and press run.  For SQL.sql just run while connected to the correct datasource.  

- AI.txt: My AI Conversation 
- PYTHON.ipynb: My Python Notebook
- SEGMENTS_UNFILTERED.csv: The result of SQL.sql 
- SEGMENTS.csv: The final result from PYTHON.ipynb 
- SQL.sql: The core rating system used 

# Programming Paradigms Used

This project uses three different programming paradigms: Declarative, Imperative, and AI-assisted development.

## Declarative Paradigm (SQL)

The declarative paradigm was implemented using SQL in Snowflake. Declarative programming focuses on describing what result should be returned rather than specifying the step-by-step procedure to compute it.

Most of the data processing in this project was done in SQL. SQL was used to join multiple datasets, calculate EV and truck traffic percentages, rank segments using NTILE, and perform geospatial analysis to detect conservation areas within a 1 km buffer using ST_DWITHIN. SQL was also used to determine proximity to highway interchanges.

SQL was chosen for these operations because relational databases are optimized for filtering, joining, and aggregating large datasets. In practice, the entire analysis could have been completed using SQL alone, since Snowflake is designed for large-scale analytical queries.

## Imperative Paradigm (Python)

The imperative paradigm was implemented using Python in a Snowflake notebook. Imperative programming focuses on defining explicit steps that the program executes sequentially.

Python was used to apply additional filters to the dataset, calculate a composite scoring formula for each highway segment, rank the segments, and export the final results as a CSV file. While this logic could also have been written in SQL, Python makes it easier to experiment with scoring models and perform step-by-step data analysis.
  
## AI-Assisted Development

AI tools were used during development to assist with debugging, refactoring, and improving code structure. AI was particularly helpful for optimizing Python code, suggesting improvements to the scoring model, troubleshooting issues with Snowflake notebooks, and the Reflection/README files. 

AI was used as a development aid rather than a replacement for understanding the code. Traditional documentation and online resources were still used to verify concepts and understand the technologies involved.

## Summary

This project demonstrates how data workflows combine multiple paradigms:
    
- SQL (Declarative) for large-scale data processing and geospatial analysis   
- Python (Imperative) for flexible analysis and scoring logic
- AI tools to assist with debugging, refactoring, and improving code quality
 

# Limitations, Constraints, and Assumptions

## Limitations

The datasets used in this project contain several limitations. Traffic counts such as AADT (Annual Average Daily Traffic) represent averages and may not reflect real-time traffic conditions or seasonal variation. Crash and incident data may also vary based on reporting practices, which can affect the accuracy of risk measurements.

Weather risk data represents general regional conditions rather than exact conditions at each road segment.

## Constraints

Environmental constraints were applied by identifying wetlands within a 1 km buffer using ST_DWITHIN. This assumes that wetlands within that distance represent a meaningful environmental restriction, although real-world regulations may vary.

Interchange proximity was calculated using geometric distance, which may not perfectly represent actual roadway access patterns.

## Assumptions

The scoring model assumes that lower values for crash rate, incident rate, and weather risk indicate safer locations, while higher EV usage and lower truck traffic are more favorable for deployment. Each factor was treated with equal weight in the scoring model.

The analysis also assumes that the datasets provided are accurate and representative of typical traffic and roadway conditions.

Money was not considered as a factor.  

