from pptx.oxml.xmlchemy import OxmlElement


# https://github.com/scanny/python-pptx/issues/71
# https://groups.google.com/g/python-pptx/c/UTkdemIZICw
def SubElement(parent, tagname, before=(), **kwargs):
    element = OxmlElement(tagname)
    element.attrib.update(kwargs)
    if before:
        parent.insert_element_before(element, *before)
    else:
        parent.append(element)
    return element
