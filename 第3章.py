# %%

# 自作Knockツール。knock.pyを参照。
from knock import Knock
import re
print("第三章")

"""
https://nlp100.github.io/ja/ch03.html

Wikipediaの記事を以下のフォーマットで書き出したファイルjawiki-country.json.gzがある．

1行に1記事の情報がJSON形式で格納される
各行には記事名が”title”キーに，記事本文が”text”キーの辞書オブジェクトに格納され，そのオブジェクトがJSON形式で書き出される
ファイル全体はgzipで圧縮される
以下の処理を行うプログラムを作成せよ．
 """

# %%

k = Knock(""" 20. JSONデータの読み込みPermalink
Wikipedia記事のJSONファイルを読み込み，「イギリス」に関する記事本文を表示せよ．問題21-29では，ここで抽出した記事本文に対して実行せよ． """)

# JSONファイルのパース課題として理解した。
k.expected = lambda x: "イギリス" in x  # 必要条件
TEXT = ""
with open("jawiki-country.json", mode="r", encoding="utf-8") as f:
    arr = []
    texts = filter(lambda t: ('"title": "イギリス"' in t), f.readlines())
    texts = list(texts)
    # print(texts)
    if len(texts) == 1:
        text = texts[0]
        s = text.find('"text": "') + len('"text": "')
        e = text[s:].find('"title":')
        # print(s,e)
        if e == -1:
            e = -len('"}')-1
        TEXT = text[s:e]
        print(TEXT[-50:], end="\n\n")
    else:
        print(len(texts))
    # display(arr)
# print(TEXT)
k.A = TEXT
k.display()

# JSONモジュールぐらい使ってよかった気がする。。。

# %%

k = Knock(""" 21. カテゴリ名を含む行を抽出Permalink
記事中でカテゴリ名を宣言している行を抽出せよ． """)


# k.expected = lambda x: "カテゴリ名" in x
a = filter(lambda x: "Category" in x, TEXT.split("\\n"))

k.A = list(a)
k.display()

# %%
k = Knock(""" 22. カテゴリ名の抽出Permalink
記事のカテゴリ名を（行単位ではなく名前で）抽出せよ． """)

k.A = [t[11:-2] for t in filter(lambda x: "Category" in x, TEXT.split("\\n"))]
k.A.pop(0)
k.display()
# %%

k = Knock("""23. セクション構造Permalink
記事中に含まれるセクション名とそのレベル（例えば”== セクション名 ==”なら1）を表示せよ．""")

# filtered_text = filter(lambda x: "== " in x, TEXT.split("\\n"))


def f(x):
    if len(x) > 0:
        return x[0] == "=" and x[-1] == "="
    else:
        return False


filtered_text = list(filter(f, TEXT.split("\\n")))
levels = [t.count("=")/2 for t in filtered_text]

labels = [t.replace("=", "") for t in filtered_text]
k.A = list(zip(labels, levels))
k.display()

# %%

k = Knock("""24. ファイル参照の抽出Permalink
記事から参照されているメディアファイルをすべて抜き出せ．""")

texts = filter(lambda x: "ファイル" in x, TEXT.split("\n"))
k.A = []
for t in texts:
    for i in range(t.count("ファイル")):
        s = t.find("[[ファイル:") + len("[[ファイル:")
        # print("|" in t[s:])
        e = t[s:].find("|")+s
        if "]" in t[s:e]:
            e = t[s:].find("]") + s
        k.A.append(t[s:e])
        t = t[e:]
k.expected = lambda x: len(x) == TEXT.count("[[ファイル:")

k.display()
# %%
k = Knock("""25. テンプレートの抽出Permalink
記事中に含まれる「基礎情報」テンプレートのフィールド名と値を抽出し，辞書オブジェクトとして格納せよ．""")
s = TEXT.find("{{基礎情報 国\\n|") + len("{{基礎情報 国\\n|")
temp = s
e = TEXT[s:].find("}}") + s
while ("{{" in TEXT[temp:e]):
    temp = e + 2
    e = TEXT[temp:].find("}}") + temp
