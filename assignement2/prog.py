import sys
import os
import re
import string
import glob
import math

STOP_WORDS = []
ID_doc = 0
docs = []

def open_stop(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text

def open_file(filename):
    global ID_doc
    ID_doc += 1
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text

def word_split(text):
    wlist = []
    wlist = text.split()
    return wlist

def words_cleanup(words):
    cleaned_words = []
    for word in words:
        new = re.sub(r'[^\w\s]','',word)
        if (len(new) == 0):
            continue
        if (new.isnumeric() == True):
            continue
        if (new not in STOP_WORDS):
            cleaned_words.append(new)
    return cleaned_words

def words_lowercase(words):
    wlist = []
    for word in words:
        wordlower = word.lower()
        wlist.append(wordlower)
    return wlist

def word_index(text ,my_list):
    text = open_file(text)
    text = word_split(text)
    text = words_lowercase(text)
    text = words_cleanup(text)
    text = sorted(text)
    my_list[str(ID_doc)] = text

def add_all(text, my_list):
    for a in text:
        my_list.append(a)

def read_all(dirs, my_list):
    for a in dirs:
        word_index(a, my_list)

def do_dict(my_list, name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path += "/film/"+ name +"/*.txt"
    #dir_path += "/test/"+"/*.txt"
    mylist = glob.glob(dir_path)
    global docs
    docs += mylist
    read_all(mylist, my_list)

def count_occurence(tab, query_list):
    new = {}
    for value in tab:
        if (value in query_list):
            if (value not in new):
                new[value] = 1
            else:
                new[value] += 1
    return (new)

def do_stats(stats):
    total = 0
    for keys, value in stats.items():
        total += value
    for keys, value in stats.items():
       stats[keys] = (value/total) *100 

def search_query(my_list, cond, var):
    query = var.split();
    count_word_in = 0
    relevant = []
    for keys, value in my_list.items():
        count = 0
        for i in range(0, len(query)):
            if (query[i] in value):
                count += 1
        if (cond == "precision"):
            if (count >= 2):
               relevant.append(1)
            else:
               relevant.append(0)
        elif (cond == "recall"):
            if (count > 0):
                relevant.append(count)

    return relevant

def do_measures(rel, ret, nrel):
    tp = rel
    fp = ret - rel
    tn = nrel
    fn = len(docs) - ret - rel

    calc_precision = (tp / (tp + fp)) * 100
    print("Precision:",calc_precision, "%")
    calc_recall = ((tp / (tp + fn))) * 100
    print("Recall:", calc_recall, "%")

def search_occ_word(my_list, new_query):
    query_list = {}
    count = 1
    for keys, value in my_list.items():
        doc = count_occurence(value, new_query)
        query_list[count] = doc
        count += 1
    return (query_list)

def TF(nb_occ, query):
    newtf = {}
    for keys, value in nb_occ.items():
        newtf[keys] = subTf(value)
    return newtf


def subTf(my_item):
    tf = {}
    for keys, value in my_item.items():
            if (keys not in tf):
                tf[keys] = value
            else:
                tf[keys] += value
    for keys, value in tf.items():
        tf[keys] = 1 + math.log(value)
    return tf

def IDF(nb_occ, query):
    idf = {}
    
    for keys, value in nb_occ.items():
        for k, v in value.items():
            for i in range(0, len(query)):
                if (k == query[i]):
                    if (query[i] in idf):
                        idf[k] += 1
                    else:
                        idf[k] = 1
    for keys, value in idf.items():
        idf[keys] = math.log2(len(docs) / value)
    return idf


def IDFbyTF(nb_occ, idf, tf):
    new_dict = tf

    for key, value in new_dict.items():
        tmp = {}
        for k, v in value.items():
            value[k] = submult(k , v, idf)
    return new_dict

def submult(key, value, idf):
    new = 0
    for k, v in idf.items():
        if (k == key):
            new = v * value
    return new


def cosSIM(ibyt, query):
    new = ibyt
    q = 1
    to_return = {}
    for keys, value in new.items():
        var = 0
        var2 = 0
        var3 = 1
        for k, v in value.items():
            var += v * 1 
            var2 += v * v
            var3 += 1 * 1
        if (var2 == 0 or var3 == 0):
            var = 0
        else:
            var = var/ math.sqrt((var2)*(var3))
        to_return[keys] = var

    return to_return

def sort(tab, words):
    my = {}
    word = []

    for k, v in words.items():
        word.append(list(v.items()))

    for key ,value in tab.items():
        my[key] = (value, word[key - 1])
        
    new = list(my.items())

    for i in range(len(new) -1, -1, -1):
        swap = False
        for j in range(i):
            if new[j][1] <= new[j + 1][1]:
                new[j], new[j + 1] = new[j + 1], new[j]
                swap = True
        if not swap:
            break
    return new

def relevant(tab, newquery):
    re = 0
    for (i,j) in tab:
        for a in range(0, len(j) - 1):
            is_relevant = 0
            for b in j[1]:
                for c in range(0, len(b) - 1):
                    if (b[c] in newquery):
                        is_relevant += 1
                        if (is_relevant == len(newquery)):
                            re += 1
                        
    return (re)


def retrieval(tab, nb):
    newtab = []
    for i in range(0, nb):
        newtab.append(tab[i])
    return (newtab)

if __name__ == "__main__":
    ret = 10
    query = "killed people garden"
    newquery = query.split()
    all_list = {}
    STOP_WORDS = word_split(open_stop("stopwords.txt"))
    do_dict(all_list, "Crime")
    do_dict(all_list, "Comedy")
    nb_occ = search_occ_word(all_list, newquery)
    tf = TF(nb_occ, newquery)
    idf = IDF(nb_occ, newquery)
    ibyt = IDFbyTF(nb_occ, idf, tf)
    a = cosSIM(ibyt, newquery)
    sorted_doc = sort(a, nb_occ)
    retrieve = retrieval(sorted_doc, ret)
    rel = relevant(retrieve, newquery)
    nrelandnotretrieved = ret - relevant(sorted_doc, newquery)
    do_measures(rel, ret, nrelandnotretrieved)
