import unittest
from pathlib import Path
from html.parser import HTMLParser

DASHBOARD = Path(__file__).resolve().parents[1] / "webui" / "bmad-dashboard.html"


class TagCounter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.open_divs = 0
        self.close_divs = 0
        self.open_templates = 0
        self.close_templates = 0
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            self.open_divs += 1
        elif tag == "template":
            self.open_templates += 1

    def handle_endtag(self, tag):
        if tag == "div":
            self.close_divs += 1
        elif tag == "template":
            self.close_templates += 1

    def error(self, message):
        self.errors.append(message)


class TestBmadDashboardHTML(unittest.TestCase):
    # A4: bmad-dashboard.html has no stray closing tags

    def test_div_tags_balanced(self):
        content = DASHBOARD.read_text()
        counter = TagCounter()
        counter.feed(content)
        self.assertEqual(counter.open_divs, counter.close_divs,
                         f"Unbalanced divs: {counter.open_divs} open vs {counter.close_divs} close")

    def test_template_tags_balanced(self):
        content = DASHBOARD.read_text()
        counter = TagCounter()
        counter.feed(content)
        self.assertEqual(counter.open_templates, counter.close_templates,
                         f"Unbalanced templates: {counter.open_templates} open vs {counter.close_templates} close")


if __name__ == "__main__":
    unittest.main()
