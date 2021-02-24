# Fidelity

Introduction
============
using beautifulsoup and the Fidelity API to get data back from Fidelity.co.uk

Fidelity has a good site
But there were a few financical bits i wanted to see which aren't easily viewable on 1 page.
1) check current price of funds v a benchmark i have set
2) check which funds have an overlap in their portfolio

This is version 3 , version 1 and 2 were build on a local machine, 
the main difference being version 3 where possible makes use of the Fidelity API (which is a lot nicer than trying to scrape data from a webpage)

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

Pre-REquistses
==============
written in python3.6 (anything less than version 3.6 it will error due to string formatting)
beautiful soup and requests have been installed in pip.
Need to be run in Linux as commands such as `clear` are called.

Steps to get running
====================

Edit the stockstocheck.txt as needed ( format: fundname, ISIN number, benchmark cost):

* fundname -can be anything you want, (note if its to long the print formatting will look odd)

* ISIN number - found on the funds page

* Benchmark cost - enter a price here, i entered a price on the last day i invested so if the fund went up or down against the benchmark it was easy for me to see.

Run python script

Example
=======
Help Options
```
# ./version3.py -h
usage: version3.py [-h] [-v] [-t] [-tt]

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  increase output verbosity
  -t, --timer    add timer to output to help troubleshoot
  -tt, --etimer  a much more in depth add timer to output to help troubleshoot

```

For current % change in Fidelity Pension
```
# ./version3.py
Enter your options:
1) For current % change in Fidelity Pension
2) Overlapping portfolio
3) Search for funds (if you want up to date funds run step 9 first)
There are 3 tests:
    A) Is the fund beating the 5 year annualized return of the fund
    B) Does the Fund have a 'Above Average' or 'High' 3 and 5 year Morningstar return values
    C) Is it an accumlation fund (i.e not an income fund)
9) Load all funds - (about 3,000)
10) Load 2 finds - used in testing
11) Load 100 funds - used in testing
12) Load 500 funds - used in testing
1
Ok i am going to start but due to rate limiting each request will wait 0 second before running
Fund                     Current Price            Historic Price           % Change
Japanese fund            3.13                     3.22                     -2.8
Fidelity global          5.20                     5.37                     -3.2
Fidelity pacific         2.303                    2.389                    -3.6
Fundsmith                5.4963                   5.64                     -2.5
Hsbc Ftse                5.9656                    5.91                    0.9
Glg Europe               7.38                     7.38                     0
Marlborough Ss           22.29                    22.68                    -1.7
Rathbourne               1.63                     1.63                     0
Vanguard Dev World       450.9346                 464.43                   -2.9
Jpm US Small Cap         12.84                    12.95                    -0.8

Press a button to continue
```

Overlapping portfolio
```
# ./version3.py
Enter your options:
1) For current % change in Fidelity Pension
2) Overlapping portfolio
3) Search for funds (if you want up to date funds run step 9 first)
There are 3 tests:
    A) Is the fund beating the 5 year annualized return of the fund
    B) Does the Fund have a 'Above Average' or 'High' 3 and 5 year Morningstar return values
    C) Is it an accumlation fund (i.e not an income fund)
9) Load all funds - (about 3,000)
10) Load 2 finds - used in testing
11) Load 100 funds - used in testing
12) Load 500 funds - used in testing
2
Ok i am going to start but due to rate limiting each request will wait 0 second before running
Here is what is duplicated in the portfolio...
Alphabet Inc A           Fidelity global
Alphabet Inc A           Vanguard Dev World
Amazon.com Inc           Rathbourne
Amazon.com Inc           Vanguard Dev World
Apple Inc                Fidelity global
Apple Inc                Vanguard Dev World
Facebook Inc A           Fundsmith
Facebook Inc A           Vanguard Dev World
Freshpet Inc             Jpm US Small Cap
Freshpet Inc             Rathbourne
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
load 500 records
```
[root@g4 Fidelity]# ./version3.py
Enter your options:
1) For current % change in Fidelity Pension
2) Overlapping portfolio
3) Search for funds (if you want up to date funds run step 9 first)
There are 3 tests:
    A) Is the fund beating the 5 year annualized return of the fund
    B) Does the Fund have a 'Above Average' or 'High' 3 and 5 year Morningstar return values
    C) Is it an accumlation fund (i.e not an income fund)
