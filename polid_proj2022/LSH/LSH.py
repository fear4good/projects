import pandas as pd
import csv
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder


def main():

    data = pd.read_csv("scientists_new.csv")
    scientists = data["scientists"].tolist()
    awards = data["awards"].tolist()
    education = data["education"].tolist()
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(scientists)
    #print(len(integer_encoded))
    l = []
    a = []
    e = []
    for el in integer_encoded:
        l.append(integer_encoded[el])

    a = [[x] for x in awards]
    e = [[x] for x in education]
    s = [[x] for x in scientists]
    List = []
    List = [[x] for x in l]
    for x in range(0, len(List)):
        List[x].extend(a[x])
        List[x].extend(e[x])
        List[x].extend(s[x])
    print(List)

    myFile = open('demo.csv', 'w', encoding="utf-8", newline="")
    writer = csv.writer(myFile)
    writer.writerow(['cord','award', 'Education', 'Name'])
    for data_list in List:
        writer.writerow(data_list)
    myFile.close()


    """
    my_vocab_size = 669
    encode = [one_hot(i, my_vocab_size) for i in scientists]

    print(encode)

    
    length = 10
    padded_sent = pad_sequences(encode, maxlen=length, padding='pre')
    print(padded_sent)

    a = [1 if x in merged else 0 for x in merged]
    print(a)


    hash_ex = list(range(1,len(merged)+1))
    shuffle(hash_ex)

    for i in range(1,10):
        print(f"{i} -> {hash_ex.index(i)}")

    signature= []
    for i in range(1, len(merged)+1):
        idx = hash_ex.index(i)
        signature_val = a[idx]
        print(f"{i} -> {idx} -> {signature_val}")
        if signature_val == 1:
            signature.append(idx)
            break
    print(signature)
"""


if __name__ == "__main__":
    main()