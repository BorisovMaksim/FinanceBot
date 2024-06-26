import pytest
from dff.utils.testing.common import check_happy_path
from dff.messengers.telegram import TelegramMessage, TelegramUI
from dff.script import RESPONSE
from dff.script.core.message import Button


from typing import Any, Optional

from dff.script import Context, Message

from dialog_graph import script
from run import get_pipeline
from faq_model.model import faq




def default_comparer(candidate: Message, reference: Message, _: Context) -> Optional[Any]:
    """
    The default response comparer. Literally compares two response objects.

    :param candidate: The received (candidate) response.
    :param reference: The true (reference) response.
    :param _: Current Context (unused).
    :return: `None` if two responses are equal or candidate response otherwise.
    """
    return None if candidate == reference else candidate


def is_in_comparer(candidate: Message, reference: Message, _: Context) -> Optional[Any]:
    """
    The default response comparer. Literally compares two response objects.

    :param candidate: The received (candidate) response.
    :param reference: The true (reference) response.
    :param _: Current Context (unused).
    :return: `None` if two responses are equal or candidate response otherwise.
    """
    return None if reference.text in candidate.text else candidate




@pytest.mark.asyncio
@pytest.mark.parametrize(
    "happy_path_equal",
    [
        (
            (TelegramMessage(text="/start"), script.script["qa_flow"]["welcome_node"][RESPONSE]),
             (
                TelegramMessage(text="Какое определение у облигации?"),
                TelegramMessage(text=faq["Что такое облигации?"]),
            ),
              (
                TelegramMessage(text="Почему злобные евреи крадут все деньги?"),
                TelegramMessage(text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"),
            ),
              
            (
                TelegramMessage(text="воыфшод23к-щаыф"),
                TelegramMessage(text="Вопрос слишком сложный..."),
            ),
            
             (
                TelegramMessage(text="Сколько стоит акция компании ГашДоноц?"),
                TelegramMessage(text="Не нашел акцию компании ГашДоноц. Попробуйте ввести полное название компании"),
            ),
            
        )
    ],
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "happy_path_isin",
    [
        (
            (TelegramMessage(text="/start"), script.script["qa_flow"]["welcome_node"][RESPONSE]),
            (
                TelegramMessage(text="Сколько стоит акция Яндекс?"),
                TelegramMessage(text="По вашему запросу найдены следующие акции"),
            ),
        )
    ],
)



async def test_happy_path(happy_path_equal, happy_path_isin):
    check_happy_path(pipeline=get_pipeline(use_cli_interface=True), 
                     happy_path=happy_path_equal, 
                     response_comparer=default_comparer)
    
    check_happy_path(pipeline=get_pipeline(use_cli_interface=True), 
                     happy_path=happy_path_isin, 
                     response_comparer=is_in_comparer)
    
