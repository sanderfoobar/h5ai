import re

def table_print(data, title_row):
    """
    data: list of dicts,
    title_row: e.g. [('name', 'Programming Language'), ('type', 'Language Type')]
    """
    max_widths = {}
    data_copy = [dict(title_row)] + list(data)
    for col in data_copy[0].keys():
      max_widths[col] = max([len(str(row[col])) for row in data_copy])
    cols_order = [tup[0] for tup in title_row]

    def custom_just(col, value):
      if type(value) == int:
        return str(value).rjust(max_widths[col])
      else:
        return value.ljust(max_widths[col])

    for row in data_copy:
      row_str = " | ".join([custom_just(col, row[col]) for col in cols_order])
      print "| %s |" % row_str
      if data_copy.index(row) == 0:
        underline = "-+-".join(['-' * max_widths[col] for col in cols_order])
        print '+-%s-+' % underline

