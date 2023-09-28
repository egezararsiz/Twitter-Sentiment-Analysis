import pandas 
import argparse 
import os, sys
import os.path as osp
from pathlib import Path
import json
import re
import math

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="csv tweet base", required=True)
    return parser.parse_args()

categories = {
    "a": {},
    "r": {},
    "c": {},
    "p": {},
    "e": {},
    "o": {},
    "nc": {}
}

def update_cat_wc(row, sw):
    if type(row["TEXT"]) != str:
        return
    text = re.sub("https?:[^ ]*", " ", row["TEXT"])
    text = re.sub(r"\\x..", " ", text)
    text = re.sub("[()\[\],.?!\-:;#&]", " ", text)
    words = text.split()
    cat = row["CATEGORY"].lower()
    if cat in categories:
        cat_words = categories[cat]
        for word in words:
            word = word.lower()
            if word in sw:
                continue
            if re.fullmatch("@.*", word) is not None:
                continue
            if re.fullmatch("[0-9]*", word) is not None:
                continue
            if re.fullmatch("[a-z0-9]*", word) is None:
                continue
            if word in cat_words:
                cat_words[word] += 1
            else:
                cat_words[word] = 1
        categories[cat] = cat_words

def clean_cats(categories):
    new_cats = {}
    for (name, words) in categories.items():
        new_cats[name] = {}
        for (word, count) in words.items():
            if count >= 3:
                new_cats[name][word] = count
    return new_cats

def stopwords():
    p = Path(__file__).resolve().parent.parent
    path = os.path.join(p, "data", "stopwords.txt")
    return open(path)

def compile_word_counts(csv_base):
    with stopwords() as s:
        sw = set(map(lambda s: s.strip(), filter(lambda s: not s.startswith("#"), s.readlines())))
    df = pandas.DataFrame()
    for csv in os.listdir(csv_base):
        ndf = pandas.read_csv(os.path.join(csv_base, csv))
        df = df.append(ndf)
    df.apply(lambda r: update_cat_wc(r, sw), axis=1)
    return categories

def tf_idf(word, cat, wc):
    return tf(word, cat, wc) * idf(word, wc)

def tf(word, cat, wc):
    return wc[cat][word]

def idf(word, wc):
    cats_using_w = 0
    for cat in wc.values():
        if word in cat:
            cats_using_w += 1
    n = len(wc.keys()) / cats_using_w
    return math.log(n, 10)

def compute_cat_lang(categories, n):
    counts = categories
    output = {}
    for (cat_name, cat_words) in counts.items():
        ws = {}
        for word in cat_words:
            ws[word] = tf_idf(word, cat_name, counts)
        s = sorted(ws, key=ws.get)
        s.reverse()
        output[cat_name] = [x for _, x in zip(range(n), s)]
    return json.dumps(output, indent=2)
            
def main():
    args = parse_args()
    output = compile_word_counts(args.t)
    output = clean_cats(output)
    output = compute_cat_lang(output, 10)
    print(output)

if __name__ == "__main__":
    main()
