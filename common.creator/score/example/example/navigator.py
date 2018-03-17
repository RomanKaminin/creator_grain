#coding: utf-8
import json
from common.api.datapanels.datapanel import TabOrder
from common.api.events.action import Action
from common.api.events.activities import DatapanelActivity
from common.api.navigator.node import NavigatorNode

def exampleNavigator(context, session=None):
    session_json = json.loads(session)['sessioncontext']
    # создаём корневой фиктивный узел (не отображаемый)
    rootNode = NavigatorNode('root', 'root')

    # далее строим дерево, добавляя дочерние узлы, если требуется.
    # Класс NavigatorNode сам определяет уровни узлов - group, level

    # создаём узел раздела 1
    exampleMain = NavigatorNode('example', u'Тестовый раздел')

    # пункт раздела 11
    exampleSub = NavigatorNode('exampleSub', u'Тестовы подраздел').setSelectOnLoad(True)
    exampleSub.setAction(
        Action().addActivity(
            DatapanelActivity('example.datapanels.exampleDatapanel.exampleDatapanel.celesta', TabOrder.FIRST_OR_CURRENT)
        )
    )
    exampleMain.addChild(exampleSub)
    rootNode.addChild(exampleMain)

    return rootNode.toJSONDict()
