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

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11,7), sharex=True)
    fig.suptitle("Försäljning och antal ordrar per år")

    # Försäljning
    ax1.bar(df["Year"], df["TotalSales"])
    ax1.set_ylabel("Total försäljning")

    # Ordrar
    ax2.bar(df["Year"], df["OrderCount"])
    ax2.set_ylabel("Antal ordrar")
    ax2.set_xticks(df["Year"])
    ax2.set_xticklabels(df["Year"])

    plt.tight_layout()
    plt.show()



    max_sales = df.loc[df['TotalSales'].idxmax()]
    min_sales = df.loc[df["TotalSales"].idxmin()]

    max_orders = df.loc[df['OrderCount'].idxmax()]
    min_orders = df.loc[df['OrderCount'].idxmin()]

    print(f"Högst försäljning: {int(max_sales['Year'])} ({max_sales['TotalSales']:})")
    print(f"Lägst försäljning: {int(min_sales['Year'])} ({min_sales['TotalSales']:})")

    print(f"Flest ordrar: {int(max_orders['Year'])} ({int(max_orders['OrderCount'])})")
    print(f"Minst ordrar: {int(min_orders['Year'])} ({int(min_orders['OrderCount'])})")

    return df