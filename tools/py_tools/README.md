# Requirements

1. Mac OS X 10.7 or later
2. [Anaconda](https://www.continuum.io/downloads); as of 7/8/17, this package uses version 4.3.0, which ships with Python 3.5.0
    1. Add `/Users/$USER/anaconda/bin:` to the beginning of your `PATH` variable
3. If you are using [PostgreSQL](https://www.postgresql.org/),
    1. Install [PostgreSQL](https://www.postgresql.org/download/macosx/) if it does not already exist; as of 7/8/17, this package uses version 9.5
    2. Add `Postgres/Library/PostgreSQL/9.5/bin:` to the beginning of your `PATH` variable
    3. Install [`psycopg2`](https://anaconda.org/anaconda/psycopg2) if it does not already exist; as of 7/8/17, this package uses version 2.6.2
4. If you are using [Amazon Redshift](https://aws.amazon.com/redshift/),
    1. Go back and complete Step 3
    2. Install [`sqlalchemy-redshift`](https://anaconda.org/conda-forge/sqlalchemy-redshift); as of 7/8/17, this package uses version 0.5.0
5. If you are using [MySQL](https://www.mysql.com/),
    1. Install [MySQL](https://dev.mysql.com/downloads/mysql/) if it does not already exist; as of 7/8/17, this package uses version 14.14
    2. Add  `/usr/local/mysql/bin:` to the beginning of your `PATH` variable
    

# Setup
1. Clone or fork https://github.com/ycfeng/data-science
2. From the repository's root directory, run `python tools/py_tools/setup.py install`
3. Run `mkdir /Users/$USER/.authentication`
4. If you are using Redshift,
    1. Create a file called `redshift_connection_info.json` with content `{"username": "yourusername", "password": "yourpassword", "host": "yourhost", "port": "yourport", "database": "yourdatabase", "drivername": "redshift+psycopg2"}`
    2. Create a file called `redshift_connection_args.json` with content `{"sslmode" : "prefer"}`

