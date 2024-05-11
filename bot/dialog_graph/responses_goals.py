from typing import cast

from dff.script import Context
from dff.pipeline import Pipeline
from dff.messengers.telegram import TelegramMessage, ParseMode

from dialog_graph.loan_calc import loanCalc
from dialog_graph.generate import risk_profile, init_model


llm, tokenizer = init_model()


def response_handler_risk(ctx: Context, _: Pipeline) -> TelegramMessage:
    text = str(risk_profile(llm, tokenizer, ctx.misc['invest_goals'], ctx.misc['duration'], ctx.misc['funds_volume'], ctx.misc['daily_expenses'],
                                        ctx.misc['is_risky'], ctx.misc['invest_experience'], ctx.misc['capital_reduction'], ctx.misc['early_withdrawal'],
                                        ctx.misc['reserve_fund'], ctx.misc['private_property'], ctx.misc['retirement'], ctx.misc['monthly_income_expenses'],
                                        ctx.misc['debt_obligation'], ctx.misc['age']))     
    return TelegramMessage(text=text, parse_mode=ParseMode.HTML)


def response_handler_loan(ctx: Context, _: Pipeline) -> TelegramMessage:
    text = str(loanCalc(ctx.misc['loan'], ctx.misc['interest'], ctx.misc['init_pay'], ctx.misc['period']))
    return TelegramMessage(text=text, parse_mode=ParseMode.HTML) 



