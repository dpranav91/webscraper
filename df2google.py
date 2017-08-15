import pdb
from df2gspread import df2gspread as d2g
from df2gspread import gspread2df as g2d


class DF2GoogleSpreadSheet:
    def __init__(self, spreadsheet='1uMa11jIIYyKMj2o73fgdHzYI5IUNdPzZzu_pocwoUx0', sheetname='Sheet1'):
        self.spreadsheet = spreadsheet
        self.sheetname = sheetname

    def upload(self, df, sheetname=None, max_retry_count=3):
        sheetname = sheetname if sheetname else self.sheetname
        counter = 0
        while counter < max_retry_count:
            try:
                return d2g.upload(df, self.spreadsheet, sheetname)
            except Exception as e:
                counter += 1
                error = e
        raise Exception(error)
        # logger and logger.info("DataFrame got uploaded to {}: {}".format(self.spreadsheet, sheetname))

    def download(self, max_retry_count=3):
        counter = 0
        while counter < max_retry_count:
            try:
                return g2d.download(self.spreadsheet, self.sheetname, col_names=True, row_names=True)
            except Exception as e:
                counter += 1
                # error = e
        return None
        # logger and logger.error("No SpreadSheet found with {}".format(self.spreadsheet))


if __name__ == '__main__':
    obj = DF2GoogleSpreadSheet()
    print(obj.download())

    import pandas as pd

    d = [pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
         pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])]
    df = pd.DataFrame(d)
    # pdb.set_trace()
    res = obj.upload(df, 'sheet 2')
    print("Upload Done: {}".format(res))
