from stango.files import Files
import views

index_file = 'index.html'

files = Files(
    ('', views.hello, { 'message': 'Hello, World!', 'link': 'greeting.html' }),
    ('greeting.html', views.hello, { 'message': 'Greetings, World!', 'link': 'index.html' }),
)
