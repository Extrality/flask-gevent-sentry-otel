# Create app core with basic configuration and logging
from werkzeug.middleware.proxy_fix import ProxyFix

from super_api.create_app import create_app

app = create_app(name="Extrality UserAPI", package=__package__)
application = ProxyFix(app)  # WSGI wants `application`


@app.route("/health_check")
def health_check():
    return "", 200
