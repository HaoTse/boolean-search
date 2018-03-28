# Boolean Search

## Data Format

Query format example:
```python
MLB and 春訓
iPhone or MLB
好棒棒 and 好爛爛
```

Output format example:
```
1,4,6,40,150
1,2,4,6,40,150,1000
0
```

## Result

- The number of query is `11`.
- The number of sentences in source is `100000`.
- Use `time` command to compuate the spending time.

| method | time  |
| ------ | ----- |
| scan   | 46.71 |