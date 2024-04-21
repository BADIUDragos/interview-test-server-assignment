import logging

from flask import jsonify, redirect, request, abort
from app import app
from . import controllers
from ..error_handlers import format_error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/tax-calculator/',  methods=['GET'])
def tax_calculator_instructions():
    for param in ['annual_income', 'tax_year']:
        if request.args.get(param) is None:
            error_message = f"Please provide {param.replace('_', ' ')}"
            logger.info(error_message)
            error_response = format_error(
                message=error_message,
                field=param,
                code=f"NO_{param.upper()}"
            )
            return jsonify({'errors': error_response}), 400

    try:
        annual_income = float(request.args['annual_income'])
    except ValueError:
        error_message = "annual_income must be a number"
        logger.info(error_message)
        error_response = format_error(
            message=error_message,
            field="annual_income",
            code="INVALID_ANNUAL_INCOME"
        )
        return jsonify({'errors': error_response}), 400

    if annual_income < 0:
        error_message = "annual_income must be positive"
        logger.info(error_message)
        error_response = format_error(
            message=error_message,
            field="annual_income",
            code="SUB_ZERO_INCOME"
        )
        return jsonify({'errors': error_response}), 400

    try:
        tax_year = int(request.args['tax_year'])
    except ValueError:
        error_message = "tax_year must be a valid year"
        logger.info(error_message)
        error_response = format_error(
            message=error_message,
            field="tax_year",
            code="INVALID_TAX_YEAR"
        )
        return jsonify({'errors': error_response}), 400

    if tax_year < 2019 or tax_year > 2023:
        error_message = "tax_year must be between 2019 and 2023 inclusively"
        logger.info(error_message)
        error_response = format_error(
            message=error_message,
            field="tax_year",
            code="TAX_YEAR_OUT_OF_RANGE"
        )
        return jsonify({'errors': error_response}), 400

    try:
        result = controllers.calculate_marginal_tax(annual_income, tax_year)
    except Exception as e:
        error_message = str(e)
        logger.error(error_message)
        error_response = format_error(
            message=error_message,
        )
        return jsonify({'errors': error_response}), 520

    return jsonify(result), 200


# odd way of doing things but ok, would probably clean realistically
@app.route('/tax-calculator/tax-year')
def default_brackets():
    return redirect('/')


@app.route('/tax-calculator/tax-brackets/<tax_year>')
def tax_year_brackets(tax_year):

    # would prefer not to write this in both endpoints but get the info from the same place
    years_supported = ['2019', '2020', '2021', '2022', '2023']

    if tax_year not in years_supported:
        error_response = format_error(
            message="We only support tax calculations for years: " + ", ".join(years_supported),
            field="tax_year",
            code="UNSUPPORTED_YEAR"
        )

        return jsonify({'errors': error_response}), 404

    return jsonify({
        'tax_brackets': controllers.get_reliable_brackets(tax_year)
    })
