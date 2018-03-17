# coding: utf-8
from common.api.datapanels.grids import LyraGrid
from example.grids import exampleGrid
from example.toolbars import exampleToolbar
from example.filters import exampleFilter
from example.cards import exampleCard
from common.api.datapanels.datapanel import XForm,  Datapanel, Tab

def exampleDatapanel(context, main=None, session=None):
    data = Datapanel()
    tab1 = Tab('1', u'Название тестовой датапанели')

    # грид
    yourExampleGrid = LyraGrid(u"yourExampleGrid",
                               exampleGrid.ExampleGridForm) \
        .setToolbarProc(exampleToolbar.gridToolBar)
    tab1.addElement(yourExampleGrid)

    # форма добавления записей в грид
    exampleEditCard = XForm(u"exampleCard",
                        u"exampleCard.xml",
                         exampleCard.cardData) \
        .setSaveProc(exampleCard.cardSave) \
        .setNeverShowInPanel(True) \
        .addRelated(yourExampleGrid)
    tab1.addElement(exampleEditCard)

    # фильтр по записям грида
    yourExampleFilter = XForm(u"yourExampleFilter",
                           u"filter_card/generalFilterCard.xml",
                           exampleFilter.cardData) \
        .setNeverShowInPanel(True) \
        .setSaveProc(exampleFilter.cardSave) \
        .addRelated(yourExampleGrid)
    tab1.addElement(yourExampleFilter)


    data.addTab(tab1)
    return data.toXML()
