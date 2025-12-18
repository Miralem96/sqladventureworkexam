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