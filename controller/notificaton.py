from flask import Blueprint, render_template

notificationControl = Blueprint('notificationControl', __name__)

@notificationControl.route('/notification')
def gotoNotif():
    return render_template('notification.html')