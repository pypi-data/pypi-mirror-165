# PyelDriver

A python HTML tool to use with FastAPI to deliver 'Hypermedia as The Engine of Application State'.
The idea is based on Apple's SwiftUI & Elm's HTML library and how it curries functions to return a 'super body'.

In scripts you can use all HTML elements as functions allowing deterministic HTML that can be tested.

## Standard Examples

- calling `div()` returns
  `<div></div>`

- calling `div("hello world")` returns
  `<div>hello world</world>`

- calling `div("content", atts({"class":"active"}))` returns
  `<div class="active">content</div>`

- calling `div("content", att({"class":"active", "id":"my-div"}))` returns
  `<div class="active" id="mydiv">content</div>`

- calling `div("content", atts({"special": False}))` returns
  `<div special >content</div>`
  (edited)

## Grouping Examples

You can optionally nest elements within each other.

- `body(div(h1("Hello world))))` returns

```
<body>
   <div>
      <h1>Hello world</h1>
   </div>
</body>
```

- Sibling elements are wrapped with a `Children` function.

```
ol(children([
   li("item 1"),
   li("item 2"),
   ])
)
```

giving

```
<ol>
   <li>Item 1</li>
   <li>Item 2</li>
</ol>
```

# Empty Elements

Elements that do not require an 'end tag' are called 'empty' elements.
This are automatically handled by El. (but you do currently need to know what they are)

`img(atts({"src":"test_image.jpg", "alt":""})`
returns

```
<img src="test_image.jpg" alt="" >
```

## Content and Attributes

Elements are made of a few parts. Ignoring empty elements for now we have:

`<tagname>` `content` `</tagname>`

Optionally all HTML elements can have attributes to provide additonal info.
These are always specified in the start tag and usually are name/value pairs.

### Key Value Pairs

As elements can handle multiple attributes El handles attributes as a `dict` and iterates over them.
This is generally done by passing `atts` as the attributes argument. (although in theory you 'could' hand craft this in certain circumstances.

`div("content", atts({"key":"value"})`

returns

`<div key="value">content</content>`

### Key Only Attribute

Certain elements take just a key. In this circumstances you can set empty to True when passing them in.

`video("Your browser does not support the video tag.", atts({"width":"320", "height":"240", "controls": True}))`

`<video width="320" height="240" controls>Your browser does not support the video tag.</video>`

## Composable

Much like SwiftUi It is expected that multiple smaller items are bundled together to create views.

```
head_view = head(title("Page title"))

nav_view = nav(
    children(
        [
            a("HTML", atts({"href": "/html/"})),
            a("CSS", atts({"href": "/css/"})),
            a("JavaScript", atts(["href": "/js/"})),
            a("Python", atts({"href": "/python/"})),
        ]
    )
)

body_view = body(
    children(
        [
            nav_view,
            main(
                children(
                    [
                        h1("Hello World"),
                        p(
                            "Chrome, Firefox, and Edge are the most popular browsers today."
                        ),
                        article(
                            children(
                                [
                                    h2("Google Chrome"),
                                    p(
                                        "Google Chrome is a web browser developed by Google, released in 2008. Chrome is the world's most popular web browser today!"
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            ),
        ]
    )
)

html_output = html(
    children(
        [
            head_view,
            body_view,
        ]
    )
)

```

returns

```
<html>
  <head>
    <title>Page title</title>
  </head>
  <body>
    <nav>
      <a href="/html/">HTML</a>
      <a href="/css/">CSS</a>
      <a href="/js/">JavaScript</a>
      <a href="/python/">Python</a>
    </nav>
    <main>
      <h1>Hello World</h1>
      <p>Chrome, Firefox, and Edge are the most popular browsers today.</p>
      <article>
        <h2>Google Chrome</h2>
        <p>
          Google Chrome is a web browser developed by Google, released in 2008.
          Chrome is the world's most popular web browser today!
        </p>
      </article>
    </main>
  </body>
</html>
```

## Helper functions

With all El outputs being `str` the opportunity to combine it with normal flow is useful.

For example converting a list to to `select` options is trivial.

```

cars = ["Volvo", "Saab", "Mercedes", "Audi"]


def car_options(cars: list) -> str:
    return "".join(
        [option(f"{car}", atts({"value": f"{car}".lower()})) for car in cars]
    )


html_output = children(
    [
        label("Choose a car:", atts({"for": "cars"})),
        select(car_options(cars)),
    ]
)
```

outputs

```
<label for="cars">Choose a car:</label>

<select>
  <option value="volvo">Volvo</option>
  <option value="saab">Saab</option>
  <option value="mercedes">Mercedes</option>
  <option value="audi">Audi</option>
</select>
```

## Extensibility

Can I extend this?
Probably, it's just python.

Each element is basically a lambda function assigned to a var.
To create an element you can add:

`tagname = _el_factory("tagname")`

or

`tagname = _el_factory("tagname", end_tag=False)`

for a 'empty' element.

## Thoughts and Considerations

... But! this is hard to read! It's not very 'pythonic!'...
I've played with Jinja and template partials but I don't like templating so much.
I want to be able to bring in external data and use it like I normally use Python.

## Todos

- [] Add Tests 😳
- [] Add Pydantic to validate elements.
- [] Add Components for rapid development
- [] Auto 'Prettify' the output HTML as it currently just concatenates.
