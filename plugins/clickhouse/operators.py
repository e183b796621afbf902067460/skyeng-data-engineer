from airflow.decorators import task


@task()
def PandasDataFrameToClickHouseOperator(df, table, engine):
    import pandas as pd

    pd.DataFrame.from_dict(data=df).to_sql(name=table, con=engine, if_exists='append', index=False)
