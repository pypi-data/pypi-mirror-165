from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd


class Snowflake:

    def __init__(self, url=None, warehouse=None, db=None, schema=None):
        if url is not None:
            self.url = url
        elif (url is None) and (warehouse is not None) and (db is not None) and (schema is not None):
            self.url = f'{url}/{db}/{schema}?warehouse={warehouse}'

    def execute(self, sql):
        engine = create_engine(self.url)
        Session = sessionmaker(bind=engine)
        session = Session()
        statements = sql.split(';')
        statements = [i for i in statements if i]
        for statement in statements:
            t = session.execute(statement)
            print(t.rowcount, statement.replace('\n', ' ')[:50])
            if t.returns_rows:
                df = pd.DataFrame(t.fetchall())
                df.columns = t.keys()
                session.commit()
                session.close()
                return df
        session.commit()
        session.close()
        engine.dispose()

    def load_from_s3(self, warehouse, table, url, aws_access_key_id, aws_secret_access_key, file_format):
        sql = f'''
                use warehouse {warehouse};
                copy into {table} 
                from s3://tpsda-staging/{url} 
                credentials=(aws_key_id='{aws_access_key_id}' aws_secret_key='{aws_secret_access_key}') 
                file_format = ({file_format});'''
        self.execute(sql)

    def run_setupsql(self, warehouse, db, schema):
        sql = f'USE WAREHOUSE {warehouse}; USE DATABASE {db}; USE SCHEMA {schema};'
        self.execute(sql)

    def create_fileformat(self, warehouse, db, schema, source, fileformat):
        db = db.upper()
        schema = schema.upper()
        fileformat_name = f'{source}_{fileformat}_format'
        fileformat_name = fileformat_name.upper()

        if fileformat == 'json':
            fileformat_sql = f'''
                use warehouse {warehouse};
                CREATE FILE FORMAT IF NOT EXISTS {db}.{schema}.{fileformat_name}
                TYPE = \'{fileformat}\'
                STRIP_OUTER_ARRAY=true;
                '''
        elif fileformat == 'csv':
            fileformat_sql = f'''
                use warehouse {warehouse};
                CREATE FILE FORMAT IF NOT EXISTS {db}.{schema}.{fileformat_name}
                TYPE = \'{fileformat}\';
                '''
        self.execute(sql=fileformat_sql)

    def create_internalstage(self, warehouse, db, schema, stage_name, snowflakefileformat):
        internalstage_sql = f'''
                use warehouse {warehouse};
                CREATE STAGE IF NOT EXISTS {db}.{schema}.{stage_name}
                COMMENT = 'internal stage' file_format = {db}.{schema}.{snowflakefileformat};
                '''
        self.execute(sql=internalstage_sql)

    def create_table(self, warehouse, db, schema, source, columns, if_exists, prefix=None):
        """
        creates table in specified location with specified columns; note that this method auto-includes a column for
        the raw data ('src') and a timestamp ('currentTimestamp')
        :param columns: columns of target table in dictionary format
        :type columns: dict
        :param if_exists: if you're ok replacing existing table, use 'replace'
        :type if_exists: str
        """

        if if_exists == 'replace':
            create_sql = 'CREATE OR REPLACE TABLE'
        else:
            create_sql = 'CREATE TABLE IF NOT EXISTS'

        if prefix is None:
            table_name = f'{db}.{schema}.{source}'
        else:
            table_name = f'{db}.{schema}.{prefix}_{source}'

        column_sql = ','.join([k + ' ' + v for k, v in columns.items()]) \
                     + ',src variant, currentTimestamp timestamp_ntz'

        create_sql = f'''
            use warehouse {warehouse};
            {create_sql} {table_name}
            ({column_sql});        
            '''
        self.execute(sql=create_sql)

    def load_data_into_stage(self, db, schema, stage, filepath):
        put_sql = f'put \'file:///{filepath}\' @{db}.{schema}.{stage} AUTO_COMPRESS=True;'
        load_sql = f'{put_sql}'
        self.execute(sql=load_sql)

    def copy_data_from_stage(self, warehouse, db, schema, stage, table, columns, fileformat):

        """
        :param warehouse: warehouse
        :param db:  database
        :param schema: schema
        :param stage: staging area to load from
        :param table: destination table
        :param columns: dict of columns + dtypes
        :param fileformat: name of custom fileformat that was created
        """

        db = db.upper()
        schema = schema.upper()
        table = table.upper()

        column_sql = ','.join(['$1:' + k + '::' + v + ' as ' + k for k,v in columns.items()])
        copy_sql = f'''
            use warehouse {warehouse};
            COPY INTO {db}.{schema}.{table}
            from (
                select
                    {column_sql}
                    , $1::variant as src
                    ,current_timestamp::timestamp_ntz as currentTimestamp
                from @{db}.{schema}.{stage})
            ON_ERROR = skip_file
            FORMAT_NAME = {fileformat};
            '''
        self.execute(sql=copy_sql)

    def merge_tables(self, warehouse, db, schema, source_table, target_table, match_columns):
        # TODO: account for edge indeterministic cases, e.g. source table has duplicate/multiple records per key
        # NOTE: columns are case-sensitive, which is stupid.
        db = db.upper()
        schema = schema.upper()
        source_table = source_table.upper()
        target_table = target_table.upper()

        all_src_columns = self.get_columns(db=db, schema=schema, table=source_table)
        all_columns_string = ', '.join(all_src_columns)
        all_columns_prefixed = ', '.join(['source_table.' + each for each in all_src_columns])

        match_sql = ' AND '.join(['source_table.' + each.upper() + ' = target_table.' + each.upper() for each in match_columns])
        update_sql = ', '.join(['target_table.' + each.upper() + ' = source_table.' + each.upper() for each in all_src_columns])
        merge_sql = f'''
            use warehouse {warehouse};
            MERGE INTO {target_table} target_table
            USING {source_table} source_table
            ON 
                {match_sql}
            WHEN MATCHED THEN
              UPDATE set {update_sql}
            WHEN NOT MATCHED THEN
              INSERT ({all_columns_string})
              VALUES ({all_columns_prefixed});
            '''
        self.execute(sql=merge_sql)

    def remove_from_stage(self, db, schema, stage):
        remove_sql = f'remove @{db}.{schema}.{stage}/;'  # remove all files from stage (can restrict to certain directory or pattern
        self.execute(sql=remove_sql)

    def get_columns(self, db, schema, table):
        db = db.upper()
        schema = schema.upper()
        table = table.upper()

        sql = f'''
            select 
                COLUMN_NAME as column_name
            from {db}.INFORMATION_SCHEMA.COLUMNS
            where 1=1
                and TABLE_SCHEMA = '{schema}'
                and TABLE_NAME = '{table}'
            order by ORDINAL_POSITION;
            '''

        df = self.execute(sql=sql)
        print(df.columns)
        columns_list = df['column_name'].tolist()

        return columns_list

    def drop_table(self, warehouse, db, schema, table):
        db = db.upper()
        schema = schema.upper()
        table = table.upper()

        sql = f'use warehouse {warehouse}; DROP TABLE {db}.{schema}.{table};'
        self.execute(sql=sql)
        
        
    ## WRAPPER functions
    def setup_snowflake(self, warehouse, db, schema, source, fileformat, columns):
        fileformat_name = f'{source}_{fileformat}_format'
        stage_name = f'stage_{source}_{fileformat}'

        # SETUP DESTINATIONS
        # create source-specific file formats, stage, raw table (if not exist) for staging
        print('create snowflake file format')
        self.create_fileformat(warehouse=warehouse, db=db, schema=schema, source=source, fileformat=fileformat)

        print('create snowflake internal stage')
        self.create_internalstage(warehouse=warehouse,
                                  db=db,
                                  schema=schema,
                                  stage_name=stage_name,
                                  snowflakefileformat=fileformat_name)

        print('create tmp table in snowflake')
        self.create_table(warehouse=warehouse,
                          db=db,
                          schema=schema,
                          prefix='tmp',
                          source=source,
                          columns=columns,
                          if_exists='replace'
                          )

        print('create raw table in snowflake')
        self.create_table(db=db,
                          schema=schema,
                          prefix='raw',
                          source=source,
                          columns=columns,
                          if_exists='append'
                          )

    def load_into_snowflake(self, warehouse, db, schema, source, fileformat, filepath, columns):
        tmptable_name = f'tmp_{source}'
        stage_name = f'stage_{source}_{fileformat}'
        fileformat_name = f'{source}_{fileformat}_format'

        # upload compressed file into stage & copy into tmp
        print(f'load data into stage {stage_name}')
        self.load_data_into_stage(db=db, schema=schema, stage=stage_name, filepath=filepath)

        print(f'data loaded into {stage_name}, now copy data from stage into {tmptable_name}')
        self.copy_data_from_stage(warehouse=warehouse,
                                  db=db,
                                  schema=schema,
                                  stage=stage_name,
                                  table=tmptable_name,
                                  columns=columns,
                                  fileformat=fileformat_name)
        print(f'data copied from stage into {tmptable_name}')

    def merge_into_snowflake(self, warehouse, db, schema, source, match_columns):
        rawtable_name = f'raw_{source}'
        tmptable_name = f'tmp_{source}'

        # merge data from tmp into raw table
        print('merge from stage')
        self.merge_tables(warehouse=warehouse,
                          db=db,
                          schema=schema,
                          source_table=tmptable_name,
                          target_table=rawtable_name,
                          match_columns=match_columns
                          )

    def cleanup_snowflake(self, warehouse, db, schema, source, fileformat):
        tmptable_name = f'tmp_{source}'
        stage_name = f'stage_{source}_{fileformat}'

        self.drop_table(warehouse=warehouse, db=db, schema=schema, table=tmptable_name)
        self.remove_from_stage(db=db, schema=schema, stage=stage_name)
