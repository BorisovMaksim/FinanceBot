"""
Script
--------
This module defines a script that the bot follows during conversation.
"""
from dff.script import RESPONSE, TRANSITIONS, LOCAL
import dff.script.conditions as cnd
from dff.messengers.telegram import TelegramMessage

from .responses import answer_question
from .conditions import received_text

from .conditions_goals import (
    received_text_wrong_risk, received_text_node_1, 
    received_text_node_2, received_text_node_3,
    received_text_node_4, received_text_node_5,
    received_text_node_6, received_text_node_7,
    received_text_node_8, received_text_node_9,
    received_text_node_10, received_text_node_11,
    received_text_node_12, received_text_node_13,
    received_text_node_14, received_loan, received_wrong_value,
    received_init_pay, received_init_pay_wrong,
    received_interest, received_period, received_period_wrong
    )
from .responses_goals import response_handler_risk, response_handler_loan

script = {
    "service_flow": {
        "start_node": {
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/start")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/start_loan_calc")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/start_risk_profile"))
                },
        },
        "fallback_node": {
            RESPONSE: TelegramMessage(text="Something went wrong. Use `/restart` or `/restart_loan_calc` or `/restart_risk_profile` to start over."),
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile"))
                },
        },
    },

    "qa_flow": {
        LOCAL: {
            TRANSITIONS: {                
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                ("qa_flow", "answer_question"): received_text,
            },
        },
        "welcome_node": {
            RESPONSE: TelegramMessage(text="Привет! Задай вопрос о финансах."),
        },
        "answer_question": {
            RESPONSE: answer_question,
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                },
        },
    },

     "loan_flow": {
         LOCAL: {
            TRANSITIONS: {("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/start_loan_calc"))},
        }, 

        "node1": {
            RESPONSE: TelegramMessage(
                text="Рассчитаем ежемесячный платеж и переплату по ипотеке. Пожалуйста, вводите неотрицательные значения в числовом формате. Какова сумма ипотеки?"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1_wrong":received_wrong_value,
                "node2":received_loan,
            },
        },

         "node1_wrong": {
            RESPONSE: TelegramMessage(
                text="Пожалуйста, введите корректное значение (неотрицательное число)"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1_wrong":received_wrong_value,
                "node2":received_loan,
            },
        },
        "node2": {
            RESPONSE: TelegramMessage(
                text="Какова сумма первоначального взноса?"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node2_wrong_1":received_wrong_value,
                "node2_wrong_2":received_init_pay_wrong,
                "node3":received_init_pay,
            },
        },

         "node2_wrong_1": {
            RESPONSE: TelegramMessage(
                text="Пожалуйста, введите корректное значение в числовом формате"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node2_wrong_1":received_wrong_value,
                "node2_wrong_2":received_init_pay_wrong,
                "node3":received_init_pay,
            },
        },

         "node2_wrong_2": {
            RESPONSE: TelegramMessage(
                text="Первоначальный взнос не может быть больше суммы ипотеки. Пожалуйста, введите корректное значение"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node2_wrong_1":received_wrong_value,
                "node2_wrong_2":received_init_pay_wrong,
                "node3":received_init_pay,
            },
        },

        "node3": {
            RESPONSE: TelegramMessage(
                text="Какова годовая процентная ставка?"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node3_wrong":received_wrong_value,
                "node4":received_interest,
            },
        },

        "node3_wrong": {
            RESPONSE: TelegramMessage(
                text="Пожалуйста, введите корректное значение в числовом формате"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node3_wrong":received_wrong_value,
                "node4":received_interest,
            },
        },

        "node4": {
            RESPONSE: TelegramMessage(
                text="Каков срок ипотеки в годах?"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node4_wrong_1":received_wrong_value,
                "node4_wrong_2":received_period_wrong,
                "node5":received_period,
            },
        },

        "node4_wrong_1": {
            RESPONSE: TelegramMessage(
                text="Пожалуйста, введите корректное значение в числовом формате"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node4_wrong_1":received_wrong_value,
                "node4_wrong_2":received_period_wrong,
                "node5":received_period,
            },
        },

        "node4_wrong_2": {
            RESPONSE: TelegramMessage(
                text="Пожалуйста, введите число больше 0"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node4_wrong_1":received_wrong_value,
                "node4_wrong_2":received_period_wrong,
                "node5":received_period,
            },
        },

        "node5": {
            RESPONSE: response_handler_loan,
            TRANSITIONS: {
            "node1": cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
            ("risk_flow", "node1"): cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
            ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
            },
        },
    },
    "risk_flow": {
        LOCAL: {
            TRANSITIONS: {("risk_flow","node1"): cnd.exact_match(TelegramMessage(text="/start_risk_profile"))},
        },

        "node1": {
            RESPONSE: TelegramMessage(
                text="Определим Ваш риск-профиль: консервативный, умеренный или рискованный. Какие инвестиционные задачи вы преследуете (например, защита основного капитала и получение умеренного дохода, рост активов или получение значительного текущего дохода)?"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1_wrong":received_text_wrong_risk,
                "node2":received_text_node_1,
            },
        },

        "node1_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node1_wrong":received_text_wrong_risk,
                "node2":received_text_node_1,
            },
        },

        "node2": {
            RESPONSE: TelegramMessage(
                text="На какой срок в годах Вы готовы инвестировать средства?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node2_wrong":received_text_wrong_risk,
                "node3":received_text_node_2,
            }
        },

        "node2_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node2_wrong":received_text_wrong_risk,
                "node3":received_text_node_2,
            },
        },

        "node3": {
            RESPONSE: TelegramMessage(
                text="Какой объем Ваших финансовых активов Вы планируете инвестировать (в рублях)?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node3_wrong":received_text_wrong_risk,
                "node4":received_text_node_3
            },
        },

        "node3_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node3_wrong":received_text_wrong_risk,
                "node4":received_text_node_3,
            },
        },

         "node4": {
            RESPONSE: TelegramMessage(
                text="Планируете ли Вы использовать инвестируемые средства для финансирования ежедневных расходов?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node4_wrong":received_text_wrong_risk,
                "node5":received_text_node_4
            },
        },

        "node4_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node4_wrong":received_text_wrong_risk,
                "node5":received_text_node_4,
            },
        },

        "node5": {
            RESPONSE: TelegramMessage(
                text="Будете ли Вы принимать более высокий риск для достижения более высокого потенциального прироста?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node5_wrong":received_text_wrong_risk,
                "node6":received_text_node_5
            },
        },

        "node5_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node5_wrong":received_text_wrong_risk,
                "node6":received_text_node_5,
            },
        },

        "node6": {
            RESPONSE: TelegramMessage(
                text="Есть ли у вас опыт в качестве инвестора?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node6_wrong":received_text_wrong_risk,
                "node7":received_text_node_6
            },
        },

        "node6_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node6_wrong":received_text_wrong_risk,
                "node7":received_text_node_6,
            },
        },

        "node7": {
            RESPONSE: TelegramMessage(
                text="Готовы ли вы к тому, что ваш инвестиционный капитал может снизиться?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node7_wrong":received_text_wrong_risk,
                "node8":received_text_node_7
            },
        },

        "node7_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node7_wrong":received_text_wrong_risk,
                "node8":received_text_node_7,
            },
        },

        "node8": {
            RESPONSE: TelegramMessage(
                text="Есть ли вероятность, что Вы захотите изъять большую часть или всю инвестированную сумму досрочно, до истечения предполагаемого срока инвестиций?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node8_wrong":received_text_wrong_risk,
                "node9":received_text_node_8
            },
        },

        "node8_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node8_wrong":received_text_wrong_risk,
                "node9":received_text_node_9,
            },
        },

        "node9": {
            RESPONSE: TelegramMessage(
                text="Сформирован ли у вас резервный фонд (подушка безопасности), и если да, то в каком размере (в рублях)?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node9_wrong":received_text_wrong_risk,
                "node10":received_text_node_9
            },
        },

        "node9_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node9_wrong":received_text_wrong_risk,
                "node10":received_text_node_9,
            },
        },

        "node10": {
            RESPONSE: TelegramMessage(
                text="Вы владеете частной собственностью? Если да, то какой?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node10_wrong":received_text_wrong_risk,
                "node11":received_text_node_10
            },
        },

        "node10_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node10_wrong":received_text_wrong_risk,
                "node11":received_text_node_10,
            },
        },

        "node11": {
            RESPONSE: TelegramMessage(
                text="Примерно через сколько лет Вы планируете отойти от дел, жить на пассивный доход (пенсию)?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node11_wrong":received_text_wrong_risk,
                "node12":received_text_node_11
            },
        },

        "node11_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node11_wrong":received_text_wrong_risk,
                "node12":received_text_node_11,
            },
        },

        "node12": {
            RESPONSE: TelegramMessage(
                text="Какова сумма Вашей ежемесячной разницы между доходами и расходами?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node12_wrong":received_text_wrong_risk,
                "node13":received_text_node_12
            },
        },

        "node12_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node12_wrong":received_text_wrong_risk,
                "node13":received_text_node_12,
            },
        },

        "node13": {
            RESPONSE: TelegramMessage(
                text="Есть ли у Вас долговые обязательства?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node13_wrong":received_text_wrong_risk,
                "node14":received_text_node_13
            },
        },

        "node13_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node13_wrong":received_text_wrong_risk,
                "node14":received_text_node_13,
            },
        },

        "node14": {
            RESPONSE: TelegramMessage(
                text="Сколько вам лет?"
            ),  
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node14_wrong":received_text_wrong_risk,
                "node15":received_text_node_14
            }
        },
        
        "node14_wrong": {
            RESPONSE: TelegramMessage(
                text="Ваше сообщение содержит недопустимый контент. Пожалуйста, переформулируйте запрос"
            ), 
            TRANSITIONS: {
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow","node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                "node14_wrong":received_text_wrong_risk,
                "node15":received_text_node_14,
            },
        },

        "node15": {
            RESPONSE:
                response_handler_risk,  
            TRANSITIONS: {
                "node1": cnd.exact_match(TelegramMessage(text="/restart_risk_profile")),
                ("qa_flow", "welcome_node"): cnd.exact_match(TelegramMessage(text="/restart")),
                ("loan_flow", "node1"): cnd.exact_match(TelegramMessage(text="/restart_loan_calc")),
            },
        },
    },
}

