# -*- coding: utf-8 -*-
"""
@author: Federico Cerchiari <federicocerchiari@gmail.com>
"""
import unittest
from tempy import T
from tempy.tags import P


class TestTag(unittest.TestCase):

    def test_markdown_return_empty(self):
        t = ''
        r = T.from_markdown(t)
        self.assertEqual(r, [])
        self.assertIsInstance(r, list)

    def test_markdown_return_P_wrap(self):
        t = 'Lorem ipsum'
        r = T.from_markdown(t)
        self.assertIsInstance(r[0], P)

    def test_heading(self):
        t = """Heading
            ======="""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<h1>Heading</h1>')

    def test_sub_heading(self):
        t = """Sub-heading
 -----------"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<h2>Sub-heading</h2>')

    def test_h3_heading(self):
        t = """### H3 heading"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<h3>H3 heading</h3>')

    def test_line_break(self):
        t = """Text in a paragraph that ends with two spaces  
other text"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p>Text in a paragraph that ends with two spaces<br/>other text</p>')

    def test_italic(self):
        t = """*italic*"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><em>italic</em></p>')

    def test_bold(self):
        t = """**bold**"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><strong>bold</strong></p>')

    def test_code_inline(self):
        t = """`monospace`"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><code>monospace</code></p>')

    def test_strikethrough(self):
        t = """~~strikethrough~~"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><del>strikethrough</del></p>')

    def test_link(self):
        t = """A [link](https://hrabal.github.io/TemPy/)."""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p>A <a href="https://hrabal.github.io/TemPy/">link</a>.</p>')

    def test_list(self):
        t = """Important list:
 
   * foo
   * bar
   * baz"""
        r = T.from_markdown(t)
        self.assertEqual(''.join(t.render() for t in r), '<p>Important list:</p><ul><li>foo</li><li>bar</li><li>baz</li></ul>')

    def test_list_numbered(self):
        t = """Important Numbered list:
 
   1. foo
   2. bar
   3. baz"""
        r = T.from_markdown(t)
        self.assertEqual(''.join(t.render() for t in r), '<p>Important Numbered list:</p><ol><li>foo</li><li>bar</li><li>baz</li></ol>')

    def test_markdown_escape(self):
        t = """&"""
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p>&amp;</p>')

    def test_code_block(self):
        t = """```
some code here
```
        """
        r = T.from_markdown(t)
        self.assertEqual(''.join(t.render() for t in r), '<pre><code>some code here</code></pre>')

    def test_code_block_lang(self):
        t = """```python
some code here
```
        """
        r = T.from_markdown(t)
        self.assertEqual(''.join(t.render() for t in r), '<pre><code class="lang-python">some code here</code></pre>')

    def test_quote(self):
        t = "> this is a quote"
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<blockquote><p>this is a quote</p></blockquote>')

    def test_hr(self):
        t = "---"
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<hr/>')

    def test_table_styled(self):
        t = """Test markdown table

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |"""
        r = T.from_markdown(t)
        self.assertEqual(''.join(t.render() for t in r), '<p>Test markdown table</p><table><thead><tr><th>Tables</th><th style="text-align: center;">Are</th><th style="text-align: right;">Cool</th></tr></thead><tbody><tr><td>col 3 is</td><td style="text-align: center;">right-aligned</td><td style="text-align: right;">$1600</td></tr><tr><td>col 2 is</td><td style="text-align: center;">centered</td><td style="text-align: right;">$12</td></tr><tr><td>zebra stripes</td><td style="text-align: center;">are neat</td><td style="text-align: right;">$1</td></tr></tbody></table>')

    def test_table_non_styled(self):
        t = """Test markdown table

| Tables        | Are           | Cool  |
| ------------- | ------------- | ----- |
| col 3 is      | foo           | $1600 |
| col 2 is      | bar.          |   $12 |
| zebra stripes | baz.          |    $1 |"""
        r = T.from_markdown(t)
        self.assertEqual(''.join(t.render() for t in r), '<p>Test markdown table</p><table><thead><tr><th>Tables</th><th>Are</th><th>Cool</th></tr></thead><tbody><tr><td>col 3 is</td><td>foo</td><td>$1600</td></tr><tr><td>col 2 is</td><td>bar.</td><td>$12</td></tr><tr><td>zebra stripes</td><td>baz.</td><td>$1</td></tr></tbody></table>')

    def test_table_non_styled_non_pretty(self):
        t = """Test markdown table non pretty

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3"""
        r = T.from_markdown(t)
        self.assertEqual(''.join(t.render() for t in r), '<p>Test markdown table non pretty</p><table><thead><tr><th>Markdown</th><th>Less</th><th>Pretty</th></tr></thead><tbody><tr><td><em>Still</em></td><td><code>renders</code></td><td><strong>nicely</strong></td></tr><tr><td>1</td><td>2</td><td>3</td></tr></tbody></table>')

    def test_autolink(self):
        t = "https://hrabal.github.io/TemPy"
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><a href="https://hrabal.github.io/TemPy">https://hrabal.github.io/TemPy</a></p>')

    def test_email_link(self):
        t = "<hey@you.com>"
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><a href="mailto:hey@you.com">hey@you.com</a></p>')

    def test_img(self):
        t = '![alt text](foo.png "Title text")'
        r = T.from_markdown(t)
        self.assertEqual(r[0].render(), '<p><img src="foo.png" alt="alt text" title="Title text"/></p>')        