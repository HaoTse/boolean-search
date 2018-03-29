import pandas as pd
import jieba
import re
import time

"""
setup of jieba
"""
# load zh-TW dictionary
jieba.set_dictionary('src/dict.txt.big')
# load user dictionary
jieba.load_userdict('src/dict.user')
# load stopwords
with open('src/stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = [line.strip() for line in f.readlines()]

"""
initial variable
"""
index = {}

def load_csv(file_name):
    """
    Use pandas to load csv file.
    """
    df = pd.read_csv(file_name, delimiter=',', header=None)
    return df


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
    sentence = row.iloc[1]
    sentence = re.sub(r'[0-9]+(.?[0-9]+)?%?', 'TAG_NUM', sentence)
    
    def n_gram(w):
        """
        find out bi-gram and tri-gram
        """
        bigram = []
        trigram = []

        for i in range(len(w) - 1):
            # bi-gram
            bi = w[i:i+2]
            if verify(bi):
                bigram.append(bi)

            # tri-gram
            if i < len(w) - 2 and verify(w[i:i+3]):
                trigram.append(w[i:i+3])

        return bigram + trigram

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
        if w not in index:
            index[w] = []
        index[w].append(row.iloc[0])

    return seg


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
    
    return sorted(rtn) if bool(rtn) else set([0])


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
    
    # TODO load source data, build search engine
    start_time = time.time()
    source_data = load_csv(args.source)
    source_data.iloc[:, 1] = source_data.apply(cut, axis=1)
    print('Finish loading source data, and building search engine. Wasting %s seconds.' % (time.time() - start_time))

    # TODO compute query result
    # read query file
    with open(args.query, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # compute query result
    outputs = []
    # initial time variable
    and_time = []
    or_time = []
    not_time = []
    total_time = []
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
    # output excution time
    print("Average and query wasting %s seconds." % (sum(and_time) / len(and_time)))
    print("Average or query wasting %s seconds." % (sum(or_time) / len(or_time)))
    print("Average not query wasting %s seconds." % (sum(not_time) / len(not_time)))
    print("Average total wasting %s seconds." % (sum(total_time) / len(total_time)))
    
    # TODO output result
    tmp = []
    with open(args.output, 'w', encoding='utf-8') as f:
        for output in outputs:
            tmp.append(','.join(str(x) for x in output))
        f.write('\n'.join(tmp))
