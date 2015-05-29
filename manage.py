# -*- coding: utf-8 -*-
__author__ = 'puras'
__email__ = 'he@puras.me'

from flask.ext.script import Manager

from app import create_app

# Used by app debug & livereload
PORT = 5050

app = create_app()

manager = Manager(app)

@manager.command
def run():
    """Run App."""
    app.run(port = PORT)

@manager.command
def live():
    """Run Livereload server"""
    from livereload import Server
    import formic

    server = Server(app)

    # css
    for filepath in formic.FileSet(include='app/assets/css/**/*.css'):
        server.watch(filepath)
    # js
    for filepath in formic.FileSet(include='app/assets/js/**/*.js'):
        server.watch(filepath)
    #image
    for filepath in formic.FileSet(include='app/assets/img/**/*.*'):
        server.watch(filepath)
    # html
    for filepath in formic.FileSet(include='app/templates/**/*.html'):
        server.watch(filepath)

    server.serve(port=PORT)

if __name__ == '__main__':
    manager.run()