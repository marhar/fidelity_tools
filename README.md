# fidelity\_tools -- Extracting and working with data from Fidelity.

Here are a couple of tools that make it easy to download your financial
data stored at Fidelity.

- fix\-fidelity\_csv.sql (duckdb script)
- parse\_fullview\_networth\_html.py
- repair\_positions\_download.py (coming)
- combine\_positions\_download.py (coming)

## Account Positions

The default account poisitions download is broken... dollar amounts include
the "$" and ",", making them strings, etc.

- go to https://digital.fidelity.com/ftgw/digital/portfolio/positions
- three-dot menu / Download
- this gives you a file something like `~/Downloads/Portfolio_Positions_Apr-19-2026.csv`.
- run ./code/repair\_positions\_download.py

The repaired and deduped results are in `positions.csv`.

I've included an older duckdb sql query that does this as well.

## Compbining Account Positions (e.g. for a married couple)

The easiest way to do this is to "Authorize" accounts, so that one
person can view the other person's accounts.  However, some kinds
of accounts (e.g. 403b) don't allow this.

Dowloading and combining two accounts needs to dedupe; for example,
a shared brokerage account might end up in both downloads.

Fidelity doesn't allow one person to log into another
person's account, so this is a two person operation:

person 1:
- download account positions as above (don't repair)
- give file to person 2

person 2:
- receive account positions from person 1
- download account positions as above (don't repair)
- run ./code/combine\_positions\_download.py, giving paths to the two files

The repaired and deduped results are in `combined.csv`.


## Fullview

Fullview is Fidelity's free account aggregation service.  You don't have
to have accounts at Fidelity to create and use a Fullview account.

https://www.fidelity.com/go/monitoring-your-financial-portfolio

To download the account data as CSV:

- go to https://digital.fidelity.com/ftgw/pna/customer/pgc/networth
- in browser, File / Save page as... / web page, complete / overwrite
- run `python code/parse_fullview_html.py`

This will give you a file `networth.csv`.

## Queries and Fancy Stuff

I have a workflow where particulars are hard-coded for myself... I'll
try and get a generic version and put it here.

The basic result is a duckdb time-series database of holdings. Detailed
holdings for Fidelity accounts, and less detailed for Fullview accounts.

But these are good for custom reports, rebalancing, etc.
