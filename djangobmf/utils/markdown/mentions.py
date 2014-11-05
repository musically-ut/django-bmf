import markdown


# Global Vars
MENTION_RE = '((\s|^)@(\w+)(\s|$))'


class MentionPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):  # noqa
        text = m.group(4)
        el = markdown.util.etree.Element("span")
        el.set('class', 'label label-primary')
        el.text = markdown.util.AtomicString(text)
        return el


class MentionExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):  # noqa
        md.inlinePatterns['mention'] = MentionPattern(MENTION_RE, md)
