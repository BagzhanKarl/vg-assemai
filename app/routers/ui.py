from flask import Blueprint, render_template, request, redirect, url_for

from app.db import SystemMessages
from app.db.models.system import delete_data

ui_bp = Blueprint('ui', __name__)

@ui_bp.route('/admin')
def index():
    system = SystemMessages.query.all()
    return render_template('system.html', system=system)

@ui_bp.route('/admin/system')
def system_message():
    system = SystemMessages.query.all()
    return render_template('system.html', system=system)

@ui_bp.route('/admin/users')
def users():
    return render_template('users.html')

@ui_bp.route('/admin/chats')
def chats():
    pass

@ui_bp.route('/admin/chats/<int:id>')
def chat(id):
    pass

@ui_bp.route('/admin/payment')
def payment():
    pass

@ui_bp.route('/admin/stats')
def stats():
    pass

@ui_bp.route('/admin/system/create', methods=['POST'])
def system_create():
    data = request.form.to_dict()
    if data.get('id'):
        edit = SystemMessages(id=data['id'], content=data['content'])
        edit.edit_system_saver()
        return redirect(url_for('ui.system_message'))
    else:
        new = SystemMessages(content=data['content'])
        new.create_system_saver()
        return redirect(url_for('ui.system_message'))

@ui_bp.route('/admin/system/delete/<int:id>', methods=['GET'])
def system_delete(id):
    delete = delete_data(id=id)
    return redirect(url_for('ui.system_message'))