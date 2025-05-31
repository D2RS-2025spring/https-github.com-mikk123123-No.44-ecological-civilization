from flask import Flask, render_template, abort
import json
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 加载博客数据
    with open(app.config['POSTS_JSON'], 'r', encoding='utf-8') as f:
        app.posts = json.load(f)
    # 加载生态实践案例
    with open(app.config['INITIATIVES_JSON'], 'r', encoding='utf-8') as f:
        app.initiatives = json.load(f)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/initiatives')
    def initiatives():
        return render_template('initiatives.html', initiatives=app.initiatives)

    @app.route('/blog')
    def blog():
        posts = sorted(app.posts, key=lambda p: p['date'], reverse=True)
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
    app.run(host='0.0.0.0', port=5000, debug=True)
