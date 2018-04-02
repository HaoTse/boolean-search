import csv
import re
import time

"""
initial variable
"""
# inverted index map
index = {}


def search(ty, querys):
    """
    According to type, do different computing.
    The type can be 'and', 'or', or 'not'.
    Return the set of result. If empty return 0.
    """

    tmp = querys[0].strip()
    rtn = set(value for key, value in index.items() if tmp in key)
    if ty == 'and':
        for query in querys[1:]:
            tmp = set(value for key, value in index.items() if query.strip() in key)
            rtn = rtn & tmp
    elif ty == 'or':
        for query in querys[1:]:
            tmp = set(value for key, value in index.items() if query.strip() in key)
            rtn = rtn | tmp
    elif ty == 'not':
        for query in querys[1:]:
            tmp = set(value for key, value in index.items() if query.strip() in key)
            rtn = rtn - tmp
    
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
    
    # load source data, build search engine
    start_time = time.time()
    with open(args.source, 'r', encoding='utf-8') as f:
        for row in csv.reader(f):
            index[row[1]] = row[0]
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
    print("| {0:5.2f} | {1:14e} | {2:13e} | {3:14e} | {4:18e} |".format(index_time,
            sum(and_time) / len(and_time), sum(or_time) / len(or_time),
            sum(not_time) / len(not_time), sum(total_time) / len(total_time)))
    print("| ---------------------------------------------------------------------------- |")
