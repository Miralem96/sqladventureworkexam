import matplotlib.pyplot as plt

def run(q):
    # Total försäljning per produktkategori
    sql = """
    SELECT
        pc.Name AS Category,
        SUM(sod.LineTotal) AS TotalSales
    FROM Sales.SalesOrderDetail sod
    JOIN Production.Product p
        ON p.ProductID = sod.ProductID
    JOIN Production.ProductSubcategory psc
        ON psc.ProductSubcategoryID = p.ProductSubcategoryID
    JOIN Production.ProductCategory pc
        ON pc.ProductCategoryID = psc.ProductCategoryID
    GROUP BY pc.Name
    ORDER BY TotalSales DESC;
    """
    df = q(sql)

    df_plot = df.sort_values('TotalSales', ascending=True)
    plt.figure(figsize=(11,6))
    plt.barh(df_plot['Category'], df_plot['TotalSales'])
    plt.title('Total försäljning per produktkategori')
    plt.xlabel('Total försäljning')
    plt.tight_layout()
    plt.show()

    max_row = df.loc[df['TotalSales'].idxmax()]
    min_row = df.loc[df["TotalSales"].idxmin()]
    print(f'Störst försäljning: {max_row['Category']} ({max_row['TotalSales']:})')
    print(f'Minst försäljning: {min_row['Category']} ({min_row['TotalSales']:})')

    return df