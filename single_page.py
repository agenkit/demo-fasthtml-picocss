from fasthtml.common import * # type: ignore
from fasthtml.js import MarkdownJS, SortableJS, HighlightJS
from fastapi import Request

#—————————————————————————————————————————————————————————————————————————————
# HTML 5 conventions
html = Html(lang='en', 
    # data_theme="light"
    )
head = (
    Meta(charset="utf-8"),
    Meta(name="viewport", content="width=device-width, initial-scale=1"),
    Meta(name="color-scheme", content="light dark"),
    Script(src="https://unpkg.com/hyperscript.org@0.9.12"),
    )
line_numbers = (
    Script(src="//cdn.jsdelivr.net/npm/highlightjs-line-numbers.js@2.8.0/dist/highlightjs-line-numbers.min.js"),
    Script("hljs.highlightAll(); hljs.initLineNumbersOnLoad({singleLine: false});")
    )
#—————————————————————————————————————————————————————————————————————————————
# Page-specific
title = Title('FastHTML 🧡 Pico CSS')
footer_text = P("Made by kit using FastHTML & Pico CSS + PrismJS, June 2024.")
#—————————————————————————————————————————————————————————————————————————————
# <head> scripts & css
pico_css = Link(
    rel="stylesheet",
    href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.pumpkin.min.css",
    type="text/css"
    )
page_css = Link(
    rel="stylesheet",
    href="style/single-page copy.css",
    type="text/css"
    )
#—————————————————————————————————————————————————————————————————————————————
# FastHTML app
app = FastHTML(hdrs=(
    head,
    pico_css,
    page_css,
    MarkdownJS('.markdown'),
    SortableJS('.sortable'),
    HighlightJS('.highlight'),
    line_numbers,
    # title,
    ))
rt = app.route

@rt("/{fname:path}.{ext:static}") # Serve static files
async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}') # type: ignore

#—————————————————————————————————————————————————————————————————————————————
# Features
# Dark/Light mode toggle
def theme_switch():
    return Article(
        Button(
        f"Toggle theme",
        cls="contrast",
        hx_post="/toggle_theme",
        hx_swap="outerHTML",
        hx_target="#theme-switcher"
        ),
        id="theme-switcher",
        aria_label="Theme switcher",
    )

#—————————————————————————————————————————————————————————————————————————————
# Helper functions to build proper HTML structure (nesting, etc.)
# Must-have to change ALL at once (CSS class, HTML layout, whatever)
# ⚠️ Absolutely minimalist and specific to this website
def span_code(code, lang=None):
    '''Returns an inline <code> block.
    Use within <h4> sections to display code examples.
    '''
    if lang:
        cls = "inline-code highlight language-"+lang
    else:
        # cls = "inline-code highlight"
        cls = "inline-code"
    return Code(code, cls=cls)

def div_code(code, lang=None):
    '''Returns a <div> wrapping a <pre><code> block.
    Use within <h4> sections to display code examples.
    '''
    if lang: cls='highlight language-'+lang
    else:    cls='highlight'
    return Div(
            Pre(
                Code(code,
                    cls=cls
                ),
            ),
            cls='code',
        )

# TRY: make two wrapper versions of div_code(…) function:
#     1. cl_h(…, lang='html')    🡆 HTML
#     2. cl_f(…, lang='python')  🡆 FastHTML (Python)
# Advantages:
# - everything hardwired even `lang` → it will never change in relation to the code itself but to the highlighter
# - readability
#   - only diff is style, logic is the same
# - maintainability (→ select all HTML or all Python at once)
# - faster to write

def cl_h(code, lang='html'):
    '''Think of this as div_code_html().
    '''
    return div_code(code, lang)

def cl_f(code, lang='python'):
    '''Think of this as div_code_python_fasthtml().
    '''
    return div_code(code, lang)



# def div_code_footer(code, lang=None):
#     '''⚠ DEPRECATED → looks bad, useless.
    
#     Returns a <footer> wrapping a <pre><code> block.
#     Use in <article> to display code examples.
#     '''
#     return Footer(div_code(code, lang), cls="code")

def heading(lv:int, title:str, desc=None):
    '''Returns a header block with title and anchor link. Followed by optional description.
    '''
    h = [H1, H2, H3, H4, H5, H6]
    hn = h[lv-1]
    anchor = title.lower().replace(' ', '-')
    return (
        hn(
            title,
            A(
                '🔗',
                href='#'+anchor,
                id=anchor,
                cls='secondary',
                tabindex="-1",
            )
        ),
        P(desc) if desc else None,
    )

def aside(*aside_tags):
    '''Returns an <aside> block. TODO: Implementation lol 😹
    `aside_tags` needs to be created (ToC) from the list of H2, H3, H4…
    '''
    return Aside(aside_tags)

#   ➕
# def art_c(*c): # c for content
#     return (*c, )

# #   ➕
# def art_footer(html, python):
#     return Footer(Pre(span_code(html)), Pre(span_code(python)))

#   🡇
def article(*c, hd=None, ft=None, card=False, **kwargs):
    return Card(*c, header=hd, footer=ft, **kwargs) if card else Article(*c, header=hd, footer=ft, **kwargs)


# c: lv2_s & lv3_s contain other sections (lv3_s & lv4_s respectively);
#    lv4_s contains c_n_m_k (tuple of HTML tags)
def section(*c, lv:int, title:str, desc=None, **kwargs):
    return Section(heading(lv=lv, title=title, desc=desc), *c, **kwargs)

# We wrap all lv2 (MAIN) sections in a div with proper id and role.
def div_lv2_s(*sections, **kwargs):
    return Div(*sections, id="content", role="document", **kwargs)

# Create <main> with flat lv2 (MAIN) sections. Optional aside etc.
def main(*lv2_s, aside_tags=None, **kwargs):
    return (
        Main(
            aside(aside_tags) if aside_tags else None,
            div_lv2_s(*lv2_s, **kwargs),
            cls="container",
        )
    )

#—————————————————————————————————————————————————————————————————————————————
# PAGE CONTENTS

# pico_ → HTML/CSS code
# fh_   → FastHTML (Python) code
# body_ → Tags
# sec_  → section
# #_#_# → section number
# lv#_sec → <h#> (h2, h3, h4) section

#——————————————————————————————————————————————————————————————————————————— 1
# 1. Getting started
# 1.1. Quick start
# 1.2. Version picker
# 1.3. Color schemes
# 1.4. Class-less version
# 1.5. Conditional styling
# 1.6. RTL

#—————————————————————————————————— 1.1
# 1.1 Quick start
# 1.1.1 Install manually
# 1.1.2 Usage from CDN
# 1.1.3 Usage with NPM
# 1.1.4 Install with Composer
# 1.1.5 Starter HTML template

pico_1_1_1 = div_code(
    """<link rel="stylesheet" href="css/pico.min.css" />""",
    lang="html",
    )
#    🡇🡇🡇
body_1_1_1 = (
    P(
        A(
            "Download Pico",
            rel="noopener noreferrer",
            href="https://github.com/picocss/pico/archive/refs/heads/main.zip",
            target="_blank"
        ),
        """ and link """,
        span_code("/css/pico.min.css"),
        """ in the """,
        span_code("""<head>""", lang="html", ),
        """ of your website.""",
    ),
    pico_1_1_1,
)
#   🡇🡇🡇
sec_1_1_1 = section(
    body_1_1_1,
    lv=4, title="Install manually",
)

#  ＋

pico_1_1_2 = div_code(
"""<link 
  rel="stylesheet" 
  href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
/>""",
  lang="html",
)
#    🡇🡇🡇
body_1_1_2 = P(
    """Alternatively, you can use """,
    A(
        "jsDelivr CDN",
        rel="noopener noreferrer",
        href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/",
        target="_blank"
    ),
    """ to link """,
    span_code("pico.min.css"),
    '.',
    pico_1_1_2,
)
# 🡇🡇🡇
sec_1_1_2 = section(body_1_1_2,
    lv=4, title="Usage from CDN",
)

#  ＋

pico_1_1_5 = div_code(
"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light dark" />
    <link rel="stylesheet" href="css/pico.min.css">
    <title>Hello world!</title>
  </head>
  <body>
    <main class="container">
      <h1>Hello world!</h1>
    </main>
  </body>
</html>""",
    lang="html",
)

fh_1_1_5 = div_code(
"""from fasthtml.common import *

html = Html(lang='en')
head = (
    Meta(charset="utf-8"),
    Meta(name="viewport", content="width=device-width, initial-scale=1"),
    Meta(name="color-scheme", content="light dark"),
    Link(rel="stylesheet", 
        href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.pumpkin.min.css"
        )
    )

app = FastHTML(hdrs=head)
rt = app.route

@rt("/")
def get():
    return html, Main(H1('Hello world!'), cls="container")""",
    lang="python",
)


# 🡇🡇🡇
sec_1_1_5 = section(pico_1_1_5, fh_1_1_5,
    lv=4, title="Starter HTML template",
)

#   🡇🡇🡇
# this must nest all lv4_s
sec_1_1_0 = section(
    P("There are 4 ways to get started with pico.css:"),
    sec_1_1_1,
    sec_1_1_2,
    sec_1_1_5,
    lv=3, title="Quick start",
    desc=(
        """Link """,
        span_code("pico.css"),
         """ manually or via CDN for a dependency-free setup, or use NPM or Composer for advanced usage.""",
    ),
)


#—————————————————————————————————— 1.2



sec_1_2_0 = section(
    lv=3, title="Version picker",
    desc="Easily select the ideal Pico CSS version variant to match your project's needs."
)









#—————————————————————————————————— 1.3


body_1_3_1 = (
    P(  "Color schemes can be defined for the entire document using ",
        span_code('<html data-theme="light">', lang='html'),
        " or for specific HTML elements, such as ",
        span_code('<article data-theme="dark">', lang='html'),
        ".",
    ),
    P(  "Color schemes at the HTML tag level work great for elements such as ",
        span_code('<a>', lang='html'), ', ',
        span_code('<button>', lang='html'), ', ',
        span_code('<table>', lang='html'), ', ',
        span_code('<input>', lang='html'), ', ',
        span_code('<textarea>', lang='html'), ', ',
        span_code('<select>', lang='html'), ', ',
        span_code('<article>', lang='html'), ', ',
        span_code('<dialog>', lang='html'), ', ',
        span_code('<progress>', lang='html'), '.',
    ),
    P(  "CSS variables specific to the color scheme are assigned to every HTML tag. However, we have not enforced specific background and color settings across all HTML tags to maintain transparent backgrounds and ensure colors are inherited from the parent tag."
    ),
    P(  "For some other HTML tags, you might need to explicitly set ",
    span_code('background-color', lang='css'),
    " and ",
    span_code('color', lang='css'),
    "."
    ),
),

css_1_3_1 = div_code(
"""section {
  background-color: var(--pico-background-color);
  color: var(--pico-color);
}""",
    lang="css",
)


sec_1_3_1 = section(body_1_3_1, css_1_3_1, 
    lv=4, title="Usage",
)

def art_1_3_2(dark:bool=False) -> Article:
    if dark:
        theme, title = "dark", H2("Dark card")
    else:
        theme, title = "light", H2("Light card")
    aria = f"Forced {theme} theme example"
    pico = f"<article data-theme={theme}>\n  …\n</article>"
    footer = Footer(Pre(span_code(pico, lang='html'),),cls="code",)
    form = Form(
        Fieldset(
            Input(type="text",
                name="login",
                placeholder="Login",
                aria_label="Login",
                autocomplete="username",
            ),
            Input(type="password",
                name="password",
                placeholder="Password",
                aria_label="Password",
                autocomplete="current-password",
            ),
            Button("Login", type="submit"),
            cls='grid',
        ),
        Fieldset(
            Label(
                Input(type="checkbox", 
                    role="switch", 
                    name="switch", 
                    checked="",
                ),
                "Remember me",
            ),
        ),
    )
    return Article(
    title,
    form,
    footer,
    cls="card",
    data_theme=theme,
    aria_label=aria,
    )

art_1_3_2a = art_1_3_2()
art_1_3_2b = art_1_3_2(dark=True), 
fh_1_3_2 = P("FastHTML 🡇", cls="fh-cue"), div_code(
"""Article(…, data_theme="light")\nArticle(…, data_theme="dark")""", 
    lang="python",
    )

sec_1_3_2 = section(
    art_1_3_2a, 
    art_1_3_2b,
    fh_1_3_2,
    lv=4, title="Card example",
)

sec_1_3_0 = section(
    P("""The default color scheme is Light. The Dark scheme is automatically enabled if the user has dark mode enabled """, 
      span_code("prefers-color-scheme: dark;"), '.'),
    theme_switch(),
    sec_1_3_1,
    sec_1_3_2,
    lv=3, title="Color Schemes",
    desc=(
        """Pico CSS comes with both Light and Dark color schemes, automatically enabled based on user preferences."""
    )
)

#—————————————————————————————————— 1.4

sec_1_4_0 = section(
    lv=3, title="Class-less version",
    desc=(
        "Embrace minimalism with Pico’s ",
        span_code(".classless"),
        " version, a semantic option for wild HTML purists who prefer a stripped-down approach.",
    ),
)

#—————————————————————————————————— 1.5

sec_1_5_0 = section(
    lv=3, title="Conditional styling",
    desc=(
        "Apply Pico CSS styles selectively by wrapping elements in a ",
        span_code(".pico"),
        " container, ideal for mixed-style environments.",
    ),
)

#—————————————————————————————————— 1.6

sec_1_6_0 = section(
    lv=3, title="RTL",
    desc="Support for Right-To-Left text."
)

#  🡇
# lv2_s must nest all lv3_s
sec_1_0_0 = section(
    sec_1_1_0,
    sec_1_2_0,
    sec_1_3_0,
    sec_1_4_0,
    sec_1_5_0,
    sec_1_6_0,
    lv=2, title="Getting started",
)
#——————————————————————————————————————————————————————————————————————————— 2
# 2. Customization
# 2.1 CSS Variables
# 2.2 Sass
# 2.3 Colors

#—————————————————————————————————— 2.1

sec_2_1_0 = section(
    lv=3, title="CSS Variables",
    desc="Customize Pico's design system with over 130 CSS variables to create a unique look and feel."
)

#—————————————————————————————————— 2.2

sec_2_2_0 = section(
    lv=3, title="Sass",
    desc=(
        "Build your own minimal design system by compiling a custom version of Pico CSS framework with ",
        A("SASS"),
        "."),
)

#—————————————————————————————————— 2.3

sec_2_3_0 = section(
    lv=3, title="Colors",
    desc="Pico comes with 380 manually crafted colors to help you personalize your brand design system."
)


sec_2_0_0 = section(
    sec_2_1_0,
    sec_2_2_0,
    sec_2_3_0,
    lv=2, title="Customization",
)

#——————————————————————————————————————————————————————————————————————————— 3
# 3.Layout
# 3.1 Container
# 3.2 Landmarks & section
# 3.3 Grid
# 3.4 Overflow auto NEW

#—————————————————————————————————— 3.1
# 3.1 Container
# 3.1.1 Breakpoints
# 3.1.2 Fixed width
# 3.1.3 Fluid width
# 3.1.4 Semantic containers

body_3_1_1a = (
    P("Pico includes six default breakpoints. These breakpoints can be customized with ",
      A("Sass", href="https://picocss.com/docs/sass"), "."),
)

table_3_1_1 = Table(
    Thead(Tr(Th("Device"), Th("Breakpoint"), Th("Viewport"))),
    Tbody(
        Tr(Td("Extra small"), Td("<576px"), Td("100%")),
        Tr(Td("Small"), Td("≥576px"), Td("510px")),
        Tr(Td("Medium"), Td("≥768px"), Td("700px")),
        Tr(Td("Large"), Td("≥1024px"), Td("950px")),
        Tr(Td("Extra large"), Td("≥1280px"), Td("1200px")),
        Tr(Td("Extra extra large"), Td("≥1536px"), Td("1450px")),
    ),
)

body_3_1_1b = (
    P(span_code(".container"),
    " and ",
    span_code(".container-fluid"),
    " are not available in the ",
    A("class‑less version", href="https://picocss.com/docs/classless"),
    " (see ",
    A("Semantic containers", href="https://picocss.com/docs/container#semantic-containers"),
    " for an alternative)."),
)

sec_3_1_1 = section(
    body_3_1_1a,
    table_3_1_1,
    body_3_1_1b,
    lv=4, title="Breakpoints",
)

body_3_1_2 = (
    P(span_code(".container"), " provides a centered container with a fixed width."),
    div_code(
"""<body>
  <main class="container">
    ...
  </main>
</body>
""", lang="html"),
)

sec_3_1_2 = section(
    body_3_1_2,
    lv=4, title="Fixed width",
)

body_3_1_3 = (
    P(span_code(".container-fluid"), " provides a full-width container."),
    div_code(
"""<body>
  <main class="container-fluid">
    ...
  </main>
</body>
""", lang="html"),
)

sec_3_1_3 = section(
    body_3_1_3,
    lv=4, title="Fluid width",
)

body_3_1_4 = (
    P(
        "In the classless version, ",
        span_code("<header>", lang='html'), ", ",
        span_code("<main>", lang='html'), ", and ",
        span_code("<footer>", lang='html'),
        " inside ",
        span_code("<body>", lang='html'),
        " act as containers to define a centered or a fluid viewport."),
    P("See ", A("Class-less version", href="https://picocss.com/docs/classless"), "."),
)

sec_3_1_4 = section(
    body_3_1_4,
    lv=4, title="Semantic containers",
)

sec_3_1_0 = section(
    sec_3_1_1,
    sec_3_1_2,
    sec_3_1_3,
    sec_3_1_4,
    lv=3, title="Container",
    desc=("Use ", span_code('.container'), "for a centered viewport or ", span_code('.container-fluid'), " for a full-width layout.")
)

#—————————————————————————————————— 3.2
# 3.2 Landmarks & section
# 3.2.1 Landmarks
# 3.2.2 Custom root container
# 3.2.3 Section


body_3_2_1 = (
    P(
        span_code("<header>", lang='html'), ", ",
        span_code("<main>", lang='html'), ", and ",
        span_code("<footer>", lang='html'),
        " as direct children of ",
        span_code("<body>", lang='html'),
        " provide a responsive vertical padding.",
    ),
)

pico_3_2_1 = div_code(
"""<body>
  <header>...</header>
  <main>...</main>
  <footer>...</footer>
</body>
""", lang="html"),


sec_3_2_1 = section(
    body_3_2_1,
    pico_3_2_1,
    lv=4, title="Landmarks",
)

body_3_2_2a = (
    P(
        "If you need to customize the default root container for ",
        span_code("<header>", lang='html'), ", ",
        span_code("<main>", lang='html'), ", and ",
        span_code("<footer>", lang='html'),
        ", you can recompile Pico with another CSS selector.",
    ),
    P("Useful for ", A("React", href="https://reactjs.org/"), ", ", A("Gatsby", href="https://www.gatsbyjs.com/"), " or ", A("Next.js", href="https://nextjs.org/"), "."),
)

pico_3_2_2a = div_code(
"""/* Custom Class-less version for React */
@use "pico" with (
  
  // Define the root element used to target <header>, <main>, <footer>
  // with $enable-semantic-container and $enable-responsive-spacings
  $semantic-root-element: "#root";
  
  // Enable <header>, <main>, <footer> inside $semantic-root-element as containers
  $enable-semantic-container: true;

  // Enable .classes
  $enable-classes: false;
)
""", lang="jsx"),

body_3_2_2b = (
    P("The code above will compile Pico with the containers defined like this:"),
)

pico_3_2_2b = div_code(
"""/* Containers */
#root > header,
#root > main,
#root > footer {
  ...
}
""", lang="css"),

body_3_2_2c = (
    P(
        "Learn more about ", 
        A("compiling a custom version of Pico with SASS", 
          href="https://picocss.com/docs/sass"), "."),
)

sec_3_2_2 = section(
    body_3_2_2a,
    pico_3_2_2a,
    body_3_2_2b,
    pico_3_2_2b,
    body_3_2_2c,
    lv=4, title="Custom root container",
)


body_3_2_3 = (
    P(
        span_code("<section>", lang='html'), 
        " provides a responsive margin-bottom to separate your sections."),
)

sec_3_2_3 = section(
    body_3_2_3,
    lv=4, title="Section",
)

sec_3_2_0 = section(
    sec_3_2_1,
    sec_3_2_2,
    sec_3_2_3,
    lv=3, title="Landmarks & section",
    desc="Structure your pages with semantic landmarks and sections for better accessibility and graceful spacings.",
)

#—————————————————————————————————— 3.3
# 3.3 Grid
# 3.3.1 Syntax
# 3.3.2 About CSS Grids

art_3_3_1 = Article(
    Div(
        Div(1),
        Div(2),
        Div(3),
        Div(4),
        cls="grid"
    ),
    Footer(
        div_code(
"""<div class="grid">
  <div>1</div>
  <div>2</div>
  <div>3</div>
  <div>4</div>
