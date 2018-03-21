import pandas as pd
import jieba
import re

# load zh-TW dictionary
jieba.set_dictionary('src/dict.txt.big')
# load stopwords
with open('src/stopwords.txt', 'r', encoding='utf-8') as f:
    stopwords = [line.strip() for line in f.readlines()]

# output = open('tmp', 'w', encoding='utf-8')

def cut(row):
    # preprocess number, decimal and percent
    sentence = row.iloc[1]
    sentence = re.sub(r'[0-9]+(.?[0-9]+)?%?', 'TAG_NUM', sentence)
    
    # cut the sentence
    words = jieba.cut_for_search(sentence)
    seg = []
    for word in words:
        if word not in stopwords and not word.isspace():
            seg.append(word)

    # output.writelines(["%s " % s for s in seg])
    # output.write('\n')
    return seg

def load_csv(file_name):
    df = pd.read_csv(file_name, delimiter=',', header=None)
    return df

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
    
    # Please implement your algorithm below
    
    # TODO load source data, build search engine
    source_data = load_csv(args.source)
    source_data.iloc[:, 1] = source_data.apply(cut, axis=1)
    print('Finish loading source data, and building search engine.')

    # TODO compute query result
  
    # TODO output result