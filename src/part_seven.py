import matplotlib.pyplot as plt

def run(q):
    # Genomsnittligt ordervärde per region + kundtyp (Store vs Individual)
    sql = """
    WITH base AS (
        SELECT
            st.Name AS Region,
            CASE WHEN c.StoreID IS NOT NULL THEN 'Store' ELSE 'Individual' END AS CustomerType,
            COUNT(*) AS OrderCount,
            SUM(soh.TotalDue) AS TotalSales
        FROM Sales.SalesOrderHeader soh
        JOIN Sales.SalesTerritory st ON st.TerritoryID = soh.TerritoryID
        JOIN Sales.Customer c ON c.CustomerID = soh.CustomerID
        LEFT JOIN Sales.Store s ON s.BusinessEntityID = c.StoreID
        GROUP BY st.Name, CASE WHEN c.StoreID IS NOT NULL THEN 'Store' ELSE 'Individual' END
    )
    SELECT
        Region,
        CustomerType,
        (TotalSales * 1.0) / NULLIF(OrderCount, 0) AS AvgOrderValue,
        TotalSales,
        OrderCount
    FROM base;
    """
    df = q(sql)

    region_total = (
        df.groupby('Region')
          .apply(lambda x: x['TotalSales'].sum() / x['OrderCount'].sum())
          .sort_values(ascending=False)
    )
    order = region_total.index.tolist()

    pivot = df.pivot(index='Region', columns='CustomerType', values='AvgOrderValue').reindex(order)

    x = list(range(len(pivot)))
    width = 0.4

    plt.figure(figsize=(11,6))
    plt.bar([i - width/2 for i in x], pivot.get('Store'), width=width, label='Store')
    plt.bar([i + width/2 for i in x], pivot.get('Individual'), width=width, label='Individual')
    plt.title('Genomsnittligt ordervärde per region och kundtyp')
    plt.xticks(x, pivot.index, rotation=45, ha='right')
    plt.ylabel('Genomsnittligt ordervärde')
    plt.tight_layout()
    plt.legend()
    plt.show()

    avg_store = df[df['CustomerType']=='Store']['TotalSales'].sum() / df[df['CustomerType']=='Store']['OrderCount'].sum()
    avg_ind   = df[df['CustomerType']=='Individual']['TotalSales'].sum() / df[df['CustomerType']=='Individual']['OrderCount'].sum()
    print(f'Totalt genomsnitt Store: {avg_store:}')
    print(f'Totalt genomsnitt Individual: {avg_ind:}')
    print('Högst totalt:', 'Store' if avg_store > avg_ind else 'Individual')

    best = df.loc[df['AvgOrderValue'].idxmax()]
    print(f'Högst region+kundtyp: {best['Region']} / {best['CustomerType']} ({best['AvgOrderValue']:})')

    return df