</div>""", 
        lang="html"),
        cls="code",
    ),
    cls="component"
)

body_3_3_1 = (
    P("Columns intentionally collapse on small devices (", span_code("<768px"), ")."),
    P(span_code(".grid"), "is not available in the ", A("class‑less", href="https://picocss.com/docs/classless"), " version."),
)

sec_3_3_1 = section(
    art_3_3_1,
    body_3_3_1,
    lv=4, title="Syntax",
)

body_3_3_2 = (
    P("As Pico focuses on native HTML elements, we kept this grid system minimalist."),
    P("A complete grid system in flexbox, with all the ordering, offsetting, and breakpoints utilities, can be heavier than the total size of the Pico library. Not really in the Pico spirit."),
    P("If you need a quick way to prototype or build a complex layout, you can look at ", Strong("Flexbox grid layouts"), "—for example, ", A("Bootstrap Grid System", href="https://getbootstrap.com/docs/4.2/getting-started/contents/"), " or ", A("Flexbox Grid", href="http://flexboxgrid.com/"), "."),
    P("If you need a light and custom grid, you can look at CSS Grid Generators—for example, ", A("CSS Grid Generator", href="https://cssgrid-generator.netlify.com/"), ", ", A("Layoutit!", href="http://grid.layoutit.com/"), " or ", A("Griddy", href="https://griddy.io/"), "."),
    P("Alternatively, you can ", A("learn about CSS Grid", href="https://learncssgrid.com/"), "."),
)

sec_3_3_2 = section(
    body_3_3_2,
    lv=4, title="About CSS Grids",
)



sec_3_3_0 = section(
    sec_3_3_1,
    sec_3_3_2,
    lv=3, title="Grid",
    desc=(
        "Create minimal responsive layouts with ", 
        span_code(".grid"), 
        " to enable auto-layout columns."),
)

#—————————————————————————————————— 3.4
# 3.4 Overflow auto


body_3_4_1 = (
    P("Useful to have responsive ", span_code("<table>", lang='html'), "."),
)

table_3_4_1 = (Div(
    Table(
        Thead(
            Tr(Th("Heading"),Th("Heading"),Th("Heading"),Th("Heading"),
               Th("Heading"),Th("Heading"),Th("Heading"),Th("Heading"),
               Th("Heading"),Th("Heading"),Th("Heading"),Th("Heading"))),
        Tbody(
            Tr(Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),
               Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell")),
            Tr(Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),
               Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell")),
            Tr(Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),
               Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell"),Td("Cell")),)
    ), 
    cls="overflow-auto",
))

pico_3_4_1 = div_code(
"""<div class="overflow-auto">
  <table>
    …
  </table>
</div>""", 
        lang="html"
)

sec_3_4_0 = section(
    body_3_4_1,
    table_3_4_1,
    pico_3_4_1,
    lv=3, title="Overflow auto",
    desc=(
        span_code(".overflow-auto"),
        " enables automatic scrollbars to an element if its content extends beyond its limits."),
)

sec_3_0_0 = section(
    sec_3_1_0,
    sec_3_2_0,
    sec_3_3_0,
    sec_3_4_0,
    lv=2, title="Layout",
)
#————————————————————————————————————————————————————————————————————————————4
# 4. Content
# 4.1 Typography
# 4.2 Link
# 4.3 Button
# 4.4 Table

#—————————————————————————————————— 4.1
# 4.1 Typography
# 4.1.1 Font sizes
# 4.1.2 Headings
# 4.1.3 Heading group
# 4.1.4 Inline text elements
# 4.1.5 Blockquote
# 4.1.6 Horizontal rule

table_4_1_1a = Table(
    Thead(
        Tr(Th("Breakpoint"),Th("xs"),Th("sm"),Th("md"),Th("lg"),Th("xl"),Th("xxl")),
    ),
    Tbody(
        Tr(Td("Base"),Td("16px"),Td("17px"),Td("18px"),    Td("19px"),   Td("20px"),    Td("21px")),
        Tr(Td(span_code("<h1>")   ),  Td("32px"),Td("34px"),    Td("36px"),   Td("38px"),    Td("40px"),  Td("42px")),
        Tr(Td(span_code("<h2>")   ),  Td("28px"),Td("29.75px"), Td("31.5px"), Td("33.25px"), Td("35px"),  Td("36.75px")),
        Tr(Td(span_code("<h3>")   ),  Td("24px"),Td("25.5px"),  Td("27px"),   Td("28.5px"),  Td("30px"),  Td("31.5px")),
        Tr(Td(span_code("<h4>")   ),  Td("20px"),Td("21.25px"), Td("22.5px"), Td("23.75px"), Td("25px"),  Td("26.25px")),
        Tr(Td(span_code("<h5>")   ),  Td("18px"),Td("19.125px"),Td("20.25px"),Td("21.375px"),Td("22.5px"),Td("23.625px")),
        Tr(Td(span_code("<h6>")   ),  Td("16px"),Td("17px"),    Td("18px"),   Td("19px"),    Td("20px"),  Td("21px")),
        Tr(Td(span_code("<small>")),  Td("14px"),Td("14.875px"),Td("15.75px"),Td("16.625px"),Td("17.5px"),Td("18.375px")),
    ),
    cls="overflow-auto",
)

body_4_1_1a = P("In ", span_code("rem"), " units:")

table_4_1_1b = Table(
    Thead(
        Tr(Th("Breakpoint"),Th("xs"),Th("sm"),Th("md"),Th("lg"),Th("xl"),Th("xxl")),
    ),
    Tbody(
        Tr(Td("Base"),Td("100%"),Td("106.25%"),Td("112.5%"),Td("118.75%"),Td("125%"),Td("131.25%")),
        Tr(Td(span_code("<h1>")   ),Td("x 2rem"),Td("x 2rem"),Td("x 2rem"),Td("x 2rem"),Td("x 2rem"),Td("x 2rem")),
        Tr(Td(span_code("<h2>")   ),Td("x 1.75rem"),Td("x 1.75rem"),Td("x 1.75rem"),Td("x 1.75rem"),Td("x 1.75rem"),Td("x 1.75rem")),
        Tr(Td(span_code("<h3>")   ),Td("x 1.5rem"),Td("x 1.5rem"),Td("x 1.5rem"),Td("x 1.5rem"),Td("x 1.5rem"),Td("x 1.5rem")),
        Tr(Td(span_code("<h4>")   ),Td("x 1.25rem"),Td("x 1.25rem"),Td("x 1.25rem"),Td("x 1.25rem"),Td("x 1.25rem"),Td("x 1.25rem")),
        Tr(Td(span_code("<h5>")   ),Td("x 1.125rem"),Td("x 1.125rem"),Td("x 1.125rem"),Td("x 1.125rem"),Td("x 1.125rem"),Td("x 1.125rem")),
        Tr(Td(span_code("<h6>")   ),Td("x 1rem"),Td("x 1rem"),Td("x 1rem"),Td("x 1rem"),Td("x 1rem"),Td("x 1rem")),
        Tr(Td(span_code("<small>")),Td("x 0.875em"),Td("x 0.875em"),Td("x 0.875em"),Td("x 0.875em"),Td("x 0.875em"),Td("x 0.875em")),
    ),
    cls="overflow-auto",
)

body_4_1_1b = (
    P("To ensure that the user’s default font size is followed, the base font size is defined as a percentage that grows with the user’s screen size, while HTML elements are defined in ", span_code("rem"), "."), 
    P("Since ", span_code("rem"), " is a multiplier of the HTML document font size, all HTML element’s font sizes grow proportionally with the size of the user’s screen.")
    )

sec_4_1_1 = section(
    body_4_1_1a,
    table_4_1_1a,
    body_4_1_1b,
    table_4_1_1b,
    lv=4, title="Font sizes",
)

#——————————————————
art_4_1_2 = article(
    H1("Heading 1"),
    H2("Heading 2"),
    H3("Heading 3"),
    H4("Heading 4"),
    H5("Heading 5"),
    H6("Heading 6"),)
    
pico_4_1_2 = div_code(
code="""<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6</h6>""",
lang="html"),

sec_4_1_2 = section(
    art_4_1_2,
    pico_4_1_2,
    lv=4, title="Headings",
)

#——————————————————

sec_4_1_3 = section(
    P("Not implemented in FastHTML (as of 2024.06.24)."),
    P("I've done a basic rendering (in CSS) of the ", span_code("<hgroup>"), " demo on the Pico CSS website to style this page's ", span_code("<h3>"), " titles."),

    lv=4, title="Heading group",
)

#——————————————————
body_4_1_4 = Div(
    Div(P("Abbr.", span_code("<abbr>", lang='html')),
    P("Bold", span_code("<strong>", lang='html'), span_code("<b>", lang='html')),
    P("Italic", span_code("<i>", lang='html'), span_code("<em>", lang='html'), span_code("<cite>", lang='html')),
    P("Deleted", span_code("<del>", lang='html')),
    P("Inserted", span_code("<ins>", lang='html')),
    P("Ctrl + S", span_code("<kbd>", lang='html')),
    ),
    Div(P("Highlighted", span_code("<mark>", lang='html')),
    P("Strikethrough", span_code("<s>", lang='html')),
    P("Small", span_code("<small>", lang='html')),
    P("Text Sub", span_code("<sub>", lang='html')),
    P("Text Sup", span_code("<sup>", lang='html')),
    P("Underline", span_code("<u>", lang='html')),
    ),
    cls="grid",
)

sec_4_1_4 = section(
    P("Some of these are not implemented in FastHTML (as of 2024.06.24)."),
    body_4_1_4,
    lv=4, title="Inline text elements",
)
#——————————————————
sec_4_1_5 = section(
    P("Not implemented in FastHTML (as of 2024.06.24)."),
    lv=4, title="Blockquote",
)
#——————————————————
art_4_1_6 = article(
    P("Paragraph above the horizontal line."),
    Hr(),
    P("Paragraph below the horizontal line."),
)
pico_4_1_6 = div_code(
    code="""<p>Paragraph above the horizontal line.</p>
