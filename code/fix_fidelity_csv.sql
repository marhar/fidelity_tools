WITH raw AS (
SELECT *
FROM read_csv_auto('p1.csv', header=true, ignore_errors=true)
WHERE "Account Number" IS NOT NULL
  AND "Symbol" IS NOT NULL
  AND "Type" IS NOT NULL
),
converted AS (
SELECT
"Account Number" as acct_num,
"Account Name" as acct_name,
"Symbol" as symbol,
"Description" as description,
"Quantity"::decimal(10,3) as quantity,
regexp_replace("Last Price", '[^0-9\.\-]', '', 'g')::decimal(10,3) as last_price,
regexp_replace("Last Price Change", '[^0-9\.\-]', '', 'g')::decimal(8,3) as last_price_change,
regexp_replace("Current Value", '[^0-9\.\-]', '', 'g')::decimal(10,2) as current_value,
regexp_replace("Today's Gain/Loss Dollar", '[^0-9\.\-]', '', 'g')::decimal(10,2) as today_gl_dollar,
regexp_replace("Today's Gain/Loss Percent", '[^0-9\.\-]', '', 'g')::double as today_gl_pct,
regexp_replace("Total Gain/Loss Dollar", '[^0-9\.\-]', '', 'g')::decimal(12,2) as total_gl_dollar,
regexp_replace("Total Gain/Loss Percent", '[^0-9\.\-]', '', 'g')::double as total_gl_pct,
regexp_replace("Percent Of Account", '[^0-9\.\-]', '', 'g')::double as pct_of_acct,
regexp_replace("Cost Basis Total", '[^0-9\.\-]', '', 'g')::decimal(10,2) as cost_basis_total,
CASE
WHEN "Average Cost Basis" = '--' THEN NULL
ELSE regexp_replace("Average Cost Basis", '[^0-9\.\-]', '', 'g')::decimal(6,2)
END AS avg_cost_basis,
"Type" as acct_type
FROM raw
),
filtered as (
  SELECT * exclude (
    last_price_change,
    total_gl_dollar,
    total_gl_pct,
    today_gl_dollar,
    today_gl_pct,
    pct_of_acct,
    cost_basis_total,
    avg_cost_basis,
    acct_type
  )
  FROM converted
)
SELECT * from filtered
ORDER BY 1
;

