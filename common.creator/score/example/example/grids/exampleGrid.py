# coding: utf-8
from lyra.gridForm import GridForm
from lyra.basicForm import form
from lyra.basicForm import formfield
from example._example_orm import ExampleCursor
from common.filtertools.filter import filtered_function
from java.text import SimpleDateFormat
from common.api.context.sessioncontext import SessionContext


@form(
    gridwidth='100%',
)
class ExampleGridForm(GridForm):
    def __init__(self, context):
        super(ExampleGridForm, self).__init__(context)
        self.createField('first_column1')
        self.createField('second_column1')
        self.createField('third_column1')
        self.createField('fourth_column1')
        self.createField('fifth_column1')
        gridheight = SessionContext(context.getShowcaseContext().getSession()).getGridHeight()
        self.getFormProperties().setGridheight(str(gridheight  -20) + "px")

    @formfield(celestatype='VARCHAR',
               caption=u'Кол-во реализованных проектов',
               visible=True,
               width=50)
    def first_column1(self):
        t = self.rec().first_column
        return str(t) if t else u'0'

    @formfield(celestatype='VARCHAR',
               caption=u'ФИО',
               visible=True,
               width=50)
    def second_column1(self):
        t = self.rec().second_column
        return t if t else ''

    @formfield(celestatype='VARCHAR',
               caption=u'На каком языке пишите код',
               visible=True,
               width=50)
    def third_column1(self):
        t = self.rec().third_column
        if t == u'python':
            return u'Питон'
        elif t == u'Java':
            return u'Джава'

    @formfield(celestatype='VARCHAR',
               caption=u'Курс круче всех?',
               visible=True,
               width=50)
    def fourth_column1(self):
        t = self.rec().fourth_column
        if t is True:
            return u'Да'
        else:
            return ''

    @formfield(celestatype='VARCHAR',
               caption=u'Дата начала работы в компании',
               visible=True,
               width=60)
    def fifth_column1(self):
        t = self.rec().fifth_column
        return SimpleDateFormat('dd.MM.yyyy').format(t) if t else ''


    def _getCursor(self, context):
        c = ExampleCursor(context)
        filter_name = 'yourExampleFilter'
        if filter_name in context.getData().get('card_save', []):
            unbound_dict = filtered_function(context, filter_name, c)
            local_filter(context, c, unbound_dict)
        c.orderBy('guid DESC')
        return c


    def getGridHeight(self):
        return 50

def local_filter(context, cursor, unbound_dict):
    u"Фильтрация данных в курсоре фильтром"

