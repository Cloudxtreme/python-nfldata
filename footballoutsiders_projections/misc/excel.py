import collections
from xlrd import open_workbook

wb = open_workbook('2015 KUBIAK 20150817.xls')

def column_headers(s):

    colnames = {}

    # create mapping of original column name to column index
    for colidx in range(s.ncols):
        colname = str(s.cell(0,colidx).value).lower()
        colnames[colname] = colidx

    # now create ordered dictionary of the columns I want and the respective index
    wanted_cols_od = collections.OrderedDict()
    wanted_cols = ['fo id', 'key', 'player', 'team', 'pos', 'age', 'risk', 'bye', 'dynamic fantasy points']
    cols_transform = {'player': 'name', 'fo id': 'fo_player_id', 'dynamic fantasy points': 'fpts'}

    for wcn in wanted_cols:
        idx = colnames.get(wcn, None)

        # transform column names
        transformed = cols_transform.get(wcn, None)
        if transformed:
            wanted_cols_od[transformed] = idx
        else:
            wanted_cols_od[wcn] = idx

    return wanted_cols_od

def is_not_idp(val):

    if 'IDP' in val:
        return False

    else:
        return True

for s in wb.sheets():

    if s.name == '2015 KUBIAK Projections':

        wanted_columns = column_headers(s)
        print ','.join(wanted_columns.keys())

        for rowidx in range(1,s.nrows):

            if is_not_idp(str(s.cell(rowidx, wanted_columns['pos']).value)):

                row_cells = []

                for colname, colidx in wanted_columns.items():

                    if colname in ['bye', 'age']:

                        try:
                            row_cells.append(str(int(s.cell(rowidx,colidx).value)))

                        except:
                           row_cells.append(str(s.cell(rowidx,colidx).value))

                    else:
	                    row_cells.append(str(s.cell(rowidx,colidx).value))

                print ','.join(row_cells)