<hr />
<p>Paragraph below the horizontal line.</p>""",
    lang="html",
)
sec_4_1_6 = section(
    art_4_1_6,
    pico_4_1_6,
    lv=4, title="Horizontal rule",
)

#——————————————————
sec_4_1_0 = section(
    sec_4_1_1,
    sec_4_1_2,
    sec_4_1_3,
    sec_4_1_4,
    sec_4_1_5,
    sec_4_1_6,
    lv=3, title="Typography",
    desc="All typographic elements are responsive and scale gracefully across devices and viewports.",
)

#—————————————————————————————————— 4.2
# 4.2 Link


art_4_2_0a = article(
    A("Primary"),
    Br(),
    A("Secondary", cls="secondary"),
    Br(),
    A("Contrast", cls="contrast"),
)

pico_4_2_0a = div_code(
    code="""<a href="#">Primary</a>
<a href="#" class="secondary">Secondary</a>
<a href="#" class="contrast">Contrast</a>""",
    lang="html",
)

body_4_2_0a = (
    P(
        span_code(".secondary"), 
        " and ", 
        span_code(".contrast"), 
        " classes are not available in the class‑less version."
    ), 
    P(
        span_code("aria-current"), 
        " send the active state to assistive technologies and is displayed as the hover links."
    ),
)


art_4_2_0b = article(
    A("Regular link"),
    Br(),
    A("Active link", aria_current="page"),
    Br(),
    A("Regular link"),
)

pico_4_2_0b = div_code(
    code="""<a href="#">Regular link</a>
<a href="#" aria-current="page">Active link</a>
<a href="#">Regular link</a>""",
    lang="html",
)



sec_4_2_0 = section(
    art_4_2_0a,
    pico_4_2_0a,
    body_4_2_0a,
    art_4_2_0b,
    pico_4_2_0b,
    lv=3, title="Link",
    desc=(
        "Links come with ",
        span_code(".secondary"),
        " and ",
        span_code(".contrast"),
        " styles."
    ),
)

#—————————————————————————————————— 4.3
# 4.3 Button
# 4.3.1 Syntax
# 4.3.2 Variants
# 4.3.3 Form buttons
# 4.3.4 Disabled
# 4.3.5 Role button
# 4.3.6 Usage with group

#——————————————————
art_4_3_1 = article(
    Button("Button"),
)

pico_4_3_1 = div_code(
    code="""<button>Button</button>""",
    lang="html",
)

sec_4_3_1 = section(
    art_4_3_1,
    pico_4_3_1,
    lv=4, title="Syntax",
)

#——————————————————
body_4_3_2a = P("Buttons come with ", span_code(".secondary"), " and ", span_code(".contrast"), "styles (not available in the ", A("class-less version", href="https://picocss.com/docs/classless"), ")."),

art_4_3_2a = article(Div(
    Button("Secondary", cls="secondary"),
    Button("Contrast", cls="contrast"),
    cls="grid",
    )
)

pico_4_3_2 = div_code(
    code="""<button class="secondary">Button</button>
<button class="contrast">Button</button>""",
    lang="html",
)

body_4_3_2b = P("They also come with a classic outline style (not available in the ", A("class-less version", href="https://picocss.com/docs/classless"), ").")

art_4_3_2b = article(Div(
    Button("Primary", cls="outline"),
    Button("Secondary", cls="outline secondary"),
    Button("Contrast", cls="outline contrast"),
    cls="grid",
))

pico_4_3_2b = div_code(
    code="""<button class="outline">Primary</button>
<button class="outline secondary">Secondary</button>
<button class="outline contrast">Contrast</button>""",
    lang="html",
)

sec_4_3_2 = section(
    body_4_3_2a,
    art_4_3_2a,
    pico_4_3_2,
    body_4_3_2b,
    art_4_3_2b,
    pico_4_3_2b,
    lv=4, title="Variants",
)

#——————————————————

body_4_3_3a = P(
    span_code('type="submit"'), 
    " and ", 
    span_code('type="button"'), 
    " inputs are also displayed as buttons. All form buttons are ", 
    span_code('width: 100%;'), 
    " by default, to match with the other form elements."
)

art_4_3_3a = article(
    Input(type="submit"),
    Input(type="button", value="Input"),
)

pico_4_3_3a = div_code(
    code="""<input type="submit" />
<input type="button" value="Input" />""",
    lang="html",
)

body_4_3_3b = P("Reset inputs have the secondary style by default.")

art_4_3_3b = article(
    Input(type="reset"),
)

pico_4_3_3b = div_code(
    code="""<input type="reset" />""",
    lang="html",
)

sec_4_3_3 = section(
    body_4_3_3a,
    art_4_3_3a,
    pico_4_3_3a,
    body_4_3_3b,
    art_4_3_3b,
    pico_4_3_3b,
    lv=4, title="Form buttons",
)

#——————————————————

body_4_3_4 = (
    P("Not implemented in FastHTML (as of 2024.06.24)."),
    P("Buttons come with a disabled style."),
    )

art_4_3_4 = article(
    Button("Button", disabled=True),
)

pico_4_3_4 = div_code(
    code="""<button disabled>Button</button>""",
    lang="html",
)

sec_4_3_4 = section(
    body_4_3_4,
    art_4_3_4,
    pico_4_3_4,
    lv=4, title="Disabled",
)

#——————————————————

body_4_3_5 = P("Clickable elements with ", 
               span_code("role='button'"), 
               " are rendered as buttons.")

art_4_3_5 = article(
    Div("Div as a button", role="button", tabindex="0"),
)

pico_4_3_5 = div_code(
    code="""<div role="button" tabindex="0">Div as a button</div>""",
    lang="html",
)

sec_4_3_5 = section(
    body_4_3_5,
    art_4_3_5,
    pico_4_3_5,
    lv=4, title="Role button",
)

#——————————————————

body_4_3_6 = P("You can use ", span_code("role='group'"), " with buttons. See Group.")

art_4_3_6 = article(
    Div(
        Button("Button"),
        Button("Button"),
        Button("Button"),
        role="group",
    )
)

pico_4_3_6 = div_code(
    code="""<div role="group">
  <button>Button</button>
  <button>Button</button>
  <button>Button</button>
</div>""",
    lang="html",
)

sec_4_3_6 = section(
    body_4_3_6,
    art_4_3_6,
    pico_4_3_6,
    lv=4, title="Usage with group",
)

#——————————————————
sec_4_3_0 = section(
    sec_4_3_1,
    sec_4_3_2,
    sec_4_3_3,
    sec_4_3_4,
    sec_4_3_5,
    sec_4_3_6,
    lv=3, title="Button",
    desc=(
        "Buttons are using the native ",
        span_code("<button>", lang='html'),
        " tag, without ",
        span_code(".classes"),
        ". for the default style."),
)

#—————————————————————————————————— 4.4
# 4.4 Table
# 4.4.1 Syntax
# 4.4.2 Color schemes
# 4.4.3 Striped

table_4_4_1 = Table(
    Thead(
        Tr(
            Th("Planet"),
            Th("Diameter (km)"),
            Th("Distance to Sun (AU)"),
            Th("Orbit (days)"),
        )
    ),
    Tbody(
        Tr(
            Td("Mercury"),
            Td("4,880"),
            Td("0.39"),
            Td("88"),
        ),
        Tr(
            Td("Venus"),
            Td("12,104"),
            Td("0.72"),
            Td("225"),
        ),
        Tr(
            Td("Earth"),
            Td("12,742"),
            Td("1.00"),
            Td("365"),
        ),
        Tr(
            Td("Mars"),
            Td("6,779"),
            Td("1.52"),
            Td("687"),
        ),
        Tfoot(
            Td("Average"),
            Td("9,126"),
            Td("0.91"),
            Td("341"),
        ),
    )
)

pico_4_4_1 = div_code(
    code="""<table>
  <thead>
    <tr>
      <th scope="col">Planet</th>
      <th scope="col">Diameter (km)</th>
      <th scope="col">Distance to Sun (AU)</th>
      <th scope="col">Orbit (days)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Mercury</th>
      <td>4,880</td>
      <td>0.39</td>
      <td>88</td>
    </tr>
    <tr>
      <th scope="row">Venus</th>
      <td>12,104</td>
      <td>0.72</td>
      <td>225</td>
    </tr>
    <tr>
      <th scope="row">Earth</th>
      <td>12,742</td>
      <td>1.00</td>
      <td>365</td>
    </tr>
    <tr>
      <th scope="row">Mars</th>
      <td>6,779</td>
      <td>1.52</td>
      <td>687</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row">Average</th>
      <td>9,126</td>
      <td>0.91</td>
      <td>341</td>
    </tr>
  </tfoot>
</table>""",
    lang="html",
)


sec_4_4_1 = section(
    table_4_4_1,
    pico_4_4_1,
    lv=3, title="Table",
    desc=(
        "Clean and minimal styles for ",
        span_code("<table>", lang='html'),
        ", providing consistent spacings and a minimal unbordered look."),
)

#——————————————————
body_4_4_2 = P(
    span_code("data-theme='light'", lang='html'),
    " or ",
    span_code("data-theme='dark'", lang='html'),
    " can be used at any level: ",
    span_code("<table>", lang='html'),
    ", ",
    span_code("<thead>", lang='html'),
    ", ",
    span_code("<tbody>", lang='html'),
    ", ",
    span_code("<tfoot>", lang='html'),
    ", ",
    span_code("<tr>", lang='html'),
    ", ",
    span_code("<th>", lang='html'),
    ", ",
    span_code("<td>", lang='html'),
    ".",
)

table_4_4_2 = Table(
    Thead(
        Tr(
            Th("Planet"),
            Th("Diameter (km)"),
            Th("Distance to Sun (AU)"),
            Th("Orbit (days)"),
        ),
        data_theme="light",
    ),
    Tbody(
        Tr(
            Td("Mercury"),
            Td("4,880"),
            Td("0.39"),
            Td("88"),
        ),
        Tr(
            Td("Venus"),
            Td("12,104"),
            Td("0.72"),
            Td("225"),
        ),
        Tr(
            Td("Earth"),
            Td("12,742"),
            Td("1.00"),
            Td("365"),
        ),
        Tr(
            Td("Mars"),
            Td("6,779"),
            Td("1.52"),
            Td("687"),
        ),
        Tfoot(
            Td("Average"),
            Td("9,126"),
            Td("0.91"),
            Td("341"),
        ),
    )
)

pico_4_4_2 = div_code(
    code="""<table>
  <thead data-theme="light">
    ...
  </thead>
  <tbody>...</tbody>
  <tfoot>...</tfoot>
</table>""",
    lang="html",
)

sec_4_4_2 = section(
    body_4_4_2,
    table_4_4_2,
    pico_4_4_2,
    lv=4, title="Color schemes",
)


#——————————————————

body_4_4_3 = P(
    span_code(".striped"),
    " enable striped rows (not available in the class‑less version).",
)

table_4_4_3 = Table(
    Thead(
        Tr(
            Th("Planet"),
            Th("Diameter (km)"),
            Th("Distance to Sun (AU)"),
            Th("Orbit (days)"),
        ),
    ),
    Tbody(
        Tr(
            Td("Mercury"),
            Td("4,880"),
            Td("0.39"),
            Td("88"),
        ),
        Tr(
            Td("Venus"),
            Td("12,104"),
            Td("0.72"),
            Td("225"),
        ),
        Tr(
            Td("Earth"),
            Td("12,742"),
            Td("1.00"),
            Td("365"),
        ),
        Tr(
            Td("Mars"),
            Td("6,779"),
            Td("1.52"),
            Td("687"),
        ),
        Tfoot(
            Td("Average"),
            Td("9,126"),
            Td("0.91"),
            Td("341"),
        ),
    ),
    cls="striped",
)

pico_4_4_3 = div_code(
    code="""<table class="striped">
  ...
</table>""",
    lang="html",
)



sec_4_4_3 = section(
    body_4_4_3,
    table_4_4_3,
    pico_4_4_3,
    lv=4, title="Striped",
)


#——————————————————
sec_4_4_0 = section(
    sec_4_4_1,
    sec_4_4_2,
    sec_4_4_3,
    lv=2, title="Table",
)

#——————————————————
sec_4_0_0 = section(
    sec_4_1_0,
    sec_4_2_0,
    sec_4_3_0,
    sec_4_4_0,
    lv=2, title="Content",
)
#————————————————————————————————————————————————————————————————————————————5
# 5. Forms
# 5.1 Overview
# 5.2 Input
# 5.3 Textarea
# 5.4 Select
# 5.5 Checkboxes
# 5.6 Radios
# 5.7 Switch
# 5.8 Range

#—————————————————————————————————— 5.1
# 5.1 Overview
# 5.1.1 Introduction
# 5.1.2 Helper text
# 5.1.3 Usage with grid
# 5.1.4 Usage with group

body_5_1_1a = P(
    "Inputs are ",
    span_code("width: 100%;", lang='css'),
    " by default and are the same size as the buttons to build consistent forms."
)

art_5_1_1a = article(
    Form(Fieldset(
        Label(
            "First name", 
            Input(name="first_name", placeholder="First name", autocomplete="given-name"),
        ),
        Label("Email", For="email"),
            Input(type="email", id="email", placeholder="Email", autocomplete="email"),
        ),
    ),
    Input(type="submit", value="Subscribe"),
)
   

pico_5_1_1a = div_code(
    code="""<form>
  <fieldset>
    <label>
      First name
      <input
        name="first_name"
        placeholder="First name"
        autocomplete="given-name"
      />
    </label>
    <label>
      Email
      <input
        type="email"
        name="email"
        placeholder="Email"
        autocomplete="email"
      />
    </label>
  </fieldset>

  <input
    type="submit"
    value="Subscribe"
  />
</form>""",
    lang="html",
)

body_5_1_1b = P(
    span_code("<input>", lang='html'),
    " can be inside or outside ",
    span_code("<label>", lang='html'),
    "."
)

art_5_1_1b = article(
    Form(
        Label("First name", Input(name="first_name", placeholder="First name", autocomplete="given-name")),
        Label("Email", For="email"),
        Input(name="email", placeholder="Email", autocomplete="email"),
    ),
)

pico_5_1_1b = div_code(
    code="""<form>
  
  <!-- Input inside label -->
  <label>
    First name
    <input
      name="first_name"
      placeholder="First name"
      autocomplete="given-name"
    />
  </label>

  <!-- Input outside label -->
  <label for="email">Email</label>
  <input
    type="email"
    id="email"
    placeholder="Email"
    autocomplete="email"
  />

