from typing import Callable

## TAG BUILDER
def _el_factory(name: str, end_tag: bool = True) -> Callable:
    if end_tag:
        return lambda c="", a="": _element(name, c, a)
    else:
        return lambda a="": _element(name, attributes=a, end_tag=end_tag)


def _element(tag: str, content: str = "", attributes: str = "", end_tag: bool = True):
    head = f"<{tag}"
    atts = f" {attributes}>" if attributes else ">"
    tail = f"{content}</{tag}>" if end_tag else ""

    return f"{head}{atts}{tail}"


def children(children: list[str]) -> str:
    return "".join([child for child in children])


def atts(attributes: dict) -> str:
    """Check k, v pairs and stringify them. If value is `True` then return just the key without the value."""

    atts = []

    for key, value in attributes.items():
        if value == True:
            atts.append(key)
        else:
            atts.append(f'{key}="{value}"')

    return " ".join(atts)


# Doctype


# Generated from _html_element_maker.py

a = _el_factory("a")
abbr = _el_factory("abbr")
address = _el_factory("address")
area = _el_factory("area", end_tag=False)
article = _el_factory("article")
aside = _el_factory("aside")
audio = _el_factory("audio")
base = _el_factory("base", end_tag=False)
blockquote = _el_factory("blockquote")
body = _el_factory("body")
br = _el_factory("br", end_tag=False)
button = _el_factory("button")
canvas = _el_factory("canvas")
caption = _el_factory("caption")
circle = _el_factory("circle")
cite = _el_factory("cite")
code = _el_factory("code")
col = _el_factory("col", end_tag=False)
colgroup = _el_factory("colgroup")
data = _el_factory("data")
datalist = _el_factory("datalist")
dd = _el_factory("dd")
del_ = _el_factory("del_")
details = _el_factory("details")
dialog = _el_factory("dialog")
div = _el_factory("div")
dl = _el_factory("dl")
dt = _el_factory("dt")
ellipse = _el_factory("ellipse")
em = _el_factory("em")
embed = _el_factory("embed", end_tag=False)
fieldset = _el_factory("fieldset")
figcaption = _el_factory("figcaption")
figure = _el_factory("figure")
footer = _el_factory("footer")
form = _el_factory("form")
h1 = _el_factory("h1")
h2 = _el_factory("h2")
h3 = _el_factory("h3")
h4 = _el_factory("h4")
h5 = _el_factory("h5")
h6 = _el_factory("h6")
head = _el_factory("head")
header = _el_factory("header")
hr = _el_factory("hr", end_tag=False)
html = _el_factory("html")
iframe = _el_factory("iframe")
img = _el_factory("img", end_tag=False)
input = _el_factory("input", end_tag=False)
kbd = _el_factory("kbd")
label = _el_factory("label")
legend = _el_factory("legend")
li = _el_factory("li")
link = _el_factory("link", end_tag=False)
main = _el_factory("main")
map = _el_factory("map")
mark = _el_factory("mark")
menu = _el_factory("menu")
meta = _el_factory("meta", end_tag=False)
meter = _el_factory("meter")
nav = _el_factory("nav")
noscript = _el_factory("noscript")
ol = _el_factory("ol")
optgroup = _el_factory("optgroup")
option = _el_factory("option")
output = _el_factory("output")
p = _el_factory("p")
picture = _el_factory("picture")
polygon = _el_factory("polygon")
portal = _el_factory("portal")
pre = _el_factory("pre")
progress = _el_factory("progress")
param = _el_factory("param", end_tag=False)
q = _el_factory("q")
rect = _el_factory("rect")
s = _el_factory("s")
samp = _el_factory("samp")
script = _el_factory("script")
section = _el_factory("section")
select = _el_factory("select")
slot = _el_factory("slot")
small = _el_factory("small")
source = _el_factory("source", end_tag=False)
span = _el_factory("span")
strong = _el_factory("strong")
style = _el_factory("style")
sub = _el_factory("sub")
summary = _el_factory("summary")
sup = _el_factory("sup")
svg = _el_factory("svg")
table = _el_factory("table")
tbody = _el_factory("tbody")
td = _el_factory("td")
template = _el_factory("template")
text = _el_factory("text")
textarea = _el_factory("textarea")
tfoot = _el_factory("tfoot")
th = _el_factory("th")
thead = _el_factory("thead")
time = _el_factory("time")
title = _el_factory("title")
tr = _el_factory("tr")
track = _el_factory("track", end_tag=False)
u = _el_factory("u")
ul = _el_factory("ul")
var = _el_factory("var")
video = _el_factory("video")
wbr = _el_factory("wbr", end_tag=False)
