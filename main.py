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

def load_csv(file_name):
    """
    Use pandas to load csv file.
    """
    df = pd.read_csv(file_name, delimiter=',', header=None)
    return df


def cut(row):
    """
    Use jieba to cut the source sentence.
    """
    
    # preprocess number, decimal and percent
    sentence = row.iloc[1]
    sentence = re.sub(r'[0-9]+(.?[0-9]+)?%?', 'TAG_NUM', sentence)
    
    # cut the sentence
    words = jieba.cut_for_search(sentence)
    seg = []
    for word in words:
        if word not in stopwords and not word.isspace():
            seg.append(word)

    return seg


def check(ty, querys, row):
    """
    According to type, do different computing.
    The type can be 'and', 'or', or 'not'.
    Return true if meeting the type. Else, return false.
    """

    if ty == 'and':
        for query in querys:
            if not query.strip() in row[1]:
                return False
        return True
    elif ty == 'or':
        for query in querys:
            if query.strip() in row[1]:
                return True
        return False
    elif ty == 'not':
        if querys[0].strip() in row[1]:
            for query in querys[1:]:
                if query.strip() in row[1]:
                    return False
            return True
    
    return False


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
    source_data = load_csv(args.source)
    # source_data.iloc[:, 1] = source_data.apply(cut, axis=1)
    # print('Finish loading source data, and building search engine.')

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
        result = []
        for index, row in source_data.iterrows():
            if check(ty, querys, row):
                result.append(str(row[0]))

        # check if has result
        if result:
            outputs.append(result)
        else:
            outputs.append([str(0)])

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
            tmp.append(','.join(output))
        f.write('\n'.join(tmp))
