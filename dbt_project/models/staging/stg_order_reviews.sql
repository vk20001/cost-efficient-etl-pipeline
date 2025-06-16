-- staging/stg_order_reviews.sql
select
  review_id,
  order_id,
  review_score,
  review_comment_title,
  review_comment_message,
  cast(review_creation_date as timestamp) as review_creation_date,
  cast(review_answer_timestamp as timestamp) as review_answer_timestamp
from public.order_reviews
