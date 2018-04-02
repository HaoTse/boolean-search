# Boolean Search

## Requirements
- We will only use `2-gram`, `3-gram`, and English terms in queries.
- Each query will contain only one kind of operation type (either `and`, `or`, or `not`), but may contain many times.

### prerequisite
- python 3.6.4
- `pip install -r requirements.txt`

### command
```
$ python main.py
```
```
usage: main.py [-h] [--source SOURCE] [--query QUERY] [--output OUTPUT]

optional arguments:
  -h, --help       show this help message and exit
  --source SOURCE  input source data file name
  --query QUERY    query file name
  --output OUTPUT  output file name
```

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

## Data Process
- Use `jieba`.
- Find out number, decimal and percent, and ignore them.
- Handle Englist and Chinese separately, and beacuse of the requirements, we only find out bigram and trigram in Chinese.

```
words = cut list from source sentences using jieba
for word in words:
    next = the next word in words
    if word or next is English:
        store the English one directly
        get bigram and trigram form the Chinese one
    else:
        concat word and next, and get bigram and trigram from it
```
- The index size is 1,056,375.

## Result

- The number of query is `11`.
- The number of sentences in source is `100000`.
- Use `time` command to compuate the spending total time.

| method             | index time | average query time | total time |
| ------------------ | ---------- | ------------------ | ---------- |
| scan               |            | 3.93 s             | 44.42 s    |
| **inverted index** | 15.36 s    | 5.23e-04 s         | 16.44 s    |

### each query excution time

| method         | and query | or query  | not query |
| -------------- | --------- | --------- | --------- |
| scan           | 3.72 s    | 4.51 s    | 3.72 s    |
| inverted index | 1.1e-04 s | 1.1e-03 s | 4.2e-04 s |
