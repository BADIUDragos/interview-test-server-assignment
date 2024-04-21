from flask import jsonify, render_template, redirect, request, abort
from app import app
from . import controllers
from .. import error_handlers
from ..error_handlers import format_error


@app.route('/tax-calculator/',  methods=['GET'])
def tax_calculator_instructions():
    try:
        annual_income = float(request.args.get('salary'))
    except TypeError as e:
        pass



    return jsonify({
        'tax_brackets': controllers.get_reliable_brackets()
    })


@app.route('/tax-calculator/tax-year')
def default_brackets():
    return redirect('/')


@app.route('/tax-calculator/tax-brackets/<tax_year>')
def tax_year_brackets(tax_year):

    years_supported = ['2019', '2020', '2021', '2022', '2023']

    if tax_year not in years_supported:
        error_response = format_error(
            message="We only support tax calculations for years: " + ", ".join(years_supported),
            field="tax year",
            code="UNSUPPORTED_YEAR"
        )

        abort(jsonify({'errors': error_response}), 404)

    return jsonify({
        'tax_brackets': controllers.get_reliable_brackets(tax_year)
    })
