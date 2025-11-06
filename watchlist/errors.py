from flask import render_template, request


def register_errors(app):

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

def register_static_status(app, status_code=305):
    """
    将静态文件响应的状态码统一改为指定整数。
    使用方法：在 create_app() 或 app 初始化后调用 register_static_status(app, 500)
    注意：不要传入含非 latin-1 字符的字符串到 response.status
    """
    @app.after_request
    def set_static_status(response):
        static_prefix = app.static_url_path or '/static'
        # 兼容 endpoint 判断（某些情况下静态文件可能由 endpoint='static' 提供）
        if request.path.startswith(static_prefix) or getattr(request, 'endpoint', None) == 'static':
            response.status_code = int(status_code)
            response.status = str(status_code) + ' Static File'
        return response

