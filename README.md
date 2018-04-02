# Boolean Search

## Requirements
- We will only use `2-gram`, `3-gram`, and English terms in queries.
- Each query will contain only one kind of operation type (either `and`, `or`, or `not`), but may contain many times.
- Only use `100` querys.

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
- In the process of searching, I will construct the word key based map.
- If the word key based map has the current key, directly access it. Otherwise, search from sentence key based map.
- Implementation is in `main.py`.

### inverted index
- Find out number, decimal and percent, and ignore them.
- Find out the English words.
- Make english words and punctuation to be splitting token
- Use splitting token to split sentences, and beacuse of the requirements, we only find out bigram and trigram.
- Implementation is in `inverted_index.py`.

## Result
- Use `time` command to compuate the spending total time.

### small set
- The number of query is `11`.
- The number of sentences in source is `100000`.

| method         | index time | average per query time | total time |
| -------------- | ---------- | ---------------------- | ---------- |
| scan           |            | 3.93 s                 | 44.42 s    |
| sentence key   | 0.07 s     | 7.877111e-03 s         | 0.18 s     |
| inverted index | 2.69 s     | 4.261190e-04 s         | 3.31 s     |

### large set
- The number of query is `100`.
- The number of sentences in source is `2,692,730`.

| method         | index time | average per query time | total time |
| -------------- | ---------- | ---------------------- | ---------- |
| sentence key   | 11.66 s    | 1.035 s                | 116 s      |
| inverted index | 1018.51 s  | 0.015 s                | 1091.09 s  |

### note

- 在小量資料的實驗下 sentence key 的方法會比 inverted index 快上許多，在少量的 query 下，sentence key 的總體速度比較快，但是每個 query 的平均執行時間是 inverted index 的 25 倍左右，所以隨著 query 的數量增加，sntence key 的執行時間會漸漸的超越 inverted index
- 在大量資料的實驗下，sentence key 的速度仍遠快於 inverted index
- 測試中，當 query 數量達到上千時，inverted index 的速度會快於 sentence key，然而在 Requirements 中提到只使用 100 條 query，所以 `main.py` 所使用的方法為 `sentence key`
