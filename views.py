def hello(context, message, link):
    return context.render_template('hello.html', message=message, link=link)
