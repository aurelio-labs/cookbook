pql_reference = """
# KumoRFM Predictive Query Language (PQL) Reference

## Overview

Predictive Query Language (PQL) is KumoRFM's declarative SQL-like syntax for defining predictive modeling tasks using the foundation model.

## Core Structure

### Basic Syntax
```sql
PREDICT <target>
FOR <entity> IN (<id1>, <id2>, ...)
[WHERE <filter>]
[ASSUMING <conditions>]
```

### Minimum Requirements
- **Entity**: Explicit list of entity IDs (required)
- **Target**: What to predict (required)  
- **Filter**: Optional conditions to scale down results

## Main Commands

### PREDICT
Defines the target variable to predict. Must start every PQL query.

```sql
PREDICT SUM(transactions.price, 0, 30, days)
PREDICT COUNT(transactions.*, 0, 30, days) = 0
PREDICT FIRST(purchases.type, 0, 7)
```

### FOR ... IN
Specifies explicit entity IDs for predictions. KumoRFM requires specific entity lists, not general entity types.

```sql
FOR customers.customer_id IN ('cust_123', 'cust_456', 'cust_789')
FOR users.user_id IN ('user_abc', 'user_def')
FOR products.product_id IN ('prod_1', 'prod_2', 'prod_3')
```

### WHERE
Applies filtering conditions. Can be used multiple times:
- Entity filters
- Target filters within aggregations  
- Conditional aggregations

```sql
WHERE COUNT(transactions.*, -30, 0) > 0
WHERE users.status = 'active'
WHERE transactions.value > 50
```

### ASSUMING
Specifies conditions assumed true during prediction time. Used for hypothetical scenarios.

```sql
ASSUMING COUNT(notifications.*, 0, 7) > 2
ASSUMING LIST_DISTINCT(coupons.type, 0, 3) CONTAINS '50% off'
```

## Aggregation Functions

### Syntax
```sql
AGGREGATION_FUNCTION(table.column, start, end, [time_unit])
```

**Parameters:**
- **start/end**: Time period boundaries (must be non-negative integers)
- **end > start**: End value must be greater than start value
- **time_unit**: days (default), hours, months

### Available Functions

| Function | Description | Example |
|----------|-------------|---------|
| `AVG()` | Average value | `AVG(sales.amount, 0, 30, days)` |
| `COUNT()` | Count occurrences | `COUNT(transactions.*, -90, 0, days)` |
| `COUNT_DISTINCT()` | Count unique values | `COUNT_DISTINCT(products.id, 0, 7)` |
| `FIRST()` | First value in range | `FIRST(purchases.type, 0, 7)` |
| `LAST()` | Last value in range | `LAST(sessions.status, -30, 0)` |
| `LIST_DISTINCT()` | List of unique values | `LIST_DISTINCT(articles.id, 0, 7)` |
| `MAX()` | Maximum value | `MAX(transactions.amount, 0, 30)` |
| `MIN()` | Minimum value | `MIN(orders.value, -7, 0)` |
| `SUM()` | Sum of values | `SUM(purchases.price, 0, 30, days)` |

## Boolean Operators

### Comparison Operators
- `=` Equal
- `!=` Not equal
- `<` Less than
- `<=` Less than or equal
- `>` Greater than
- `>=` Greater than or equal

### Logical Operators
- `AND` Logical AND
- `OR` Logical OR
- `NOT` Logical NOT

### String Operations
- `CONTAINS` String contains
- `STARTS_WITH` String starts with
- `ENDS_WITH` String ends with
- `IN` Value in list
- `LIKE` Pattern matching

## Time Windows

### Time Reference System
- **Positive values**: Future time (0 = now, 30 = 30 days future)
- **Negative values**: Past time (-90 = 90 days ago)
- **Zero point**: Prediction time

### Supported Time Units
- `days` (default)
- `hours`
- `months`

### Examples
```sql
-- Last 90 days
COUNT(transactions.*, -90, 0, days)

-- Next 30 days  
COUNT(transactions.*, 0, 30, days)

-- Last 3 months
SUM(sales.amount, -3, 0, months)

-- Next week in hours
COUNT(sessions.*, 0, 168, hours)
```

## Task Types

Kumo automatically determines task type based on query structure:

### 1. Regression
Predicts continuous real number values.

```sql
PREDICT SUM(transactions.price, 0, 30, days)
FOR customers.customer_id IN ('cust_123', 'cust_456')
```

### 2. Binary Classification
Predicts true/false outcomes using comparison operators.

```sql
PREDICT COUNT(transactions.*, 0, 30, days) = 0
FOR customers.customer_id IN ('cust_123', 'cust_456')
WHERE COUNT(transactions.*, -90, 0, days) > 0
```

### 3. Multi-class/Multi-label Classification
Predicts class labels.

```sql
PREDICT FIRST(purchases.type, 0, 7) 
FOR users.user_id IN ('user_abc', 'user_def')
```

### 4. Link Prediction
Predicts lists of items using ranking.

```sql
PREDICT LIST_DISTINCT(transactions.article_id, 0, 7) 
RANK TOP 10 FOR customers.customer_id IN ('cust_123', 'cust_456')
```

## Temporal vs Static Queries

### Temporal Queries
- Predict aggregations over specific time windows
- Require time columns
- Handle complex temporal data splitting
- Prevent data leakage through proper time-based splits

```sql
PREDICT SUM(transactions.price, 0, 30, days)
FOR customers.customer_id IN ('cust_123', 'cust_456')
```

### Static Queries
- Do not require time columns
- Use random 80/10/10 data split
- Simpler data handling

```sql
PREDICT user.category
FOR users.user_id IN ('user_abc', 'user_def')
WHERE users.active = true
```

## Advanced Features

### Nested Filters
```sql
COUNT(orders.* WHERE orders.status = 'completed' AND orders.value > 50, -30, 0)
```

### Multiple Conditions
```sql
PREDICT COUNT(sessions.*, 0, 7) > 10 OR SUM(transactions.value, 0, 5) > 100
FOR users.user_id IN ('user_123', 'user_456')
WHERE users.status = 'active' AND COUNT(sessions.*, -30, 0) > 5
```

### Inline Filters
```sql
SUM(transactions.price WHERE transactions.category = 'electronics', 0, 30)
```

### Column References
- Format: `table.column` or `table.*`
- Supports dot notation for nested fields
- Use `*` to reference all columns/records

### Ranking (Link Prediction)
```sql
PREDICT LIST_DISTINCT(products.id, 0, 30)
RANK TOP 5 FOR customers.customer_id IN ('cust_123', 'cust_456')
```

## Complete Examples

### Customer Churn Prediction (Binary Classification)
```sql
PREDICT COUNT(transactions.*, 0, 30, days) = 0
FOR customers.customer_id IN ('cust_123', 'cust_456', 'cust_789')
WHERE COUNT(transactions.*, -90, 0, days) > 0
```
*Predicts if active customers will churn in next 30 days*

### Revenue Forecasting (Regression)
```sql
PREDICT SUM(transactions.price, 0, 30, days)
FOR customers.customer_id IN ('gold_cust_1', 'platinum_cust_2')
```

### High-Value Transaction Prediction
```sql
PREDICT COUNT(transactions.* WHERE transactions.value > 100, 0, 7)
FOR users.user_id IN ('user_abc', 'user_def', 'user_ghi')
WHERE COUNT(transactions.*, -30, 0) > 5
```

### Product Recommendation (Link Prediction)
```sql
PREDICT LIST_DISTINCT(purchases.product_id, 0, 14)
RANK TOP 10 FOR customers.customer_id IN ('cust_123', 'cust_456')
WHERE COUNT(sessions.*, -7, 0) > 0
```

### Multi-Category Classification
```sql
PREDICT FIRST(transactions.category, 0, 30)
FOR customers.customer_id IN ('active_cust_1', 'active_cust_2')
```

### Complex Conditional Prediction
```sql
PREDICT (COUNT(premium_features.*, 0, 30) > 5) AND (SUM(usage.minutes, 0, 30) > 1000)
FOR users.user_id IN ('trial_user_1', 'trial_user_2')
WHERE users.subscription_type = 'trial'
ASSUMING COUNT(notifications.*, 0, 7) > 3
ASSUMING marketing_campaigns.type = 'premium_upgrade'
```

### Product Recommendation with Ranking
```sql
PREDICT LIST_DISTINCT(transactions.article_id, 0, 30)
RANK TOP 10 FOR customers.customer_id IN ('cust_123', 'cust_456')
```

*IMPORTANT: when using RANK TOP K you CANNOT set K=1, so if finding the top customer just use RANK TOP 2*

## Syntax Rules & Constraints

### Time Window Rules
1. Both start and end must be non-negative integers
2. End value must be greater than start value
3. Time unit defaults to 'days' if not specified

### Entity Rules
1. Must specify explicit entity IDs using IN clause
2. Use `FOR table.column IN (id1, id2, ...)` format
3. Entity IDs must exist in your graph schema
4. Cannot use `FOR EACH` - must provide specific entity list

### Target Rules
1. Must use `PREDICT` as first command
2. Can combine multiple conditions with AND/OR/NOT
3. Comparison operators create classification tasks
4. Raw aggregations create regression tasks

### Filter Rules
1. WHERE clauses can be nested and combined
2. Support both static and temporal conditions
3. Can filter at entity level or within aggregations
4. Multiple WHERE clauses are combined with AND

## Best Practices

### Performance Optimization
1. **Filter Early**: Use WHERE clauses to reduce computation
2. **Choose Appropriate Time Windows**: Match business context
3. **Entity Selection**: Filter entities to relevant subset

### Query Design
1. **Start Simple**: Begin with basic queries, add complexity gradually
2. **Test Incrementally**: Validate each component before combining
3. **Clear Intent**: Make prediction goal explicit in target definition

### Temporal Considerations
1. **Avoid Data Leakage**: Use proper time boundaries
2. **Balance Splits**: Ensure sufficient data in each time period
3. **Business Logic**: Align time windows with business cycles

### Task Type Selection
1. **Regression**: Use for continuous predictions
2. **Classification**: Use comparison operators for categories
3. **Link Prediction**: Use LIST_DISTINCT with RANK TOP K
4. **Multi-class**: Use FIRST/LAST for category prediction

## Error Prevention

### Common Mistakes
1. **Invalid Time Windows**: Ensure end > start and both ≥ 0
2. **Missing Entities**: Verify entity exists in graph
3. **Type Mismatches**: Match aggregation functions to data types
4. **Data Leakage**: Don't reference future data in historical queries

### Validation Checklist
- [ ] Entity specified with FOR table.column IN (...) 
- [ ] Target defined with PREDICT
- [ ] Time windows follow start < end rule
- [ ] Filters reference valid columns
- [ ] Syntax follows SQL-like structure
- [ ] Time boundaries prevent data leakage
- [ ] No use of FOR EACH (KumoRFM requires explicit entity lists)
"""
