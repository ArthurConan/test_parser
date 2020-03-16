from app import parser

routes = (
    dict(method='GET', path='/{letter:[aA-zZ]{0,1}}', handler=parser.Parser, name='parser'),
)