import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker


class MsSql:
    def __init__(self, url):
        self.url = url

    def pull(self, sql):
        engine = create_engine(self.url)
        df = pd.read_sql(sql, engine)
        engine.dispose()
        return df

    def push(self, df, name, if_exists='append'):
        engine = create_engine(self.url)

        # check if table exists first
        table_exists = name in inspect(engine).get_table_names()
        if table_exists and if_exists == 'append':
            s = engine.execute(f'select count(*) from {name}').fetchone()
            start = int(s[0])  # return first value of returned rowproxy object (which should be the rowcount)
        else:
            start = 0

        df.to_sql(name, con=engine, if_exists=if_exists, index=False)
        e = engine.execute(f'select count(*) from {name}').fetchone()
        end = int(e[0])  # return first value of returned rowproxy object (which should be the rowcount)

        if end == start + len(df):
            print(f'{len(df)} rows added to {name}.')
        else:
            print(f'Push to {name} unsuccessful. Please try again.')

        engine.dispose()

    def push_staging(self, df, db, stage_table):
        engine = create_engine(self.url)
        self.drop(db, stage_table)
        df.to_sql(stage_table, con=engine, if_exists='replace', index=False)
        engine.dispose()

    def execute(self, sql):
        statements = sql.split(';')
        statements = [i + ';' for i in statements if i]
        engine = create_engine(self.url)
        Session = sessionmaker(bind=engine)
        session = Session()
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

    def execute_direct(self, sql):
        statements = sql.split(';')
        statements = [i for i in statements if i]
        engine = create_engine(self.url, isolation_level="AUTOCOMMIT")
        connection = engine.connect()
        for statement in statements:
            r = connection.execute(statement)
        engine.dispose()

    def execute_to_csv(self, sql, file, header=False):
        statements = sql.split(';')
        statements = [i for i in statements if i]
        engine = create_engine(self.url, connect_args={'connect_timeout': 1500})  # try connect:1500 for query timeout
        for chunk in pd.read_sql_query(sql, engine, chunksize=10000):
            chunk.to_csv(file, index=False, header=header, mode='a')
        engine.dispose()

    def merge(self, db, source_table, target_table, match_columns, sort_columns, drop_source_table=True):
        source_columns = self.get_columns(db, source_table)
        source_columns = [x.lower() for x in source_columns]
        target_columns = self.get_columns(db, target_table)
        target_columns = [x.lower() for x in target_columns]
        if len(source_columns) == 0:
            print(f'Source table does not exist.')
            return
        if len(target_columns) == 0:
            print(f'Target table does not exist. Creating..')
            create_sql = f"USE [{db}]; SELECT TOP 0* INTO [{target_table}] FROM [{source_table}];"
            self.execute(create_sql)
            target_columns = source_columns
        if source_columns != target_columns:
            print(f'Columns do not match. Source: {source_columns}. Target: {target_columns}')
            return
        else:
            print(f'Merging..')
            merge_sql = self.construct_merge_sql(db, source_table, target_table, match_columns, sort_columns,
                                                 target_columns)
            if drop_source_table:
                drop_sql = f"USE [{db}]; DROP TABLE [{source_table}];"
                merge_sql += drop_sql
            self.execute(merge_sql)

    def construct_merge_sql(self, db, source_table, target_table, match_columns, sort_columns, columns):
        set_columns = ', '.join([f't.[{x}] = s.[{x}]' for x in columns])
        join_columns = ' AND '.join([f't.[{x}] = s.[{x}]' for x in match_columns])
        update_where_columns = ' OR '.join([f'coalesce(t.[{x}],0) < s.[{x}]' for x in sort_columns])
        select_columns = ', '.join([f's.[{x}]' for x in columns])
        insert_where_columns = ' AND '.join([f't.[{x}] IS NULL' for x in match_columns])
        partition_columns = ', '.join([f'[{x}]' for x in match_columns])
        order_columns = ', '.join([f'[{x}] DESC' for x in sort_columns])

        update_sql = f"""
        USE [{db}];
        UPDATE t
        SET {set_columns}
        FROM [{target_table}] t
        INNER JOIN [{source_table}] s
            ON {join_columns}
        WHERE {update_where_columns};
        """

        insert_sql = f"""
        USE [{db}];
        INSERT INTO [{target_table}]
        SELECT {select_columns}
        FROM [{source_table}] s
        LEFT JOIN [{target_table}] t
            ON {join_columns}
        WHERE {insert_where_columns};
        """

        delete_sql = f"""
        USE [{db}];
        WITH cte AS (
            SELECT  
                ROW_NUMBER() OVER (
                    PARTITION BY {partition_columns}
                    ORDER BY {order_columns}
                ) rn
             FROM [{target_table}]
        )
        DELETE FROM cte
        WHERE rn > 1;
        """
        merge_sql = f'{update_sql}\n{insert_sql}\n{delete_sql}'
        return merge_sql

    def get_columns(self, db, table):
        df = self.get_schema(db, table)
        columns = df['column_name'].tolist()
        return columns

    def get_schema(self, db, table):
        sql = f"select column_name, data_type from {db}.information_schema.columns where table_name='{table}' order by ordinal_position"
        df = self.pull(sql=sql)
        return df

    def drop(self, db, table):
        sql = f"USE {db}; IF OBJECT_ID('dbo.{table}', 'U') IS NOT NULL DROP TABLE dbo.{table};"
        self.execute(sql=sql)

    def is_match(df, _df):
        is_match = df.equals(_df)
        return is_match
