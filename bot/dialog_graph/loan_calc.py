import math


def loanCalc(total_loan, percent, initial_payment, years):
    loan_principal = total_loan - initial_payment
    num_periods = years*12
    if percent == 0:
        monthly_payment = math.ceil(loan_principal / num_periods)
        overpay = 0
    elif total_loan == 0:
         monthly_payment =0
         overpay = 0
    else:
        nominal_interest = percent / (12 * 100)
        monthly_payment = math.ceil(loan_principal * (nominal_interest * (1 + nominal_interest) ** num_periods) /
                                    ((1 + nominal_interest) ** num_periods - 1))
        overpay = math.ceil((monthly_payment * num_periods) - loan_principal)

    return(f"Ежемесячный платеж = {monthly_payment}\nПереплата = {overpay}")
    

