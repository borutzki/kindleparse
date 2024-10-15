import pytest
from src.kindle_parser import (
    parse_clipping,
    parse_my_clippings,
    sort_clippings,
    dump_book_to_markdown,
)
from src.clipping import Clipping, Book
from dataclasses import asdict


@pytest.mark.parametrize(
    "clipping, expected",
    [
        (
            Clipping(
                book=Book(author="Antoine de Saint-Exupery", title="Mały Książę"),
                clipping_type="Highlight",
                timestamp="Tuesday, 5 May 2020 23:26:59",
                content="Wszyscy dorośli byli kiedyś dziećmi.",
                location=(6, 6),
                page=None,
            ),
            "> Wszyscy dorośli byli kiedyś dziećmi.\n\n",
        ),
        (
            Clipping(
                book=Book(author="Marek Aureliusz", title="Rozmyślania"),
                clipping_type="Note",
                timestamp="Thursday, 28 January 2021 15:26:14",
                content="Swietna mantra",
                location=(736, 736),
                page=48,
            ),
            "- Swietna mantra\n\n",
        ),
    ],
)
def test_clipping_to_string(clipping, expected):
    assert str(clipping) == expected


@pytest.mark.parametrize(
    "text, expectation",
    [
        (
            """Mały Książę (Antoine de Saint-Exupery)
- Your Highlight at location 6-6 | Added on Tuesday, 5 May 2020 23:26:59

Wszyscy dorośli byli kiedyś dziećmi.""",
            Clipping(
                book=Book(author="Antoine de Saint-Exupery", title="Mały Książę"),
                clipping_type="Highlight",
                timestamp="Tuesday, 5 May 2020 23:26:59",
                content="Wszyscy dorośli byli kiedyś dziećmi.",
                location=(6, 6),
                page=None,
            ),
        ),
        (
            """Deep Work (Cal Newport)
- Your Highlight on page 128 | location 1950-1956 | Added on Monday, 10 August 2020 17:15:55

To simplify matters, when scheduling Internet use after work, you can allow time-sensitive communication into your offline blocks (e.g., texting with a friend to agree on where you’ll meet for dinner), as well as time-sensitive information retrieval (e.g., looking up the location of the restaurant on your phone). Outside of these pragmatic exceptions, however, when in an offline block, put your phone away, ignore texts, and refrain from Internet usage. As in the workplace variation of this strategy, if the Internet plays a large and important role in your evening entertainment, that’s fine: Schedule lots of long Internet blocks. The key here isn’t to avoid or even to reduce the total amount of time you spend engaging in distracting behavior, but is instead to give yourself plenty of opportunities throughout your evening to resist switching to these distractions at the slightest hint of boredom.
""",
            Clipping(
                book=Book(author="Cal Newport", title="Deep Work"),
                clipping_type="Highlight",
                timestamp="Monday, 10 August 2020 17:15:55",
                content="To simplify matters, when scheduling Internet use after work, you can allow time-sensitive communication into your offline blocks (e.g., texting with a friend to agree on where you’ll meet for dinner), as well as time-sensitive information retrieval (e.g., looking up the location of the restaurant on your phone). Outside of these pragmatic exceptions, however, when in an offline block, put your phone away, ignore texts, and refrain from Internet usage. As in the workplace variation of this strategy, if the Internet plays a large and important role in your evening entertainment, that’s fine: Schedule lots of long Internet blocks. The key here isn’t to avoid or even to reduce the total amount of time you spend engaging in distracting behavior, but is instead to give yourself plenty of opportunities throughout your evening to resist switching to these distractions at the slightest hint of boredom.",
                location=(1950, 1956),
                page=128,
            ),
        ),
        (
            """Rozmyślania (Marek Aureliusz)
- Your Note on page 48 | location 736 | Added on Thursday, 28 January 2021 15:26:14

Swietna mantra
""",
            Clipping(
                book=Book(author="Marek Aureliusz", title="Rozmyślania"),
                clipping_type="Note",
                timestamp="Thursday, 28 January 2021 15:26:14",
                content="Swietna mantra",
                location=(736, 736),
                page=48,
            ),
        ),
        (
            """Rewolucja energetyczna. Ale po co? (Marcin Popkiewicz)
- Your Highlight on page 519 | location 7945-7949 | Added on Saturday, 19 December 2020 12:57:21

Chcę gorąco podziękować osobom, którym zawdzięczam zwrócenie mojej uwagi na kwestie granic wzrostu, działania systemu finansowego i gospodarczego, problemy zasobów, klimatu i środowiska, a także działania systemu energetycznego – obecnego i kształtującego się. Tylko niewielka część przemyśleń zawartych w tej książce jest w pełni oryginalna, większość danych, przykładów i argumentów pochodzi od osób i organizacji od lat zajmujących się tą tematyką. Olbrzymia ilość wiedzy i materiałów trafiła też do mnie za pośrednictwem wielu wspaniałych ludzi.
""",
            Clipping(
                book=Book(
                    author="Marcin Popkiewicz",
                    title="Rewolucja energetyczna. Ale po co?",
                ),
                clipping_type="Highlight",
                timestamp="Saturday, 19 December 2020 12:57:21",
                content="Chcę gorąco podziękować osobom, którym zawdzięczam zwrócenie mojej uwagi na kwestie granic wzrostu, działania systemu finansowego i gospodarczego, problemy zasobów, klimatu i środowiska, a także działania systemu energetycznego – obecnego i kształtującego się. Tylko niewielka część przemyśleń zawartych w tej książce jest w pełni oryginalna, większość danych, przykładów i argumentów pochodzi od osób i organizacji od lat zajmujących się tą tematyką. Olbrzymia ilość wiedzy i materiałów trafiła też do mnie za pośrednictwem wielu wspaniałych ludzi.",
                location=(7945, 7949),
                page=519,
            ),
        ),
        (
            """Dziennik (Anne Frank)
- Your Highlight on page 177 | location 2710-2717 | Added on Thursday, 4 February 2021 23:57:17

Oficyna: Myśli pan, że Niemcy są zbyt szlachetni lub zbyt filantropijni, żeby zrobić coś takiego? Oni myślą: jeżeli my musimy zginąć, to zginą też wszyscy ludzie, którzy znajdują się w zasięgu naszej władzy. Jan: Proszę mi nie opowiadać, nie wierzę w to. Oficyna: To jest wciąż ta sama śpiewka, nikt nie chce widzieć niebezpieczeństwa, dopóki go nie poczuje na własnej skórze. Jan: Państwo nigdy nie widzą niczego pozytywnego. Przecież państwo też to tylko zakładają. Oficyna: Bo sami to wszystko przeżyliśmy, najpierw w Niemczech, a teraz tutaj. A co się dzieje w Rosji? Jan: Proszę na razie nie brać Żydów pod uwagę, sądzę, że nikt nie wie, co się w Rosji dzieje. Anglicy i Rosjanie przesadzają w celach propagandowych podobnie jak Niemcy.

""",
            Clipping(
                book=Book(
                    author="Anne Frank",
                    title="Dziennik",
                ),
                clipping_type="Highlight",
                timestamp="Thursday, 4 February 2021 23:57:17",
                content="Oficyna: Myśli pan, że Niemcy są zbyt szlachetni lub zbyt filantropijni, żeby zrobić coś takiego? Oni myślą: jeżeli my musimy zginąć, to zginą też wszyscy ludzie, którzy znajdują się w zasięgu naszej władzy. Jan: Proszę mi nie opowiadać, nie wierzę w to. Oficyna: To jest wciąż ta sama śpiewka, nikt nie chce widzieć niebezpieczeństwa, dopóki go nie poczuje na własnej skórze. Jan: Państwo nigdy nie widzą niczego pozytywnego. Przecież państwo też to tylko zakładają. Oficyna: Bo sami to wszystko przeżyliśmy, najpierw w Niemczech, a teraz tutaj. A co się dzieje w Rosji? Jan: Proszę na razie nie brać Żydów pod uwagę, sądzę, że nikt nie wie, co się w Rosji dzieje. Anglicy i Rosjanie przesadzają w celach propagandowych podobnie jak Niemcy.",
                location=(2710, 2717),
                page=177,
            ),
        ),
        (
            """Boating Pollution Economics & Impacts  
- Your Highlight on page 1-1 | Added on Friday, 30 October 2020 14:53:27

Can preventing pollution save money? young. 12,17 This page will answer your questions on the
""",
            Clipping(
                book=Book(
                    author="",
                    title="Boating Pollution Economics & Impacts",
                ),
                clipping_type="Highlight",
                timestamp="Friday, 30 October 2020 14:53:27",
                content="Can preventing pollution save money? young. 12,17 This page will answer your questions on the",
                location=(None, None),
                page=1,
            ),
        ),
        (
            """Market barriers towards electric boats  
- Your Note on page 1 | Added on Friday, 30 October 2020 15:01:17

Silniki spalinowe lodzi zuzywaja duzo paliwa i odpowiedzia na to moga byc elktryki
""",
            Clipping(
                book=Book(
                    author="",
                    title="Market barriers towards electric boats",
                ),
                clipping_type="Note",
                timestamp="Friday, 30 October 2020 15:01:17",
                content="Silniki spalinowe lodzi zuzywaja duzo paliwa i odpowiedzia na to moga byc elktryki",
                location=(None, None),
                page=1,
            ),
        ),
    ],
)
def test_parse_template(text, expectation):
    assert asdict(parse_clipping(text)) == asdict(expectation)


