import matplotlib.pyplot as plt
import numpy as np

def run(q):
    # Försäljning + unika kunder per region
    sql = """
    SELECT
        st.Name AS Region,
        SUM(soh.TotalDue) AS TotalSales,
        COUNT(DISTINCT c.CustomerID) AS UniqueCustomers
    FROM Sales.SalesOrderHeader soh
    JOIN Sales.SalesTerritory st
        ON st.TerritoryID = soh.TerritoryID
    JOIN Sales.Customer c
        ON c.CustomerID = soh.CustomerID
    GROUP BY st.Name
    ORDER BY TotalSales DESC;
    """
    df = q(sql).sort_values('TotalSales', ascending=False).reset_index(drop=True)

    regions = df['Region'].values
    sales = df['TotalSales'].values
    customers = df['UniqueCustomers'].values

    x = np.arange(len(regions))
    w = 0.4

    fig, ax1 = plt.subplots(figsize=(12,5))

    # blå = försäljning (vänster)
    ax1.bar(x - w/2, sales, width=w, color='tab:blue', label='Försäljning')
    ax1.set_ylabel('Försäljning')
    ax1.set_xticks(x)
    ax1.set_xticklabels(regions, rotation=45, ha='right')

    # orange = unika kunder (höger)
    ax2 = ax1.twinx()
    ax2.bar(x + w/2, customers, width=w, color='tab:orange', alpha=1, label='Unika kunder')
    ax2.set_ylabel('Unika kunder')

    plt.title('Försäljning och antal kunder per region')
    plt.tight_layout()
    plt.show()

    best = df.iloc[0]
    worst = df.iloc[-1]
    print(f'Starkast region: {best['Region']} ({best['TotalSales']:})')
    print(f'Svagast region: {worst['Region']} ({worst['TotalSales']:})')
    print(f'{best['Region']} sales/kund: {best['TotalSales']/best['UniqueCustomers']:}')

    return df