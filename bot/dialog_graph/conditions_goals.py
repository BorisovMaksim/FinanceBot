from typing import cast

from dff.script import Context
from dff.pipeline import Pipeline
from dff.messengers.telegram import TelegramMessage, ParseMode



def convert_to_numeric(value_str):
    try:
        float_value = float(value_str)
        if (float_value>=0):
            return float_value
        else:
            return False
    except ValueError:
        return False


def received_text_wrong_risk(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    if last_request.is_toxic:
        return True
    return False


def received_text_node_1(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['invest_goals'] = last_request.text
    return last_request.text is not None


def received_text_node_2(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['duration'] = last_request.text
    return last_request.text is not None


def received_text_node_3(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['funds_volume'] = last_request.text
    return last_request.text is not None


def received_text_node_4(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['daily_expenses'] = last_request.text
    return last_request.text is not None


def received_text_node_5(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['is_risky'] = last_request.text
    return last_request.text is not None


def received_text_node_6(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['invest_experience'] = last_request.text
    return last_request.text is not None


def received_text_node_7(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['capital_reduction'] = last_request.text
    return last_request.text is not None


def received_text_node_8(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['early_withdrawal'] = last_request.text
    return last_request.text is not None


def received_text_node_9(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['reserve_fund'] = last_request.text
    return last_request.text is not None



def received_text_node_10(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['private_property'] = last_request.text
    return last_request.text is not None


def received_text_node_11(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['retirement'] = last_request.text
    return last_request.text is not None


def received_text_node_12(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['monthly_income_expenses'] = last_request.text
    return last_request.text is not None


def received_text_node_13(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['debt_obligation'] = last_request.text
    return last_request.text is not None


def received_text_node_14(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['age'] = last_request.text
    return last_request.text is not None


def received_loan(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['loan'] = convert_to_numeric(last_request.text)
    return last_request.text is not None


def received_wrong_value(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    if (convert_to_numeric(last_request.text) is False):
        return True 
    return False


def received_init_pay(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['init_pay'] = convert_to_numeric(last_request.text)
    return last_request.text is not None


def received_init_pay_wrong(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request 
    if (convert_to_numeric(last_request.text) is not False)&(convert_to_numeric(last_request.text)>ctx.misc['loan']):
        return True 
 

def received_interest(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['interest'] = convert_to_numeric(last_request.text)
    return last_request.text is not None


def received_period(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    ctx.misc['period'] = convert_to_numeric(last_request.text)
    return last_request.text is not None


def received_period_wrong(ctx: Context, _: Pipeline):
    """Return true if the last update from user contains text."""
    last_request = ctx.last_request
    if (convert_to_numeric(last_request.text))==0:
         return True
    return False
