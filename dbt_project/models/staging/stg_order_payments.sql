-- staging/stg_order_payments.sql
select
  order_id,
  payment_sequential,
  payment_type,
  payment_installments,
  payment_value
from public.order_payments
