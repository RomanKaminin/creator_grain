# coding: utf-8
from common.api.events.action import Action, ModalWindow
from common.api.events.activities import DatapanelElement
from common.filtertools.filter_cards_gen import add_filter_buttons
from common.api.datapanels.grids import Toolbar, ToolbarItem
try:
    from ru.curs.showcase.core.jython import JythonDTO
except:
    from ru.curs.celesta.showcase import JythonDTO




def gridToolBar(context, main=None, add=None, filterinfo=None, session=None, elementId=None):
    u'''Toolbar для грида '''

    toolBar = Toolbar()
    enableActiveButton = True

    toolBar.addItem(
        ToolbarItem("exampleCard")
            .setCaption(u"Добавить")
            .setHint(u"Добавить")
            .setAction(
            Action().add(DatapanelElement("exampleCard", "add")
                         )
                .showIn(ModalWindow(u"Добавить", 500, 400).setCloseOnEsc(enableActiveButton)
                        )
        )
    )
    toolBar.addItem(add_filter_buttons(filter_id=u"yourExampleFilter", session=session, is_object=True))

    return toolBar.toXML()
