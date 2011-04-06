from stango.files import *
from .lib.blog import Blog

index_file = 'index.html'

# Views
def render_template(name, ctx={}):
    if name.endswith('.md'):
        pass
    return lambda context: context.render_template(name, **ctx)

blog = Blog(
    '', 'blog',
    default_author='Jyrki Pulliainen',
    entry_suffix='.html',
)

files = Files(
    blog.files,
    # Static files
    files_from_dir('', 'static', strip=1),
    ('about/', render_template('about.html')),
    ('projects/', render_template('projects.html')),
)
