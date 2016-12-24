from flask import Blueprint
from flask.ext.paginate import Pagination

mod = Blueprint('users', __name__)


@mod.route('/')
def index():
    search = False
    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    users = User.find(...)
    
    pagination = Pagination(page=page, total=users.count(), search=search, record_name='users')

    return render_template('learn_pagination.html',users=users,pagination=pagination,)