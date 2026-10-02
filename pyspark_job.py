from pyspark.sql.functions import col

def clean_data(df):
    """
    Cleans the input DataFrame based on specific business rules.
    """
    # remove rows where amount <= 0 and where name is NULL
    filtered_df = df.filter((col("amount") > 0) & (col("name").isNotNull()))
    
    # add a column amount_with_tax calculated as amount * 1.20
    final_df = filtered_df.withColumn("amount_with_tax", col("amount") * 1.20)
    
    return final_df
