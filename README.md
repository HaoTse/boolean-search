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

## method

### sentence key
- Use complete sentence to be the key of index map.
- Implementation is in `simple.py`.

### inverted index
- Find out number, decimal and percent, and ignore them.
- Find out the English words.
- Make english words and punctuation to be splitting token
- Use splitting token to split sentences, and beacuse of the requirements, we only find out bigram and trigram.
- The map size is `1,172,261`.
- Implementation is in `main.py`.

## Result

- The number of query is `11`.
- The number of sentences in source is `100000`.
- Use `time` command to compuate the spending total time.

| method             | index time | average query time | total time |
| ------------------ | ---------- | ------------------ | ---------- |
| scan               |            | 3.93 s             | 44.42 s    |
| sentence key       | 0.07 s     | 1.860671e-02       | 0.34 s     |
| **inverted index** | 3.25 s     | 4.261190e-04 s     | 3.63 s     |

### each query excution time

| method         | and query      | or query       | not query      |
| -------------- | -------------- | -------------- | -------------- |
| scan           | 3.72 s         | 4.51 s         | 3.72 s         |
| sentence key   | 1.711277e-02 s | 2.236072e-02 s | 1.780224e-02 s |
| inverted index | 1.060963e-04 s | 1.161814e-03 s | 4.591942e-04 s |

### note

在目前的實驗數據下 sentence key 的方法會比 inverted index 快上許多，然而 sentence key 卻有以下幾個問題
- 隨著 source sentence 增加，在 sentence key 中每句句子都要進行 in operator 的搜尋，時間複雜度為 O(n)，因此搜尋時間可能會快速的增長，然而在 inverted index 的 map 中搜尋 word 的速度為 O(1)
- 在少量的 query 下，sentence key 的總體速度比較快，然而每個 query 的平均執行時間是 inverted index 的 25 倍左右，所以隨著 query 的數量增加，sntence key 的執行時間會漸漸的超越 inverted index
- 因此 `main.py` 中採用的方法為 inverted index