# TEXT[s:e].split("\\n|")
k.A = {t[:t.find("=")].strip(): t[t.find("=")+1:].strip()
       for t in TEXT[s:e].split("\\n|")}


k.display()

# %%
k = Knock("""26. 強調マークアップの除去Permalink
25の処理時に，テンプレートの値からMediaWikiの強調マークアップ（弱い強調，強調，強い強調のすべて）を除去してテキストに変換せよ（参考: マークアップ早見表）．""")


def parse_value(x):
    x = re.sub(r"('{1,3})(.+)\1", r"\2", x)
    return x[x.find("=")+1:].strip()


# コピペここから
s = TEXT.find("{{基礎情報 国\\n|") + len("{{基礎情報 国\\n|")
temp = s
e = TEXT[s:].find("}}") + s
while ("{{" in TEXT[temp:e]):
    temp = e + 2
    e = TEXT[temp:].find("}}") + temp
# ここまで

k.A = {t[:t.find("=")].strip(): parse_value(t)
       for t in TEXT[s:e].split("\\n|")}

k.display()


# %%

k = Knock("""27. 内部リンクの除去Permalink
26の処理に加えて，テンプレートの値からMediaWikiの内部リンクマークアップを除去し，テキストに変換せよ（参考: マークアップ早見表）．""")


# def erase_links(x):
# while "[[" in x and "]]" in x:
#     s = x.find("[[")
#     e = x.find("]]") + 2
#     # if x[s:e].count("|")>1:
#     #     print(x[s:e])

#     if s >= e:
#         print("ERROR：")
#         print(x[s:e])
#     elif x[s:e].startswith("[[ファイル"):
#         print("ファイル：")
#         print(x[s:e])
#         break

#     if "|" in x[s:e]:
#         a = "{{" in x[s:e]
#         b = "}}" in x[s:e]
#         if a and b:
#             print(x[s:e])
#             c = x[s:e].find("{{") + s
#             d = x[s:e].find("}}") + s
#             bar_n_L = x[s:e].count("|", 0, c)
#             bar_n_R = x[s:e].count("|", d)
#             if bar_n_L + bar_n_R == 1:
#                 bar = x[s:e].find("|") if bar_n_L == 1 else x[s:e].find("|", d)
#                 bar += s
#             else :
#                 print("ERROR：")
#                 print(x[s:e])
#         elif a or b:
#             print("ERROR：")
#             print(x[s:e])
#         else:
#             bar = x[s:e].find("|") + s

#         print(x[bar+1:e-2])
#         x = x.replace(x[s+2:bar+1], "")

#     # template_s = x[s:e].find("{{")
#     # template_e = x[s:e].find("}}")
#     # is_not_found = -1 in [template_e, template_s]
#     # is_ordered = template_s < template_e
#     # if (is_not_found and is_ordered) or (not is_not_found and not is_ordered):
#     #     print("ERROR：")
#     #     print(x[s:e])
#     # elif is_not_found and not is_ordered:
#     #     template_s += s
#     #     template_e += s + 2
#     #     print(x[template_s:template_e])
#     #     if x[template_s:template_e].startswith("{{lang"):
#     #         bar = x[template_s:template_e].rfind("|")
#     #         bar += template_s + 1
#     #         x.replace(x[template_s:bar], "")
#     #         x.replace(x[template_e-2:template_e], "")

#     x = x.replace("[[", "", 1)
#     x = x.replace("]]", "", 1)
# return parse_value(x)

def erase_links(x):
    # display(x)
    # display(repr(x))
    matches = re.finditer(r"\[\[(?!ファイル:)(.+?)\]\]", x)
    for y in matches:
        if y:
            # display(y.group(1))
            z = re.search(
                r"\|?([^\{\}\|]*\{\{[^\{\}]+\}\}|[^\{\}\|]+$)", y.group(1))
            if z:
                # display(z.group(1))
                # display(f"x:{x}, y0: {y[0]}, y1: {y[1]}, z0: {z[0]}, z1: {z[1]}")
                x = x.replace(y[0], z[1])
                # x =
            else:
                print("例外：")
                print(y.group(0))
    return parse_value(x)


