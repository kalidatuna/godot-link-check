import unittest
from godot_link_check.parse import parse_resource

class InlineCommentTests(unittest.TestCase):
    def test_inline_comments_do_not_hide_declarations_or_create_references(self):
        text = '[ext_resource path="res://script;name.gd" id="x"] ; header comment\nscript = ExtResource("x") ; ignored = ExtResource("ghost")\n'
        declarations, references = parse_resource(text)
        self.assertEqual([(item.resource_id, item.path) for item in declarations], [('x', 'res://script;name.gd')])
        self.assertEqual([item.resource_id for item in references], ['x'])
