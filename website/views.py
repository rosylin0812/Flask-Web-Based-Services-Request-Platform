from pickle import TRUE
from types import NoneType
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Service
from . import db
import json
import re

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        phone = request.form.get('phone')
        address = request.form.get('address')
        service = Service.query.get('service')
     
        phone = Service.query.filter_by(phone=phone).first()
        if phone:
            flash('Invalid format of phone number', category='error')
        elif address is None:
            flash('Please enter address!', category='error')     
        elif service is None:
            flash('Comments is too short!', category='error')
        elif len(service) == 0:
            flash('Comments is too short!', category='error')
        else:
            new_service = Service(phone= phone, address = address, data=service, user_id=current_user.id)
            db.session.add(new_service)
            db.session.commit()
            flash('Service added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-service', methods=['POST'])
def delete_service():
    Service = json.loads(request.data)
    serviceId = Service['serviceId']
    service = Service.query.get(serviceId)
    if service:
        if service.user_id == current_user.id:
            db.session.delete(service)
            db.session.commit()

    return jsonify({})
