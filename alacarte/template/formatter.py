# encoding: utf-8

from __future__ import with_statement

from string import Formatter

from alacarte.template.engine import Engine


__all__ = ['FormatterEngine']

renderer = Formatter()



class FormatterEngine(Engine):
    """A basic string.Formatter string templating language.

    This templating engine is associated with the '.formatter' filename extension
    and defaults to the 'text/plain' mimetype.

    See:

        http://www.python.org/doc/2.6/library/string.html#string-formatting

    Simple (string-based) usage:

        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('formatter:', dict(name="world"), string="Hello {name}!")
        ('text/plain', 'Hello world!')

    File-based usage:

        >>> from alacarte.core import Engines
        >>> render = Engines()
        >>> render('formatter:./tests/templates/hello3.txt', dict(name="world"))
        ('text/plain', 'Hello world!')

    """

    mapping = {
            'formatter': 'text/plain',
            None: 'text/plain'
        }

    def render(self, template, data, **options):
        """Implemented by a sub-class, this returns the 2-tuple of mimetype and unicode content."""

        return self.mapping[None], renderer.vformat(
                template,
                data if not isinstance(data, dict) else tuple(),
                data if isinstance(data, dict) else dict()
            )
