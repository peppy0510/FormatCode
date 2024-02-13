# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com

requirements:

description:

reference:

'''


import json
import os
import platform
import sublime
import sublime_plugin
import subprocess

from .JSXTagComment import JSXTagComment
from .SingleLineComment import SingleLineComment
# import html
# from pathlib import Path


SYNTAX_DICTIONARY = {
    'java': ['Java'],
    'c': ['C', 'C++', 'C#'],
    'dart': ['Dart'],
    'typescript': ['TypeScript', 'TypeScriptReact'],
    'css': ['CSS', 'CSS (Django)', 'SCSS', 'naomi.css3'],
    'json': ['JSON', 'JSON (Sublime)', 'JSON Key-Value', 'Sublime Text Project'],
    'markdown': ['Markdown', 'Markdown GFM', 'MultiMarkdown'],
    'javascript': [
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
    'shell': ['Shell-Unix-Generic'],
    # 'shell': ['PowershellSyntax', 'Shell-Unix-Generic'],
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
    def run(self, edit, comment=False):

        plugin_name = self.__class__.__name__[:-7]
        viewport_position = self.view.viewport_position()

        syntax = self.view.settings().get('syntax')
        syntax = os.path.splitext(os.path.split(syntax)[-1])[0]
        filename = os.path.basename(self.view.file_name())
        extension = os.path.splitext(filename)[-1].strip('.')

        if comment:
            if extension in ('reg', 'pip', 'apt', 'bat', 'cmd',) or \
                    syntax in ('REG', 'Batch File', 'EditorConfig'):
                singlelinecomment = SingleLineComment(
                    edit, self.view, syntax, extension)
                singlelinecomment.toggle()
                print('{}.Comment().SingleLineComment()'.format(plugin_name))
                return

            if (syntax in syntaxmap('javascript') or extension in ('js', 'jsx') or
                    syntax in syntaxmap('typescript') or extension in ('ts', 'tsx')):
                jsxtagcomment = JSXTagComment(edit, self.view)
                if jsxtagcomment.is_jsxtag:
                    jsxtagcomment.toggle()
                    print('{}.Comment().JSXTagComment()'.format(plugin_name))
                    return

            print('{}.Comment()'.format(plugin_name))
            self.view.run_command('toggle_comment')
            return

        print(
            "{}({{'syntax': '{}', 'extension': '{}'}})".format(
                plugin_name, syntax, extension
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
            'sublime-project',
            'sublime-workspace',
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

        if (syntax in syntaxmap('javascript') or extension in ('js', 'jsx') or
                syntax in syntaxmap('typescript') or extension in ('ts', 'tsx')):
            self.view.run_command('javascript_fix_imports')
            self.view.run_command('js_prettier')
            # self.view.run_command('sort_js_imports')

        if syntax in syntaxmap('css') or extension in ('css', 'scss', 'sass'):
            self.view.run_command('css_comb')

        if syntax in syntaxmap('python') or extension in ('py', 'pyw'):
            self.view.run_command('python_fiximports')
            self.view.run_command('auto_pep8', {'preview': False})
            # self.view.run_command('black')
            # self.view.run_command('auto_pep8')
            # self.view.run_command('pep8_autoformat')

        if syntax in syntaxmap('typescript') or extension in ('ts', 'tsx'):
            # self.view.run_command('javascript_fix_imports')
            self.view.run_command('js_prettier')
            # self.view.run_command('typescript_format_document')
            # self.view.run_command('typescript_organize_imports')

        if syntax in syntaxmap('lua') or extension in ('lua',):
            self.view.run_command('lua_format')

        if syntax in syntaxmap('c', 'java') or extension in ('cpp', 'java'):
            self.view.run_command('astyleformat')

        if syntax in syntaxmap('markdown') or extension in ('md',):
            self.view.run_command('markdown_table_format')
            # self.view.run_command('js_prettier')

        if syntax in syntaxmap('pip') or extension in ('pip', 'apt'):
            self.view.run_command('python_fix_requirements')

        if syntax in syntaxmap('lua') or extension in ('lua',):
            self.view.run_command('lua_format')

        if syntax in syntaxmap('shell') or extension in ('sh', 'bash'):
            self.view.run_command('pretty_shell')

        if syntax in syntaxmap('dart') or extension in ('dart'):
            line_length = 80
            region = sublime.Region(a=0, b=10 ** 16)

            pipe = subprocess.PIPE
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            dart_path = None
            for path in os.environ.get('PATH').split(';'):
                # if 'flutter' in path.split(os.path.sep):
                #     dart_path = '/cache/dart-sdk/bin/dart'
                parts = path.split(os.path.sep)
                if 'flutter' in parts and 'dart-sdk' not in parts:
                    dart_path = '/cache/dart-sdk/bin/dart'
                    if platform.system() == 'Windows':
                        dart_path = '\\cache\\dart-sdk\\bin\\dart.exe'
                    dart_path = str(path) + dart_path
                    # if platform.system() == 'Windows':
                    #     dart_path += '.exe'

            if dart_path:
                # print(dart_path)
                # --fix --indent --selection --summary --line-length
                # self.view.file_name(),
                proc = subprocess.Popen([
                    dart_path, 'format',
                    '--output', 'json',
                    '--indent', str(0),
                    '--line-length', str(line_length),
                ], stdin=pipe, stdout=pipe, stderr=pipe, startupinfo=startupinfo)
                resp, error = proc.communicate(self.view.substr(region).encode('utf-8'))

                if not error and resp:
                    source = json.loads(resp.decode('utf-8')).get('source')
                    # print(source)
                    self.view.replace(edit, region, source)
                else:
                    print(error.decode('utf-8'))

        self.view.set_viewport_position(viewport_position)
