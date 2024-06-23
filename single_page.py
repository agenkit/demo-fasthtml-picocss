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

#————————————————————————————————————————————————————————————————————————————1
# 1. Getting started
# 1.1. Quick start
# 1.2. Version picker
# 1.3. Color schemes
# 1.4. Class-less version
# 1.5. Conditional styling
# 1.6. RTL


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



sec_1_2_0 = section(
    lv=3, title="Version picker",
)












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

sec_1_4_0 = section(
    lv=3, title="Class-less version",
)

sec_1_5_0 = section(
    lv=3, title="Conditional styling",
)

sec_1_6_0 = section(
    lv=3, title="RTL",
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
#————————————————————————————————————————————————————————————————————————————2
# Customization
# - CSS Variables
# - Sass
# - Colors

sec_2_1_0 = section(
    lv=3, title="CSS Variables",
)

sec_2_2_0 = section(
    lv=3, title="Sass",
)
sec_2_3_0 = section(
    lv=3, title="Colors",
)


sec_2_0_0 = section(
    sec_2_1_0,
    sec_2_2_0,
    sec_2_3_0,
    lv=2, title="Customization",
)

#————————————————————————————————————————————————————————————————————————————3
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






sec_3_2_1 = section(
    lv=4, title="Landmarks",
)




sec_3_2_2 = section(
    lv=4, title="Custom root container",
)





sec_3_2_3 = section(
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

sec_3_3_1 = section(
    lv=4, title="Syntax",
)



sec_3_3_2 = section(
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

sec_3_4_0 = section(

    lv=3, title="Overflow auto",

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

sec_4_1_0 = section(
    lv=3, title="Typography",
)

sec_4_2_0 = section(
    lv=3, title="Link",
)
sec_4_3_0 = section(
    lv=3, title="Button",
)
sec_4_4_0 = section(
    lv=3, title="Table",
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

sec_5_1_0 = section(
    lv=3, title="Overview",
)

sec_5_2_0 = section(
    lv=3, title="Input",
)

sec_5_3_0 = section(
    lv=3, title="Textarea",
)

sec_5_4_0 = section(
    lv=3, title="Select",
)

sec_5_5_0 = section(
    lv=3, title="Checkboxes",
)

sec_5_6_0 = section(
    lv=3, title="Radios",
)

sec_5_7_0 = section(
    lv=3, title="Switch",
)

sec_5_8_0 = section(
    lv=3, title="Range",
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

sec_6_1_0 = section(
    lv=3, title="Accordion",
)

sec_6_2_0 = section(
    lv=3, title="Card",
)

sec_6_3_0 = section(
    lv=3, title="Dropdown",
)

sec_6_4_0 = section(
    lv=3, title="Group",
)

sec_6_5_0 = section(
    lv=3, title="Loading",
)

sec_6_6_0 = section(
    lv=3, title="Modal",
)

sec_6_7_0 = section(
    lv=3, title="Nav",
)

sec_6_8_0 = section(
    lv=3, title="Progress",
)

sec_6_9_0 = section(
    lv=3, title="Tooltip",
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

sec_7_1_0 = section(
    lv=3, title="What’s new in v2?",
)

sec_7_2_0 = section(
    lv=3, title="Mission",
)

sec_7_3_0 = section(
    lv=3, title="Usage scenarios",
)

sec_7_4_0 = section(
    lv=3, title="Brand",
)

sec_7_5_0 = section(
    lv=3, title="Built With",
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
