ORM examples:

1. Filter with Q and F
```python
result = Product.objects.filter(
    Q(quantity__lt=F('min_stock')) &
    Q(quantity=1) &
    Q(name__icontains="laptop")
)
```
```sql
SELECT * FROM products
WHERE
    quantity < min_stock
    AND
    quantity = 4
    AND
    name ilike '%laptop%'
```  

2. Filter
```python
authors_complex_query = Author.objects.annotate(
        num_posts=Count('posts'),  # Анотація: кількість постів
        avg_rating=Avg('posts__rating')  # Анотація: середній рейтинг постів
    ).filter(
        Q(num_posts__gt=5) | Q(avg_rating__gt=4.0)  # Фільтр по анотаціям з АБО
    ).exclude(
        name='admin'
    ).order_by(
        'name'
    )
```
```sql
SELECT 
    *, 
    COUNT(posts) as num_posts, 
    AVG (posts__rating) as avg_rating
FROM Author
    WHERE  
        (num_posts > 5 OR
        avg_rating > 4.0) AND 
        name != admin
ORDER BY name
```