# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com

requirements:

description:

reference:

'''


import os
import sublime_plugin


SYNTAX_DICTIONARY = {
    'java': ['Java'],
    'c': ['C', 'C++', 'C#'],
    'typescript': ['TypeScript', 'TypeScriptReact'],
    'css': ['CSS', 'CSS (Django)', 'SCSS', 'naomi.css3'],
    'json': ['JSON', 'JSON (Sublime)', 'JSON Key-Value'],
    'markdown': ['Markdown', 'Markdown GFM', 'MultiMarkdown'],
    'javacript': [
        'JSX',
        'TSX',
        'JavaScript',
        'JavaScriptNext',
        'JavaScript (Babel)',
        'JavaScript (Webpack)',
    ],
    'python': ['Python', 'Python3', 'Python Django', 'MagicPython'],
    'html': [
        'HTML',
        'HTML (Django)',
        'HTML-extended',
        'XML',
        'NgxHTML',
        'naomi.html5',
        'HTML (Underscore)',
    ],
    'pip': ['requirements.txt'],
    'lua': ['Lua'],
}


class Syntax:
    def __contains__(self, name):
        for key in self.keywords:
            dictionary = SYNTAX_DICTIONARY.get(key)
            if dictionary and name in dictionary:
                return True
        return False

    def syntaxmap(self, *keywords):
        self.keywords = keywords
        return self


syntaxmap = Syntax().syntaxmap


class FormatCodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        viewport_position = self.view.viewport_position()

        syntax = self.view.settings().get('syntax')
        syntax = os.path.splitext(os.path.split(syntax)[-1])[0]
        filename = os.path.basename(self.view.file_name())
        extension = os.path.splitext(filename)[-1].strip('.')

        print(
            "{}({{'syntax': '{}', 'extension': '{}'}})".format(
                self.__class__.__name__[:-7], syntax, extension
            )
        )

        if syntax in syntaxmap(
            'c', 'java', 'json', 'html', 'css', 'python', 'javascript', 'typescript'
        ):
            self.view.run_command('unexpand_tabs')
            self.view.run_command('set_setting', {'setting': 'tab_size', 'value': 4})
            self.view.run_command('expand_tabs', {'set_translate_tabs': True})
            self.view.run_command('expand_tabs', {'translate_tabs_to_spaces': True})
            # self.view.run_command('re_indent_to_four')
            # self.view.run_command('indentation_convert_to_spaces')
            # "detect_indentation": true,
            # "tab_size": 4,
            # "translate_tabs_to_spaces": false

        if syntax in syntaxmap('c', 'java', 'html', 'css', 'javascript', 'typescript'):
            self.view.run_command('reindent', {"single_line": False})

        if syntax in syntaxmap('json') or extension in (
            'json',
            'sublime-settings',
            'sublime-commands',
            'sublime-keymap',
            'htmlhint.htmlhintrc',
            'sublime-menu',
            'jsbeautifyrc',
            'hidden-color-scheme',
        ):
            self.view.run_command('js_prettier')
            # self.view.set_syntax_file('JSON Key-Value')
            # self.view.run_command('set_syntax', 'JSON Key-Value')
            # self.view.run_command('pretty_json')

        if syntax in syntaxmap('html') or extension in ('htm', 'html'):
            self.view.run_command('htmlprettify')

        if syntax in syntaxmap('javacript') or extension in ('js', 'jsx'):
            # self.view.run_command('sort_js_imports')
            self.view.run_command('javascript_fix_imports')
            self.view.run_command('js_prettier')

        if syntax in syntaxmap('css') or extension in ('css', 'scss', 'sass'):
            self.view.run_command('css_comb')

        if syntax in syntaxmap('python') or extension in ('py', 'pyw'):
            self.view.run_command('python_fiximports')
            self.view.run_command('black')
            # self.view.run_command('auto_pep8')
            # self.view.run_command('pep8_autoformat')

        if syntax in syntaxmap('typescript') or extension in ('ts',):
            self.view.run_command('typescript_format_document')
            self.view.run_command('typescript_organize_imports')

        if syntax in syntaxmap('lua') or extension in ('lua',):
            self.view.run_command('lua_format')

        if syntax in syntaxmap('c', 'java') or extension in ('cpp', 'java'):
            self.view.run_command('astyleformat')

        if syntax in syntaxmap('markdown') or extension in ('md',):
            self.view.run_command('markdown_table_format')

        if syntax in syntaxmap('pip') or extension in ('pip', 'apt'):
            self.view.run_command('python_fix_requirements')

        self.view.set_viewport_position(viewport_position)
