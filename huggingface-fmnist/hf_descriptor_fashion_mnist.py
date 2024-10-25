import duckdb
import mlcroissant as mlc

## 1. Point to the Croissant file
url = "https://huggingface.co/api/datasets/fashion_mnist/croissant"
ds = mlc.Dataset(url)
metadata = ds.metadata.to_json()

## 2. Print basic information
print(f"{metadata['name']}: {metadata['description']}")

## 3. Inspect the distribution
print("Distribution inspect", metadata['distribution'])
for item in metadata['distribution']:
    if 'contentUrl' in item:
        print(f"{item['@type']} -> contentUrl: {item['contentUrl']}, encodingFormat: {item['encodingFormat']}")

## 4. Get the correct record set ID from metadata
record_set_id = metadata['recordSet'][0]['@id']  # Should be "fashion_mnist"
print(f"Using record set ID: {record_set_id}")


## 5. Print all available record sets to make sure we're using the correct ID
for record_set in metadata['recordSet']:
    print(f"Available record set: {record_set['@id']}")


####################################################################
## Read the records from the dataset using DuckDB

# 1. Setup DuckDB
con = duckdb.connect()
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# 2. Define the working URLs for train and test sets
train_url = "https://huggingface.co/datasets/zalando-datasets/fashion_mnist/resolve/refs%2Fconvert%2Fparquet/fashion_mnist/train/0000.parquet"
test_url = "https://huggingface.co/datasets/zalando-datasets/fashion_mnist/resolve/refs%2Fconvert%2Fparquet/fashion_mnist/test/0000.parquet"

try:
    # 3. Create a temporary view for the data
    con.execute(f"""
    CREATE OR REPLACE VIEW fashion_mnist_data AS 
    SELECT * FROM read_parquet('{train_url}');
    """)

    # 4. Create the label mappings
    con.execute("""
    CREATE OR REPLACE TEMP TABLE label_mapping AS 
    SELECT * FROM (
        VALUES 
            (0, 'T-shirt/Top'),
            (1, 'Trouser'),
            (2, 'Pullover'),
            (3, 'Dress'),
            (4, 'Coat'),
            (5, 'Sandal'),
            (6, 'Shirt'),
            (7, 'Sneaker'),
            (8, 'Bag'),
            (9, 'Ankle Boot')
    ) AS t(label_id, label_name);
    """)

    # 5. Show total records
    count_query = "SELECT COUNT(*) as total_count FROM fashion_mnist_data;"
    print("Total records:", con.execute(count_query).fetchall())

    # 6. Distribution query
    distribution_query = """
    SELECT 
        lm.label_name,
        COUNT(*) as count,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
    FROM fashion_mnist_data fmd
    JOIN label_mapping lm ON fmd.label = lm.label_id
    GROUP BY lm.label_id, lm.label_name
    ORDER BY lm.label_id;
    """
    
    # print("\nLabel distribution with names:")
    # result = con.execute(distribution_query).fetchall()
    # for row in result:
    #     print(f"Label: {row[0]:<12} Count: {row[1]:<6} Percentage: {row[2]}%")

    # 7. Fixed category statistics query
    category_stats_query = """
    SELECT 
        lm.label_id,
        lm.label_name,
        COUNT(*) as sample_count,
        COUNT(DISTINCT fmd.label) as unique_labels
    FROM fashion_mnist_data fmd
    JOIN label_mapping lm ON fmd.label = lm.label_id
    GROUP BY lm.label_id, lm.label_name
    ORDER BY lm.label_id;
    """
    
    print("\nCategory statistics:")
    stats_results = con.execute(category_stats_query).fetchall()
    for row in stats_results:
        print(f"Category ID: {row[0]}, Name: {row[1]:<12} Samples: {row[2]:<6} Unique Labels: {row[3]}")

    # # 8. Get data for a specific category
    # def get_category_data(category_name):
    #     category_query = f"""
    #     SELECT 
    #         lm.label_name,
    #         COUNT(*) as count,
    #         MIN(fmd.label) as min_label,
    #         MAX(fmd.label) as max_label
    #     FROM fashion_mnist_data fmd
    #     JOIN label_mapping lm ON fmd.label = lm.label_id
    #     WHERE lm.label_name = '{category_name}'
    #     GROUP BY lm.label_name;
    #     """
    #     return con.execute(category_query).fetchall()

    # # Example: Get data for specific categories
    # print("\nDetailed category information:")
    # for category in ['T-shirt/Top', 'Trouser', 'Dress']:
    #     results = get_category_data(category)
    #     for row in results:
    #         print(f"\nCategory: {row[0]}")
    #         print(f"Total samples: {row[1]}")
    #         print(f"Label range: {row[2]} to {row[3]}")

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    print(traceback.format_exc())
    
finally:
    # 9. Clean up
    con.execute("DROP VIEW IF EXISTS fashion_mnist_data")
    con.execute("DROP TABLE IF EXISTS label_mapping")

# 10. Function to get specific category data (can be called after cleanup)
def analyze_category(category_name):
    try:
        # Recreate the view and mapping table
        con.execute(f"CREATE OR REPLACE VIEW fashion_mnist_data AS SELECT * FROM read_parquet('{train_url}')")
        con.execute("""
        CREATE OR REPLACE TEMP TABLE label_mapping AS 
        SELECT * FROM (VALUES 
            (0, 'T-shirt/Top'), (1, 'Trouser'), (2, 'Pullover'), (3, 'Dress'),
            (4, 'Coat'), (5, 'Sandal'), (6, 'Shirt'), (7, 'Sneaker'),
            (8, 'Bag'), (9, 'Ankle Boot')
        ) AS t(label_id, label_name);
        """)
        
        query = f"""
        SELECT 
            lm.label_name,
            COUNT(*) as count
        FROM fashion_mnist_data fmd
        JOIN label_mapping lm ON fmd.label = lm.label_id
        WHERE lm.label_name = '{category_name}'
        GROUP BY lm.label_name;
        """
        return con.execute(query).fetchall()
    finally:
        con.execute("DROP VIEW IF EXISTS fashion_mnist_data")
        con.execute("DROP TABLE IF EXISTS label_mapping")


result = analyze_category('Pullover')
print(f"\nQuery for Pullover:")
print(f"Count: {result[0][1]}")



# def get_sample_images(label_name, limit=5):
#     sample_query = f"""
#     SELECT 
#         lm.label_name,
#         fmd.image
#     FROM fashion_mnist_data fmd
#     JOIN label_mapping lm ON fmd.label = lm.label_id
#     WHERE lm.label_name = '{label_name}'
#     LIMIT {limit};
#     """
#     return con.execute(sample_query).fetchall()

# # Example usage:
# print("\nGetting sample images for Pullover:")
# samples = get_sample_images('Pullover', limit=3)
# for i, sample in enumerate(samples, 1):
#     print(f"Sample {i} from category {sample[0]}")


