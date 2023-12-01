from flask import Blueprint, render_template, request, redirect

terms_of_use_bp = Blueprint('terms_of_use', __name__)

@terms_of_use_bp.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html')