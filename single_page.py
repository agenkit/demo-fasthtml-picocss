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
    href="style/single-page.css",
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

def div_code(code, lang=None):
    '''Returns a <div> wrapping a <pre><code> block.
    Use within <h4> sections to display code examples.
    '''
    return Div(
        Pre(
            Code(code,
                cls="highlight language-"+lang if lang else "highlight",
            ),
        ),
        cls="pre-code",
    )

def aside(*aside_tags):
    '''Returns an <aside> block. TODO: Implementation lol 😹
    `aside_tags` needs to be created (ToC) from the list of H2, H3, H4…
    '''
    return Aside(aside_tags)

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

#   ➕
def art_c(*c): # c for content
    return (*c, )

#   ➕
def art_footer(html, python):
    return Footer(Pre(Code(html)), Pre(Code(python)))

#   🡇
# def article(c, hd=None, ft=None, **kwargs):
#     return Card(*c, header=hd, footer=ft, **kwargs)


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
        Code("/css/pico.min.css"),
        """ in the """,
        Code("""<head>""", cls="highlight language-html", ),
        """ of your website.""",
    ),
    pico_1_1_1,
)
#   🡇🡇🡇
sec_1_1_1 = section(body_1_1_1,
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
    Code("pico.min.css"),
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
        Code("pico.css"),
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
        Code('<html data-theme="light">', cls='highlight language-html'),
        " or for specific HTML elements, such as ",
        Code('<article data-theme="dark">', cls='highlight language-html'),
        ".",
    ),
    P(  "Color schemes at the HTML tag level work great for elements such as ",
        Code('<a>', cls='highlight language-html'), ', ',
        Code('<button>', cls='highlight language-html'), ', ',
        Code('<table>', cls='highlight language-html'), ', ',
        Code('<input>', cls='highlight language-html'), ', ',
        Code('<textarea>', cls='highlight language-html'), ', ',
        Code('<select>', cls='highlight language-html'), ', ',
        Code('<article>', cls='highlight language-html'), ', ',
        Code('<dialog>', cls='highlight language-html'), ', ',
        Code('<progress>', cls='highlight language-html'), '.',
    ),
    P(  "CSS variables specific to the color scheme are assigned to every HTML tag. However, we have not enforced specific background and color settings across all HTML tags to maintain transparent backgrounds and ensure colors are inherited from the parent tag."
    ),
    P(  "For some other HTML tags, you might need to explicitly set ",
    Code('background-color', cls='highlight'),
    " and ",
    Code('color', cls='highlight'),
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
    footer = Footer(Pre(Code(pico, cls='highlight language-html'),),cls="code",)
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
      Code("prefers-color-scheme: dark;", cls="highlight"), '.'),
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
        Code(".classless"),
        " version, a semantic option for wild HTML purists who prefer a stripped-down approach.",
    ),
)

#—————————————————————————————————— 1.5

