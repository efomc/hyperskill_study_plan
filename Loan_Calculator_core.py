from math import ceil, log, floor
from argparse import ArgumentParser

ERROR_MESSAGE = 'Incorrect parameters'

def get_start_args():
    parser = ArgumentParser(description="This program prints recipes \
            consisting of the ingredients you provide.")

    parser.add_argument("--type",
                        help='You need to choose from the options "annuity" or "diff".')
    parser.add_argument("--payment",
                        help="You need to input the monthly payment amount in dollars.")
    parser.add_argument("--principal",
                        help="You need to input the loan principal in dollars.")
    parser.add_argument("--periods",
                        help="You need to input the number of months needed to repay the loan.")
    parser.add_argument("--interest",
                        help="You need to specified it without a percent sign. "
                             "Note that it can accept a floating-point value")
    return parser.parse_args()


def check_args_correction(args_data):
    check_result = False
    if args_data.type in ('annuity', 'diff'):
        check_result = True
    if check_result and args_data.type and args_data.type == 'diff':
        if args_data.payment:
            check_result = False
    digital_parameters_list = [
        args_data.payment,
        args_data.principal,
        args_data.periods,
        args_data.interest
    ]
    for item in digital_parameters_list:
        if item:
            if check_result and float(item) >= 0:
                check_result = True
            else:
                check_result = False
    if check_result and args_data.interest:
        check_result = True
    else:
        check_result = False
    if check_result and len(digital_parameters_list) >= 3:
        check_result = True
    else:
        check_result = False
    return check_result


def monthly_payments_number(loan_value, monthly_payment_value, loan_interest):
    monthly_interest_rate = loan_interest * 0.01 / 12
    months_numbers = log(monthly_payment_value /
                         (monthly_payment_value - monthly_interest_rate * loan_value),
                         1 + monthly_interest_rate)
    months_numbers = ceil(months_numbers)
    if months_numbers < 12:
        if months_numbers == 1:
            date_interval = '1 month'
        else:
            date_interval = f'{months_numbers} months'
    elif months_numbers % 12:
        year_amount = months_numbers // 12
        date_interval = f'{year_amount} years and {months_numbers % 12} months'
    elif months_numbers // 12 == 1:
        date_interval = '1 year'
    else:
        date_interval = f'{months_numbers // 12} years'
    print(f'It will take {date_interval} to repay this loan!')
    total_payment = monthly_payment_value * months_numbers
    overpayment = total_payment - loan_value
    print(f'Overpayment = {overpayment}')


def loan_principal(annuity_payment, periods_number, loan_interest):
    monthly_interest_rate = loan_interest * 0.01 / 12
    loan_value = floor(
        annuity_payment
        / (
            (monthly_interest_rate * (1 + monthly_interest_rate) ** periods_number)
            / ((1 + monthly_interest_rate) ** periods_number - 1)
        )
    )
    print(f'Your loan principal = {loan_value}!')
    overpayment = annuity_payment * periods_number - loan_value
    print(f'Overpayment = {overpayment}')


def differentiated_payments(loan_value, payments_number, loan_interest):
    monthly_interest_rate = loan_interest * 0.01 / 12
    total_payment = 0
    for month in range(1, payments_number + 1):
        different_payment = (loan_value / payments_number) \
                            + monthly_interest_rate \
                            * (loan_value
                               - (loan_value * (month - 1) / payments_number))
        different_payment = ceil(different_payment)
        print(f'Month {month}: payment is {different_payment}')
        total_payment += different_payment
    overpayment = total_payment - loan_value
    print(f'Overpayment = {overpayment}')


def annuity_payment_amount(loan_value, periods_number, loan_interest):
    monthly_interest_rate = loan_interest * 0.01 / 12
    monthly_payment_value = ceil(
        loan_value
        * (monthly_interest_rate * (1 + monthly_interest_rate) ** periods_number)
        / ((1 + monthly_interest_rate) ** periods_number - 1)
    )
    print(f'Your annuity payment = {monthly_payment_value}!')
    total_payment = monthly_payment_value * periods_number
    overpayment = total_payment - loan_value
    print(f'Overpayment = {overpayment}')


def calculate_actions(args_data):
    if args_data.type == 'diff':
        differentiated_payments(
            int(args_data.principal),
            int(args_data.periods),
            float(args_data.interest),
        )
    elif args_data.type == 'annuity':
        if not args_data.payment:
            annuity_payment_amount(
                int(args_data.principal),
                int(args_data.periods),
                float(args_data.interest),
            )
        elif not args_data.principal:
            loan_principal(
                int(args_data.payment),
                int(args_data.periods),
                float(args_data.interest),
            )
        elif not args_data.periods:
            monthly_payments_number(
                int(args_data.principal),
                int(args_data.payment),
                float(args_data.interest),
            )


def main():
    calculation_args = get_start_args()
    correct_check = check_args_correction(calculation_args)
    if correct_check:
        calculate_actions(calculation_args)
    else:
        print(ERROR_MESSAGE)


if __name__ == "__main__":
    main()
