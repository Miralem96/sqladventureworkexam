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

    return df