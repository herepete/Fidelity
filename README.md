# Fidelity

Introduction
============
using beautifulsoup and the Fidelity API to get data back from Fidelity.co.uk

Fidelity has a good site
But there were a few financical bits i wanted to see which aren't easily viewable on 1 page.
1) check current price of funds v a benchmark i have set
2) check which funds have an overlap in their portfolio

This is version 3 , version 1 and 2 were build on a local machine, 
the main difference being version 3 where possible makes use of the Fidelity API

the key thing to understand in the API is the ISIN number which is a unique value per fund.

Key Urls/Api
============

Key statisitcs https://www.fidelity.co.uk/factsheet-data/factsheet/{ISIN}/key-statistics

Growth https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/growthChart

Performance https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/performance

Charges and Documents https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/chargesAndDocs

Dividends https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/dividends

Portfolio https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/portfolio

Risk and Rating https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/riskAndRating

Managment https://www.fidelity.co.uk/factsheet-data/api/factsheet/{ISIN}/fundManagement

Steps to get running
====================

written in python3.6 (anything less than version 3.6 it will error due to string formatting)
beautiful soup and requests have been installed in pip

edit the stockstocheck.txt as needed ( format: fundname, ISIN number, benchmark cost)

fundname -can be anything you want, (note if its to long the print formatting will look odd)

ISIN number - found on the funds page

Benchmark cost - enter a price here, i entered a price on the last day i invested so if the fund went up or down against the benchmark it was easy for me to see.

Run python script

Notes
======
i have put a 1 second delay (which can be edited in memory) in between each external call to stop hammering of Fidelity.

Example
=======

```
./version3.py
Enter your options:
1) For current % change in Fidelity Pension
2) Overlapping portfolio
2
Ok i am going to start but due to rate limiting each request will wait 1 second before running
Here is what is duplicated in the portfolio...
Alphabet Inc A           Fidelity global
Alphabet Inc A           Vanguard Dev World
Amazon.com Inc           Rathbourne
Amazon.com Inc           Vanguard Dev World
Apple Inc                Fidelity global
Apple Inc                Vanguard Dev World
Facebook Inc A           Fundsmith
Facebook Inc A           Vanguard Dev World
Intuit Inc               Fundsmith
Intuit Inc               Rathbourne
L'Oreal SA               Fundsmith
L'Oreal SA               Glg Europe
Microsoft Corp           Fidelity global
Microsoft Corp           Fundsmith
Microsoft Corp           Vanguard Dev World
PayPal Holdings Inc      Fundsmith
PayPal Holdings Inc      Rathbourne
SAP SE                   Fidelity global
SAP SE                   Glg Europe
```





```
./version3.py
Enter your options:
1) For current % change in Fidelity Pension
2) Overlapping portfolio
1
Ok i am going to start but due to rate limiting each request will wait 1 second before running
Fund                     Current Price            Historic Price           % Change
Japanese fund            3.23                     3.22                     0.3
Fidelity global          5.418                    5.37                     0.9
Fidelity pacific         2.37                     2.285                    3.7
Fundsmith                5.7001                   5.64                     1.1
Hsbc Ftse                5.9189                    5.91                    0.2
Glg Europe               7.8                      7.71                     1.2
Marlborough Ss           22.56                    22.68                    -0.5
Rathbourne               1.73                     1.71                     1.2
Vanguard Dev World       464.4838                 464.43                   0.0
```

Installation
============

```
pip3.6 install bs4
git clone https://github.com/herepete/Fidelity.git
```