</form>""",
    lang="html",
)

sec_5_1_1 = section(
    body_5_1_1a,
    art_5_1_1a,
    pico_5_1_1a,
    body_5_1_1b,
    art_5_1_1b,
    pico_5_1_1b,
    lv=3, title="Introduction",
)
#——————————————————
body_5_1_2 = P(
    span_code("<small>", lang='html'),
    " below form elements are muted and act as helper texts.",
)

art_5_1_2 = article(
    Input(type="email", name="email", placeholder="Email", autoComplete="email", aria_label="Email", aria_describedby="email-helper"),
    Small("We'll never share your email with anyone else.", id="email-helper"),
)

pico_5_1_2 = div_code(
    code="""<input
  type="email"
  name="email"
  placeholder="Email"
  autoComplete="email"
  aria-label="Email"
  aria-describedby="email-helper"
/>
<small id="email-helper">
  We'll never share your email with anyone else.
</small>""",
    lang="html",
)

sec_5_1_2 = section(
    body_5_1_2,
    art_5_1_2,
    pico_5_1_2,
    lv=3, title="Helper text",
)
#——————————————————
body_5_1_3 = P(
    "You can use ",
    span_code(".grid"),
    " inside a form. See ",
    A("Grid", href="https://picocss.com/docs/grid"),
    ".",
)

art_5_1_3 = article(
    Form(
        Fieldset(
            Input(name="login", placeholder="Login", aria_label="Login", autocomplete="username"),
            Input(type="password", name="password", placeholder="Password", aria_label="Password", autocomplete="current-password"),
            Input(type="submit", value="Log in"),
            cls="grid"
        ),
    ),
)

pico_5_1_3 = div_code(
    code="""<form>
  <fieldset class="grid">
    <input 
      name="login"
      placeholder="Login"
      aria-label="Login"
      autocomplete="username"
    />
    <input
      type="password"
      name="password"
      placeholder="Password"
      aria-label="Password"
      autocomplete="current-password"
    />
    <input
      type="submit"
      value="Log in"
    />
  </fieldset>
</form>""",
    lang="html",
)

sec_5_1_3 = section(
    body_5_1_3,
    art_5_1_3,
    pico_5_1_3,
    lv=3, title="Usage with grid",
)
#——————————————————
body_5_1_4 = P(
    "You can use ",
    span_code('role="group"'),
    " inside a form. See ",
    A("Group", href="https://picocss.com/docs/group"),
    ".",
)

art_5_1_4 = article(
    Form(
        Fieldset(
            Input(type="email", name="email", placeholder="Enter your email", autocomplete="email"),
            Input(type="submit", value="Subscribe"),
            role="group"
        ),
    ),
)

pico_5_1_4 = div_code(
    code="""<form>
  <fieldset role="group">
    <input
      type="email"
      name="email"
      placeholder="Enter your email"
      autocomplete="email"
    />
    <input type="submit" value="Subscribe" />
  </fieldset>
</form>""",
    lang="html",
)

sec_5_1_4 = section(
    body_5_1_4,
    art_5_1_4,
    pico_5_1_4,
    lv=3, title="Usage with group",
)
#——————————————————
sec_5_1_0 = section(
    sec_5_1_1,
    sec_5_1_2,
    sec_5_1_3,
    sec_5_1_4,
    lv=3, title="Overview",
    desc="All form elements are fully responsive with pure semantic HTML, enabling forms to scale gracefully across devices and viewports."
)

#—————————————————————————————————— 5.2
# 5.2 Input
# 5.2.1 Syntax
# 5.2.2 Datetime
# 5.2.3 Search
# 5.2.4 Color
# 5.2.5 File
# 5.2.6 Disabled
# 5.2.7 Readonly
# 5.2.8 Validation states

art_5_2_1 = article(
    Input(type="text", name="text", placeholder="Text", aria_label="Text"),
    Input(type="email", name="email", placeholder="Email", aria_label="Email", autocomplete="email"),
    Input(type="number", name="number", placeholder="Number", aria_label="Number"),
    Input(type="password", name="password", placeholder="Password", aria_label="Password"),
    Input(type="tel", name="tel", placeholder="Tel", aria_label="Tel", autocomplete="tel"),
    Input(type="url", name="url", placeholder="Url", aria_label="Url"),
)

pico_5_2_1 = div_code(
    code="""<input type="text" name="text" placeholder="Text" aria-label="Text" />
<input type="email" name="email" placeholder="Email" aria-label="Email" autocomplete="email" />
<input type="number" name="number" placeholder="Number" aria-label="Number" />
<input type="password" name="password" placeholder="Password" aria-label="Password" />
<input type="tel" name="tel" placeholder="Tel" aria-label="Tel" autocomplete="tel" />
<input type="url" name="url" placeholder="Url" aria-label="Url" />""",
    lang="html",
)

sec_5_2_1 = section(
    art_5_2_1,
    pico_5_2_1,
    lv=3, title="Syntax",
)

#——————————————————
body_5_2_2 = P("Datetime inputs come with an icon.")

art_5_2_2 = article(
    Input(type="date", name="date", aria_label="Date"),
    Input(type="datetime-local", name="datetime-local", aria_label="Datetime local"),
    Input(type="month", name="month", aria_label="Month"),
    Input(type="time", name="time", aria_label="Time"),
)

pico_5_2_2 = div_code(
    code="""<input type="date" name="date" aria-label="Date" />
<input type="datetime-local" name="datetime-local" aria-label="Datetime local" />
<input type="month" name="month" aria-label="Month" />
<input type="time" name="time" aria-label="Time" />""",
    lang="html",
)

sec_5_2_2 = section(
    body_5_2_2,
    art_5_2_2,
    pico_5_2_2,
    lv=3, title="Datetime",
)


body_5_2_3 = P(
    span_code('type="search"'),
    " comes with a distinctive style.")

art_5_2_3 = article(
    Input(type="search", name="search", aria_label="Search"),
)

pico_5_2_3 = div_code(
    code="""<input type="search" name="search" placeholder="Search" aria-label="Search" />""",
    lang="html",
)

sec_5_2_3 = section(
    body_5_2_3,
    art_5_2_3,
    pico_5_2_3,
    lv=3, title="Search",
)
#——————————————————
body_5_2_4 = P(
    span_code('type="color"'),
    " is also consistent with the other input types.",
)

art_5_2_4 = article(
    Input(type="color", value="#ff9500", aria_label="Color picker"),
)

pico_5_2_4 = div_code(
    code="""<input
  type="color"
  value="#ff9500"
  aria-label="Color picker"
/>""",
    lang="html",
)

sec_5_2_4 = section(
    body_5_2_4,
    art_5_2_4,
    pico_5_2_4,
    lv=3, title="Color",
)
#——————————————————
body_5_2_5 = P("Input type file button has a ", span_code("secondary button style"), ".")

art_5_2_5 = article(
    Input(type="file"),
)

pico_5_2_5 = div_code(
    code="""<input type="file" />""",
    lang="html",
)

sec_5_2_5 = section(
    body_5_2_5,
    art_5_2_5,
    pico_5_2_5,
    lv=3, title="File",
)
#——————————————————
art_5_2_6 = article(
    Input(type="text", 
          name="text",
          placeholder="Disabled",
          aria_label="Disabled input", 
          disabled=True,),
)

pico_5_2_6 = div_code(
    code="""<input
  type="text"
  name="text"
  placeholder="Disabled"
  aria-label="Disabled input"
  disabled
/>""",
    lang="html",
)

sec_5_2_6 = section(
    art_5_2_6,
    pico_5_2_6,
    lv=3, title="Disabled",
)
#——————————————————
art_5_2_7 = article(
    Input(type="text", name="text", value="Read-only", aria_label="Read-only input", readonly=True),
)

pico_5_2_7 = div_code(
    code="""<input
  type="text"
  name="text"
  value="Read-only"
  aria-label="Read-only input"
  readonly
/>""",
    lang="html",
)

sec_5_2_7 = section(
    art_5_2_7,
    pico_5_2_7,
    lv=3, title="Readonly",
)
#——————————————————
body_5_2_8a = P("Validation states are provided with ", span_code("aria-invalid"), ".")

art_5_2_8a = article(
    Input(type="text", name="valid", value="Valid", aria_invalid="false"),
    Input(type="text", name="invalid", value="Invalid", aria_invalid="true"),
)

pico_5_2_8a = div_code(
    code="""<input
  type="text"
  name="valid"
  value="Valid"
  aria-invalid="false"
/>

<input
  type="text"
  name="invalid"
  value="Invalid"
  aria-invalid="true"
/>""",
    lang="html",
)

body_5_2_8b = P("Helper texts, defined with ", span_code("<small>"), ", below the form element, inherit the validation state color.")

art_5_2_8b = article(
    Input(type="text", name="valid", value="Valid", aria_invalid="false", aria_describedby="valid-helper"),
    Small("Looks good!"),
    Input(type="text", name="invalid", value="Invalid", aria_invalid="true", aria_describedby="invalid-helper"),
    Small("Please provide a valid value!"),
)

pico_5_2_8b = div_code(
    code="""<input
  type="text"
  name="valid"
  value="Valid"
  aria-invalid="false"
  aria-describedby="valid-helper"
/>
<small id="valid-helper">Looks good!</small>

<input
  type="text"
  name="invalid"
  value="Invalid"
  aria-invalid="true"
  aria-describedby="invalid-helper"
/>
<small id="invalid-helper">
  Please provide a valid value!
</small>""",
    lang="html",
)

sec_5_2_8 = section(
    body_5_2_8a,
    art_5_2_8a,
    pico_5_2_8a,
    body_5_2_8b,
    art_5_2_8b,
    pico_5_2_8b,
    lv=3, title="Validation states",
)
#——————————————————
sec_5_2_0 = section(
    sec_5_2_1,
    sec_5_2_2,
    sec_5_2_3,
    sec_5_2_4,
    sec_5_2_5,
    sec_5_2_6,
    sec_5_2_7,
    sec_5_2_8,
    lv=3, title="Input",
    desc="All input types are consistently styled and come with validation states."
)

#—————————————————————————————————— 5.3
# 5.3 Textarea
# 5.3.1 Syntax
# 5.3.2 Disabled
# 5.3.3 Readonly
# 5.3.4 Validation states
#——————————————————

art_5_3_1 = article(
    Textarea(name="bio", placeholder="Write a professional short bio...", aria_label="Professional short bio"),
)

pico_5_3_1 = div_code(
    code="""<textarea
  name="bio"
  placeholder="Write a professional short bio..."
  aria-label="Professional short bio"
>
</textarea>""",
    lang="html",
)

sec_5_3_1 = section(
    art_5_3_1,
    pico_5_3_1,
    lv=3, title="Syntax",
)
#——————————————————

art_5_3_2 = article(
    Textarea("Disabled", name="disabled", disabled=True),
)

pico_5_3_2 = div_code(
    code="""<textarea name="disabled" disabled>
  Disabled
</textarea>""",
    lang="html",
)

sec_5_3_2 = section(
    art_5_3_2,
    pico_5_3_2,
    lv=3, title="Disabled",
)
#——————————————————

art_5_3_3 = article(
    Textarea("Read-only", name="readonly", readonly=True),
)

pico_5_3_3 = div_code(
    code="""<textarea name="readonly" readonly>
  Read-only
</textarea>""",
    lang="html",
)

sec_5_3_3 = section(
    art_5_3_3,
    pico_5_3_3,
    lv=3, title="Readonly",
)
#——————————————————

body_5_3_4a = P("Validation states are provided with ", span_code("aria-invalid"), ".")

art_5_3_4a = article(
    Textarea("Valid", name="valid", aria_invalid="false", aria_describedby="valid-helper"),
    Small("Looks good!"),
)

pico_5_3_4a = div_code(
    code="""<textarea name="valid" aria-invalid="false">
  Valid
</textarea>

<textarea name="invalid" aria-invalid="true">
  Invalid
</textarea> """,
    lang="html",
)

body_5_3_4b = P("Helper texts, defined with ", span_code("<small>"), ", below the form element, inherit the validation state color.")

art_5_3_4b = article(
    Textarea("Valid", name="valid", aria_invalid="false", aria_describedby="valid-helper"),
    Small("Looks good!"),
    Textarea("Invalid", name="invalid", aria_invalid="true", aria_describedby="invalid-helper"),
    Small("Please provide a valid value!"),
)

pico_5_3_4b = div_code(
    code="""<textarea
  name="valid"
  aria-invalid="false"
  aria-describedby="valid-helper"
>
  Valid
</textarea>
<small id="valid-helper">Looks good!</small>

<textarea
  name="invalid"
  aria-invalid="true"
  aria-describedby="invalid-helper"
>
  Invalid
</textarea>
<small id="invalid-helper">
  Please provide a valid value!
</small>""",
    lang="html",
)

sec_5_3_4 = section(
    body_5_3_4a,
    art_5_3_4a,
    pico_5_3_4a,
    body_5_3_4b,
    art_5_3_4b,
    pico_5_3_4b,
    lv=3, title="Validation states",
)
#——————————————————
sec_5_3_0 = section(
    sec_5_3_1,
    sec_5_3_2,
    sec_5_3_3,
    sec_5_3_4,
    lv=3, title="Textarea",
    desc=(
        "The native ",
        span_code("<textarea>", lang='html'),
        " is styled like the input for consistency."
    ),
)
#—————————————————————————————————— 5.4
# 5.4 Select
# 5.4.1 Syntax
# 5.4.2 Multiple
# 5.4.3 Disabled
# 5.4.4 Validation states
# 5.4.5 Dropdown
#———————————————————
art_5_4_1 = article(
    Select(
        "Select your favorite cuisine...", 
        Option("Select your favorite cuisine...", disabled=True, selected=True),
        Option("Italian"),
        Option("Japanese"),
        Option("Indian"),
        Option("Thai"),
        Option("French"),
        name="favorite-cuisine", 
        aria_label="Select your favorite cuisine...", 
        required=True,
    ),
)

pico_5_4_1 = div_code(
    code="""<select name="favorite-cuisine" aria-label="Select your favorite cuisine..." required>
  <option selected disabled value="">
    Select your favorite cuisine...
  </option>
  <option>Italian</option>
  <option>Japanese</option>
  <option>Indian</option>
  <option>Thai</option>
  <option>French</option>
</select>""",
    lang="html",
)

sec_5_4_1 = section(
    art_5_4_1,
    pico_5_4_1,
    lv=3, title="Syntax",
)
#——————————————————
art_5_4_2 = article(
    Select(
        "Select your favorite snacks...", 
        Option("Select your favorite snacks...", disabled=True),
        Option("Cheese"),
        Option("Fruits", selected=True),
        Option("Nuts", selected=True),
        Option("Chocolate"),
        Option("Crackers"),
        multiple=True, 
        size="6",
        aria_label="Select your favorite snacks...",
    ),
)

pico_5_4_2 = div_code(
    code="""<select aria-label="Select your favorite snacks..." multiple size="6">
  <option disabled>
    Select your favorite snacks...
  </option>
  <option>Cheese</option>
  <option selected>Fruits</option>
  <option selected>Nuts</option>
  <option>Chocolate</option>
  <option>Crackers</option>
