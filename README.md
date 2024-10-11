# kindleparse

The aim of this tool is to simply convert `My Clippings` file from Amazon Kindle into multiple `.md` files (usable in e.g. Obsidian), on a single book basis.

This script aims to solve a single problem. When highlights and notes are created on Kindle for books that are side-loaded (not bought from Amazon Kindle Store), extracting them to usable format might be time consuming. There exist some paid services which do that, but the task seems so simple that it makes no sense to pay for them.

Hence, this simple script.

## Assumptions

This project is purely personal, but if you find it useful - feel free to fork or develop.

The aim here is to avoid external dependencies as long as possible, to not bloat this tool
that definitely should serve a single purpose.

Exception: testing and linting. But Ruff and PyTest won't be included in setup file, anyway.

## Example

Given file containing the following input in `My Clippings`:

```text
Mały Książę (Antoine de Saint-Exupery)
- Your Highlight at location 6-6 | Added on Tuesday, 5 May 2020 23:26:59

Wszyscy dorośli byli kiedyś dziećmi.
==========
﻿Mały Książę (Antoine de Saint-Exupery)
- Your Highlight at location 6-7 | Added on Tuesday, 5 May 2020 23:27:24

Wszyscy dorośli byli kiedyś dziećmi. Choć niewielu z nich o tym pamięta.
==========
﻿Mały Książę (Antoine de Saint-Exupery)
- Your Highlight at location 86-86 | Added on Tuesday, 5 May 2020 23:38:07

Idąc prosto przed siebie nie można zajść daleko ...
==========
```

When `kindleparse` is used:

```bash
kindleparse "My Clippings.txt" target_directory
```

Then new markdown file is created, based on title and content of clippings:

```markdown
# Antoine de Saint-Exupery - Mały Książę

First note: Tuesday, 5 May 2020 23:26:59
Last note: Tuesday, 5 May 2020 23:26:59

> Wszyscy dorośli byli kiedyś dziećmi.

> Wszyscy dorośli byli kiedyś dziećmi. Choć niewielu z nich o tym pamięta.

> Idąc prosto przed siebie nie można zajść daleko ...
```

With `>` (blockquotes) marking highlights and `-` (bullet points) marking notes, each separated with a line break, and sorted with `location` or `Page` (depending on which is available, with `location` as a primary value).

## Basic features

- [x] creation of markdown file for each book, with highlights and notes marked from the file
- [x] simple command line interface
- [x] conversion from Kindle's `.txt` format to a `.md` file compatible with Obsidian.

## Features to include later

- [ ] support for templates of clippings
- [ ] support for other readers (currently, only `Kindle Paperwhite 4` is assumed in code)
- [ ] translations (for predefined templates)
- [ ] ability to update existing files instead of only creating new ones, using e.g. database
- [ ] improvements in performance, e.g. with usage of generators
