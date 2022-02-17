# Create Datasource

MindsDB enables connections to your favorite databases, data warehouses, data lakes, etc in a simple way.

Our SQL API supports creating a datasource connection by passing any credentials needed by each type of system that you are connecting to. 

# Syntax

```sql
CREATE DATASOURCE datasource_name
WITH
	engine=engine_string, 
	parameters={"key":"value", ...};
```

# Example: MySQL

Here is a concrete example to connect to a MySQL database.

```sql
CREATE DATASOURCE mysql_datasource 
WITH 
	engine='mysql', 
	parameters={
        "user":"root",
        "port": 3307, 
        "password": "password", 
        "host": "127.0.0.1", 
        "database": "mysql"
        };
```

Once a datasource has been correctly created, you will see it registered in `mindsdb.datasources`.

```sql
select * from mindsdb.datasources;
```

![Once a datasource has been correctly created, you will see it registered in `mindsdb.datasources`](../../assets/sql/datasource_listing.png)


After you have connected your data, you can train a predictor by selecting some data within the datasource.

```sql
CREATE PREDICTOR predictor
FROM mysql_datasource (
	SELECT * FROM test_data.home_rentals
)
PREDICT rental_price;
```
