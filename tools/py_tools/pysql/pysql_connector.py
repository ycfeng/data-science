import datetime as dt
import json
import math
import os
import pandas as pd
import sqlalchemy as sql
import time

from IPython.core.display import display, Markdown

"""
#################### Base Class for Database Interaction ####################
"""
class SqlUtil:
    def __init__(self):
        self._attempts = 3
        self._authentication_directory = os.path.join(os.path.expanduser("~"), '.authentication')
        self._engine = None
        self._errors = {}
        self._verbose = True
        self.set_default_engine()
        self.set_default_errors()

    @property
    def attempts(self):
        return self._attempts

    @attempts.setter
    def attempts(self, value):
        self._attempts = value

    @property
    def authentication_directory(self):
        return self._authentication_directory

    @authentication_directory.setter
    def authentication_directory(self, value):
        self._authentication_directory = value

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        self._errors = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

    def get_engine(self, connection_info_json, connection_args_json=None):
        with open(connection_info_json, 'r') as f:
            creds = json.load(f)

        try:
            engine_url = sql.engine.url.URL(**creds)

            if connection_args_json is None:
                engine = sql.create_engine(engine_url)
            else:
                with open(connection_args_json, 'r') as g:
                    c_args = json.load(g)

                engine = sql.create_engine(engine_url, connect_args=c_args)

            pd.read_sql_query('select 1;', engine)

            return engine
        except Exception as e:
            display(Markdown('Check credentials.'))

    def check_engine(self):
        try:
            pd.read_sql_query('select 1;', self.engine)
        except Exception as e:
            self.handle_exception(e)

    def set_default_engine(self):
        raise NotImplementedError

    def set_default_errors(self):
        raise NotImplementedError

    def handle_exception(self, exception):
        raise NotImplementedError

    def string_format_a_file(self, file, *args):
        with open(file, 'r') as f:
            s = f.read()
        return s.format(*args)

    def query(self, query_or_query_file, read_write_flag, *args, **kwargs):
        if os.path.exists(query_or_query_file):
            q = self.string_format_a_file(query_or_query_file, *args)
        else:
            q = query_or_query_file

        self.attempts = 3
        while self.attempts > 0:
            try:
                self.check_engine()

                if self.verbose:
                    display(Markdown(
                        'Querying with args ```[{0}]``` at ```{1}```.'.format(
                            ', '.join([str(a) for a in args])
                            , dt.datetime.now().strftime('%y/%m/%d %H:%M:%S')
                        )
                    ))
                    display(Markdown('Attempt: {0}'.format(self.attempts)))
                    display(Markdown('```SQL\n{0}```'.format(q)))

                if 'query_group' in kwargs:
                    self.engine.execute(sql.text(
                        "set query_group to '{0}';".format(kwargs['query_group'])
                    ).execution_options(autocommit=True))

                if 'query_slots' in kwargs:
                    self.engine.execute(sql.text(
                        'set wlm_query_slot_count to 3;'
                    ).execution_options(autocommit=True))

                if read_write_flag == 'w':
                    self.engine.execute(sql.text(
                        q
                    ).execution_options(autocommit=True))
                elif read_write_flag == 'r':
                    df = pd.read_sql_query(sql.text(q), self.engine)

                if 'query_group' in kwargs:
                    self.engine.execute(sql.text(
                        'reset query_group;'
                    ).execution_options(autocommit=True))

                if 'query_slots' in kwargs:
                    self.engine.execute(sql.text(
                        'set wlm_query_slot_count to 1;'
                    ).execution_options(autocommit=True))

                if self.verbose:
                    display(Markdown('Finished at ```{0}```.'.format(
                        dt.datetime.now().strftime('%y/%m/%d %H:%M:%S')
                    )))

                break
            except Exception as e:
                stop = self.handle_exception(e)
                if stop:
                    break
            finally:
                self.attempts -= 1

        if read_write_flag == 'r':
            return df



"""
#################### Redshift Implementation ####################
"""
class RedshiftUtil(SqlUtil):
    def set_default_engine(self):
        self.engine = self.get_engine(
            os.path.join(self.authentication_directory, 'redshift_connection_info.json')
            , os.path.join(self.authentication_directory, 'redshift_connection_args.json')
        )

    def set_default_errors(self):
        self.errors = {
            'disconnect': [
                'server closed the connection unexpectedly'
                , 'error with no message from the libpq'
                , 'connection has been closed unexpectedly'
                , 'SSL SYSCALL error: EOF detected'
                , 'SSL SYSCALL error: Operation timed out'
                , "'NoneType' object has no attribute 'execute'"
                , "'NoneType' object has no attribute 'cursor'"
            ]
            , 'exists': ['already exists']
        }

    def handle_exception(self, exception):
        s = ','.join(exception.args)

        if True in [True if e in s else False for e in self.errors['disconnect']]:
            time.sleep(math.pow(self.attempts, 2))

            self.set_default_engine()

            if self.verbose:
                display(Markdown('Disconnect exception; now reconnected.'))

            return False
        elif True in [True if e in s else False for e in self.errors['exists']]:
            if self.verbose:
                display(Markdown('Table exists exception; no action taken.'))

            return True
        else:
            raise exception

    def copy_from_s3(self, schema_table, s3_path, delimiter, compression):
        if self.verbose:
            display(Markdown(
                'Copying ```{0}``` from  ```{1}``` at ```{2}```.'.format(
                    schema_table
                    , s3_path
                    , dt.datetime.now().strftime('%y/%m/%d %H:%M:%S')
                )
            ))

        q = '''copy {0}
            from '{1}'
            iam_role 'arn:aws:iam::609251445204:role/RedshiftCopyUnload'
            delimiter '{2}' {3};
            '''.format(
                schema_table
                , s3_path
                , delimiter
                , compression
            )

        self.engine.execute(sql.text(q).execution_options(autocommit=True))

    def bulk_copy_from_s3(self, schema_tables_csv, s3_paths_csv, delimiter, compression):
        with open(schema_tables_csv, 'r') as g:
            schema_tables = g.readlines()

        schema_tables = [rt.strip() for rt in schema_tables]

        with open(s3_paths_csv, 'r') as f:
            s3_paths = f.readlines()

        s3_paths = [sp.strip() for sp in s3_paths]

        for i in range(len(s3_paths)):
            self.copy_from_s3(schema_tables[i], s3_paths[i], delimiter, compression)

    def unload_to_s3(self, schema_table, s3_path, delimiter):
        if self.verbose:
            display(Markdown(
                'Unloading ```{0}``` from  ```{1}``` at ```{2}```.'.format(
                    schema_table
                    , s3_path
                    , dt.datetime.now().strftime('%y/%m/%d %H:%M:%S')
                )
            ))

        q = '''unload ('select * from {0};')
            to '{1}'
            iam_role 'arn:aws:iam::609251445204:role/RedshiftCopyUnload'
            delimiter '{2}'
            parallel off;
            '''.format(
                schema_table
                , s3_path
                , delimiter 
            )


"""
#################### Mysql Implementation ####################
"""
class MysqlUtil(SqlUtil):
    def set_default_engine(self):
        self.engine = self.get_engine(
            os.path.join(self.authentication_directory, 'mysql_connection_info.json')
        )

    def set_default_errors(self):
        self.errors = {
            'disconect': [
                'server closed the connection unexpectedly'
                , 'error with no message from the libpq'
                , 'connection has been closed unexpectedly'
                , 'SSL SYSCALL error: EOF detected'
                , "'NoneType' object has no attribute 'execute'"
            ]
            , 'exists': ['already exists']
        }

    def handle_exception(self, exception):
        raise exception
