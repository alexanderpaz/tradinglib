#  Copyright (c) Alex Paz 2018. Todos los derechos reservados
import pandas as pd


class IO:

    @staticmethod
    def leer_csv_mt4(fullpath=None, archivo=None):
        if fullpath is None:
            data = pd.read_csv('../data/{}.csv'.format(archivo), header=None)
        if archivo is None:
            data = pd.read_csv(fullpath, header=None)
        data.columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
        data.set_index('DateTime', inplace=True)
        data.drop(['Date', 'Time'], axis=1, inplace=True)
        return data
