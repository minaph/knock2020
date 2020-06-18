# %%
# 1.0

import random
"stressed"[::-1]

# %%
# 1.1
"パタトクカシーー"[1::2]

# %%
# 1.2
"".join([a+b for a, b in zip("パトカー", "タクシー")])

# %%
# 1.3
a = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
a = a.translate(str.maketrans({",": None, ".": None}))
[len(_) for _ in a.split(" ")]

# %%
# 1.4
a = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
b = [1, 5, 6, 7, 8, 9, 15, 16, 19]

# if節はおせっかい（笑）
{v[:2-(i+1 in b)] if i != 11 else "Mg": i +
 1 for i, v in enumerate(a.split(" "))}

# %%
# 1.5


def f(x, n):

    return [x[_:_+n] for _ in range(0, len(x)-n, n)] + [x[-n:]]


t = "I am an NLPer"
f(t, 2), f(t.split(" "), 2)


# %%
# 1.6
a = "paraparaparadise"
b = "paragraph"

X = set(f(a, 2))
Y = set(f(b, 2))

# 順に和・積・差・メンバー判定
X | Y, X & Y, X ^ Y, "se" in X | Y

# %%
# 1.7


def f(x, y, z): return f"{x}時の{y}は{z}"


f(x=12, y="気温", z=22.4)

# %%
# 1.8


def cipher(x):
    def f(y): return y.encode('utf-8').islower() and y.encode('utf-8').isalpha()
    l = [chr(219 - ord(_)) if f(_) else _ for _ in x]
    return "".join(l)


cipher("paraparaｄふぁｈ")

# %%
# 1.9


def f(x):
    x = x.split(" ")

    def g(s):
        return (s[:-1], s[-1]) if s[-1] in {",", "."} else (s, "")

    def h(y):
        print(y)
        return "".join(random.sample(y, len(y)))
    data = [c[0]+h(c[1:-1])+c[-1]+d if len(c) > 4 else c+d for c, d in map(g, x)]
    return " ".join(data)


f("I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind .")
# %%

# %%
