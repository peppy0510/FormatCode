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


class SingleLineComment:
    pattern = r'^([\s\t]{0,})([\W\w]{1,})$'
    commented_pattern = r'^([\s\t]{0,})([\#]{1}[\s]{0,1})([\W\w]{1,})$'

    def __init__(self, edit, view, syntax, extension):
        self.edit = edit
        self.view = view
        self.syntax = syntax
        self.extension = extension
        self.is_reg_comment = extension in ('reg',) or syntax in ('REG',)
        self.is_rem_comment = extension in ('bat', 'cmd',) or syntax in ('Batch File',)

        if self.is_reg_comment:
            self.commented_pattern = r'^([\s\t]{0,})([\#\;]{1}[\s]{0,1})([\W\w]{1,})$'

        if self.is_rem_comment:
            self.commented_pattern = (
                r'^([\s\t]{0,})'
                r'(rem[\s]{0,1}|Rem[\s]{0,1}|REM[\s]{0,1}|\:\:[\s]{0,1})'
                r'([\W\w]{1,})$'
            )

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

    def is_commented(self, line):
        return bool(re.match(self.commented_pattern, line, re.IGNORECASE))

    def is_uncommented(self, line):
        return not self.is_commented(line)

    def comment(self, line):
        repl = r'\g<1># \g<2>'
        if self.is_rem_comment:
            repl = r'\g<1>:: \g<2>'

        sub_string = re.sub(
            self.pattern, repl, line, re.IGNORECASE
        )
        return sub_string

    def uncomment(self, line):
        sub_string = re.sub(
            self.commented_pattern, r'\g<1>\g<3>', line, re.IGNORECASE
        )
        return sub_string

    def toggle(self):
        lines = self.selected_string.split('\n')
        is_commented = True
        for i in range(len(lines)):
            if lines[i] and not self.is_commented(lines[i]):
                is_commented = False

        if is_commented:
            for i in range(len(lines)):
                lines[i] = self.uncomment(lines[i])
        else:
            for i in range(len(lines)):
                lines[i] = self.comment(lines[i])

        sub_string = '\n'.join(lines)
        self.view.replace(self.edit, self.region, sub_string)
