import matplotlib.pyplot as plt

def run(q):
    # Antal unika produkter per kategori
    sql = """
    SELECT
        pc.Name AS Category,
        COUNT(DISTINCT p.ProductID) AS ProductCount
    FROM Production.ProductCategory pc
    JOIN Production.ProductSubcategory psc
        ON psc.ProductCategoryID = pc.ProductCategoryID
    JOIN Production.Product p
        ON p.ProductSubcategoryID = psc.ProductSubcategoryID
    GROUP BY pc.Name
    ORDER BY ProductCount DESC;
    """
    df = q(sql)

    plt.figure(figsize=(11,6))
    plt.bar(df['Category'], df['ProductCount'])
    plt.title('Antal produkter per kategori')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Antal produkter')
    plt.tight_layout()
    plt.show()

    max_row = df.loc[df["ProductCount"].idxmax()]
    min_row = df.loc[df["ProductCount"].idxmin()]
    print(f'Flest produkter: {max_row['Category']} ({int(max_row['ProductCount'])})')
    print(f'Minst produkter: {min_row['Category']} ({int(min_row['ProductCount'])})')

    return df