</select>""",
    lang="html",
)

sec_5_4_2 = section(
    art_5_4_2,
    pico_5_4_2,
    lv=3, title="Multiple",
)
#——————————————————
art_5_4_3 = article(
    Select(
        Option("Select a meal type…"),
        Option("…"),
        name="meal-type", 
        aria_label="Select a meal type…",
        disabled=True,
    ),
)

pico_5_4_3 = div_code(
    code="""<select name="meal-type" aria-label="Select a meal type..." disabled>
  <option>Select a meal type...</option>
  <option>...</option>
</select>""",
    lang="html",
)

sec_5_4_3 = section(
    art_5_4_3,
    pico_5_4_3,
    lv=3, title="Disabled",
)
#——————————————————
body_5_4_4 = P("Validation states are provided with ", span_code("aria-invalid"), ".")

art_5_4_4 = article(
    Select(
        Option("Select your favorite pizza topping…", selected=True, disabled=True),
        Option("Pepperoni"),
        Option("Mushrooms"),
        Option("Onions"),
        Option("Pineapple"),
        Option("Olives"),
        aria_invalid="false"
    ),
    Small("Great choice!"),
    Select(
        Option("Select your favorite pizza topping…", selected=True, disabled=True),
        Option("Pepperoni"),
        Option("Mushrooms"),
        Option("Onions"),
        Option("Pineapple"),
        Option("Olives"),        
        aria_invalid="true"
    ),
    Small("Please select your favorite pizza topping!"),
)

pico_5_4_4 = div_code(
    code="""<select aria-invalid="false">
  ...
</select>
<small>Great choice!</small>

<select required aria-invalid="true">
  ...
</select>
<small>
  Please select your favorite pizza topping!
</small>>""",
    lang="html",
)

sec_5_4_4 = section(
    body_5_4_4,
    art_5_4_4,
    pico_5_4_4,
    lv=3, title="Validation states",
)
#——————————————————
body_5_4_5 = P("The dropdown component allows you to build a custom select with the same style as the native select. See ", A("dropdown", href="https://picocss.com/docs/dropdown"), ".")

sec_5_4_5 = section(
    body_5_4_5,
    lv=3, title="Dropdown",
)
#———————————————————
sec_5_4_0 = section(
    sec_5_4_1,
    sec_5_4_2,
    sec_5_4_3,
    sec_5_4_4,
    sec_5_4_5,
    lv=3, title="Select",
    desc=(
        "The native ",
        span_code("<select>", lang='html'),
        " is styled like the input for consistency."
    ),
)
#—————————————————————————————————— 5.5
# 5.5 Checkboxes
# 5.5.1 Syntax
# 5.5.2 Horizontal stacking
# 5.5.3 Indeterminate
# 5.5.4 Validation states
#———————————————————

art_5_5_1 = article(
    Fieldset(
        Legend("Language preferences:"),
        Label(Input("English",  type="checkbox", name="english", checked=True)),
        Label(Input("French",   type="checkbox", name="french", checked=True)),
        Label(Input("Mandarin", type="checkbox", name="mandarin")),
        Label(Input("Thai",     type="checkbox", name="thai")),
        Label(Input("Dothraki", type="checkbox", name="dothraki", disabled=True)),
    ),
)

pico_5_5_1 = div_code(
    code="""<fieldset>
  <legend>Language preferences:</legend>
  <label>
    <input type="checkbox" name="english" checked />
    English
  </label>
  <label>
    <input type="checkbox" name="french" checked />
    French
  </label>
  <label>
    <input type="checkbox" name="mandarin" />
    Mandarin
  </label>
  <label>
    <input type="checkbox" name="thai" />
    Thai
  </label>
  <label aria-disabled="true">
    <input type="checkbox" name="dothraki" disabled />
    Dothraki
  </label>
</fieldset>""",
    lang="html",
)

sec_5_5_1 = section(
    art_5_5_1,
    pico_5_5_1,
    lv=3, title="Syntax",
)
#———————————————————
art_5_5_2 = article(
    Fieldset(
        Legend("Language preferences:"),
        Input("Hindi", type="checkbox", id="hindi", name="hindi", checked=True),
        Label("Swahili", Input("Swahili", type="checkbox", id="swahili", name="swahili")),
        Label("Na'vi", Input("Na'vi", type="checkbox", id="navi", name="navi", disabled=True)),
    ),
)

pico_5_5_2 = div_code(
    code="""<fieldset>
  <legend>Language preferences:</legend>
  <input type="checkbox" id="hindi" name="hindi" checked />
  <label htmlFor="hindi">Hindi</label>
  <input type="checkbox" id="swahili" name="swahili" />
  <label htmlFor="swahili">Swahili</label>
  <input type="checkbox" id="navi" name="navi" disabled />
  <label htmlFor="navi" aria-disabled="true">Na'vi</label>
</fieldset>""",
    lang="html",
)

sec_5_5_2 = section(
    art_5_5_2,
    pico_5_5_2,
    lv=3, title="Horizontal stacking",
)
#———————————————————
body_5_5_3 = P("You can change a checkbox to an indeterminate state by setting the ", span_code("indeterminate"), " property to ", span_code("true"), ".")

art_5_5_3 = article(
    Label(Input(
        "Indeterminate", 
        type="checkbox", 
        id="indeterminate", 
        name="indeterminate"
    )),
)

script_5_5_3 = Script(
    """const checkbox = document.querySelector('#indeterminate');
    checkbox.indeterminate = true;"""
)

pico_5_5_3 = div_code(
    code="""<label>
  <input type="checkbox" id="indeterminate" name="indeterminate" />
  Indeterminate
</label>

<script>
  const checkbox = document.querySelector('#indeterminate');
  checkbox.indeterminate = true;
</script>
""",
    lang="html",
)

sec_5_5_3 = section(
    body_5_5_3,
    art_5_5_3,
    pico_5_5_3,
    script_5_5_3,
    lv=3, title="Indeterminate",
)
#———————————————————

body_5_5_4 = P("Validation states are provided with ", span_code(".aria-invalid."), ".")

art_5_5_4 = article(
    Label(Input("Valid", type="checkbox", name="valid", aria_invalid="false")),
    Label(Input("Invalid", type="checkbox", name="invalid", aria_invalid="true")),
)

pico_5_5_4 = div_code(
    code="""<label>
  <input type="checkbox" name="valid" aria-invalid="false" />
  Valid
</label>

<label>
  <input type="checkbox" name="invalid" aria-invalid="true" />
  Invalid
</label>""",
    lang="html",
)

sec_5_5_4 = section(
    body_5_5_4,
    art_5_5_4,
    pico_5_5_4,
    lv=3, title="Validation states",
)
#———————————————————
sec_5_5_0 = section(
    sec_5_5_1,
    sec_5_5_2,
    sec_5_5_3,
    sec_5_5_4,
    lv=3, title="Checkboxes",
    desc=(
        "The native ",
        span_code("<input type='checkbox'>", lang='html'),
        " with a custom and responsive style."
    ),
)
#—————————————————————————————————— 5.6
# 5.6 Radios
# 5.6.1 Syntax
# 5.6.2 Horizontal stacking
# 5.6.3 Validation states
#———————————————————
art_5_6_1 = article(
    Fieldset(
        Legend("Language preference:"),
        Label(Input("English", type="radio", name="language", checked=True)),
        Label(Input("French", type="radio", name="language")),
        Label(Input("Mandarin", type="radio", name="language")),
        Label(Input("Thai", type="radio", name="language")),
        Label(Input("Dothraki", type="radio", name="language", disabled=True)),
    ),
)

pico_5_6_1 = div_code(
    code="""<fieldset>
  <legend>Language preference:</legend>
  <label>
    <input type="radio" name="language" checked />
    English
  </label>
  <label>
    <input type="radio" name="language" />
    French
  </label>
  <label>
    <input type="radio" name="language" />
    Mandarin
  </label>
  <label>
    <input type="radio" name="language" />
    Thai
  </label>
  <label aria-disabled="true">
    <input type="radio" name="language" disabled />
    Dothraki
  </label>
</fieldset>""",
    lang="html",
)

sec_5_6_1 = section(
    art_5_6_1,
    pico_5_6_1,
    lv=3, title="Syntax",
)
#———————————————————
art_5_6_2 = article(
    Fieldset(
        Legend("Second language:"),
        Input("Hindi", type="radio", id="hindi", name="second-language", checked=True),
        Input("Swahili", type="radio", id="swahili", name="second-language"),
        Input("Na'vi", type="radio", id="navi", name="second-language", disabled=True),
    ),
)

pico_5_6_2 = div_code(
    code="""<fieldset>
  <legend>Second language:</legend>
  <input type="radio" id="hindi" name="second-language" checked />
  <label htmlFor="hindi">Hindi</label>
  <input type="radio" id="swahili" name="second-language" />
  <label htmlFor="swahili">Swahili</label>
  <input type="radio" id="navi" name="second-language" disabled />
  <label htmlFor="navi" aria-disabled="true">Na'vi</label>
</fieldset>""",
    lang="html",
)

sec_5_6_2 = section(
    art_5_6_2,
    pico_5_6_2,
    lv=3, title="Horizontal stacking",
)
#———————————————————
body_5_6_3 = P("Validation states are provided with ", span_code(".aria-invalid."), ".")

art_5_6_3 = article(
    Label(Input(type="radio", name="valid", aria_invalid="false"), "Valid", ),
    Label(Input(type="radio", name="invalid", aria_invalid="true"), "Invalid", ),
)

pico_5_6_3 = div_code(
    code="""<label>
  <input type="radio" name="valid" aria-invalid="false" />
  Valid
</label>

<label>
  <input type="radio" name="invalid" aria-invalid="true" />
  Invalid
</label>""",
    lang="html",
)

sec_5_6_3 = section(
    body_5_6_3,
    art_5_6_3,
    pico_5_6_3,
    lv=3, title="Validation states",
)
#———————————————————
sec_5_6_0 = section(
    sec_5_6_1,
    sec_5_6_2,
    sec_5_6_3,
    lv=3, title="Radios",
    desc=(
        "The native ",
        span_code("<input type='radio'>", lang='html'),
        " with a custom and responsive style."
    ),
)
#—————————————————————————————————— 5.7
# 5.7 Switch
# 5.7.1 Syntax
# 5.7.2 Disabled
# 5.7.3 Validation states
art_5_7_1 = article(
    Fieldset(
        Label(Input("I agree to the Terms", type="checkbox", name="terms", role="switch")),
        Label(Input("Receive news and offers", type="checkbox", name="opt-in", role="switch", checked=True)),
    ),
)

pico_5_7_1 = div_code(
    code="""<fieldset>
  <label>
    <input name="terms" type="checkbox" role="switch" />
    I agree to the Terms
  </label>
  <label>
    <input name="opt-in" type="checkbox" role="switch" checked />
    Receive news and offers
  </label>
</fieldset>""",
    lang="html",
)

sec_5_7_1 = section(
    art_5_7_1,
    pico_5_7_1,
    lv=3, title="Syntax",
)
#———————————————————
art_5_7_2 = article(
    Fieldset(
        Label(Input("Publish on my profile", type="checkbox", name="publish", role="switch", disabled=True)),
        Label(Input("Change my password at next login", type="checkbox", name="change-password", role="switch", checked=True, disabled=True))
    ),
)

pico_5_7_2 = div_code(
    code="""<fieldset>
  <label>
    <input name="publish" type="checkbox" role="switch" disabled />
    Publish on my profile
  </label>
  <label>
    <input name="change-password" type="checkbox" role="switch" checked disabled />
    Change my password at next login
  </label>
</fieldset>""",
    lang="html",
)

sec_5_7_2 = section(
    art_5_7_2,
    pico_5_7_2,
    lv=3, title="Disabled",
)


#———————————————————

art_5_7_3 = article(
    Fieldset(
        Label(Input("Enable two-factor authentication", type="checkbox", name="2fa", role="switch", aria_invalid="false")),
        Label(Input("Automatic subscription renewal", type="checkbox", name="subscription", role="switch", aria_invalid="true")),
    ),
)

pico_5_7_3 = div_code(
    code="""<fieldset>
  <label>
    <input name="2fa" type="checkbox" role="switch" aria-invalid="false" />
    Enable two-factor authentication
  </label>
  <label>
    <input name="subscription" type="checkbox" role="switch" aria-invalid="true" />
    Automatic subscription renewal
  </label>
</fieldset>""",
    lang="html",
)

sec_5_7_3 = section(
    art_5_7_3,
    pico_5_7_3,
    lv=3, title="Validation states",
)
#———————————————————
sec_5_7_0 = section(
    sec_5_7_1,
    sec_5_7_2,
    sec_5_7_3,
    lv=3, title="Switch",
    desc=(
        "A switch component in pure CSS, using the checkbox syntax."
    ),
)
#—————————————————————————————————— 5.8
# 5.8 Range
#———————————————————
art_5_8_1 = article(
    Label(Input("Brightness", type="range")),
    Label(Input("Contrast", type="range", value="40")),
)

pico_5_8_1 = div_code(
    code="""<label>
  Brightness
  <input type="range" />
</label>

<label>
  Contrast
  <input type="range" value="40" />
</label>""",
    lang="html",
)

sec_5_8_0 = section(
    art_5_8_1,
    pico_5_8_1,
    lv=3, title="Range",
    desc=(
        "Create a slider control with ",
        span_code("<input type='range'>", lang='html'),
        "."
    ),
)
#——————————————————————————————————
sec_5_0_0 = section(
    sec_5_1_0,
    sec_5_2_0,
    sec_5_3_0,
    sec_5_4_0,
    sec_5_5_0,
    sec_5_6_0,
    sec_5_7_0,
    sec_5_8_0,
    lv=2, title="Forms",
)
#————————————————————————————————————————————————————————————————————————————6
# 6. Components
# 6.1 Accordion
# 6.2 Card
# 6.3 Dropdown
# 6.4 Group NEW
# 6.5 Loading
# 6.6 Modal
# 6.7 Nav
# 6.8 Progress
# 6.9 Tooltip

#—————————————————————————————————— 6.1
# 6.1 Accordions
# 6.1.1 Overview
# 6.1.2 Button variants
#———————————————————
art_6_1_1 = article(
    Details(
        Summary("Accordion 1"), 
        P("Flamingos are known for their bright pink feathers and distinctive long necks. These birds are social creatures that live in large groups, and a group of flamingos is called a flamboyance. They can often be seen standing on one leg, which helps them conserve body heat."), 
        open=True),
    Details(Summary("Accordion 2"), Ul(
        Li("Kangaroos are marsupials that are native to Australia."), 
        Li("They are known for their powerful hind legs, which they use to hop around."),
        Li("Kangaroos can’t walk backwards due to the shape of their legs and tail."),
        Li("Baby kangaroos, called joeys, are born very small and undeveloped and must crawl into their mother’s pouch to continue developing."),
        Li("Some species of kangaroos can leap up to 30 feet in a single bound."),
        )),
)

pico_6_1_1 = div_code(
    code="""<details open>
  <summary>Accordion 1</summary>
  <p>...</p>
</details>

<hr />

<details>
  <summary>Accordion 2</summary>
  <ul>
    <li>...</li>
    <li>...</li>
  </ul>
