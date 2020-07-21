import errno
import itertools
import os

from PyQt5.QtWidgets import QGridLayout, QWidget
from mytools.plotwidget import PlotWidget


class ErrorPlotWidget(QWidget):
    params = {
        0: {
            '00': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'Фазовая ошибка',
                'ylim': []
            },
            '01': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'Амплитудная ошибка',
                'ylim': []
            },
        },
    }

    def __init__(self, parent=None, result=None):
        super().__init__(parent)

        self._result = result
        self.only_main_states = False

        self._grid = QGridLayout()

        self._plotPhaseRmse = PlotWidget(parent=None, toolbar=True)
        self._plotAmpRmse = PlotWidget(parent=None, toolbar=True)

        self._grid.addWidget(self._plotPhaseRmse, 0, 0)
        self._grid.addWidget(self._plotAmpRmse, 0, 1)

        self.setLayout(self._grid)

        self._init()

    def _init(self, dev_id=0):

        def setup_plot(plot, pars: dict):
            plot.set_tight_layout(True)
            plot.subplots_adjust(bottom=0.150)
            # plot.set_title(pars['title'])
            plot.set_xlabel(pars['xlabel'], labelpad=-2)
            plot.set_ylabel(pars['ylabel'], labelpad=-2)
            # plot.set_xlim(pars['xlim'][0], pars['xlim'][1])
            # plot.set_ylim(pars['ylim'][0], pars['ylim'][1])
            plot.grid(b=True, which='major', color='0.5', linestyle='-')
            plot.tight_layout()

        setup_plot(self._plotPhaseRmse, self.params[dev_id]['00'])
        setup_plot(self._plotAmpRmse, self.params[dev_id]['01'])

    def clear(self):
        self._plotPhaseRmse.clear()
        self._plotAmpRmse.clear()

    def plot(self, dev_id=0):
        print('plotting S-params with att=0')
        self.clear()
        self._init(dev_id)

        freqs = self._result.freqs
        phase_error = self._result.phase_err
        amp_error = self._result.s21_err

        # TODO rename to result._psm_codes
        n = len(set(self._result._phase_codes))

        for xs, ys in zip(itertools.repeat(freqs, n), phase_error):
            self._plotPhaseRmse.plot(xs, ys)

        for xs, ys in zip(itertools.repeat(freqs, n), amp_error):
            self._plotAmpRmse.plot(xs, ys)

    def save(self, img_path='./image'):
        try:
            os.makedirs(img_path)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise IOError('Error creating image dir.')

        for plot, name in zip([self._plotPhaseRmse, self._plotAmpRmse, self._plotS21, self._plotS22], ['stats.png', 'cutoff.png', 'delta.png', 'double-triple.png']):
            plot.savefig(img_path + name, dpi=400)


