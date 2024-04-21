from flask import jsonify, render_template, redirect, request
from app import app
from . import controllers


@app.route('/tax-calculator/')
def tax_calculator_instructions():
    return jsonify({
        'tax_brackets': controllers.get_reliable_brackets()
    })


@app.route('/tax-calculator/tax-year')
def default_brackets():
    return redirect('/')


@app.route('/tax-calculator/tax-brackets/<tax_year>')
def tax_year_brackets(tax_year):
    return jsonify({
        'tax_brackets': controllers.get_tax_brackets(tax_year)
    })

@app.route('/tax-calculator/get-tax',  methods=['GET'])
def calculate_total_tax():
    try:
        annual_income = float(request.args.get('salary'))

        year = int(request.args.get('year'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input. Please provide a valid income and tax year."}), 400

