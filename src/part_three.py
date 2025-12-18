import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


def run(q):
    # Steg 3: Försäljningstrend per månad
    sql = """
    SELECT
        DATEFROMPARTS(YEAR(OrderDate), MONTH(OrderDate), 1) AS [Month],
        CONCAT(YEAR(OrderDate), '-', RIGHT('0' + CAST(MONTH(OrderDate) AS NVARCHAR(2)), 2)) AS MonthLabel,
        DATENAME(MONTH, DATEFROMPARTS(YEAR(OrderDate), MONTH(OrderDate), 1)) AS MonthName,
        SUM(TotalDue) AS TotalSales,
        AVG(DATEDIFF(DAY, OrderDate, DueDate)) AS AvgDaysToDue,
        DATEADD(MONTH, 1, DATEFROMPARTS(YEAR(OrderDate), MONTH(OrderDate), 1)) AS NextMonth
    FROM Sales.SalesOrderHeader
    GROUP BY
        DATEFROMPARTS(YEAR(OrderDate), MONTH(OrderDate), 1),
        YEAR(OrderDate),
        MONTH(OrderDate)
    ORDER BY [Month];
    """
    df = q(sql)
    df['Month'] = pd.to_datetime(df['Month'])

    plt.figure(figsize=(11,6))
    plt.plot(df["Month"], df['TotalSales'])
    plt.title('Försäljningstrend per månad')
    plt.xlabel('Månad')
    plt.ylabel('Total försäljning')
    plt.xticks(rotation=50, ha='right')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: f'${x/1_000_000:.0f}M'))
    plt.tight_layout()
    plt.show()

    max_row = df.loc[df["TotalSales"].idxmax()]
    min_row = df.loc[df["TotalSales"].idxmin()]
    print(f'Högsta månad: {max_row['Month'].date()} ({max_row['TotalSales']:})')
    print(f'Lägsta månad: {min_row['Month'].date()} ({min_row['TotalSales']:})')

    return df