# コピペここから
s = TEXT.find("{{基礎情報 国\\n|") + len("{{基礎情報 国\\n|")
temp = s
e = TEXT[s:].find("}}") + s
while ("{{" in TEXT[temp:e]):
    temp = e + 2
    e = TEXT[temp:].find("}}") + temp
# ここまで

k.A = {t[:t.find("=")].strip(): erase_links(t)
       for t in TEXT[s:e].split("\\n|")}

k.display()

# %%

k = Knock("""28. MediaWikiマークアップの除去Permalink
27の処理に加えて，テンプレートの値からMediaWikiマークアップを可能な限り除去し，国の基本情報を整形せよ．""")


def erase_refs(x):
    y = re.findall(r"(<ref(?: [^/> ]+ /|[^>]*?>.*?</ref)>)", x)
    if y:
        x = re.sub(r"(<ref(?: [^/> ]+ /|[^>]*?>.*?</ref)>)", "", x)
        # display(y)
    elif "<ref" in x and not "<references/>" in x:
        display("例外：")
        display(x)
    return template_detector(x)


def template_detector(x):
    # for identifier in ["0", "en icon", ""]
    x = x.replace(r"{{0}}", "").replace(
        r"{{en icon}}", "").replace("<references/>", "")
    x = re.sub(r"{{Cite web[^}]*}}", "", x)
    x = re.sub(r"{{center\|([^}\|]*)}}", r"\1", x)
    x = re.sub(r"{{lang\|[^\|]*\|([^}\|]*)}}", r"\1", x)
    x = re.sub(r"{{仮リンク\|[^\|]*\|[^\|]*\|([^}\|]*)}}", r"\1", x)
    x = re.sub(r"\[\[ファイル:(?:[^\|]*\|[^\|]*\|)?([^\|\]]*)\]\]", r"\1", x)
    # z = re.findall(r"\[\[ファイル:(?:[^\|]*\|[^\|]*\|)?([^\|\]]*)\]\]", x)
    # if z:
    #     for Z in z:
    #         display(Z)
    y = re.findall(r"{{(.+?)}}", x)
    if y:
        for Y in y:
            bar = Y.find("|") if "|" in Y else len(Y)
            display(Y[:bar])
        # x = re.sub(r"", "",x)
        # display(y)
    elif "" in x and not "" in x:
        display("例外：")
        display(x)
    return erase_links(x)


# コピペここから
s = TEXT.find("{{基礎情報 国\\n|") + len("{{基礎情報 国\\n|")
temp = s
e = TEXT[s:].find("}}") + s
while ("{{" in TEXT[temp:e]):
    temp = e + 2
    e = TEXT[temp:].find("}}") + temp
# ここまで

k.A = {t[:t.find("=")].strip(): erase_refs(t)
       for t in TEXT[s:e].split("\\n|")}

k.display()

# 次で使う
flag_file = k.A["国旗画像"]


# %%
import urllib.request
k = Knock("""29. 国旗画像のURLを取得するPermalink
テンプレートの内容を利用し，国旗画像のURLを取得せよ．（ヒント: MediaWiki APIのimageinfoを呼び出して，ファイル参照をURLに変換すればよい）""")

encoded = flag_file.replace(" ","%20")
url = f"https://www.mediawiki.org/w/api.php?action=query&format=json&titles=File:{encoded}&prop=imageinfo&iiprop=url"

req = urllib.request.Request(url)
with urllib.request.urlopen(req) as res:
    body = res.read().decode("utf-8")
    data = re.search(r'"url":"([^"]*)"',body)
    # display(body)
    display(data[1])
    k.A = data[1]

k.display()


# %%


# %%
