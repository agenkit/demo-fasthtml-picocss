# FastHTML 🧡 Pico CSS
🡆 *Demonstrating Pico CSS in FastHTML.*

This demo is a rewrite of the "Docs" section of the Pico CSS website as one (long) page of FastHTML.

You can clone this repo and run `main.py` locally through `uvicorn` :

```bash
uvicorn main:app
```

> [!IMPORTANT]  
> I haven't been able to deploy this particular app. (I've had success with other FastHTML apps, not sure what's up).  
It "works on my machine" but my server isn't happy with it; I need to redeploy *blablabla* (and I don't know Python deployment as HTTP apps, I've mostly used Py as scripts on servers in IT/devops, or locally as CLI or PyQt apps for instance). I should also look into e.g. Railway I guess (but I'm not sure which template to choose for FastHTML).
>
> If you can help me solve/learn ASGI Python web apps deployment, feel free to reach out.  
> → in [GH Issues](https://github.com/agenkit/demo-fasthtml-picocss/issues) or on [𝕏](https://x.com/x__kit)

> [!TIP]
> Code in `main.py` is discussed in [`/docs/main.md`](https://github.com/agenkit/demo-fasthtml-picocss/blob/main/docs/main.md) — below the big TODO list.




## TL;DR

- **Unfinished**, work in progress. No ETA.

- Usage: classic **page search**, <kbd>Ctrl</kbd> ( <kbd>⌘</kbd> ) + <kbd>F</kbd>

- (final form) About a hundred **1:1 pairs** of `HTML` ←→ `FastHTML` snippets for quick translation.

- Demonstrates **Pico CSS**,
  - which can work "classless" as well, wherein naked HTML tags are all you need for style.

- Comments warmly welcome 🎓🆘🙏 → [GH Issues](https://github.com/agenkit/demo-fasthtml-picocss/issues) or [𝕏](https://x.com/x__kit)

- Built while FastHTML was still in **beta** (June 2024), thus **may still contain errors and false information** (will be corrected eventually).  
Notably, **all HTML tags are now implemented** in FastHTML.

About me: I'm *not* a web dev. I just made a few websites since 1999 (literally).  
In 2024, I try to suck less at AI and that's already a tall order for me.  
*Especially when geniuses throw FastHTML at me randomly on an otherwise perfectly good AI day.* 😅

So feel free to school me, I know I'm doing a lot of things wrong in my code. I just don't know what—*yet*—and that's where *you* come in!




## Resources

### 📚 Docs

- FastHTML: <https://answerdotai.github.io/fasthtml>
- Pico CSS: <https://picocss.com/docs>
- This website: https://github.com/agenkit/demo-fasthtml-picocss/blob/main/docs/main.md

### 🧬 Code

- FastHTML: [https://github.com/AnswerDotAI/fasthtml](https://github.com/AnswerDotAI/fasthtml)  
(⚖️ [Apache 2](https://github.com/AnswerDotAI/fasthtml/blob/main/LICENSE) )
- Pico CSS: [https://github.com/picocss/pico](https://github.com/picocss/pico)  
(⚖️ [MIT](https://github.com/picocss/pico/blob/main/LICENSE.md) )

### 📑 Misc.

- Examples: <https://picocss.com/examples>  
  - Code: <https://github.com/picocss/examples>  
- Cursor (VSCode with *great* AI): <https://www.cursor.com/>




## Motivation & Purpose

A primary goal was to have a whole website in one plain and simple file.

- Custom JS, CSS isn't embedded in the Python file, but you could.
- Alternatively, with a SQLite db file, you can trim this massive Python code to a small fraction of its current size.
- I wanted the least obfuscated, most directly visible *everything—"Show me the f\*\*\*\*ng input!"*—such that reading the python file is all you need, so I opted for inline strings since it's all static.  
Self-evidently for learning purposes; I don't recommend such heresy.

When completed, you should be able to quickly page-search for any concept, HTML tag, CSS class, variable, etc.

- Press <kbd>Ctrl</kbd> ( <kbd>⌘</kbd> ) + <kbd>F</kbd> 

- Type `THING` to find `THING`s on the page.

- Hit <kbd>Enter</kbd> to reach the next occurrence ( `↓` )

  - <kbd>Shift</kbd> + <kbd>Enter</kbd> for previous ( `↑` )

Each HTML code snippet will be associated 1:1 to a Python FastHTML code snippet that generates it. The canonical section goes:

- Title
- \[Description\]
- HTML snippet
- FastHTML snippet

Only the last part differs from the Pico CSS website.

> [!IMPORTANT]
> FastHTML snippets are missing in v0.0.1-alpha (current latest). WIP!

Syntax highlighting is provided by [PrismJS](https://prismjs.com/), whose defaults fit better with PicoCSS than HighlightJS for me, on top of allowing inline highlighting.




## Discussion

Spoiler: I don't have any great reveal about FastHTML, as I've only skimmed the surface.  
This discussion pertains to the demo itself, and spin-off projects it might help imagine.

### Background story

*I did this naive rewrite as a learning exercise. Hadn't done much web for years; wanted to get my hands dirty with FastHTML, while diving deep enough into Pico CSS; and test CursorAI, my new editor… All at once. The latter would prove nigh in-dis-pen-sable to 'write'—or should I say* <kbd>Tab</kbd>*—those 4600-ish lines (never fear: most of them are sub-30 columns).  
It all took much less time that one would think, although I'll gladly admit I underestimated **greatly** the amount of work. lol. Silly me.* 😅


### Current status

This is a side project, and summer is always busy for me (right now I'm redeploying my entire home+SOHO infra… good times… *not*). So sadly, no ETA for completion. I intend to use it for myself eventually, and this is just a naive 0..1 version, a static PoC for something much larger that has yet to fully take form in my head.

> [!NOTE]
> **Pre-release `v0.0.1-alpha` is a test version.**  
> 
> It has *most* of the Pico CSS Docs reimplemented, but:
> 
> - still misses critical information, (e.g., CSS variables)
> - behaviors, (e.g., switching color templates)
> - and FastHTML snippets.
> - Parts of the code may be ugly.


### Features

The single-page layout was inspired by GameFaqs, whose plain-text UX is by far the most straightforward (no boilerplate) I've ever used. It's a niche use-case: you're busy with a big main thing (game, code editor, whatever) and you just need extensive docs by the side that you can quickly query for anything and get there in seconds. GameFaqs did it in plain text; we can do better with HTML, but the principle stands.

I've yet to make all proper web features.

- Some ToC doubling as navigation.
- Folding sections,
  - with collapse all/none buttons for each \[sub\]section.
- Working anchors (I'm dumb and didn't anticipate many evidently have the same name, duh.)
- Some short code form (e.g. section numbering in the Python file) for quick search
- Fix some dynamic JS things
- Search feature with nice-enough UI to quicly glance at the desired part.




### AI generation for websites

> [!NOTE] 
> This is highly speculative. I need to run tests to know if my intuition makes sense here, and prove that current SOTA can't already do it well enough.

There's (*will be*) a total of about 100 HTML:FastHTML pairs. That's a 'functionally perfect' dataset I'd like to feed some LLMs to see if it makes them great FastHTML writers and interpreters.

Two cool goals might be

- "Any webpage to FastHTML" generates FH code from web pages
  - as a browser extension perhaps, to inspect & quickly capture any component/layout → I've no idea how to do that (yet)
- "FastHTML to HTML" ← can LLMs replace the Fast 'core', doing what FastHTML does, output into a usable `.html` file?

Possible next step: add a "prompt" column → user input that produces the FastHTML snippet as output.  
This may help us reach yet another goal:

- "Prompt to FastHTML" ← in plain English: make a website

Don't get me wrong, many "no code" tools are absolute rubbish (mere prompt injection wrapping some LLM), and the few that work are incredibly narrow in actual scope, beyond the fancy GUIs. However, we can indeed narrow the problem down—e.g., aim to generate custom components, from a known set of prototypes, and simply organize them properly on the page. Even just that could reduce friction immensely from backend work to live web prototype, as informing existing components requires virtually no skill (unlike setting up all the boilerplate and wiring, however minimalist the library).

The reason why I think FastHTML lends itself impeccably well to reach great results with *less*-code LLM assistants is threefold:

- Lean and mean codebase, a simple direct mapping of HTML: as narrow a scope as it could ever get to make web things in Python.
- All batteries included are straightforward as well, with sane *great defaults* ([HTMX](https://htmx.org/), [SQLite](https://www.sqlite.org/), [Uvicorn](https://www.uvicorn.org/), [Starlette](https://www.starlette.io/), mirroring the [FastAPI](https://fastapi.tiangolo.com/) syntax…)
- Underlying "[Hypermedia](https://hypermedia.systems/)" paradigm is deemed sound and *elegant* by many great programmers. (who am I to know any better)




### Other CSS frameworks

First of all, *be my guest!* : ) The more, the merrier… 

There are great candidates — Material etc. Classes won't directly transfer, so maybe we should make a classless skeleton for all HTML tags, or abstract classes generally and then translate for each CSS at hand.
