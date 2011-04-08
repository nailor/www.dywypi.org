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


analytics_script = '''
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-22601090-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
'''.encode('utf-8')

def post_render_hook(context, data):
    # Don't add the analytics script when using the Stango test server
    if context.mode == 'serving':
        return data

    name, ext = os.path.splitext(context.realpath)
    if ext != '.html':
        return data

    offset = data.find(b'</body>')
    if offset == -1:
        return data

    return data[:offset] + analytics_script + data[offset:]