def test_parse_my_clippings():
    result = [
        clipping
        for clipping in parse_my_clippings("tests/resources/My Clippings - example.txt")
    ]
    expected = [
        Clipping(
            book=Book(author="Anne Frank", title="Dziennik"),
            clipping_type="Note",
            timestamp="Wednesday, 3 February 2021 23:00:55",
            content="Ciekawe jakie to standardy wymusily te karteczki na zywnosc",
            location=(1194, 1194),
            page=78,
        ),
        Clipping(
            book=Book(author="Anne Frank", title="Dziennik"),
            clipping_type="Highlight",
            timestamp="Wednesday, 3 February 2021 23:04:43",
            content="A my, my mamy się dobrze, tak, lepiej niż miliony innych. Jesteśmy bezpieczni i spokojni i przejadamy, jak to się mówi, swoje pieniądze. Jesteśmy tak egoistyczni, że rozmawiamy o „po wojnie”, cieszymy się z nowych ubrań i butów, podczas gdy powinniśmy oszczędzać każdego centa, żeby pomóc po wojnie tym innym ludziom, by ratować to, co jeszcze będzie do uratowania.",
            location=(1224, 1227),
            page=80,
        ),
        Clipping(
            book=Book(author="Anne Frank", title="Dziennik"),
            clipping_type="Note",
            timestamp="Wednesday, 3 February 2021 23:05:01",
            content="Absolutne zaprzeczenie stereotypu o zydach",
            location=(1226, 1226),
            page=80,
        ),
    ]
    for result_clipping, expected_clipping in zip(result, expected):
        assert asdict(result_clipping) == asdict(expected_clipping)


