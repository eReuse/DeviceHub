from .app import app

if app.config['USE_DOCS']:
    from flask.ext.bootstrap import Bootstrap
    from eve_docs import eve_docs
    Bootstrap(app)
    app.register_blueprint(eve_docs, url_prefix='/docs')