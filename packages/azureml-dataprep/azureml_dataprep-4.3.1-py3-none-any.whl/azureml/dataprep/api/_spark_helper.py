from ._loggerfactory import _LoggerFactory
logger = _LoggerFactory.get_logger('SparkHelper')


def _to_spark_dataframe_native(script, spark_session):
    raise NotImplementedError()


def _get_spark_version(spark_session):
    from pyspark.util import VersionUtils
    version_string = spark_session.sparkContext.version
    major_version, minor_version = VersionUtils.majorMinorVersion(version_string)
    return version_string, major_version, minor_version


def _get_schema(script, executor):
    __TYPE_MAP = {
        'date64': 'date',
        'decimal128': 'decimal',
        'float64': 'double',
        'float32': 'float',
        'int8': 'byte',
        'int16': 'short',
        'int32': 'integer',
        'int64': 'long',
        'timestamp[ns]': 'timestamp',
        'list': 'array',
    }

    #record_batches, _, _ = executor.execute_rsdataflow(script, True, [0])
    record_batches, _ = executor.execute_dataflow(
        script,
        True,
        False,
        False,
        False,
        '',
        [0])

    def formatter(field):
        return f'`{field.name}`: {__TYPE_MAP.get(field.type, field.type)}'

    return ', '.join(formatter(field) for field in record_batches[0].schema)


def _get_partitions(script, executor):
    return executor.get_partition_count(script)


def _get_schema_and_partitions(script):
    from azureml.dataprep.api._rslex_executor import get_rslex_executor
    executor = get_rslex_executor()
    return _get_schema(script, executor), _get_partitions(script, executor)


def _to_spark_dataframe_2x_pandas_apply(script, spark_session) -> 'pyspark.sql.DataFrame':
    import pandas
    from pyspark.sql.functions import col, pandas_udf, PandasUDFType

    import os
    run_token = os.environ['AZUREML_RUN_TOKEN']
    run_token_expiry = os.environ['AZUREML_RUN_TOKEN_EXPIRY']

    schema, num_partitions = _get_schema_and_partitions(script)
    logger.info('[_to_spark_dataframe_2x_pandas_apply] Got schema and partition count from dataflow.')

    @pandas_udf(schema, PandasUDFType.GROUPED_MAP)
    def fetch_partitions(partition_df):
        from azureml.dataprep.api._rslex_executor import get_rslex_executor
        
        import os
        os.environ['AZUREML_RUN_TOKEN'] = run_token
        os.environ['AZUREML_RUN_TOKEN_EXPIRY'] = run_token_expiry

        partitions_to_fetch = []
        for row in partition_df.iloc:
            partitions_to_fetch.append(row['id'])

        executor = get_rslex_executor()
        #record_batches, _, _ = executor.execute_rsdataflow(script, True, partitions_to_fetch)
        record_batches, _ = executor.execute_dataflow(
            script,
            True,
            False,
            False,
            False,
            '',
            partitions_to_fetch)

        return pandas.concat([record_batch.to_pandas() for record_batch in record_batches])

    partition_sdf = spark_session.range(0, num_partitions).withColumn('id', col('id'))
    logger.info('[_to_spark_dataframe_2x_pandas_apply] Created a partition dataframe.')

    return partition_sdf.groupby('id').apply(fetch_partitions)


def _to_spark_dataframe_3x_pandas_map(script, spark_session) -> 'pyspark.sql.DataFrame':
    import pandas
    from pyspark.sql.functions import col
    from typing import Iterator

    import os
    run_token = os.environ['AZUREML_RUN_TOKEN']
    run_token_expiry = os.environ['AZUREML_RUN_TOKEN_EXPIRY']

    def fetch_partitions(partition_dfs: Iterator[pandas.DataFrame]) -> Iterator[pandas.DataFrame]:
        from azureml.dataprep.api._rslex_executor import get_rslex_executor

        import os
        os.environ['AZUREML_RUN_TOKEN'] = run_token
        os.environ['AZUREML_RUN_TOKEN_EXPIRY'] = run_token_expiry

        partitions_to_fetch = []
        for partition_df in partition_dfs:
            for row in partition_df.iloc:
                partitions_to_fetch.append(row['id'])

        executor = get_rslex_executor()
        #record_batches, _, _ = executor.execute_rsdataflow(script, True, partitions_to_fetch)
        record_batches, _ = executor.execute_dataflow(
            script,
            True,
            False,
            False,
            False,
            '',
            partitions_to_fetch)
        for record_batch in record_batches:
            yield record_batch.to_pandas()
    
    schema, num_partitions = _get_schema_and_partitions(script)
    logger.info('[_to_spark_dataframe_3x_pandas_map] Got schema and partition count from dataflow.')
    partition_sdf = spark_session.range(0, num_partitions).withColumn('id', col('id'))
    logger.info('[_to_spark_dataframe_3x_pandas_map] Created a partition dataframe.')

    return partition_sdf.mapInPandas(fetch_partitions, schema=schema)


def read_spark_dataframe(script, spark_session):
    try:
        # attempt to use a spark native implementation for parsing the script.
        return _to_spark_dataframe_native(script, spark_session)
    except NotImplementedError:
        logger.info('[read_spark_dataframe] Native implementation failed to parse dataflow.')
        pass

    # this script isn't parseable by the spark native implementation. Use dataprep instead.
    v_string, v_major, v_minor = _get_spark_version(spark_session)
    logger.info(f'[read_spark_dataframe] Running on spark version \'{v_string}\'')

    if v_major == 3:
        # We're on Spark [3.0, 4.0). Use the mapInPandas API.
        logger.info('[read_spark_dataframe] Attempting to use the pyspark.sql.DataFrame.mapInPandas implementation to fetch data.')
        return _to_spark_dataframe_3x_pandas_map(script, spark_session)
    elif v_major == 2 and v_minor >= 3:
        # We're on Spark [2.3, 3.0). Use the apply API.
        logger.info('[read_spark_dataframe] Attempting to use the pyspark.sql.GroupedData.apply implementation to fetch data.')
        return _to_spark_dataframe_2x_pandas_apply(script, spark_session)
    else:
        logger.error('[read_spark_dataframe] This version of spark is not supported.')
        raise NotImplementedError(f'to_spark_dataframe() is only supported on Spark verisons [2.3, 4.0), Spark {v_string} is not supported.')
