import copy
import unittest

from yt_dlp import MetadataParserPP

from .MetadataActions import MetadataActions


class TestMetadataActions(unittest.TestCase):
    def test_parser_interpret_str_field(self):
        actions1 = MetadataActions()
        actions1.add_interpret("SoundCloud Likes", "(?s)(?P<album>.+)")
        actions2 = MetadataActions()
        actions2.parse('"SoundCloud Likes" (?s)(?P<album>.+)')
        assert actions1.actions == actions2.actions

    def test_parser_interpret_str_field2(self):
        actions1 = MetadataActions()
        actions1.add_interpret("", "(?P<description>)")
        actions2 = MetadataActions()
        actions2.parse('"" (?P<description>)')
        assert actions1.actions == actions2.actions

    def test_parser_replace_str_field(self):
        actions1 = MetadataActions()
        actions1.add_replace("artist", "approachingnirvana", "Approaching Nirvana")
        actions2 = MetadataActions()
        actions2.parse('"artist" "approachingnirvana" "Approaching Nirvana"', "replace")
        assert actions1.actions == actions2.actions

    def test_parser_replace_str_field2(self):
        actions1 = MetadataActions()
        actions1.add_replace("artist", "A", "B")
        actions1.add_replace("uploader", "A", "B")
        actions2 = MetadataActions()
        actions2.parse("artist A B", "replace")
        actions2.parse("uploader A B", "replace")
        assert actions1.actions == actions2.actions

    def test_parser_replace_str_field3(self):
        actions1 = MetadataActions()
        actions1.add_replace("artist", "A", "B")
        actions1.add_replace("uploader", "A", "B")
        actions2 = MetadataActions()
        actions2.parse("artist A B\nuploader A B", "replace")
        assert actions1.actions == actions2.actions

    def test_parser_replace_str_field4(self):
        actions1 = MetadataActions()
        actions1.add_replace("artist,uploader", "A", "B")
        actions2 = MetadataActions()
        actions2.parse(["artist A B", "uploader A B"], "replace")
        assert actions1.actions == actions2.actions

    def test_parser_replace_list_field_csv1(self):
        actions1 = MetadataActions()
        actions1.add_replace(
            ["artist", "uploader"], "approachingnirvana", "Approaching Nirvana"
        )
        actions2 = MetadataActions()
        actions2.parse(
            '"artist,uploader" "approachingnirvana" "Approaching Nirvana"', "replace"
        )
        assert actions1.actions == actions2.actions

    def test_parser_replace_list_field_csv2(self):
        actions1 = MetadataActions()
        actions1.add_replace(
            ["artist", "uploader"], "approachingnirvana", "Approaching Nirvana"
        )
        actions2 = MetadataActions()
        actions2.parse(
            'artist,uploader approachingnirvana "Approaching Nirvana"', "replace"
        )
        assert actions1.actions == actions2.actions

    def test_parser_multiple(self):
        actions1 = MetadataActions()
        actions1.add_interpret("SoundCloud Likes", "(?s)(?P<album>.+)")
        actions1.add_interpret("Various Artists", "(?s)(?P<album_artist>.+)")
        actions1.add_interpret("", "(?P<description>)")
        actions1.add_replace(
            ["artist", "uploader"], "approachingnirvana", "Approaching Nirvana"
        )
        actions2 = MetadataActions()
        actions2.parse(
            '"SoundCloud Likes" (?s)(?P<album>.+)\n'
            + '"Various Artists" (?s)(?P<album_artist>.+)\n'
            + '"" (?P<description>)'
        )
        actions2.parse(
            'artist,uploader approachingnirvana "Approaching Nirvana"', "replace"
        )
        assert actions1.actions == actions2.actions

    def test_copy(self):
        actions1 = MetadataActions()
        actions1.add_interpret("SoundCloud Likes", "(?s)(?P<album>.+)")

        for f in actions1.actions:
            action, *args = f
            assert action in MetadataParserPP.Actions

        actions1_copy = copy.copy(actions1)

        for f in actions1_copy.actions:
            action, *args = f
            assert action in MetadataParserPP.Actions

    def test_deepcopy(self):
        actions1 = MetadataActions()
        actions1.add_interpret("SoundCloud Likes", "(?s)(?P<album>.+)")

        for f in actions1.actions:
            action, *args = f
            assert action in MetadataParserPP.Actions

        actions1_copy = copy.deepcopy(actions1)

        for f in actions1_copy.actions:
            action, *args = f
            assert action in MetadataParserPP.Actions


if __name__ == "__main__":
    unittest.main()