def test_sort_clippings():
    clippings = [
        Clipping(
            book=Book(author="Anne Frank", title="Dziennik"),
            clipping_type="Note",
            timestamp="Wednesday, 3 February 2021 23:00:55",
            content="Ciekawe jakie to standardy wymusily te karteczki na zywnosc",
            location=(1194, 1194),
            page=78,
        ),
        Clipping(
            book=Book(author="Anne Frank", title="Dziennik"),
            clipping_type="Highlight",
            timestamp="Wednesday, 3 February 2021 23:04:43",
            content="A my, my mamy się dobrze, tak, lepiej niż miliony innych. Jesteśmy bezpieczni i spokojni i przejadamy, jak to się mówi, swoje pieniądze. Jesteśmy tak egoistyczni, że rozmawiamy o „po wojnie”, cieszymy się z nowych ubrań i butów, podczas gdy powinniśmy oszczędzać każdego centa, żeby pomóc po wojnie tym innym ludziom, by ratować to, co jeszcze będzie do uratowania.",
            location=(1224, 1227),
            page=80,
        ),
        Clipping(
            book=Book(author="Anne Frank", title="Dziennik"),
            clipping_type="Note",
            timestamp="Wednesday, 3 February 2021 23:05:01",
            content="Absolutne zaprzeczenie stereotypu o zydach",
            location=(1226, 1226),
            page=80,
        ),
        Clipping(
            book=Book(author="Marek Aureliusz", title="Rozmyślania"),
            clipping_type="Note",
            timestamp="Thursday, 28 January 2021 15:26:14",
            content="Swietna mantra",
            location=(736, 736),
            page=48,
        ),
    ]

    assert sort_clippings(clippings) == {
        Book(author="Anne Frank", title="Dziennik"): [
            Clipping(
                book=Book(author="Anne Frank", title="Dziennik"),
                clipping_type="Note",
                timestamp="Wednesday, 3 February 2021 23:00:55",
                content="Ciekawe jakie to standardy wymusily te karteczki na zywnosc",
                location=(1194, 1194),
                page=78,
            ),
            Clipping(
                book=Book(author="Anne Frank", title="Dziennik"),
                clipping_type="Highlight",
                timestamp="Wednesday, 3 February 2021 23:04:43",
                content="A my, my mamy się dobrze, tak, lepiej niż miliony innych. Jesteśmy bezpieczni i spokojni i przejadamy, jak to się mówi, swoje pieniądze. Jesteśmy tak egoistyczni, że rozmawiamy o „po wojnie”, cieszymy się z nowych ubrań i butów, podczas gdy powinniśmy oszczędzać każdego centa, żeby pomóc po wojnie tym innym ludziom, by ratować to, co jeszcze będzie do uratowania.",
                location=(1224, 1227),
                page=80,
            ),
            Clipping(
                book=Book(author="Anne Frank", title="Dziennik"),
                clipping_type="Note",
                timestamp="Wednesday, 3 February 2021 23:05:01",
                content="Absolutne zaprzeczenie stereotypu o zydach",
                location=(1226, 1226),
                page=80,
            ),
        ],
        Book(author="Marek Aureliusz", title="Rozmyślania"): [
            Clipping(
                book=Book(author="Marek Aureliusz", title="Rozmyślania"),
                clipping_type="Note",
                timestamp="Thursday, 28 January 2021 15:26:14",
                content="Swietna mantra",
                location=(736, 736),
                page=48,
            ),
        ],
    }


