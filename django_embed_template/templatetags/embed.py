from django.template import Library, Template
from django.template.base import TextNode
from django.template.loader_tags import (
    BLOCK_CONTEXT_KEY, do_include, ExtendsNode, BlockContext, BlockNode, Node
)
from django.utils import six

import copy

register = Library()


class EmbedNode(Node):
    must_be_first = False
    context_key = 'embeds_context'

    def __init__(self, nodelist, include_node, template_dirs=None):
        self.include_node = include_node
        self.extends_node = ExtendsNode(nodelist, include_node.template,
                                        template_dirs)

    @property
    def parent_name(self):
        return self.extends_node.parent_name

    # This function derives from django.template.base.ExtendsNode.get_parent()
    def get_parent(self, context):
        parent = self.parent_name.resolve(context)
        if not parent:
            error_msg = "Invalid template name in 'embeds' tag: %r." % parent
            if self.parent_name.filters or\
                    isinstance(self.parent_name.var, Variable):
                error_msg += " Got this from the '%s' variable." %\
                    self.parent_name.token
            raise TemplateSyntaxError(error_msg)
        if isinstance(parent, Template):
            # parent is a django.template.Template
            return parent
        if isinstance(getattr(parent, 'template', None), Template):
            # parent is a django.template.backends.django.Template
            return parent.template
        return ExtendsNode.find_template(self, parent, context)

    def render(self, context):
        old_embed_context = copy.copy(context.render_context
                                             .get(self.context_key, []))

        # The next lines derive from django.template.base.ExtendsNode.render()
        compiled_parent = self.get_parent(context)

        if BLOCK_CONTEXT_KEY not in context.render_context:
            context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()
        block_context = context.render_context[BLOCK_CONTEXT_KEY]

        old_blocks = block_context.blocks.copy()

        # Add the block nodes from this node to the block context
        block_context.add_blocks(self.extends_node.blocks)

        # If this block's parent doesn't have an extends node it is the root,
        # and its block nodes also need to be added to the block context.
        for node in compiled_parent.nodelist:
            # The ExtendsNode has to be the first non-text node.
            if not isinstance(node, TextNode):
                if not isinstance(node, ExtendsNode):
                    blocks = {n.name: n for n in
                              compiled_parent.nodelist
                                             .get_nodes_by_type(BlockNode)}
                    block_context.add_blocks(blocks)
                break

        # The next lines derive from django.template.base.IncludeNode.render()
        values = {
            name: var.resolve(context)
            for name, var in six.iteritems(self.include_node.extra_context)
        }

        # This combines IncludeNode.render() and ExtendsNode.render()
        # Call Template._render explicitly so the parser context stays
        # the same.
        try:
            if self.include_node.isolated_context:
                return compiled_parent._render(context.new(values))
            with context.push(**values):
                return compiled_parent._render(context)
        finally:
            # We must forget about the just introduced blocks
            context.render_context[BLOCK_CONTEXT_KEY].blocks = old_blocks
            context.render_context[self.context_key] = old_embed_context


@register.tag('embed')
def do_embed(parser, token):
    include_node = do_include(parser, token)

    # Briefly forget about previously seen blocks, to ignore duplicates
    try:
        old_loaded_blocks = parser.__loaded_blocks
    except AttributeError:  # parser.__loaded_blocks isn't a list yet
        old_loaded_blocks = []
    parser.__loaded_blocks = []

    nodelist = parser.parse(('endembed',))
    endembed = parser.next_token()
    if endembed.contents != 'endembed':
        parser.invalid_block_tag(endembed, 'endembed', 'endembed')

    parser.__loaded_blocks = old_loaded_blocks

    return EmbedNode(nodelist, include_node)
