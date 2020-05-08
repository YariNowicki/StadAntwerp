# Demo Stad Anwerpen

## Packages

1. dash 1.4.1
2. dash-core-componenents 1.3.1
3. dash-html-components 1.0.1
4. keras 2.3.1
5. matplotlib 3.1.3
6. numpy 1.18.1
7. pandas 1.0.3
8. plotly 4.5.2
9. scikit-learn 0.22.2
10. snowflake-connector-python 2.2.2
11. tensorflow 1.14.0
12. asn1crypto 0.24.0

## Project structure

### app.py
This separation is required to avoid circular imports: the files containing the callback definitions require access to the Dash app instance however if this were imported from index.py, the initial loading of index.py would ultimately require itself to be already imported, which cannot be satisfied.

### index.py
This python file is used to start the webpage, it loads different pages and imports their callbacks

### callbacks.py
All the callbacks of both the pages are placed here. A callback is a function, triggerd when one of their inputs change. It automatically updates the output. (More info: https://dash.plotly.com/basic-callbacks)

### layouts.py
All the layouts get created here.

### columns.py (needs an update, but it works at the moment)
Extra file, filled with array that contains column names. --> Makes the other files cleaner.

### df_calls.py
Used to group functions, so the functions are not all in different places.

### snow_calls.py
The functions that receive data from snowflake.
