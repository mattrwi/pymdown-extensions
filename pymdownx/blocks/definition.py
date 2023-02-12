"""Definition."""
import xml.etree.ElementTree as etree
from .block import Block


class Definition(Block):
    """
    Definition.

    Converts non `ul`, `ol` blocks (ideally `p` tags) into `dt`
    and will convert first level `li` elements of `ul` and `ol`
    elements to `dd` tags. When done, the `ul`, and `ol` elements
    will be removed.
    """

    NAME = 'define'

    def on_create(self, parent):
        """Create the element."""

        return etree.SubElement(parent, 'dl')

    def on_end(self, block):
        """Convert non list items to details."""

        remove = []
        offset = 0
        for i, child in enumerate(list(block)):
            if child.tag.lower() in ('dt', 'dd'):
                continue

            elif child.tag.lower() not in ('ul', 'ol'):
                if child.tag.lower() == 'p':
                    child.tag = 'dt'
                else:
                    dt = etree.Element('dt')
                    dt.append(child)
                    block.insert(i + offset, dt)
                    block.remove(child)
            else:
                for li in list(child):
                    offset += 1
                    li.tag = 'dd'
                    block.insert(i + offset, li)
                    child.remove(li)
                remove.append(child)

        for el in remove:
            block.remove(el)
