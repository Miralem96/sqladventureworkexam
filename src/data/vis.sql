USE AdventureWorks2025;
GO

SELECT top(10) * FROM Production.ProductCategory
SELECT top(10) * FROM Production.ProductSubcategory
SELECT top(10) * FROM Production.Product


/* Steg 1 */

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


/* Steg 2 */

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


/* Steg 3 */

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


/* Steg 4 */

SELECT
    YEAR(OrderDate) AS [Year],
    SUM(TotalDue) AS TotalSales,
    COUNT(*) AS OrderCount
FROM Sales.SalesOrderHeader
GROUP BY YEAR(OrderDate)
ORDER BY [Year];

/* Steg 5 */

SELECT TOP 10
    p.Name AS Product,
    SUM(sod.LineTotal) AS TotalSales
FROM Sales.SalesOrderDetail sod
JOIN Production.Product p
    ON p.ProductID = sod.ProductID
GROUP BY p.Name
ORDER BY TotalSales DESC;

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


/* Steg 6 */

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