9) Load all funds - (about 3,000)
10) Load 2 finds - used in testing
11) Load 100 funds - used in testing
12) Load 500 funds - used in testing
12
500 funds read in to fidelity_funds.csv
Press a button to continue

```

Search for funds in that 500
```
Enter your options:
1) For current % change in Fidelity Pension
2) Overlapping portfolio
3) Search for funds (if you want up to date funds run step 9 first)
There are 3 tests:
    A) Is the fund beating the 5 year annualized return of the fund
    B) Does the Fund have a 'Above Average' or 'High' 3 and 5 year Morningstar return values
    C) Is it an accumlation fund (i.e not an income fund)
9) Load all funds - (about 3,000)
10) Load 2 finds - used in testing
11) Load 100 funds - used in testing
12) Load 500 funds - used in testing
3

500  Funds at this stage - Read In
2.0 % done
5.0 % done
10.0 % done
15.0 % done
20.0 % done
35.0 % done
50.0 % done
75.0 % done
100.0 % done

42  Funds at this stage - Beat Index
23.81 % done
59.52 % done

42  Funds at this stage - Beat Morning star rating

Summary
======
Here is a full list of funds which hit your parameters

Fund Name                                         Points above 5 year Annualized return             ISIN
Baillie Gifford American B Acc                    21                                                GB0006061963
Baillie Gifford Global Discovery B Acc            17                                                GB0006059330
Baillie Gifford Global Stewardship B Acc          14                                                GB00BYNK7G95
Baillie Gifford Pacific B Acc                     12                                                GB0006063233
Baillie Gifford European B Acc                    10                                                GB0006058258
Baillie Gifford Managed B Acc                     9                                                 GB0006010168
Baillie Gifford Em Mkts Lead Coms B Acc           8                                                 GB00B06HZN29
Baillie Gifford Emerging Mkts Gr B Acc            7                                                 GB0006020647
Baillie Gifford UK Equity Alpha B Acc             7                                                 GB0005858195
Baillie Gifford Global Alpha Gr B Acc             6                                                 GB00B61DJ021
Baillie Gifford International B Acc               6                                                 GB0005941272
Aegon Global Equity GBP B Acc                     5                                                 GB0007274516
Allianz Continental European C Acc                5                                                 GB00B3Q8YX99
ASI UK Mid-Cap Equity I Acc                       5                                                 GB00B0XWNT29
ASI UK Responsible Equity I Acc                   5                                                 GB00B131GD17
AXA Framlington Global Technology Z Acc           5                                                 GB00B4W52V57
Baillie Gifford Japanese B Acc                    5                                                 GB0006011133
Allianz Total Return Asian Equity C Acc           4                                                 GB00BVYJ2G95
Artemis US Smaller Companies I Acc GBP            4                                                 GB00BMMV5766
ASI Europe ex UK Equity I Acc                     4                                                 GB00B0LG6P37
ASI Global Smaller Companies P1 Acc               4                                                 GB00B7KVX245
Aviva Investors Multi-Mgr Flexible 2£Acc          4                                                 GB00B1N95279
Aviva Investors UK Lstd S&M Cap2 GBP Acc          4                                                 GB0004460571
Baillie Gifford Global Inc Growth B Acc           4                                                 GB0005772479
Baillie Gifford Japan Small Co B Acc              4                                                 GB0006014921

Press any button to continue

```

Installation
============

```
pip3.6 install bs4
git clone https://github.com/herepete/Fidelity.git
```
