# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com

requirements:

description:

reference:

'''


import re
import sublime


class JSXTagComment:

    pattern = r'^([\s\t\r\n]{0,})(\<[\W\w]{0,}\>)([\s\t\r\n]{0,})$'
    commented_pattern = r'^([\s\t\r\n]{0,})\{\/\*[\s\t]{0,}(\<[\W\w]{0,}\>)[\s\t]{0,}\*\/\}([\s\t\r\n]{0,})$'

    def __init__(self, edit, view):
        self.edit = edit
        self.view = view
        self.region = self.view.sel()[0]
        if self.region.b == self.region.a:
            self.region = self.view.line(self.region.a)
            self.selected_string = self.view.substr(self.region)
        else:
            a, b = sorted([self.region.a, self.region.b])
            a_region = self.view.line(a)
            b_region = self.view.line(b)
            self.region = sublime.Region(a=a_region.a, b=b_region.b)
            self.selected_string = self.view.substr(self.region)

    @property
    def is_jsxtag(self):
        return bool((
            re.match(self.pattern, self.selected_string) or
            re.match(self.commented_pattern, self.selected_string)))

    @property
    def is_commented(self):
        return bool(re.match(self.commented_pattern, self.selected_string))

    @property
    def is_uncommented(self):
        return not self.is_commented

    def comment(self):
        sub_string = re.sub(
            self.pattern,
            r'\g<1>{/* \g<2> */}\g<3>',
            self.selected_string
        )
        self.view.replace(self.edit, self.region, sub_string)

    def uncomment(self):
        sub_string = re.sub(
            self.commented_pattern,
            r'\g<1>\g<2>\g<3>',
            self.selected_string
        )
        self.view.replace(self.edit, self.region, sub_string)

    def toggle(self):
        if self.is_commented:
            self.uncomment()
        else:
            self.comment()
