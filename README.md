# Fidelity
using beautifulsoup and Fidelity API to get data back from Fidelity.co.uk

Fidelity has a good site
But there were a few financical bits i wanted to see which aren't easily viewable on 1 page.

This is version 3 , version 1 and 2 were build on a local machine, 
the main difference being version 3 where possible makes use of the Fidelity API

the key thing to understand in the API is the ISIN number which is a unique value per fund.

Key statisitcs https://www.fidelity.co.uk/factsheet-data/factsheet/{ISIN}/key-statistics
Growth https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/growthChart
Performance https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/performance
Charges and Documents https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/chargesAndDocs
Dividends https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/dividends
Portfolio https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/portfolio
Risk and Rating https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/riskAndRating
Managment https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/fundManagement

