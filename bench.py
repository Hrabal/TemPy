import cProfile
import pstats
from io import StringIO
from tempy.tags import Table, Tr, Td, Div
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
         j='k') for x in range(1000)
]

tables = []
pr = cProfile.Profile()
pr.enable()
for _ in range(1000):
    tables.append(
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
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())

pr = cProfile.Profile()
pr.enable()
for t in tables:
    t.render()
pr.disable()
s = StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())

pr = cProfile.Profile()
pr.enable()
cont = Div()
for _ in range(100000):
    cont(Div())
pr.disable()
s = StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
