import jwt

def issue_token(email):
    user_id = User.get(User.email == email).id
    jwt.encode({'user_id': user_id}, app.config['FLASK_SECRET_KEY_BASE'], algorithm='HS256')


# Request handlers -- these two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@app.before_request
def before_request():
    g.db = db
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return inner
