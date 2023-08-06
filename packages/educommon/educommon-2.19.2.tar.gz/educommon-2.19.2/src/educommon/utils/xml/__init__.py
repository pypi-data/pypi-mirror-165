# coding: utf-8
from __future__ import absolute_import

from lxml import etree
import six

from .resolver import Resolver


def load_xml_schema(uri):
    u"""Возвращает XML-схему по указанному URI.

    При создании объекта схемы используется ``.resolver.Resolver``.

    :rtype: lxml.etree.XMLSchema
    """
    parser = etree.XMLParser(load_dtd=True)
    parser.resolvers.add(Resolver())

    schema_doc = etree.parse(uri, parser=parser)

    schema = etree.XMLSchema(schema_doc)

    return schema


def load_xml_document(document_uri, schema_uri):
    u"""Возвращает XML-документ, проверенный на соответствие XML-схеме.

    :rtype: lxml.etree._ElementTree

    :raises lxml.etree.DocumentInvalid: Если документ не соответствует
        XML-схеме.
    """
    document = etree.parse(document_uri)
    if schema_uri:
        schema = load_xml_schema(schema_uri)
        schema.assertValid(document)
    return document


def parse_xml(xml):
    u"""Возвращает дерево XML-документа.

    :param basestring xml: Текст XML-документа.
    :rtype: lxml.etree.ElementTree or None
    """
    if xml:
        if isinstance(xml, six.text_type):
            xml = xml.encode('utf-8')

        try:
            root = etree.fromstring(xml)
        except etree.XMLSyntaxError:
            result = None
        else:
            result = root.getroottree()
    else:
        result = None

    return result


def get_text(elements):
    u"""Возвращает текст первого элемента найденного
        с помощью make_xpath_query
    """
    return elements[0].text if elements else u''


def make_xpath_query(*tags):
    u"""Возвращает запрос, извлекающий элементы дерева XML-документа.

    :param tags: Имена тэгов XML-документа в порядке иерархии (без учета
        пространств имен).
    """
    result = u'/' + u''.join(
        u"/*[local-name()='{}']".format(tag)
        for tag in tags
    )

    return result