</details>""",
    lang="html",
)

sec_6_1_1 = section(
    art_6_1_1,
    pico_6_1_1,
    lv=4, title="Overview",
)
#———————————————————
body_6_1_2a = P(
    span_code("role='button'"),
    " can be used to turn ",
    span_code("<summary>", lang='html'),
    " into a button.",
)

art_6_1_2a = article(
    Details(Summary("Button", role="button"), P("Owls are nocturnal birds of prey that are known for their distinctive hooting calls. A group of owls is called a parliament, and these birds are often associated with wisdom and intelligence. Owls have excellent hearing and vision, which helps them hunt prey in the dark.")),
)

pico_6_1_2a = div_code(
    code="""<details>
  <summary role="button">Owls</summary>
  <p>...</p>
</details>""",
    lang="html",
)

body_6_1_2b = P(
    "Like regular buttons, they come with ",
    span_code(".secondary"),
    span_code(".contrast"),
    ", and ",
    span_code(".outline"),
    " (Not available in the class-less version).",
)

art_6_1_2b = article(
    Details(
        Summary("Secondary", role="button", cls="secondary"), 
        P("Ostriches are the largest birds in the world and are native to Africa. They have long, powerful legs that they use to run at high speeds, and they can reach up to 45 miles per hour. An ostrich’s eye is bigger than its brain, which is unusual for birds.")
        ),
    Details(
        Summary("Contrast", role="button", cls="contrast"), 
        P("Koalas are arboreal marsupials that are native to Australia. They are known for their cute and cuddly appearance, but they can be quite aggressive if provoked. The fingerprints of koalas are so similar to those of humans that they have been mistaken for crime scene prints.")
        ),
    Details(
        Summary("Primary outline", role="button", cls="outline"), 
        P("Elephants are the largest land animals and highly intelligent with intricate communication systems. They use infrasonic sounds to talk and have long memories. They create and maintain habitats for other species, and can eat up to 300 pounds of vegetation per day. Their elongated incisor teeth, called tusks, serve various purposes, including digging and defense.")
        ),
    Details(
        Summary("Secondary outline", role="button", cls="outline secondary"), 
        P("Crows are intelligent birds that are known for their problem-solving abilities. A group of crows is called a murder, and these birds have a reputation for being mischievous and sometimes even aggressive. Despite their negative image in some cultures, crows are important for their role in controlling pest populations and maintaining ecological balance.")
        ),
    Details(
        Summary("Contrast outline", role="button", cls="outline contrast"), 
        P("Penguins are flightless birds with a tuxedo-like appearance. They swim well and can hold their breath for up to 20 minutes. Penguins are social, forming tight-knit communities, and some mate for life. They have adaptations to survive in cold climates, including thick feathers and a layer of fat for insulation.")
        ),
)

pico_6_1_2b = div_code(
    code="""<!-- Secondary -->
<details>
  <summary role="button" class="secondary">Secondary</summary>
  <p>...</p>
</details>

<!-- Contrast -->
<details>
  <summary role="button" class="contrast">Contrast</summary>
  <p>...</p>
</details>

<!-- Primary outline -->
<details>
  <summary role="button" class="outline">Primary outline</summary>
  <p>...</p>
</details>

<!-- Secondary outline -->
<details>
  <summary role="button" class="outline secondary">Secondary outline</summary>
  <p>...</p>
</details>

<!-- Contrast outline -->
<details>
  <summary role="button" class="outline contrast">Contrast outline</summary>
  <p>...</p>
</details>""",
    lang="html",
)

sec_6_1_2 = section(
    body_6_1_2a,
    art_6_1_2a,
    pico_6_1_2a,
    body_6_1_2b,
    art_6_1_2b,
    pico_6_1_2b,
    lv=4, title="Button variants",
)
#———————————————————
sec_6_1_0 = section(
    sec_6_1_1,
    sec_6_1_2,
    lv=3, title="Accordion",
    desc=(
        "Toggle sections of content in pure HTML, without JavaScript, using minimal and semantic markup."
    ),
)
#—————————————————————————————————— 6.2
# 6.2 Card
# 6.2.1 Syntax
# 6.2.2 Sectioning

art_6_2_1 = Card("I’m a card!")

pico_6_2_1 = div_code(
    code="""<article>I’m a card!</article>""",
    lang="html",
)

body_6_2_1 = P(
    "You can use ",
    span_code("<header>", lang='html'),
    " and ",
    span_code("<footer>", lang='html'),
    " inside ",
    span_code("<article>", lang='html'),
    ".",
)

sec_6_2_1 = section(
    body_6_2_1,
    art_6_2_1,
    pico_6_2_1,
    lv=4, title="Syntax",
)
#———————————————————

art_6_2_2 = Article(
    Header("Header"),
    "Body",
    Footer("Footer"),
)

pico_6_2_2 = div_code(
    code="""<article>
  <header>Header</header>
  Body
  <footer>Footer</footer>
</article>""",
    lang="html",
)

sec_6_2_2 = section(
    art_6_2_2,
    pico_6_2_2,
    lv=4, title="Sectioning",
)
#———————————————————
sec_6_2_0 = section(
    sec_6_2_1,
    sec_6_2_2,
    lv=3, title="Card",
    desc=(
        "Create flexible cards with a semantic markup that provides graceful spacings across various devices and viewports."
    ),
)

#—————————————————————————————————— 6.3
# 6.3 Dropdown
# 6.3.1 Syntax
# 6.3.2 Checkboxes and radios
# 6.3.3 Button variants
# 6.3.4 Validation states
# 6.3.5 Usage with nav
#———————————————————
body_6_3_1 = (
    P(
        "Dropdowns are built with ",
        span_code("<details class='dropdown'>", lang='html'),
        " as a wrapper and ",
        span_code("<summary>", lang='html'),
        " and ",
        span_code("<ul>", lang='html'),
        " as direct childrens. Unless they are in a Nav, dropdowns are width: 100%; by default.",
    ), 
    P("Dropdowns are not available in the class‑less version."), 
    P("For style consistency with the form elements, dropdowns are styled like a select by default."),
)

art_6_3_1 = article(
    Details(
        Summary("Dropdown"), 
        Ul(
            Li(A("Solid", href="#")),
            Li(A("Liquid", href="#")),
            Li(A("Gas", href="#")),
            Li(A("Plasma", href="#")),
        ),
        cls="dropdown"
    ),
    Select(
        Option("Select", selected=True, disabled=True, value=""),
        Option("Solid"),
        Option("Liquid"),
        Option("Gas"),
        Option("Plasma"),
        name="select",
        aria_label="Select",
        required=True,
    ),
    cls="grid",
)

pico_6_3_1 = div_code(
    code="""<!-- Dropdown -->
<details class="dropdown">
  <summary>Dropdown</summary>
  <ul>
    <li><a href="#">Solid</a></li>
    <li><a href="#">Liquid</a></li>
    <li><a href="#">Gas</a></li>
    <li><a href="#">Plasma</a></li>
  </ul>
</details>

<!-- Select -->
<select name="select" aria-label="Select" required>
  <option selected disabled value="">Select</option>
  <option>Solid</option>
  <option>Liquid</option>
  <option>Gas</option>
  <option>Plasma</option>false
</select>""",
    lang="html",
)

sec_6_3_1 = section(
    body_6_3_1,
    art_6_3_1,
    pico_6_3_1,
    lv=4, title="Syntax",
)
#———————————————————
body_6_3_2 = P("Dropdowns can be used as custom selects with ", span_code("<input type='radio'>", lang='html'), " or ", span_code("<input type='checkbox'>", lang='html'), ".")

art_6_3_2 = article(
    Details(
        Summary("Select a phase of matter…"), 
        Ul(
            Li(Label(Input(type="radio", name="phase", value="solid"),
                "Solid")),
            Li(Label(Input(type="radio", name="phase", value="liquid"),
                "Liquid")),
            Li(Label(Input(type="radio", name="phase", value="gas"),
                "Gas")),
            Li(Label(Input(type="radio", name="phase", value="plasma"),
                "Plasma")),
        ),
        cls="dropdown"
    ),
    Details(
        Summary("Select phases of matter…"), 
        Ul(
            Li(Label(Input(type="checkbox", name="solid"),
                "Solid")),
            Li(Label(Input(type="checkbox", name="liquid"),
                "Liquid")),
            Li(Label(Input(type="checkbox", name="gas"),
                "Gas")),
            Li(Label(Input(type="checkbox", name="plasma"),
                "Plasma")),
        ),
        cls="dropdown"
    ),
)

pico_6_3_2 = div_code(
    code="""<!-- Radios -->
<details class="dropdown">
  <summary>
    Select a phase of matter...
  </summary>
  <ul>
    <li>
      <label>
        <input type="radio" name="phase" value="solid" />
        Solid
      </label>
    </li>
    <li>
      <label>
        <input type="radio" name="phase" value="liquid" />
        Liquid
      </label>
    </li>
    <li>
      <label>
        <input type="radio" name="phase" value="gas" />
        Gas
      </label>
    </li>
    <li>
      <label>
        <input type="radio" name="phase" value="plasma" />
        Plasma
      </label>
    </li>
  </ul>
</details>

<!-- Checkboxes -->
<details class="dropdown">
  <summary>
    Select phases of matter...
  </summary>
  <ul>
    <li>
      <label>
        <input type="checkbox" name="solid" />
        Solid
      </label>
    </li>
    <li>
      <label>
        <input type="checkbox" name="liquid" />
        Liquid
      </label>
    </li>
    <li>
      <label>
        <input type="checkbox" name="gas" />
        Gas
      </label>
    </li>
    <li>
      <label>
        <input type="checkbox" name="plasma" />
        Plasma
      </label>
    </li>
  </ul>
</details>""",
    lang="html",
)

sec_6_3_2 = section(
    body_6_3_2,
    art_6_3_2,
    pico_6_3_2,
    lv=4, title="Checkboxes and radios",
)
#———————————————————
body_6_3_3a = P(
    span_code('<summary role="button">', lang='html'), 
    " transforms the dropdown into a button.",
)

art_6_3_3a = article(
    Details(
        Summary("Dropdown as a button", role="button"), 
        Ul(Li(A("Solid", href="#")), Li(A("Liquid", href="#")), Li(A("Gas", href="#")), Li(A("Plasma", href="#")),),
        cls="dropdown"
    ),
)

pico_6_3_3a = div_code(
    code="""<details class="dropdown">
  <summary role="button">
    Dropdown as a button
  </summary>
  <ul>
    ...
  </ul>
</details>""",
    lang="html",
)

body_6_3_3b = P(
    "Like regular buttons, they come with ",
    span_code(".secondary", lang='html'),
    ", ",
    span_code(".contrast", lang='html'),
    ", and ",
    span_code(".outline", lang='html'),
    " (not available in the class-less version).",
)

art_6_3_3b = article(
    Details(
        Summary("Primary", role="button"), 
        Ul(Li(A("Solid", href="#")), Li(A("Liquid", href="#")), Li(A("Gas", href="#")), Li(A("Plasma", href="#")),),
        cls="dropdown"
    ),
    Details(
        Summary("Secondary", role="button", cls="secondary"), 
        Ul(Li(A("Solid", href="#")), Li(A("Liquid", href="#")), Li(A("Gas", href="#")), Li(A("Plasma", href="#")),),
        cls="dropdown"
    ),
    Details(
        Summary("Contrast", role="button", cls="contrast"), 
        Ul(Li(A("Solid", href="#")), Li(A("Liquid", href="#")), Li(A("Gas", href="#")), Li(A("Plasma", href="#")),),
        cls="dropdown"
    ),
    Details(
        Summary("Outline", role="button", cls="outline"), 
        Ul(Li(A("Solid", href="#")), Li(A("Liquid", href="#")), Li(A("Gas", href="#")), Li(A("Plasma", href="#")),),
        cls="dropdown"
    ),
    Details(
        Summary("Outline secondary", role="button", cls="outline secondary"), 
        Ul(Li(A("Solid", href="#")), Li(A("Liquid", href="#")), Li(A("Gas", href="#")), Li(A("Plasma", href="#")),),
        cls="dropdown"
    ),
    Details(
        Summary("Outline contrast", role="button", cls="outline contrast"), 
        Ul(Li(A("Solid", href="#")), Li(A("Liquid", href="#")), Li(A("Gas", href="#")), Li(A("Plasma", href="#")),),
        cls="dropdown"
    ),
)

pico_6_3_3b = div_code(
    code="""<!-- Primary -->
<details class="dropdown">
  <summary role="button">
    Primary
  </summary>
  <ul>
    ...
  </ul>
</details>

<!-- Secondary -->
<details class="dropdown">
  <summary role="button" class="secondary">
    Secondary
  </summary>
  <ul>
    ...
  </ul>
</details>

<!-- Contrast -->
<details class="dropdown">
  <summary role="button" class="contrast">
    Contrast
  </summary>
  <ul>
    ...
  </ul>
</details>

<!-- Primary outline -->
<details class="dropdown">
  <summary role="button" class="outline">
    Primary outline
  </summary>
  <ul>
    ...
  </ul>
</details>

<!-- Secondary outline -->
<details class="dropdown">
  <summary role="button" class="outline secondary">
    Secondary outline
  </summary>
  <ul>
    ...
  </ul>
</details>

<!-- Contrast outline -->
<details class="dropdown">
  <summary role="button" class="outline contrast">
    Contrast outline
  </summary>
  <ul>
    ...
  </ul>
</details>""",
    lang="html",
)




sec_6_3_3 = section(
    body_6_3_3a,
    art_6_3_3a,
    pico_6_3_3a,
    body_6_3_3b,
    art_6_3_3b,
    pico_6_3_3b,
    lv=4, title="Button variants",
)
#———————————————————
body_6_3_4 = P(
    "Just like any form elements, validation states are provided with ",
    span_code("aria-invalid", lang='html'),
    ".",
)

art_6_3_4 = article(
    Details(
        Summary("Valid phase of matter: Solid", aria_invalid="false"), 
        Ul(Li(A("Solid", href="#")), Li(A("Liquid", href="#")), Li(A("Gas", href="#")), Li(A("Plasma", href="#")),),
        cls="dropdown"
    ),
    Details(
        Summary("Debated classification: Plasma", aria_invalid="true"), 
        Ul(Li(A("Solid", href="#")), Li(A("Liquid", href="#")), Li(A("Gas", href="#")), Li(A("Plasma", href="#")),),
        cls="dropdown"
    ),
)

pico_6_3_4 = div_code(
    code="""<details class="dropdown">
  <summary aria-invalid="false">
    Valid phase of matter: Solid
  </summary>
  <ul>
    ...
  </ul>
</details>

<details class="dropdown">
  <summary aria-invalid="true">
    Debated classification: Plasma
  </summary>
  <ul>
    ...
  </ul>
