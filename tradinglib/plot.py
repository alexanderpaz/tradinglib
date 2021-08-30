#  Copyright (c) Alex Paz 2018. Todos los derechos reservados

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches, ticker

from matplotlib.dates import date2num
from matplotlib.ticker import FuncFormatter


class Plotter:

    def __init__(self, data_ohlc):
        self.__data = data_ohlc
        self.__formato_eje_mayor = ''
        self.__formato_eje_menor = ''

    def __encuentra_inicio_de_dias(self):
        pos = 0
        lista = []
        for v in date2num(self.__data.index.values):
            if v - int(v) == 0:
                lista.append(pos)
            pos += 1
        return lista

    def __encuentra_meses(self, freq=1):
        lista = []
        acumulado = 0
        lista.append(acumulado)
        anhos = self.__data.index.groupby(self.__data.index.year)
        for anho in anhos:
            meses = anhos[anho].groupby(anhos[anho].month)
            for mes in meses:
                acumulado += len(meses[mes])
                lista.append(acumulado)
        return lista[::freq]

    def __encuentra_anhos(self):
        lista = []
        acumulado = 0
        lista.append(acumulado)
        anhos = self.__data.index.groupby(self.__data.index.year)
        for anho in anhos:
            acumulado += len(anhos[anho])
            lista.append(acumulado)
        return lista

    def __format_date_major(self, x, pos=None):
        thisind = np.clip(int(x + 0.5), 0,
                          len(self.__data) - 1)  # np.clip(x, 0, len(data) - 1) # np.clip(int(x + 0.5), 0, len(data) - 1)
        return self.__data.index[thisind].strftime(self.__formato_eje_mayor)

    def __format_date_minor(self, x, pos=None):
        thisind = np.clip(int(x + 0.5), 0,
                          len(self.__data) - 1)  # np.clip(x, 0, len(data) - 1) # np.clip(int(x + 0.5), 0, len(data) - 1)
        return self.__data.index[thisind].strftime(self.__formato_eje_menor)

    def __procesar_formato(self, ax):
        anhos = self.__encuentra_anhos()

        if len(anhos) > 2:
            # Eje mayor
            ax.set_xticks(anhos, minor=False)
            self.__formato_eje_mayor = '%Y'

            # Eje menor
            if len(anhos) > 4:
                ax.set_xticks(self.__encuentra_meses(freq=4), minor=True)
                self.__formato_eje_menor = '%m'
            else:
                ax.set_xticks(self.__encuentra_meses(freq=1), minor=True)
                self.__formato_eje_menor = '%b'
        else:
            meses = self.__encuentra_meses()
            if len(meses) > 2:
                # Eje mayor
                ax.set_xticks(meses, minor=False)
                self.__formato_eje_mayor = '%b'

                # Eje menor
                ax.set_xticks(self.__encuentra_inicio_de_dias(), minor=True)
                self.__formato_eje_menor = '%d'
            else:

                dias = self.__encuentra_inicio_de_dias()
                if len(dias) > 3:
                    # Eje mayor
                    ax.set_xticks(dias, minor=False)
                    self.__formato_eje_mayor = '%b-%d'
                    # Eje menor
                    ax.set_xticks(np.arange(dias[0] - (np.floor(dias[0] / 6) * 6), self.__data.shape[0], 6), minor=True)
                    self.__formato_eje_menor = '%H'
                    # ax.xaxis.set_minor_locator(MaxNLocator(20)) # MultipleLocator(int(10 * len(data) / 10)))
                    # ax.xaxis.set_minor_locator(LinearLocator(numticks=len(dias)*2))
                else:
                    # Eje mayor
                    ax.set_xticks(dias, minor=False)
                    self.__formato_eje_mayor = '%b-%d'

                    # Eje menor
                    ax.set_xticks(np.arange(dias[0] - (np.floor(dias[0] / 4) * 4), self.__data.shape[0], 4), minor=True)
                    self.__formato_eje_menor = '%H'

        ax.xaxis.set_major_formatter(FuncFormatter(self.__format_date_major))  # FuncFormatter(mi_formatter))
        ax.xaxis.set_minor_formatter(FuncFormatter(self.__format_date_minor))

        ax.tick_params(axis='x', which='minor', bottom=True)
        ax.tick_params(axis='x', which='major', pad=15)

    def plot_line(self, ax):

        self.__procesar_formato(ax)
        ax.plot(np.arange(0, len(self.__data)), self.__data.Close.values)

    def plot_candlestick(self, ax, velas=36, ancho_vela=0.2, ancho_mecha=1.0, grid_alpha=0.3, dt_format='%d %b - %Hh',
                         color_vela_bull='green', color_vela_bear='red', titulo=None):

        self.__procesar_formato(ax)
        self.__data.sort_index(ascending=True)

        if len(self.__data < velas):
            velas = len(self.__data)

        maximo = (self.__data.High[-velas:].max() * 1.0001).round(decimals=4)
        minimo = (self.__data.Low[-velas:].min() * 0.9990).round(decimals=4)
        eje_y = np.arange(minimo.round(decimals=5), maximo.round(decimals=4), 0.00055)

        #plt.xticks(np.arange(0, velas, 1), data[-velas:].index.strftime(dt_format))  # :%M'))
        #plt.yticks(eje_y, eje_y)
        #ax.tick_params(axis='x', labelrotation=70, labelsize='small', grid_alpha=grid_alpha, grid_linestyle='dashed',
        #               grid_color='grey')
        #ax.tick_params(axis='y', grid_alpha=grid_alpha, grid_linestyle='dashed', grid_color='grey')
        # ax.xaxis.set_major_locator(ticker.MaxNLocator(20))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(20))
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.5f}'))
        ax.grid()
        gridlines = ax.get_xgridlines() + ax.get_ygridlines()
        plt.setp(gridlines, 'zorder', 1)

        #plt.subplots_adjust(left=.13, bottom=.2, right=.90, top=.92, wspace=.2, hspace=.05)
        if titulo is not None:
            plt.suptitle(titulo)

        for i in range(0, velas, 1):
            valores = self.__data[['Open', 'High', 'Low', 'Close']].iloc[i - velas].values
            valores.sort()
            if self.__data.Open.iloc[i - velas] > self.__data.Close.iloc[i - velas]:  # Bear candle
                ax.plot([i, i], [valores[0], valores[3]], 'r-', lw=ancho_mecha)
                rect = patches.Rectangle((i - ancho_vela, valores[1]), ancho_vela * 2, valores[2] - valores[1],
                                         linewidth=1,
                                         edgecolor=color_vela_bear, facecolor=color_vela_bear, zorder=2)
                ax.add_patch(rect)
            else:  # Bull candle
                ax.plot([i, i], [valores[0], valores[3]], 'g-', lw=ancho_mecha)
                # Create a Rectangle patch
                rect = patches.Rectangle((i - ancho_vela, valores[1]), ancho_vela * 2, valores[2] - valores[1],
                                         linewidth=1,
                                         edgecolor=color_vela_bull, facecolor=color_vela_bull, zorder=2)
                # Add the patch to the Axes
                ax.add_patch(rect)


    @staticmethod
    def plot_candlestick_timeindex(ax,
                                   fuente,
                                   velas=20,
                                   color_vela_bull='green',
                                   color_vela_bear='red',
                                   color_borde_bull='green',
                                   color_borde_bear='red',
                                   color_mecha_bull='green',
                                   color_mecha_bear='red',
                                   ancho_mecha=1.0,
                                   ancho_vela=0.4):
        # Acotar los datos
        datos = fuente.iloc[-velas:]

        # Setear los límites de Y
        miny = datos.Low.min()
        maxy = datos.High.max()
        miny_actual, maxy_actual = ax.get_ylim()
        if maxy > maxy_actual:
            maxy_actual = maxy * 1.002
            miny_actual *= 0.998
        if miny < miny_actual:
            maxy_actual *= 1.002
            miny_actual = miny * 0.998
        ax.set_ylim((miny_actual, maxy_actual))

        # Ploteo
        for i in range(0, velas):
            # iteracion
            idx = datos.index[i]

            punto_bajo = (datos.Low[i] - miny_actual) / (maxy_actual - miny_actual)
            punto_alto = (datos.High[i] - miny_actual) / (maxy_actual - miny_actual)

            if datos.Close[i] < datos.Open[i]:  # vela bear
                line = ax.axvline(idx, ymin=punto_bajo, ymax=punto_alto, c=color_mecha_bear, lw=ancho_mecha, zorder=2)
                r = patches.Rectangle((line.get_xdata(orig=False)[0] - (ancho_vela / 2), datos.Close[i]),
                              width=ancho_vela,
                              height=(datos.Open[i] - datos.Close[i]),
                              edgecolor=color_borde_bear,
                              facecolor=color_vela_bear,
                              zorder=3)
                ax.add_patch(r)
            else:
                line = ax.axvline(idx, ymin=punto_bajo, ymax=punto_alto, c=color_mecha_bull, lw=ancho_mecha, zorder=2)
                r = patches.Rectangle((line.get_xdata(orig=False)[0] - (ancho_vela / 2), datos.Open[i]),
                              width=ancho_vela,
                              height=(datos.Close[i] - datos.Open[i]),
                              edgecolor=color_borde_bull,
                              facecolor=color_vela_bull,
                              zorder=3)
                ax.add_patch(r)
