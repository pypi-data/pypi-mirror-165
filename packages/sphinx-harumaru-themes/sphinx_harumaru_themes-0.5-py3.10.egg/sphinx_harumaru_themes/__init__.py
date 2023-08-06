from os import path


themes = [
    'haruki_light',
    'haruki_dark',
    'haruki_hw',
    'daimaru_light',
    'daimaru_dark',
    'daimaru_hw',
    'erika_hw',
]

def setup(app):
    abspath = path.abspath(path.dirname(__file__))
    for theme in themes:
        app.add_html_theme(theme, path.join(abspath, f'{theme}_theme'))