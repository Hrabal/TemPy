import cProfile
import pstats
from io import StringIO
from tempy.tags import Table, Tr, Td, Div
from tempy.widgets import TempyPage
TABLE_DATA = [
    dict(a='a',
         b='b',
         c='c',
         d='d',
         e='e',
         f='f',
         g='g',
         h='h',
         i='i',
         j='k') for x in range(100)
]

page = TempyPage()
pr = cProfile.Profile()
pr.enable()
for _ in range(100):
    page.body(
        Div()(
            table=Table()(
                Tr(id='%s' % i)(
                    Td(klass='CIAO', id='%s-%s' % (i, td))(cont=td) for td in tr.values()
                ) for i, tr in enumerate(TABLE_DATA)
            )
        )
    )
pr.disable()
s = StringIO()
sortby = 'tottime'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
print('*' * 200)
print('CREATION')
ps.print_stats()
print(s.getvalue())

pr = cProfile.Profile()
pr.enable()
render = page.render()
pr.disable()
s = StringIO()
sortby = 'tottime'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
print('*' * 200)
print('RENDERING')
ps.print_stats()
print(s.getvalue())
print(render)