from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from model import db, Allocation, Session, Employee, Division
from service import (
    get_employees_for_coordinator,
    get_available_employees_for_session,
    allocate_employee,
    get_session_summary
)

main = Blueprint('main', __name__)


# ─────────────────────────────
# DASHBOARD
# ─────────────────────────────
@main.route('/')
@login_required
def dashboard():

    session_summary = get_session_summary()

    return render_template(
        'dashboard.html',
        session_summary=session_summary,
        user=current_user
    )


# ─────────────────────────────
# ALLOCATE PAGE
# ─────────────────────────────
@main.route('/allocate', methods=['GET', 'POST'])
@login_required
def allocate():

    if request.method == 'POST':

        employee_id = request.form.get('employee_id', type=int)
        session_id = request.form.get('session_id', type=int)

        if not employee_id or not session_id:
            flash('Select employee and session', 'error')
            return redirect(url_for('main.allocate'))

        success, message = allocate_employee(
            coordinator_id=current_user.id,
            employee_id=employee_id,
            session_id=session_id
        )

        flash(message, 'success' if success else 'error')
        return redirect(url_for('main.allocate'))

    # GET request
    employees, _ = get_available_employees_for_session(
        current_user.id,
        session_key=None  # optional if you want filtering later
    )

    sessions = Session.query.all()
    session_summary = get_session_summary()

    return render_template(
        'allocate.html',
        employees=employees,
        sessions=sessions,
        session_summary=session_summary,
        user=current_user
    )


# ─────────────────────────────
# EMPLOYEES PAGE
# ─────────────────────────────
@main.route('/employees')
@login_required
def employees():

    division = current_user.division

    employees = Employee.query.filter_by(
        division_id=division.id
    ).all()

    return render_template(
        'employees.html',
        employees=employees,
        division=division,
        user=current_user
    )


# ─────────────────────────────
# SESSION DETAILS
# ─────────────────────────────
@main.route('/session/<int:session_id>')
@login_required
def session_detail(session_id):

    session = Session.query.get_or_404(session_id)

    allocations = Allocation.query.filter_by(
        session_id=session.id
    ).all()

    return render_template(
        'session_detail.html',
        session=session,
        allocations=allocations,
        user=current_user
    )


# ─────────────────────────────
# REMOVE ALLOCATION
# ─────────────────────────────
@main.route('/remove/<int:allocation_id>', methods=['POST'])
@login_required
def remove_allocation(allocation_id):

    allocation = Allocation.query.get_or_404(allocation_id)

    if allocation.coordinator_id != current_user.id:
        flash('Not authorised', 'error')
        return redirect(url_for('main.dashboard'))

    db.session.delete(allocation)
    db.session.commit()

    flash('Allocation removed', 'success')
    return redirect(url_for('main.dashboard'))
