-- Docs: https://docs.mage.ai/guides/sql-blocks
INSERT INTO mcap_vol
SELECT *
FROM {{ df_1 }};
INSERT INTO prices
SELECT *
FROM {{ df_2 }};