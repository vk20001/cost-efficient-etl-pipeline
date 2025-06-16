-- staging/stg_sellers.sql
select
  seller_id,
  seller_zip_code_prefix,
  seller_city,
  seller_state
from public.sellers
