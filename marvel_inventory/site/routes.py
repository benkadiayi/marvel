from flask import Blueprint, render_template
from flask_login.utils import login_required



site = Blueprint('site', __name__, template_folder='sites_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')