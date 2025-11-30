## Source to Staging
### Car Sales 

| Source Column | Target Column | Transformation    |
| ------------- | ------------- | ----------------- |
| id_sales      | id_sales      | -                 |
| year          | year          | -                 |
| brand_car     | brand_car     | -                 |
| transmission  | transmission  | -                 |
| state         | state         | -                 |
| condition     | condition     | cast into varchar |
| odometer      | odometer      | cast into varchar |
| color         | color         | -                 |
| interior      | interior      | -                 |
| mmr           | mmr           | cast into varchar |
| sellingprice  | sellingprice  | cast into varchar |
### Car Brand

| Source Column | Target Column | Transformation |
| ------------- | ------------- | -------------- |
| brand_car_id  | brand_car_id  | -              |
| brand_name    | brand_name    | -              |

### US State

| Source Column | Target Column | Transformation |
| ------------- | ------------- | -------------- |
| code          | code          | -              |
| name          | name          | -              |

## Staging to Warehouse
### Car Sales

| Source Column | Target Column | Source Table | Transformation                  |
| ------------- | ------------- | ------------ | ------------------------------- |
| -             | sales_id      | -            | Auto Generated UUID             |
| id_sales      | id_sales_nk   | Car Sales    | -                               |
| year          | year          | Car Sales    | Cast into Integer               |
| brand_car_id  | brand_car_id  | Car Brand    | -                               |
| transmission  | transmission  | Car Sales    | -                               |
| id_state      | id_state      | US State     | -                               |
| condition     | condition     | Car Sales    | Cast into Float                 |
| odometer      | odometer      | Car Sales    | Cast into Float                 |
| color         | color         | Car Sales    | -                               |
| interior      | interior      | Car Sales    | -                               |
| mmr           | mmr           | Car Sales    | Cast into Float                 |
| sellingprice  | selling_price | Car Sales    | Rename Column & Cast into Float |
