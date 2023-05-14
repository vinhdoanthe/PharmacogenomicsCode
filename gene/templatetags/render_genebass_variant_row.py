from django import template

register = template.Library()


@register.inclusion_tag('genebass/genebass_variant_row.html')
def render_genebass_variant_row(genebass_variant):
    return {'genebass_variant': genebass_variant}
