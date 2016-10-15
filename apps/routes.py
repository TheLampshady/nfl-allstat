import logging
import webapp2
import jinja2
import settings


route_config = {
    'template_path': "apps.templates",
    'environment_args': {
        'autoescape': True,
        'extensions': [
            'jinja2.ext.autoescape',
            'jinja2.ext.with_',
            'jinja2.ext.i18n',
        ],
    },
}

_APP = webapp2.WSGIApplication([], debug=True)

def handle_response_error(request, response, exception):

    # If the exception is a HTTPException, use its error code else a generic 500 error code
    status_code = exception.code if isinstance(exception, webapp2.HTTPException) else 500
    if settings.DEBUG or status_code >= 500:
        logging.exception(exception)

    j = jinja2.get_jinja2()
    t = j.render_template(str(status_code) + '.html')

    response.write(t)
    response.set_status(status_code)


if not settings.DEBUG:
    _APP.error_handlers[403] = handle_response_error
    _APP.error_handlers[404] = handle_response_error
    _APP.error_handlers[500] = handle_response_error
