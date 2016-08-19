from django.test import TestCase
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string


class EmbedTest(TestCase):

    def test_no_overrides(self):
        self.assertHTMLEqual(
            render_to_string('embed_empty.html'),
            "included 1 2"
        )

    def test_full(self):
        self.assertHTMLEqual(
            render_to_string('embed_full.html'),
            "included one two"
        )

    def test_with(self):
        self.assertHTMLEqual(
            render_to_string('embed_with.html'),
            "includedvar 1 2"
        )

    def test_partial(self):
        self.assertHTMLEqual(
            render_to_string('embed_partial.html'),
            "included one 2"
        )

    def test_multiple_static(self):
        self.assertHTMLEqual(
            render_to_string('embed_multiple_static.html'),
            "included one two\n"
            "included one 2\n"
            "includedvar one 2"
        )

    def test_repeated_blocks(self):
        self.assertHTMLEqual(
            render_to_string('embed_repeated_after.html'),
            "I\n"
            "included one 2"
            )
        self.assertHTMLEqual(
            render_to_string('embed_repeated_before.html'),
            "included one 2\n"
            "I"
            )

    def test_duplicate_repeated_blocks(self):
        with self.assertRaisesMessage(
                TemplateSyntaxError,
                "'block' tag with name 'one' appears more than once"):
            render_to_string('embed_repeated_interleaved.html'),

    def test_extend_and_embed(self):
        self.assertHTMLEqual(
            render_to_string('extend_and_embed.html'),
            "included one two\n"
            "included one 2\n"
            "includedvar one 2"
        )

    def test_nested(self):
        self.assertHTMLEqual(
            render_to_string('embed_nested.html'),
            "included\n"
            "included I II\n"
            "two"
        )
