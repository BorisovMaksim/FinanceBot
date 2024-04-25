"""
Pre Services
---
This module defines services that process user requests before script transition.
"""
from dff.script import Context

from faq_model.model import find_similar_questions
from pipeline_services.ner_service import get_company_name
from pipeline_services.parsers import get_last_price_tinkoff





def question_processor(ctx: Context):
    """Store questions similar to user's query in the `annotations` field of a message."""
    last_request = ctx.last_request
    if last_request is None:
        return
    else:
        if last_request.annotations is None:
            last_request.annotations = {}
        else:
            if last_request.annotations.get("similar_questions") is not None:
                return
        if last_request.text is None:
            last_request.annotations["similar_questions"] = None
        else:
            similar_questions = find_similar_questions(last_request.text)
            print(f"{similar_questions=}")
            if similar_questions[0] ==  'Сколько стоит акция компании?':
                company_name = get_company_name(last_request.text)
                price = get_last_price_tinkoff(company_name)
                last_request.annotations["answer"] = f"Цена акции {company_name} = {price}"
            last_request.annotations["similar_questions"] = similar_questions

    ctx.set_last_request(last_request)


services = [question_processor]  # pre-services run before bot sends a response
