from django.template import (
    Node, Library, Template, TemplateSyntaxError, Variable
)
from django.template.loader_tags import (
    BLOCK_CONTEXT_KEY, BlockContext, BlockNode, do_include
)
from django.utils import six

register = Library()


class EmbedNode(Node):
    must_be_first = False
    context_key = 'embeds_context'

    def __init__(self, nodes, include_node):
        self.include_node = include_node
        self.embed_name = include_node.template
        self.blocks = {n.name: n for n in nodes.get_nodes_by_type(BlockNode)}

    # This function derives from django.template.base.ExtendsNode.get_parent()
    def get_embed_template(self, context):
        templ = self.embed_name.resolve(context)
        if not templ:
            error_msg = "Invalid template name in 'embeds' tag: %r." % templ
            if self.embed_name.filters or\
                    isinstance(self.embed_name.var, Variable):
                error_msg += " Got this from the '%s' variable." %\
                    self.embed_name.token
            raise TemplateSyntaxError(error_msg)
        if isinstance(templ, Template):
            # templ is a django.template.Template
            return templ
        if isinstance(getattr(templ, 'template', None), Template):
            # templ is a django.template.backends.django.Template
            return templ.template
        return context.template.engine.get_template(templ)

    def render(self, context):
        compiled_template = self.get_embed_template(context)

        old_blocks = None
        if BLOCK_CONTEXT_KEY in context.render_context:
            old_blocks = context.render_context[BLOCK_CONTEXT_KEY].blocks

        context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()
        context.render_context[BLOCK_CONTEXT_KEY].add_blocks(self.blocks)

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
                return compiled_template._render(context.new(values))
            with context.push(**values):
                return compiled_template._render(context)
        finally:
            # We must forget about the just introduced blocks
            if old_blocks:
                context.render_context[BLOCK_CONTEXT_KEY].blocks = old_blocks
            else:
                del context.render_context[BLOCK_CONTEXT_KEY]


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
