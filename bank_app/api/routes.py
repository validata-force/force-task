from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from bank_app.db.models import db, Bank

bank_bp = Blueprint('bank', __name__)

@bank_bp.route('/')
def index():
    """
    route for the home page displaying a list of all banks
    """
    banks = Bank.query.all()
    return render_template('index.html', banks=banks)

@bank_bp.route('/bank/<int:bank_id>')
def get_bank(bank_id):
    """
    Route to display details for a specific bank
    """
    bank = Bank.query.get_or_404(bank_id)
    return render_template('bank_details.html', bank=bank)

@bank_bp.route('/bank/new', methods=['GET', 'POST'])
def create_bank():
    """
    Route to create a new bank
    """
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        
        if not name or not location:
            flash('Name and location are required!', 'error')
            return redirect(url_for('bank.create_bank'))
        
        new_bank = Bank(name=name, location=location)
        db.session.add(new_bank)
        db.session.commit()
        
        flash('Bank added successfully!', 'success')
        return redirect(url_for('bank.index'))
    
    return render_template('bank_form.html', bank=None)

@bank_bp.route('/bank/<int:bank_id>/edit', methods=['GET', 'POST'])
def update_bank(bank_id):
    """
    Route to update an existing bank
    """
    bank = Bank.query.get_or_404(bank_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        
        if not name or not location:
            flash('Name and location are required!', 'error')
            return redirect(url_for('bank.update_bank', bank_id=bank_id))
        
        bank.name = name
        bank.location = location
        db.session.commit()
        
        flash('Bank updated successfully!', 'success')
        return redirect(url_for('bank.index'))
    
    return render_template('bank_form.html', bank=bank)

@bank_bp.route('/bank/<int:bank_id>/delete', methods=['POST'])
def delete_bank(bank_id):
    """
    Route to delete a bank
    """
    bank = Bank.query.get_or_404(bank_id)
    db.session.delete(bank)
    db.session.commit()
    
    flash('Bank deleted successfully!', 'success')
    return redirect(url_for('bank.index'))

@bank_bp.route('/api/banks', methods=['GET'])
def get_banks_api():
    """
    get list of all banks, JSON
    """
    banks = Bank.query.all()
    return jsonify([bank.to_dict() for bank in banks])

@bank_bp.route('/api/banks/<int:bank_id>', methods=['GET'])
def get_bank_api(bank_id):
    """
    get a specific bank, JSON
    """
    bank = Bank.query.get_or_404(bank_id)
    return jsonify(bank.to_dict())

@bank_bp.route('/api/banks', methods=['POST'])
def create_bank_api():
    """
    to create a new bank, JSON
    """
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('location'):
        return jsonify({'error': 'Name and location are required!'}), 400
    
    new_bank = Bank(name=data['name'], location=data['location'])
    db.session.add(new_bank)
    db.session.commit()
    
    return jsonify(new_bank.to_dict()), 201

@bank_bp.route('/api/banks/<int:bank_id>', methods=['PUT'])
def update_bank_api(bank_id):
    """
    endpoint to update a bank, JSON
    """
    bank = Bank.query.get_or_404(bank_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided!'}), 400
    
    if 'name' in data:
        bank.name = data['name']
    if 'location' in data:
        bank.location = data['location']
    
    db.session.commit()
    
    return jsonify(bank.to_dict())

@bank_bp.route('/api/banks/<int:bank_id>', methods=['DELETE'])
def delete_bank_api(bank_id):
    """
    to delete a bank, JSON
    """
    bank = Bank.query.get_or_404(bank_id)
    db.session.delete(bank)
    db.session.commit()
    
    return jsonify({'message': 'Bank deleted successfully!'})