</details>""",
    lang="html",
)


sec_6_3_4 = section(
    body_6_3_4,
    art_6_3_4,
    pico_6_3_4,
    lv=4, title="Validation states",
)
#———————————————————
body_6_3_5 = (P(
    "You can use dropdowns inside ",
    span_code("Nav", lang='html'),
    "."),
    P("To change the alignment of the submenu, simply use ",
    span_code("<ul dir='rtl'>", lang='html'),
    "."),
)

art_6_3_5 = article(
    Nav(
        Ul(
            Li(Strong("Acme Corp")), 
        ),
        Ul(
            Li(A("Services", href="#", cls="secondary")),
            Li(
                Details(
                    Summary("Account"), 
                    Ul(
                        Li(A("Profile", href="#")), 
                        Li(A("Settings", href="#")), 
                        Li(A("Security", href="#")), 
                        Li(A("Logout", href="#")),
                        dir="rtl",
                    ),
                    cls="dropdown"
                ),
            ),
        ),
    ),
)

pico_6_3_5 = div_code(
    code="""<nav>
  <ul>
    <li><strong>Acme Corp</strong></li>
  </ul>
  <ul>
    <li><a href="#" class="secondary">Services</a></li>
    <li>
      <details class="dropdown">
        <summary>
          Account
        </summary>
        <ul dir="rtl">
          <li><a href="#">Profile</a></li>
          <li><a href="#">Settings</a></li>
          <li><a href="#">Security</a></li>
          <li><a href="#">Logout</a></li>
        </ul>
      </details>
    </li>
  </ul>
</nav>""",
    lang="html",
)

sec_6_3_5 = section(
    body_6_3_5,
    art_6_3_5,
    pico_6_3_5,
    lv=4, title="Usage with nav",
)
#———————————————————
sec_6_3_0 = section(
    sec_6_3_1,
    sec_6_3_2,
    sec_6_3_3,
    sec_6_3_4,
    sec_6_3_5,
    lv=3, title="Dropdown",
    desc="Create dropdown menus and custom selects with minimal and semantic HTML, without JavaScript."
)

#—————————————————————————————————— 6.4
# 6.4 Group
# 6.4.1 Forms
# 6.4.2 Search
# 6.4.3 Buttons

body_6_4_1a = (
    P(span_code('role="group"'), " is used to stack children horizontally."),
    P(
        "When used with the ", 
        span_code('<form>', lang='html'), 
        " tag, the group is ", 
        span_code('width: 100%;', lang='css'), 
        "."),
    P(
        "Unlike ", 
        span_code('.grid', lang='css'), 
        " (see ",
        A("Grid", href="https://picocss.com/docs/grid", cls="secondary"),
        ")",
        " columns are not collapsed on mobile devices."),
)

art_6_4_1 = article(
    Form(
        Fieldset(
            Input(name="email", type="email", placeholder="Enter your email", autocomplete="email"),
            Input(type="submit", value="Subscribe"),
            role="group",
        ),
    ),
)

pico_6_4_1 = div_code(
    code="""<form>
  <fieldset role="group">
    <input name="email" type="email" placeholder="Enter your email" autocomplete="email" />
    <input type="submit" value="Subscribe" />
  </fieldset>
</form>""",
    lang="html",
)

body_6_4_1b = (
    P("This component is mainly designed for form elements and buttons. It brings a ", span_code(':focus', lang='css'), " style to the group depending on whether the focused child is an ", span_code('<input>', lang='html'), " or a ", span_code('<button>', lang='html'), "."),
    P("The group ", span_code(':focus'), " style relies on the ", span_code(':has()', lang='css'), " CSS selector and is therefore not (yet) supported by Firefox (see on ", A("caniuse", href="https://caniuse.com/css-has", cls="secondary"), "). When ", span_code(':has()', lang='css'), " is not supported the children have their regular ", span_code(':focus'), " style."),
)

art_6_4_1b = article(
    Form(
        Fieldset(
            Input(name="email", type="email", placeholder="Email", autocomplete="email"),
            Input(name="password", type="password", placeholder="Password"),
            Input(type="submit", value="Log in"),
            role="group",
        ),
    ),
)

pico_6_4_1b = div_code(
    code="""<form>
  <fieldset role="group">
    <input name="email" type="email" placeholder="Email" autocomplete="email" />
    <input name="password" type="password" placeholder="Password" />
    <input type="submit" value="Log in" />
  </fieldset>
</form>""",
    lang="html",
)

sec_6_4_1 = section(
    body_6_4_1a,
    art_6_4_1,
    pico_6_4_1,
    body_6_4_1b,
    art_6_4_1b,
    pico_6_4_1b,
    lv=4, title="Forms",
)
#———————————————————
body_6_4_2 = (
    P(span_code('role="search"'), " role='search' also stacks children horizontally and brings a special style, consistent with ", span_code('<input type="search" />', lang='html'), " (see ", A("Search input", href="https://picocss.com/docs/input#search", cls="secondary"), ")."),
)

art_6_4_2 = article(
    Form(
        Input(name="search", type="search", placeholder="Search"),
        Input(type="submit", value="Search"),
        role="search",
    ),
)

pico_6_4_2 = div_code(
    code="""<form role="search">
  <input name="search" type="search" placeholder="Search" />
  <input type="submit" value="Search" />
</form>""",
    lang="html",
)

sec_6_4_2 = section(
    body_6_4_2,
    art_6_4_2,
    pico_6_4_2,
    lv=4, title="Search",
)
#———————————————————
body_6_4_3 = (
    P(span_code('role="group"'), " is also useful for grouping a series of buttons."),
)

art_6_4_3a = article(
    Div(
        Button("Button"),
        Button("Button"),
        Button("Button"),
        role="group",
    ),
)

pico_6_4_3a = div_code(
    code="""<div role="group">
  <button>Button</button>
  <button>Button</button>
  <button>Button</button>
</div>""",
    lang="html",
)

art_6_4_3b = article(
    Div(
        Button("Active", aria_current="true"),
        Button("Button"),
        Button("Button"),
        role="group",
    ),
)

pico_6_4_3b = div_code(
    code="""<div role="group">
  <button aria-current="true">Active</button>
  <button>Button</button>
  <button>Button</button>
</div>""",
    lang="html",
)

art_6_4_3c = article(
    Div(
        Button("Button"),
        Button("Button", cls="secondary"),
        Button("Button", cls="contrast"),
        role="group",
    ),
)

pico_6_4_3c = div_code(
    code="""<div role="group">
  <button>Button</button>
  <button class="secondary">Button</button>
  <button class="contrast">Button</button>
</div>""",
    lang="html",
)

sec_6_4_3 = section(
    body_6_4_3,
    art_6_4_3a,
    pico_6_4_3a,
    art_6_4_3b,
    pico_6_4_3b,
    art_6_4_3c,
    pico_6_4_3c,
    lv=4, title="Buttons",
)

#———————————————————
sec_6_4_0 = section(
    sec_6_4_1,
    sec_6_4_2,
    sec_6_4_3,
    lv=3, title="Group",
    desc=(
        "Stack forms elements and buttons horizontally with ",
        span_code("role='group'"),
        " and ",
        span_code("role='search'"),
        "."
    ),
)

#—————————————————————————————————— 6.5
# 6.5 Loading
#———————————————————
body_6_5_1 = (
    P("It can be applied to any block:"),
)

art_6_5_1a = article(
    Div(
        aria_busy="true",
    ),
)

pico_6_5_1a = div_code(
    code="""<article aria-busy="true"></article>""",
    lang="html",
)

art_6_5_1b = article(
    Span(
        aria_busy="true",
    ),
)

pico_6_5_1b = div_code(
    code="""<span aria-busy="true">Generating your link...</span>""",
    lang="html",
)

art_6_5_1c = article(
    Div(
        Button(aria_busy="true", aria_label="Please wait…"),
        Button(aria_busy="true", aria_label="Please wait…", cls="secondary"),
        Button(aria_busy="true", aria_label="Please wait…", cls="contrast"),
        cls="grid", 
        style="margin-bottom: 1em;" # separation with the next div
    ),
    Div(
        Button("Please wait…", aria_busy="true", cls="outline"),
        Button("Please wait…", aria_busy="true", cls="outline secondary"),
        Button("Please wait…", aria_busy="true", cls="outline contrast"),
        cls="grid",
    ),
)

pico_6_5_1c = div_code(
    code="""<button aria-busy="true" aria-label="Please wait…" />
<button aria-busy="true" aria-label="Please wait…" class="secondary" />
<button aria-busy="true" aria-label="Please wait…" class="contrast" />
<button aria-busy="true" class="outline">Please wait…</button>
<button aria-busy="true" class="outline secondary">Please wait…</button>
<button aria-busy="true" class="outline contrast">Please wait…</button>""",
    lang="html",
)

#———————————————————
sec_6_5_0 = section(
    body_6_5_1,
    art_6_5_1a,
    pico_6_5_1a,
    art_6_5_1b,
    pico_6_5_1b,
    art_6_5_1c,
    pico_6_5_1c,
    lv=3, title="Loading",
    desc=(
        "Add a loading indicator with ",
        span_code("aria-busy='true'"),
        "."
    ),
)

#—————————————————————————————————— 6.6
# 6.6 Modal
# 6.6.1 Syntax
# 6.6.2 Demo
# 6.6.3 Utilities
#———————————————————

body_6_6_1a = (
    P("Modals are built with ", span_code('<dialog>', lang='html'), " as a wrapper and ", span_code('<article>', lang='html'), " for the modal content."),
    P("Inside ", span_code('<header>', lang='html'), " ", span_code('<button rel="prev">', lang='html'), " is defined to ", span_code('float: right;', lang='css'), " allowing a close icon to be top aligned with a title."),
)

modal_6_6_1a = Dialog(
    Article(
        Header(
                Button(aria_label="Close", rel="prev"),
            P(Strong("🗓️ Thank You for Registering!")),
            ),
            P("We're excited to have you join us for our upcoming event. Please arrive at the museum on time to check in and get started."),
            Ul(
                Li("Date: Saturday, April 15"),
                Li("Time: 10:00am - 12:00pm"),
            ),
        ),
        cls="example",
        open="true",
    ),


pico_6_6_1a = div_code(
    code="""<dialog open>
  <article>
    <header>
      <button aria-label="Close" rel="prev"></button>
      <p>
        <strong>🗓️ Thank You for Registering!</strong>
      </p>
    </header>
    <p>
      We're excited to have you join us for our
      upcoming event. Please arrive at the museum 
      on time to check in and get started.
    </p>
    <ul>
      <li>Date: Saturday, April 15</li>
      <li>Time: 10:00am - 12:00pm</li>
    </ul>
  </article>
</dialog>""",
    lang="html",
)

body_6_6_1b = (
    P("Inside ", span_code('<footer>', lang='html'), ", the content is right aligned by default."),
)

modal_6_6_1b = Dialog(
    Article(
        Header(
            H2("Confirm Your Membership"),
        ),
        P("Thank you for signing up for a membership!"),
        Ul(
            Li("Membership: Individual"),
            Li("Price: $10"),
        ),
        Footer(
            Button("Cancel", cls="secondary"),
            Button("Confirm"),
        ),
    ),
    cls="example",
    open="true",
)

pico_6_6_1b = div_code(
    code="""<dialog open>
  <article>
    <h2>Confirm Your Membership</h2>
    <p>
      Thank you for signing up for a membership!
      Please review the membership details below:
    </p>
    <ul>
      <li>Membership: Individual</li>
      <li>Price: $10</li>
    </ul>
    <footer>
      <button className="secondary">
        Cancel
      </button>
      <button>Confirm</button>
    </footer>
  </article>
</dialog>""",
    lang="html",
)

sec_6_6_1 = section(
    body_6_6_1a,
    modal_6_6_1a,
    pico_6_6_1a,
    body_6_6_1b,
    modal_6_6_1b,
    pico_6_6_1b,
    lv=4, title="Syntax",
)
#———————————————————
body_6_6_2a = (
    P("Toggle a modal by clicking the button below."),
)

# will be inserted at the end of `<body>`
modal_6_6_2 = Div(
    Article(
        Header(
            Button("×", aria_label="Close", rel="prev", hx_post="/close_modal", hx_target="#modal-demo", hx_swap="outerHTML"),
            H2("Confirm Your Membership"),
        ),
        P("Thank you for signing up for a membership!"),
        Ul(
            Li("Membership: Individual"),
            Li("Price: $10"),
        ),
        Footer(
            Button("Cancel", cls="secondary", hx_post="/close_modal", hx_target="#modal-demo", hx_swap="outerHTML"),
            Button("Confirm"),
        ),
    ),
    _="on closeModal add .closing then wait for animationend then remove me",
    id="modal",
)


def render_modal():
    return f"""
    <dialog id="modal" open>
        <article>
            <header>
                <button aria-label="Close" rel="prev" hx-get="/close_modal" hx-target="#modal" hx-swap="outerHTML">×</button>
                <h2>Confirm Your Membership</h2>
            </header>
            <p>Thank you for signing up for a membership!</p>
            <ul>
                <li>Membership: Individual</li>
                <li>Price: $10</li>
            </ul>
            <footer>
                <button aria-label="Closed" class="secondary" hx-get="/close_modal" hx-target="#modal" hx-swap="outerHTML">Cancel</button>
                <button>Confirm</button>
            </footer>
        </article>
    </dialog>
    """

# will call the above render_modal() in the router (bottom of this file)
btnmod_6_6_2a = Article(
    Button("Open Modal", hx_get="/modal", hx_target="body", hx_swap="beforeend"),
)

body_6_6_2b = (
    P("The modal can be closed by clicking the close button or by clicking outside the modal."),
    P("Pico does not include JavaScript code. You need to implement your JS to interact with modals."),
    P("As a starting point, you can look at the ", A("HTMLDialogElement", href="https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement", target="_blank"), " or the advanced examples below:"),
    Ul(
        Li(A("Vanilla JavaScript", href="https://codesandbox.io/embed/4mrnhq?view=Editor+%2B+Preview&module=%2Fjs%2Fmodal.js", target="_blank")),
        Li(A("React", href="https://codesandbox.io/p/devbox/github/picocss/examples/tree/master/v2-react-color-schemes-and-modal?embed=1&file=%2Fsrc%2Fcomponents%2FModal.js", target="_blank")),
    ),
    P("To open a modal, add the ", span_code("open", lang='html'), " attribute to the ", span_code("<dialog>", lang='html'), " container."),
)

sec_6_6_2 = section(
    body_6_6_2a,
    btnmod_6_6_2a,
    body_6_6_2b,
    lv=4, title="Demo",
)
#———————————————————

body_6_6_3a = (
    P("Modals come with 3 utility classes."),
    P("These classes are not available in the class-less version."),

    P(span_code(".modal-is-open", lang='html'), " prevents any scrolling and interactions below the modal."),
)

pico_6_6_3a = div_code(
    code="""<!doctype html>
<html class="modal-is-open">
  ...
</html>""",
    lang="html",
)

body_6_6_3b = (
    P(span_code(".modal-is-opening"), " brings an opening animation."),
)

pico_6_6_3b = div_code(
    code="""<!doctype html>
<html class="modal-is-open modal-is-opening">
  ...
</html>""",
    lang="html",
)

body_6_6_3c = (
    P(span_code(".modal-is-closing"), " brings an closing animation."),
)

pico_6_6_3c = div_code(
    code="""<!doctype html>
<html class="modal-is-open modal-is-closing">
  ...
