# Requirements #
1. Download and install [Anaconda](https://www.continuum.io/downloads); as of 7/8/17, this package uses [Anaconda 4.3.0](https://repo.continuum.io/archive/Anaconda3-4.3.0-MacOSX-x86_64.pkg)
    1. Add `/Users/$USER/anaconda/bin:` to the beginning of your `PATH` variable
2. If you are using [Amazon Redshift](https://aws.amazon.com/redshift/),
    1. Install [`psycopg2`](https://anaconda.org/anaconda/psycopg2)
    2. Install [`sqlalchemy-redshift`](https://anaconda.org/conda-forge/sqlalchemy-redshift)
    3. Install [PostgreSQL](https://www.postgresql.org/download/)
        1. Add `Postgres/Library/PostgreSQL/9.5/bin:` to the beginning of your `PATH` variable
