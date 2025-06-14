from flask import Flask, render_template, abort, request, url_for
import json
from config import Config

# 添加 ProxyFix 中间件
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app():
    app = Flask(__name__)

    # 在配置 ProxyFix 之前或之后打印，看看是否有区别
    print(f"WSGI app before ProxyFix: {app.wsgi_app}")
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    print(f"WSGI app after ProxyFix: {app.wsgi_app}")
    app.config.from_object(Config)

    # 加载博客数据
    with open(app.config['POSTS_JSON'], 'r', encoding='utf-8') as f:
        app.posts = json.load(f)
    # 加载生态实践案例
    with open(app.config['INITIATIVES_JSON'], 'r', encoding='utf-8') as f:
        app.initiatives = json.load(f)

    @app.route('/')
    def index():
        print("--- Request Environment ---")
        for key, value in sorted(request.environ.items()): # 排序方便查看
            if 'SCRIPT_NAME' in key or 'PATH_INFO' in key or 'FORWARDED' in key or 'HOST' in key or 'X_REAL_IP' in key or 'PROXY' in key:
                 print(f"{key}: {value}")
        print("--- URL Generation ---")
        print(f"url_for('index'): {url_for('index')}")
        print(f"url_for('static', filename='css/style.css'): {url_for('static', filename='css/style.css')}")
        print("--- End Request Debug ---")
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/initiatives')
    def initiatives():
        return render_template('initiatives.html', initiatives=app.initiatives)

    @app.route('/blog')
    def blog():
        posts = sorted(app.posts, key=lambda p: p['title'], reverse=True)
        return render_template('blog.html', posts=posts)

    @app.route('/blog/<slug>')
    def post(slug):
        post = next((p for p in app.posts if p['slug'] == slug), None)
        if not post:
            abort(404)
        return render_template('post.html', post=post)

    @app.route('/resources')
    def resources():
        return render_template('resources.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True, )