</html>""",
    lang="html",
)

sec_6_6_3 = section(
    body_6_6_3a,
    pico_6_6_3a,
    body_6_6_3b,
    pico_6_6_3b,
    body_6_6_3c,
    pico_6_6_3c,
    lv=4, title="Utilities",
)
#———————————————————
sec_6_6_0 = section(
    sec_6_6_1,
    sec_6_6_2,
    sec_6_6_3,
    lv=3, title="Modal",
    desc=(
        "The classic modal component with graceful spacings across devices and viewports, using the semantic HTML tag ",
        span_code("<dialog>", lang='html'),
        "."
    ),
)

#—————————————————————————————————— 6.7
# 6.7 Nav
# 6.7.1 Syntax
# 6.7.2 Link variants
# 6.7.3 Buttons
# 6.7.4 Dropdowns
# 6.7.5 Vertical stacking
# 6.7.6 Breadcrumb
# 6.7.7 Overflow
#———————————————————

art_6_7_1 = article(
    Nav(
        Ul(
            Li(Strong("Acme Corp")),
        ),
        Ul(
            Li(A("About", href="#")),
            Li(A("Services", href="#")),
            Li(A("Products", href="#")),
        ),
    )
)

pico_6_7_1 = div_code(
    code="""<nav>
  <ul>
    <li><strong>Acme Corp</strong></li>
  </ul>
  <ul>
    <li><a href="#">About</a></li>
    <li><a href="#">Services</a></li>
    <li><a href="#">Products</a></li>
  </ul>
</nav>""",
    lang="html",
)

body_6_7_1 = (
    P(span_code("<ul>", lang='html'), " are automatically distributed horizontally."),
    P(span_code("<li>", lang='html'), " are unstyled and inlined."),
    P(span_code("<a>", lang='html'), " are underlined only on :hover."),
)

sec_6_7_1 = section(
    art_6_7_1,
    pico_6_7_1,
    body_6_7_1,
    lv=4, title="Syntax",
)
#———————————————————
body_6_7_2a = (
    P("You can use  ", span_code(".secondary", lang='css'),  ", ", span_code(".contrast", lang='css'), " and  ", span_code(".outline", lang='css'), "  classes (not available in the class-less version)."),
)

art_6_7_2a = article(
    Nav(
        Ul(
            Li(Strong("Acme Corp")),
        ),
        Ul(
            Li(A("About", href="#", cls="contrast")),
            Li(A("Services", href="#", cls="contrast")),
            Li(A("Products", href="#", cls="contrast")),
        ),
    )
)

pico_6_7_2a = div_code(
    code="""<nav>
  <ul>
    <li><strong>Acme Corp</strong></li>
  </ul>
  <ul>
    <li><a href="#" class="contrast">About</a></li>
    <li><a href="#" class="contrast">Services</a></li>
    <li><a href="#" class="contrast">Products</a></li>
  </ul>
</nav>>""",
    lang="html",
)

art_6_7_2b = article(
    Nav(
        Ul(
            Li(A("...", href="#", cls="secondary")),
        ),
        Ul(
            Li(Strong("Acme Corp")),
        ),
        Ul(
            Li(A("...", href="#", cls="secondary")),
        ),
    )
)

pico_6_7_2b = div_code(
    code="""<nav>
  <ul>
    <li><a href="#" class="secondary">...</a></li>
  </ul>
  <ul>
    <li><strong>Acme Corp</strong></li>
  </ul>
  <ul>
    <li><a href="#" class="secondary">...</a></li>
  </ul>
</nav>""",
    lang="html",
)

sec_6_7_2 = section(
    body_6_7_2a,
    art_6_7_2a,
    pico_6_7_2a,
    art_6_7_2b,
    pico_6_7_2b,
    lv=4, title="Link variants",
)
#———————————————————

body_6_7_3 = (
    P("You can use  ", span_code("<button>", lang='html'), " inside ", span_code("<li>", lang='html'), "."),
    P("Button sizes automatically match link size and margin."),
)

art_6_7_3 = article(
    Nav(
        Ul(
            Li(Strong("Acme Corp")),
        ),
        Ul(
            Li(A("About", href="#")),
            Li(A("Services", href="#")),
            Li(Button("Products", href="#")),
        ),
    )
)

pico_6_7_3 = div_code(
    code="""<nav>
  <ul>
    <li><strong>Acme Corp</strong></li>
  </ul>
  <ul>
    <li><a href="#">About</a></li>
    <li><a href="#">Services</a></li>
    <li><button class="secondary">Products</button></li>
  </ul>
</nav>""",
    lang="html",
)

sec_6_7_3 = section(
    body_6_7_3,
    art_6_7_3,
    pico_6_7_3,
    lv=4, title="Buttons",
)
#———————————————————

body_6_7_4 = (
    P("You can use dropdowns inside Nav."),
)

art_6_7_4 = article(
    Nav(
        Ul(
            Li(Strong("Acme Corp")),
        ),
        Ul(
            Li(A("Services", href="#", cls="secondary")),
            Li(
                Details(
                    Summary("Account"), 
                    Ul(
                        Li(A("Profile", href="#")), 
                        Li(A("Settings", href="#")), 
                        Li(A("Security", href="#")), 
                          Li(A("Logout", href="#")),
                          dir="rtl",
                    ),
                    cls="dropdown",
                ),
            ),
        ),
    )
)

pico_6_7_4 = div_code(
    code="""<nav>
  <ul>
    <li><strong>Acme Corp</strong></li>
  </ul>
  <ul>
    <li><a href="#" class="secondary">Services</a></li>
    <li>
      <details class="dropdown">
        <summary>
          Account
        </summary>
        <ul dir="rtl">
          <li><a href="#">Profile</a></li>
          <li><a href="#">Settings</a></li>
          <li><a href="#">Security</a></li>
          <li><a href="#">Logout</a></li>
        </ul>
      </details>
    </li>
  </ul>
</nav>""",
    lang="html",
)


sec_6_7_4 = section(
    body_6_7_4,
    art_6_7_4,
    pico_6_7_4,
    lv=4, title="Dropdowns",
)
#———————————————————
body_6_7_5 = (
    P("Inside ", span_code("<aside>", lang='html'), ", navs items are stacked vertically."),
)

art_6_7_5 = article(
    Aside(
        Nav(
            Ul(
                Li(A("About", href="#")),
                Li(A("Services", href="#")),
                Li(A("Products", href="#")),
            ),
        ),
    )
)

pico_6_7_5 = div_code(
    code="""<aside>
  <nav>
    <ul>
      <li><a href="#">About</a></li>
      <li><a href="#">Services</a></li>
      <li><a href="#">Products</a></li>
    </ul>
  </nav>
</aside>""",
    lang="html",
)

sec_6_7_5 = section(
    body_6_7_5,
    art_6_7_5,
    pico_6_7_5,
    lv=4, title="Vertical stacking",
)
#———————————————————

body_6_7_6a = (
    P("With ", span_code("<nav aria-label='breadcrumb'>", lang='html'), ", you can turn a nav into a breadcrumb."),
)

art_6_7_6a = article(
    Nav(
        Ul(
            Li(A("Home", href="#")),
            Li(A("Services", href="#")),
            Li("Design"),
        ),
        aria_label="breadcrumb",
    )
)

pico_6_7_6a = div_code(
    code="""<nav aria-label="breadcrumb">
  <ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">Services</a></li>
    <li>Design</li>
  </ul>
</nav>""",
    lang="html",
)

body_6_7_6b = (
    P("You can change the divider with a local CSS custom property ", span_code("--pico-nav-breadcrumb-divider", lang='css'), "."),
)

art_6_7_6b = article(
    Nav(
        Ul(
            Li(A("Home", href="#")),
            Li(A("Services", href="#")),
            Li("Design"),
        ),
        aria_label="breadcrumb",
        style="--pico-nav-breadcrumb-divider: '✨';",
    )
)

pico_6_7_6b = div_code(
    code="""<nav
  aria-label="breadcrumb"
  style="--pico-nav-breadcrumb-divider: '✨';"
>
  <ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">Services</a></li>
    <li>Design</li>
  </ul>
</nav>""",
    lang="html",
)

sec_6_7_6 = section(
    body_6_7_6a,
    art_6_7_6a,
    pico_6_7_6a,
    body_6_7_6b,
    art_6_7_6b,
    pico_6_7_6b,
    lv=4, title="Breadcrumb",
)
#———————————————————
body_6_7_7 = (
    P("The ", span_code("<nav>"), " component uses ", span_code("overflow: visible;"), " on the container and negative margins on childrens to provide a nice ", span_code("::focus-visible"), " style for links on keyboard navigation while keeping the content aligned horizontally."),
)

art_6_7_7 = article(
    Nav(
        Ul(
            Li(A("About", href="#")),
            Li(A("Services", href="#")),
        ),
        Ul(
            Li("Products"),
        ),
        aria_label="overflow",
    ),
    Nav(
        Ul(
            Li(A("About", href="#", cls="focused")),
            Li(A("Services", href="#")),
        ),
        Ul(
            Li("Products", cls="focused"),
        ),
        aria_label="overflow-with-focus",
    )
)


sec_6_7_7 = section(
    body_6_7_7,
    art_6_7_7,
    lv=4, title="Overflow",
)
#———————————————————
sec_6_7_0 = section(
    sec_6_7_1,
    sec_6_7_2,
    sec_6_7_3,
    sec_6_7_4,
    sec_6_7_5,
    sec_6_7_6,
    sec_6_7_7,
    lv=3, title="Nav",
    desc="The essential navbar component in pure semantic HTML."
)

#—————————————————————————————————— 6.8
# 6.8 Progress
# 6.8.1 Syntax
# 6.8.2 Indeterminate
#———————————————————

# art_6_8_1 = article(
#     Progressbar(value="89", max="100"),
# )

pico_6_8_1 = div_code(
    code="""<progress value="89" max="100" />""",
    lang="html",
)



sec_6_8_1 = section(
    # art_6_8_1,
    pico_6_8_1,
    lv=4, title="Syntax",
)
#———————————————————

# art_6_8_2 = article(
#     Progress(),
# )

pico_6_8_2 = div_code(
    code="""<progress />""",
    lang="html",
)

sec_6_8_2 = section(
    # art_6_8_2,
    pico_6_8_2,
    lv=4, title="Indeterminate",
)
#———————————————————
sec_6_8_0 = section(
    sec_6_8_1,
    sec_6_8_2,
    lv=3, title="Progress",
    desc="The progress bar element in pure HTML, without JavaScript."
)
#—————————————————————————————————— 6.9
# 6.9 Tooltip
# 6.9.1 Syntax
# 6.9.2 Placement
#———————————————————

art_6_9_1 = article(
    P("Tooltip on a ", A("link", href="#", data_tooltip="Tooltip"), "."),
    P("Tooltip on an ", Em("inline element", data_tooltip="Tooltip"), "."),
    P(Button("Tooltip on a button", data_tooltip="Tooltip")),
)

pico_6_9_1 = div_code(
    code="""<p>Tooltip on a <a href="#" data-tooltip="Tooltip">link</a></p>
<p>Tooltip on <em data-tooltip="Tooltip">inline element</em></p>
<p><button data-tooltip="Tooltip">Tooltip on a button</button></p>""",
    lang="html",
)

sec_6_9_1 = section(
    art_6_9_1,
    pico_6_9_1,
    lv=4, title="Syntax",
)
#———————————————————
body_6_9_2 = (
    P("The tooltip is displayed on top by default but you can change it with the ", span_code("data-placement", lang='html'), " attribute."),
)

art_6_9_2 = article(
    Button("Top", data_tooltip="Top", data_placement="top"),
    Button("Right", data_tooltip="Right", data_placement="right"),
    Button("Bottom", data_tooltip="Bottom", data_placement="bottom"),
    Button("Left", data_tooltip="Left", data_placement="left"),
    cls="grid",
)

pico_6_9_2 = div_code(
    code="""<button data-tooltip="Top">Top</button>
<button data-tooltip="Right" data-placement="right">Right</button>
<button data-tooltip="Bottom" data-placement="bottom">Bottom</button>
<button data-tooltip="Left" data-placement="left">Left</button>""",
    lang="html",
)

sec_6_9_2 = section(
    body_6_9_2,
    art_6_9_2,
    pico_6_9_2,
    lv=4, title="Placement",
)
#———————————————————




sec_6_9_0 = section(
    sec_6_9_1,
    sec_6_9_2,
    lv=3, title="Tooltip",
    desc="Enable tooltips everywhere, without JavaScript."
)
#———————————————————
sec_6_0_0 = section(
    sec_6_1_0,
    sec_6_2_0,
    sec_6_3_0,
    sec_6_4_0,
    sec_6_5_0,
    sec_6_6_0,
    sec_6_7_0,
    sec_6_8_0,
    sec_6_9_0,
    lv=2, title="Components",
)
#————————————————————————————————————————————————————————————————————————————7
# 7. About
# 7.1 What’s new in v2?
# 7.2 Mission
# 7.3 Usage scenarios
# 7.4 Brand
# 7.5 Built With
#———————————————————




#—————————————————————————————————— 7.1

sec_7_1_0 = section(
    lv=3, title="What’s new in v2?",
    desc="Pico v2.0 features better accessibility, easier customization with SASS, a complete color palette, a new group component, and 20 precompiled color themes totaling over 100 combinations accessible via CDN."
)

#—————————————————————————————————— 7.2

sec_7_2_0 = section(
    lv=3, title="Mission",
    desc="Pico CSS is a minimalist and lightweight starter kit that prioritizes semantic syntax, making every HTML element responsive and elegant by default."
)

#—————————————————————————————————— 7.3

sec_7_3_0 = section(
    lv=3, title="Usage scenarios",
    desc="How does Pico fit into your project?"
)

#—————————————————————————————————— 7.4

sec_7_4_0 = section(
    lv=3, title="Brand",
    desc="Pico CSS brand assets and usage guidelines."
)

#—————————————————————————————————— 7.5

sec_7_5_0 = section(
    lv=3, title="Built With",
    desc="Relevant packages, tools, and resources we depend on."
)


sec_7_0_0 = section(
    sec_7_1_0,
    sec_7_2_0,
    sec_7_3_0,
    sec_7_4_0,
    sec_7_5_0,
    lv=2, title="About",
)
#—————————————————————————————————————————————————————————————————————————————
sections = (
    sec_1_0_0,
    sec_2_0_0,
    sec_3_0_0,
    sec_4_0_0,
    sec_5_0_0,
    sec_6_0_0,
    sec_7_0_0,
)
# modal = modal_6_6_2
page = (title, html, main(sections), 
        # modal_6_6_2,
        )

# Home page
@rt("/")
def get(): # type: ignore
    return page

# Dark/Light theme switch
@rt("/toggle_theme")
async def post(request: Request):
    # Get the current theme from the button's name attribute
    current_theme = request.headers.get("HX-Trigger-Name", "").split("(")[-1].strip(")")
    new_theme = "light" if current_theme == "dark" else "dark"

    response_content = f"""
    <article id="theme-switcher" aria-label="Theme switcher">
        <button class="contrast" hx-post="/toggle_theme" hx-swap="outerHTML" hx-target="#theme-switcher" name="theme-toggle({new_theme})">
            Make {new_theme}!
        </button>
    </article>
    <script>
        document.documentElement.setAttribute('data-theme', '{current_theme}');
    </script>
    """
    
    return HTMLResponse(content=response_content)

@rt("/modal")
async def get(): # type: ignore
    return HTMLResponse(content=render_modal())

@rt("/close_modal")
async def get():
    return HTMLResponse(content="")
