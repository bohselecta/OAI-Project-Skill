"""README image/link integrity; visual review is separate from these checks."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.sources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'source':
            self.sources.append(attrs)


class ReadmeTests(unittest.TestCase):
    def test_embedded_images_have_alt_text_and_portable_local_sources(self):
        parser = Images()
        parser.feed((ROOT / 'README.md').read_text(encoding='utf-8'))
        self.assertTrue(parser.images)
        for image in parser.images:
            self.assertTrue(image.get('alt', '').strip())
        for relative in [i['src'] for i in parser.images] + [i['srcset'] for i in parser.sources]:
            self.assertNotIn('://', relative)
            path = (ROOT / relative).resolve()
            self.assertTrue(path.is_relative_to(ROOT))
            self.assertTrue(path.is_file(), relative)

    def test_svgs_are_self_contained_and_accessible(self):
        for path in (ROOT / 'docs/assets').glob('*.svg'):
            document = ET.parse(path).getroot()
            ns = {'svg': 'http://www.w3.org/2000/svg'}
            self.assertIsNotNone(document.find('svg:title', ns))
            self.assertIsNotNone(document.find('svg:desc', ns))
            self.assertIn('viewBox', document.attrib)
            for node in document.iter():
                self.assertNotIn(node.tag.rsplit('}', 1)[-1], {'script', 'foreignObject', 'image'})
                for name, value in node.attrib.items():
                    self.assertFalse(name.lower().startswith('on'), name)
                    if name.rsplit('}', 1)[-1] == 'href':
                        self.assertTrue(value.startswith('#'))
            self.assertNotRegex(path.read_text(), r'url\(\s*["\']?(?:https?:|data:)')

    def test_readme_local_links_and_own_anchors_resolve(self):
        text = (ROOT / 'README.md').read_text(encoding='utf-8')
        anchors = {re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
                   for heading in re.findall(r'^#{1,6} (.+)$', text, re.M)}
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in target:
                continue
            if target.startswith('#'):
                self.assertIn(target[1:], anchors)
            else:
                self.assertTrue((ROOT / target.split('#')[0]).is_file(), target)


if __name__ == '__main__':
    unittest.main()
