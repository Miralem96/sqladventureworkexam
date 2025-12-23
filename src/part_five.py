import matplotlib.pyplot as plt

def run(q):
    # Top 10 produkter
    sql = """
    SELECT TOP 10
        p.Name AS Product,
        SUM(sod.LineTotal) AS TotalSales
    FROM Sales.SalesOrderDetail sod
    JOIN Production.Product p
        ON p.ProductID = sod.ProductID
    GROUP BY p.Name
    ORDER BY TotalSales DESC;
    """
    df = q(sql)

    df_plot = df.sort_values('TotalSales', ascending=True)
    plt.figure(figsize=(11,6))
    plt.barh(df_plot['Product'], df_plot['TotalSales'])
    plt.title('top 10 produkter efter försäljning')
    plt.xlabel('Total försäljning')
    plt.tight_layout()
    plt.show()

    top1 = df.iloc[0]
    print(f'#1 produkt: {top1['Product']} ({top1['TotalSales']:})')

    sql2 = """
    SELECT TOP 10
        pc.Name AS Category,
        p.Name AS Product,
        SUM(sod.LineTotal) AS TotalSales
    FROM Sales.SalesOrderDetail sod
    JOIN Production.Product p ON p.ProductID = sod.ProductID
    JOIN Production.ProductSubcategory psc ON psc.ProductSubcategoryID = p.ProductSubcategoryID
    JOIN Production.ProductCategory pc ON pc.ProductCategoryID = psc.ProductCategoryID
    GROUP BY pc.Name, p.Name
    ORDER BY TotalSales DESC;
    """
    df2 = q(sql2)
    print('Kategori fördelning i top 10:')
    print(df2['Category'].value_counts())
    print('Dominerande kategori', df2['Category'].value_counts().idxmax())

    return df