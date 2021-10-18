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

        # region = self.view.sel()[0]
        # if region.b == region.a:
        #     region = self.view.line(region.a)
        #     selected_string = self.view.substr(region)
        # else:
        #     selected_string = self.view.substr(region)

        # pattern = r'^([\s\t\r\n]{0,})\{\/\*[\s\t]{0,}(\<[\W\w]{0,}\>)[\s\t]{0,}\*\/\}([\s\t\r\n]{0,})$'
        # if re.match(pattern, selected_string):
        #     selected_string = re.sub(
        #         pattern,
        #         r'\g<1>\g<2>\g<3>',
        #         selected_string
        #     )
        #     print(selected_string)
        #     self.view.replace(edit, region, selected_string)

        # else:
        #     pattern = r'^([\s\t\r\n]{0,})(\<[\W\w]{0,}\>)([\s\t\r\n]{0,})$'
        #     if re.match(pattern, selected_string):
        #         selected_string = re.sub(
        #             pattern,
        #             r'\g<1>{/* \g<2> */}\g<3>',
        #             selected_string
        #         )
        #         print(selected_string)
        #         # self.view.sel().clear()
        #         # self.view.sel().add(sublime.Region(**kwargs['region']))
        #         self.view.replace(edit, region, selected_string)
        #         # self.view.replace(edit, sublime.Region(a=region.a), selected_string)
        # # uncommented_m = re.match(uncomented_pattern, selected_string)
