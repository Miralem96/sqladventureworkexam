import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


def run(q):
    # Försäljningstrend per månad
    sql = """
    SELECT
        YEAR(OrderDate) AS [Year],
        MONTH(OrderDate) AS [MonthNr],
        DATENAME(MONTH, OrderDate) AS [MonthName],
        CONCAT(YEAR(OrderDate), '-', RIGHT('0' + CAST(MONTH(OrderDate) AS nvarchar(2)), 2)) AS MonthLabel,
        SUM(TotalDue) AS TotalSales
    FROM Sales.SalesOrderHeader
    GROUP BY
        YEAR(OrderDate),
        MONTH(OrderDate),
        DATENAME(MONTH, OrderDate)
    ORDER BY
        [Year], [MonthNr];
    """
    df = q(sql)

    # skapar month som ett riktigt datum: YYYY-MM-01
    df['Month'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['MonthNr'].astype(str) + '-01')

    plt.plot(df['Month'], df['TotalSales'])
    plt.title('Försäljningstrend per månad')
    plt.xticks(rotation=45, ha='right')
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: f'${x/1_000_000:.0f}M'))
    plt.tight_layout()
    plt.show()

    max_row = df.loc[df['TotalSales'].idxmax()]
    min_row = df.loc[df['TotalSales'].idxmin()]
    print(f'Högsta månad: {max_row['Month'].date()} ({max_row['TotalSales']:})')
    print(f'Lägsta månad: {min_row['Month'].date()} ({min_row['TotalSales']:})')

    return df