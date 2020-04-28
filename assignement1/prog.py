import sys
import os
import re
import string
import glob

STOP_WORDS = []
ID_doc = 0

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
    mylist = glob.glob(dir_path)
    read_all(mylist, my_list)

def count_occurence(stats, my_list):
    for keys, value in my_list.items():
        for a in value:
            if (a not in stats):
               stats[a] = 1
            else:
                stats[a] += 1

def do_stats(stats):
    total = 0
    for keys, value in stats.items():
        total += value
    for keys, value in stats.items():
       stats[keys] = (value/total) *100 
    return total

def print_tab(stats):
    for keys, value in stats.items():
        print("Key:", keys, value, "%")

def search_word(stats):
    var = "murder"
    for keys, value in stats.items():
        if (var == keys):
            print(keys, value)

def print_menu():
    print("Choose option:")
    print("1 - murder in the 2 categories")
    print("2 - Print graph")

def top_word(stats):
    val = 0.0
    name = ''
    for keys, value in stats.items():
        if (value > val):
            val = value
            name = keys
    print('Top word in this category: %s %.7f \n' %(keys, value))

if __name__ == "__main__":
    list_stats = {}
    list_stats2 = {}
    all_list = {}
    all_list2 = {}
    STOP_WORDS = word_split(open_stop("stopwords.txt"))
    do_dict(all_list, "Crime")
    count_occurence(list_stats,all_list)
    total = do_stats(list_stats)
    do_dict(all_list2, "Comedy")
    count_occurence(list_stats2,all_list2)
    total2 = do_stats(list_stats2)
    print_menu()
    x = input()
    if (x == "1"):
        print("Murder in Crime")
        search_word(list_stats)
        print("Total number of murder",total)
        print("Murder in Comedy")
        search_word(list_stats2)
        print("Total number of murder",total2)
    if (x == "2"):
        print("CRIME")
        print_tab(list_stats)
        print("COMEDY")
        print_tab(list_stats2)