def test_dump_book_to_markdown_file_list(tmp_path):
    mapping = {
        Book(author="Anne Frank", title="Dziennik"): [
            Clipping(
                book=Book(author="Anne Frank", title="Dziennik"),
                clipping_type="Note",
                timestamp="Wednesday, 3 February 2021 23:00:55",
                content="Ciekawe jakie to standardy wymusily te karteczki na zywnosc",
                location=(1194, 1194),
                page=78,
            ),
            Clipping(
                book=Book(author="Anne Frank", title="Dziennik"),
                clipping_type="Highlight",
                timestamp="Wednesday, 3 February 2021 23:04:43",
                content="A my, my mamy się dobrze, tak, lepiej niż miliony innych. Jesteśmy bezpieczni i spokojni i przejadamy, jak to się mówi, swoje pieniądze. Jesteśmy tak egoistyczni, że rozmawiamy o „po wojnie”, cieszymy się z nowych ubrań i butów, podczas gdy powinniśmy oszczędzać każdego centa, żeby pomóc po wojnie tym innym ludziom, by ratować to, co jeszcze będzie do uratowania.",
                location=(1224, 1227),
                page=80,
            ),
            Clipping(
                book=Book(author="Anne Frank", title="Dziennik"),
                clipping_type="Note",
                timestamp="Wednesday, 3 February 2021 23:05:01",
                content="Absolutne zaprzeczenie stereotypu o zydach",
                location=(1226, 1226),
                page=80,
            ),
        ],
        Book(author="Marek Aureliusz", title="Rozmyślania"): [
            Clipping(
                book=Book(author="Marek Aureliusz", title="Rozmyślania"),
                clipping_type="Note",
                timestamp="Thursday, 28 January 2021 15:26:14",
                content="Swietna mantra",
                location=(736, 736),
                page=48,
            ),
        ],
        Book(author="", title="Boating Pollution Economics & Impacts"): [
            Clipping(
                book=Book(
                    author="",
                    title="Boating Pollution Economics & Impacts",
                ),
                clipping_type="Highlight",
                timestamp="Friday, 30 October 2020 14:53:27",
                content="Can preventing pollution save money? young. 12,17 This page will answer your questions on the",
                location=(None, None),
                page=1,
            ),
        ],
    }
    dump_book_to_markdown(mapping, tmp_path)
    files = [str(f.relative_to(tmp_path)) for f in tmp_path.iterdir() if f.is_file()]
    print(files)
    assert (
        files.sort()
        == [
            "Anne Frank - Dziennik.md",
            "Marek Aureliusz - Rozmyślania.md",
            "Boating Pollution Economics & Impacts.md",
        ].sort()
    )


# TODO: Add test case for verification of created file's content
