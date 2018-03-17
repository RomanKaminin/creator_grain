# coding: utf-8
import json
from java.text import SimpleDateFormat
from common.api.events.action import Action, DatapanelElement, DatapanelActivity
from common.api.events.events import Event, EVENT_TAG
from common.api.context.sessioncontext import SessionContext
from example._example_orm import ExampleCursor
from common.api.utils.tools import createJythonDTO
import uuid


def cardData(context, main=None, add=None, filterinfo=None, session=None, elementId=None):
    u'''Данные для карточки.'''
    grid_context = SessionContext(session).getGridContext()

    if add == 'add':
        xforms_data = {
            "schema": {
                "@xmlns": "",
                "context": {
                    "guid": str(uuid.uuid4()),
                    "first_column": "",
                    "second_column": "",
                    "third_column": "",
                    "fourth_column": "",
                    "fifth_column": "",
                }
            }
        }

    event_save = Event("event_save").setAction(
        Action().addActivity(
            DatapanelActivity()
                .setPanel("current")
                .setTab("current")
                .addElement(
                DatapanelElement(grid_context.id, None)
            )
        )
    )

    xforms_settings = {
        "properties": {
            EVENT_TAG: [event_save.toJSONDict()]
        }
    }
    return createJythonDTO(xforms_data, xforms_settings)


def cardSave(context, main=None, add=None, filterinfo=None, session=None, elementId=None, xformsdata=None):
    u'''Сохранение карточки. '''

    exam_cur = ExampleCursor(context)
    xformsdata = json.loads(xformsdata)['schema']['context']

    if add == 'add':
        exam_cur.guid = str(uuid.uuid4())
    exam_cur.first_column = None if xformsdata['first_column'] == "" else xformsdata['first_column']
    exam_cur.second_column = None if xformsdata['second_column'] == "" else xformsdata['second_column']
    exam_cur.third_column = None if xformsdata['third_column'] == "" else xformsdata['third_column']
    exam_cur.fourth_column = True if xformsdata['fourth_column'] == 'true' else False
    exam_cur.fifth_column = None if xformsdata['fifth_column'] == "" else SimpleDateFormat("yyyy-MM-dd").parse(xformsdata['fifth_column'])

    if add == 'add':
        exam_cur.insert()
