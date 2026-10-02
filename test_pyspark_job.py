import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark_job import clean_data

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("pytest_pyspark").getOrCreate()

def test_clean_data(spark):
    # Define schema and mock data covering all test scenarios[cite: 1]
    schema = StructType([
        StructField("name", StringType(), True),
        StructField("amount", DoubleType(), True)
    ])
    
    data = [
        ("Alice", 100.0),   # Valid record[cite: 1]
        ("Bob", 0.0),       # Amount <= 0[cite: 1]
        ("Charlie", -50.0), # Amount <= 0[cite: 1]
        (None, 200.0)       # NULL name[cite: 1]
    ]
    
    df = spark.createDataFrame(data, schema)
    result_df = clean_data(df)
    results = result_df.collect()

    # verify invalid records are removed and valid records are kept
    assert len(results) == 1
    assert results[0]["name"] == "Alice"
    
    # Vverify amount_with_tax is calculated correctly (100.0 * 1.20 = 120.0)[cite: 1]
    assert results[0]["amount_with_tax"] == 120.0
