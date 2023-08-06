# pytest-pymysql-autorecording

A pytest plugin for recording database query results and mocking with the stored data.

## Mocking with real database data

In principle, mocking database data is a good idea. But if your database is very complex, this may easily become tedious and may lack the richness of the real data.

Testing with real data leads to another problem, though: You might not want to grant your CI/CD pipeline on, say, GitHub, access to a database.

So this plugin offers a compromise. You still run tests against a real database, and you store the query results. The stored results can then be used by the CI/CD pipeline to mock the database queries.

## Using the plugin

Please refer to the [Quickstart Guide](https://saltastroops.github.io/pytest-pymysql-autorecord/quickstart.html) to find out how to use the plugin.
