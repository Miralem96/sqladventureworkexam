import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def run(q):
    # Försäljning och antal ordrar per år
    sql = """
    SELECT
        YEAR(OrderDate) AS [Year],
        SUM(TotalDue) AS TotalSales,
        COUNT(*) AS OrderCount
    FROM Sales.SalesOrderHeader
    GROUP BY YEAR(OrderDate)
    ORDER BY [Year];
    """
    df = q(sql)

    plt.figure(figsize=(11,4))
    plt.bar(df['Year'], df['TotalSales'])
    plt.title('Total försäljning per år')
    plt.xticks(df['Year'], df['Year'])
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(11,4))
    plt.bar(df['Year'], df['OrderCount'])
    plt.title('Antal ordrar per år')
    plt.xticks(df['Year'], df['Year'])
    plt.tight_layout()
    plt.show()


    max_sales = df.loc[df['TotalSales'].idxmax()]
    min_sales = df.loc[df["TotalSales"].idxmin()]

    max_orders = df.loc[df['OrderCount'].idxmax()]
    min_orders = df.loc[df['OrderCount'].idxmin()]

    print(f"Högst försäljning: {int(max_sales['Year'])} ({max_sales['TotalSales']:,.0f})")
    print(f"Lägst försäljning: {int(min_sales['Year'])} ({min_sales['TotalSales']:,.0f})")

    print(f"Flest ordrar: {int(max_orders['Year'])} ({int(max_orders['OrderCount'])})")
    print(f"Minst ordrar: {int(min_orders['Year'])} ({int(min_orders['OrderCount'])})")

    return df