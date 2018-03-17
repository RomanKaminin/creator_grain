# coding: UTF-8
import json
from common.api.context.sessioncontext import SessionContext
from common.api.events.action import Action
from common.api.events.activities import DatapanelElement, NavigatorActivity
from common.api.events.events import Event
from common.filtertools.filter import filter_assembly, filtered_function
from common.filtertools.filter_cards_gen import card_info, card_save
from example._example_orm import ExampleCursor

from ru.curs.celesta.showcase.utils import XMLJSONConverter

try:
    from ru.curs.showcase.core.jython import JythonDTO
except:
    from ru.curs.celesta.showcase import JythonDTO

def getField():
    field = [
        {
            "name": "first_column",
            "label": u"Кол-во реализованных проектов",
            "type": "INT",
        },
        {
            "name": "second_column",
            "label": u"ФИО",
            "type": "TEXT",
        },
        {
            "name": "fifth_column",
            "label": u"Дата начала работы в компании",
            "type": "DATE",
        },
        {
            "name": "third_column",
            "label": u"На каком языке пишите код",
            "type": "TEXT",
            "select":
                {   'python': u'Питон',
                    'Java': u'Джава',
                    },
        },

    ]

    return field


def cardData(context, main=None, add=None, filterinfo=None,
             session=None, elementId=None):
    u"""Процедура, описывающая структуру фильтра для карточки телеграмм"""
    session_obj = SessionContext(session)
    if elementId not in context.getData():
        # Курсор фильтруемой таблицы
        cur = ExampleCursor(context)
        # Функция, собирающая данные каждого поля, которое необходимо фильтровать

        field_list = getField()
        filter_assembly(context, cur, elementId,
                        field_list, "example.Example")# Гранула.таблица

    xforms_data = {
        "schema": {
            "@xmlns": "",
            "filters": {"filter": card_info(context, elementId)}
        }
    }

    xforms_data["schema"]["@maxFilters"] = len(context.getData()[elementId])

    xforms_settings = {
        "properties": {
            "event": [
                {
                    "@name": "single_click",
                    "@linkId": "1",
                    "action": {
                        "@keep_user_settings": 'false',
                        "main_context": "current",
                        "datapanel": {
                            "@type": "current",
                            "@tab": "current",
                            "element": {
                                "@id": 'yourExampleGrid'
                            }
                        }
                    }
                }
            ]
        }
    }


    return JythonDTO(XMLJSONConverter.jsonToXml(json.dumps(xforms_data)),
                     XMLJSONConverter.jsonToXml(json.dumps(xforms_settings)))


def cardSave(context, main=None, add=None, filterinfo=None, session=None,
             elementId=None, xformsdata=None):
    xformsdata = json.loads(xformsdata)
    card_save(xformsdata, context, elementId)

