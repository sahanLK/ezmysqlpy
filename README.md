

mysqlpy is a python package that intended to make it easy to perform most common
MySQL database operations for anyone without any SQL knowledge.

## Installation

Easiest way to install mysqlpy is by using [pip](https://pip.pypa.io/en/stable/).

```bash
pip install mysqlpy
```

## Usage

```python
# Import the class 
from mysqlpy import MySQLPy

# Creating an instance
sqlpy = MySQLPy(
    host="your_database_host",
    user="username",
    pwd="password",
)
```
Just by creating an instance of tha ```MySQLPy``` class you can perform some sql
queries that does not require access to the database tables.

###
#### Getting a list of all the databases stored in the server.
```python
all_dbs = sqlpy.get_all_dbs() 
```

###
#### Checking the existance of a database.
To check if a database exists or not, use ```db_exists(database_name)``` method:
```python
if sqlpy.db_exists("information_schema"):
    print("Database exists")
else:
    print("Database does not exists")
```

###
#### Creating a database.
To create a database use ```create_db('database_name')``` method:
```python
sqlpy.create_db("my_new_db")
```

###
#### Deleting a database.
To delete a database use ```delete_db('database_name')``` method:
```python
sqlpy.delete_db("my_new_db")
```

###
#### Accessing database tables.
To execute any kind of database table related queries, you should first select 
a database using ```select_db(database_name)``` method:
```python
sqlpy.select_db("my_new_db")
```
You may change the current database using this method anywhere in your code.
So if you are handling more than one database in your programme, make sure you
use this method in appropriate locations to avoid getting errors or unnecessary 
modificatios to the data.

###
#### Getting a list of all the tables.
```get_all_tbs()``` method returns a list of all table names stored in the 
currently selected database:
```python
# Select your database
sqlpy.select_db('information_schema')

# Print all the tables
for db in sqlpy.get_all_tbs():
    print(db)
```

###
#### Checking table existance.
use ```tb_exists(table_name)``` method to check if the specified table exists
or not:

```python
# If table exists return True, otherwise False
if sqlpy.tb_exists('statistics'):
    print("Table exists")
else:
    print("Table does not exists")
```

###
#### Clear all the records from a table.
Use clear_tb(table_name) to clear all the records from a table. This does not 
delete the table from the database but clear all the data from the table:

```python
sqlpy.clear_tb('countries')
```
###
#### Delete a table.
```python
sqlpy.delete_tb('countries')
```
###
#### Creating a table.
To create a table, use ```create_tb(table_name, cols, primary_key)``` method along 
with it's 2 required parameters and 1 optional parameter.

Second paramater accepts a dictionary, the key as the TABLE NAME and the value 
as the DATATYPE(MAX_LENGTH). Optional third parameter accepts a column name as a
string for the primary key.

```python
# Table columns.
cols = {
    'Name': 'varchar(255)',
    "Age": "int(10)"
}

# Creating a table called 'friends'. 
sqlpy.create_tb('friends', cols, 'name')

```

###
#### Getting a list of table columns.
```python
# To get a list of column names of a table called 'friends'.
cols = sqlpy.get_tb_cols('friends')
```
###
#### Create a new record.
Use ```add_record(table, values_as_a_list)``` method to add a new record into a 
table. You can add only one record at once. When passing values, make sure you 
are passing corresponding values to the table columns.

```python
# Adding a single record at a time
sqlpy.add_record('friends', ["Sahan", 23])

# Adding multiple records.
values = [
    ["Pasindu", 23],
    ["Tharindu", 12],
    ["Sandun", 18],
    ["Sandun", 15],
    ["Sandun", 25],
]
for value in values:
    sqlpy.add_record('friends', value)
```
###
#### Updating records.
Use ```update_tb(table, column, value, condition)``` to update an existing table
record. 

```column``` specifies the name of the column that you are going
to update. 

```value``` specifies the new value for the selected column.

```conditions``` specifies the conditions as a string, to be matched to select
only the appropriate records. For example: ```name="mark" and age=25```

```python
# Change the age into 45 that name equals to "pasindu"
sqlpy.update_tb('friends', 'age', 45, 'name="pasindu"')
```
###
#### Selecting all the records.
To select all the records from a table use ```select_all(table, sort_by, limit, offset)```
method.

Optional ```sort_by``` is a dictionary as ```{column_name: ASC or DESC}```.

Optional ```limit``` is an integer to specify, how many results should be returned.

Optional ```offset``` parameter specify from which position the results should be taken.

```python
# Select all the records of the table: friends
all_results = sqlpy.select_all('friends')

# output: A list of all the table records.
```

###
#### Select only filtered data from a table.
If you want to select only some specific columns, use 
```select_filtered(table, cols, conditions, limit, offset)``` method.

```cols```: A list of column names.

```conditions```: A string of conditions to filter the results.

Optional ```limit``` and ```offset``` parmeters are also available to help you get
the desired records.

```python
fitlered = sqlpy.select_filtered(
    table="friends",
    conditions="name='Sandun'",
    limit=1, # Get only one result
    offset=2, # Starting from second record
)

for record in filtered:
    print(record)
```

###
#### Deleting records.
To delete a record from a table use ```delete_records(table_name, conditions)``` method.
If you didn't specify the conditions, this method will not work.
```python
sqlpy.delete_records("friends", "name='Tharindu' and age=12")
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what 
you would like to change.


## License
This project is licensed under the [MIT License]('https://github.com/sahan').