sec_1_5_0 = section(
    lv=3, title="Conditional styling",
    desc=(
        "Apply Pico CSS styles selectively by wrapping elements in a ",
        Code(".pico"),
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
    P(Code(".container"),
    " and ",
    Code(".container-fluid"),
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
    P(Code(".container"), " provides a centered container with a fixed width."),
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
    P(Code(".container-fluid"), " provides a full-width container."),
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
        Code("<header>", cls="highlight"), ", ",
        Code("<main>", cls="highlight"), ", and ",
        Code("<footer>", cls="highlight"),
        " inside ",
        Code("<body>", cls="highlight"),
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
    desc=("Use ", Code('.container'), "for a centered viewport or ", Code('.container-fluid'), " for a full-width layout.")
)

#—————————————————————————————————— 3.2
# 3.2 Landmarks & section
# 3.2.1 Landmarks
# 3.2.2 Custom root container
# 3.2.3 Section


body_3_2_1 = (
    P(
        Code("<header>", cls="highlight"), ", ",
        Code("<main>", cls="highlight"), ", and ",
        Code("<footer>", cls="highlight"),
        " as direct children of ",
        Code("<body>", cls="highlight"),
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
        Code("<header>", cls="highlight"), ", ",
        Code("<main>", cls="highlight"), ", and ",
        Code("<footer>", cls="highlight"),
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
        Code("<section>", cls="highlight"), 
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
    P("Columns intentionally collapse on small devices (", Code("<768px"), ")."),
    P(Code(".grid"), "is not available in the ", A("class‑less", href="https://picocss.com/docs/classless"), " version."),
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
        Code(".grid"), 
        " to enable auto-layout columns."),
)

#—————————————————————————————————— 3.4
# 3.4 Overflow auto


body_3_4_1 = (
    P("Useful to have responsive ", Code("<table>", cls="highlight"), "."),
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
        Code(".overflow-auto"),
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

sec_4_1_0 = section(
    lv=3, title="Typography",
    desc="All typographic elements are responsive and scale gracefully across devices and viewports.",
)

#—————————————————————————————————— 4.2
# 4.2 Link







sec_4_2_0 = section(
    lv=3, title="Link",
    desc=(
        "Links come with ",
        Code(".secondary"),
        " and ",
        Code(".contrast"),
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










sec_4_3_0 = section(
    lv=3, title="Button",
    desc=(
        "Buttons are using the native ",
        Code("<button>", cls="highlight"),
        " tag, without ",
        Code(".classes"),
        ". for the default style."),
)

#—————————————————————————————————— 4.4
# 4.4 Table
# 4.4.1 Syntax
# 4.4.2 Color schemes
# 4.4.3 Striped





sec_4_4_0 = section(
    lv=3, title="Table",
    desc=(
        "Clean and minimal styles for ",
        Code("<table>", cls="highlight"),
        ", providing consistent spacings and a minimal unbordered look."),
)

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

sec_5_1_0 = section(
    lv=3, title="Overview",
    desc="All form elements are fully responsive with pure semantic HTML, enabling forms to scale gracefully across devices and viewports."
)

#—————————————————————————————————— 5.2

sec_5_2_0 = section(
    lv=3, title="Input",
    desc="All input types are consistently styled and come with validation states."
)

#—————————————————————————————————— 5.3

sec_5_3_0 = section(
    lv=3, title="Textarea",
    desc=(
        "The native ",
        Code("<textarea>", cls="highlight"),
        " is styled like the input for consistency."
    ),
)

#—————————————————————————————————— 5.4

sec_5_4_0 = section(
    lv=3, title="Select",
    desc=(
        "The native ",
        Code("<select>", cls="highlight"),
        " is styled like the input for consistency."
    ),
)

#—————————————————————————————————— 5.5

sec_5_5_0 = section(
    lv=3, title="Checkboxes",
    desc=(
        "The native ",
        Code("<input type='checkbox'>", cls="highlight"),
        " with a custom and responsive style."
    ),
)

#—————————————————————————————————— 5.6

sec_5_6_0 = section(
    lv=3, title="Radios",
    desc=(
        "The native ",
        Code("<input type='radio'>", cls="highlight"),
        " with a custom and responsive style."
    ),
)

#—————————————————————————————————— 5.7

sec_5_7_0 = section(
    lv=3, title="Switch",
    desc=(
        "A switch component in pure CSS, using the checkbox syntax."
    ),
)

#—————————————————————————————————— 5.8

sec_5_8_0 = section(
    lv=3, title="Range",
    desc=(
        "Create a slider control with ",
        Code("<input type='range'>", cls="highlight"),
        "."
    ),
)

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

sec_6_1_0 = section(
    lv=3, title="Accordion",
    desc=(
        "Toggle sections of content in pure HTML, without JavaScript, using minimal and semantic markup."
    ),
)

#—————————————————————————————————— 6.2

sec_6_2_0 = section(
    lv=3, title="Card",
    desc=(
        "Create flexible cards with a semantic markup that provides graceful spacings across various devices and viewports."
    ),
)

#—————————————————————————————————— 6.3

sec_6_3_0 = section(
    lv=3, title="Dropdown",
    desc="Create dropdown menus and custom selects with minimal and semantic HTML, without JavaScript."
)

#—————————————————————————————————— 6.4

sec_6_4_0 = section(
    lv=3, title="Group",
    desc=(
        "Stack forms elements and buttons horizontally with ",
        Code("role='group'"),
        " and ",
        Code("role='search'"),
        "."
    ),
)

#—————————————————————————————————— 6.5

sec_6_5_0 = section(
    lv=3, title="Loading",
    desc=(
        "Add a loading indicator with ",
        Code("aria-busy='true'"),
        "."
    ),
)

#—————————————————————————————————— 6.6

sec_6_6_0 = section(
    lv=3, title="Modal",
    desc=(
        "The classic modal component with graceful spacings across devices and viewports, using the semantic HTML tag ",
        Code("<dialog>", cls="highlight"),
        "."
    ),
)

#—————————————————————————————————— 6.7

sec_6_7_0 = section(
    lv=3, title="Nav",
    desc="The essential navbar component in pure semantic HTML."
)

#—————————————————————————————————— 6.8

sec_6_8_0 = section(
    lv=3, title="Progress",
    desc="The progress bar element in pure HTML, without JavaScript."
)

#—————————————————————————————————— 6.9

sec_6_9_0 = section(
    lv=3, title="Tooltip",
    desc="Enable tooltips everywhere, without JavaScript."
)



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
page = (title, html, main(sections))

# Home page
@rt("/")
def get():
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
