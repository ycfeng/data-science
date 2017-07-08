# Requirements #
This section assumes that you are running OS X 10.7 or later.

1. Download and install [Anaconda](https://www.continuum.io/downloads); as of 7/8/17, this package uses version 4.3.0, which ships with Python 3.5.0
    1. Add `/Users/$USER/anaconda/bin:` to the beginning of your `PATH` variable
2. If you are using [Amazon Redshift](https://aws.amazon.com/redshift/),
    1. Install [`psycopg2`](https://anaconda.org/anaconda/psycopg2); as of 7/8/17, this package uses version 2.6.2
    2. Install [`sqlalchemy-redshift`](https://anaconda.org/conda-forge/sqlalchemy-redshift); as of 7/8/17, this package uses version 0.5.0
    3. Add `Postgres/Library/PostgreSQL/9.5/bin:` to the beginning of your `PATH` variable
