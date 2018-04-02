import csv
import jieba
import re
import time

"""
initial variable
"""
# load stopwords
with open('src/stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = [line.strip() for line in f.readlines()]
# inverted index map
index = {}


def verify(w):
    """
    Verify the word if in stopwords or is empty.
    """
    if w not in stopwords and not w.isspace():
        return True
    return False


def cut(row):
    """
    Use jieba to cut the source sentence.
    """
    
    # preprocess number, decimal and percent
    sentence = row[1]
    sentence = re.sub(r'[0-9]+(.?[0-9]+)?%?', 'TAG_NUM', sentence)
    
    def n_gram(w):
        """
        find out bi-gram and tri-gram
        """
        rtn = []

        for i in range(len(w) - 1):
            # bi-gram
            bi = w[i:i+2]
            if verify(bi) and bi not in rtn:
                rtn.append(bi)

            # tri-gram
            tri = w[i:i+3]
            if i < len(w) - 2 and verify(tri) and tri not in rtn:
                rtn.append(tri)

        return rtn

    # cut the sentence
    words = jieba.lcut(sentence)
    seg = []
    for i in range(len(words) - 1):
        word = words[i]
        next_word = words[i + 1]
        concat_str = word + next_word
        # check if has chinese
        if not re.search(u'[\u4e00-\u9fff]', word) or not re.search(u'[\u4e00-\u9fff]', next_word):
            # two words are both English
            if not re.search(u'[\u4e00-\u9fff]', word) and not re.search(u'[\u4e00-\u9fff]', next_word):
                if verify(word):
                    seg.append(word)
                if verify(next_word):
                    seg.append(next_word)
            else:
                eng_word, chi_word = (word, next_word) if not re.search(u'[\u4e00-\u9fff]', word) else (next_word, word)
                if verify(eng_word):
                    seg.append(eng_word)
                # deal with Chinese word
                if len(chi_word) == 2 and verify(chi_word):
                    seg.append(chi_word)
                elif len(chi_word) > 2:
                    seg.extend(n_gram(chi_word))
        elif len(concat_str) == 2 and verify(concat_str):
            seg.append(concat_str)
        else:
            seg.extend(n_gram(concat_str))

    seg = list(set(seg))
    # construct index
    for w in seg:
        try:
            index[w].append(row[0])
        except:
            index[w] = [row[0]]


def search(ty, querys):
    """
    According to type, do different computing.
    The type can be 'and', 'or', or 'not'.
    Return the set of result. If empty return 0.
    """

    tmp = querys[0].strip()
    rtn = set(index[tmp]) if tmp in index else set()
    if ty == 'and':
        for query in querys[1:]:
            tmp = query.strip()
            rtn = rtn & set(index[tmp]) if tmp in index else rtn & set()
    elif ty == 'or':
        for query in querys[1:]:
            tmp = query.strip()
            rtn = rtn | set(index[tmp]) if tmp in index else rtn | set()
    elif ty == 'not':
        for query in querys[1:]:
            tmp = query.strip()
            rtn = rtn - set(index[tmp]) if tmp in index else rtn - set()
    
    return sorted(rtn, key=lambda x: int(x)) if bool(rtn) else set([str(0)])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                       default='source.csv',
                       help='input source data file name')
    parser.add_argument('--query',
                        default='query.txt',
                        help='query file name')
    parser.add_argument('--output',
                        default='output.txt',
                        help='output file name')
    args = parser.parse_args()

    # setup of jieba
    # load zh-TW dictionary
    jieba.set_dictionary('src/dict.txt.big')
    # load user dictionary
    jieba.load_userdict('src/dict.user')
    
    # load source data, build search engine
    start_time = time.time()
    with open(args.source, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            cut(row)
    index_time = time.time() - start_time
    print('Finish loading source data, and building search engine.')

    # compute query result
    print('Loading query file and computing.')
    # read query file
    with open(args.query, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # compute query result
    outputs = []
    # initial time variable
    and_time, or_time, not_time, total_time = [], [], [], []
    for line in lines:
        # initial start time
        start_time = time.time()

        # get querys type and content
        if 'and' in line:
            ty = 'and'
            querys = line.split('and')
        elif 'or' in line:
            ty = 'or'
            querys = line.split('or')
        elif 'not' in line:
            ty = 'not'
            querys = line.split('not')
        else:
            print(line + ': format error!')
            continue
        
        # compute
        result = search(ty, querys)
        outputs.append(result)

        # compute excution time
        waste = time.time() - start_time
        if ty == 'and':
            and_time.append(waste)
        elif ty == 'or':
            or_time.append(waste)
        elif ty == 'not':
            not_time.append(waste)
        total_time.append(waste)
    
    # output result
    tmp = []
    with open(args.output, 'w', encoding='utf-8') as f:
        for output in outputs:
            tmp.append(','.join(output))
        f.write('\n'.join(tmp))
    print("Output the result to %s." % (args.output))

    # output excution time
    print("| -----------------------------Excution time---------------------------------- |")
    print("| index | and(per query) | or(per query) | not(per query) | average(per query) |")
    print("| ----- | -------------- | ------------- | -------------- | ------------------ |")
    print("| %2.2f | %2.12f | %2.11f | %2.12f | %2.16f |" %
            (index_time, sum(and_time) / len(and_time), sum(or_time) / len(or_time),
            sum(not_time) / len(not_time), sum(total_time) / len(total_time)))
    print("| ---------------------------------------------------------------------------- |")
