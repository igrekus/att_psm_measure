import errno
import itertools
import os

from PyQt5.QtWidgets import QGridLayout, QWidget
from mytools.plotwidget import PlotWidget

main_states = [0, 1, 2, 4, 8, 16, 32, 63]


class AttPlotWidget(QWidget):
    params = {
        0: {
            '00': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21, дБ, 0гр',
                'ylim': []
            },
            '01': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21, дБ, 5гр',
                'ylim': []
            },
            '02': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21, дБ, 11гр',
                'ylim': []
            },
            '03': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21, дБ, 22гр',
                'ylim': []
            },
            '10': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21, дБ, 45гр',
                'ylim': []
            },
            '11': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21, дБ, 90гр',
                'ylim': []
            },
            '12': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21, дБ, 180гр',
                'ylim': []
            },
            '13': {
                'xlabel': 'F, ГГц',
                'xlim': [],
                'ylabel': 'S21, дБ, 360гр',
                'ylim': []
            },
        },
    }

    def __init__(self, parent=None, result=None):
        super().__init__(parent)

        self._result = result
        self.only_main_states = False

        self._grid = QGridLayout()

        self._plot000000 = PlotWidget(parent=None, toolbar=True)
        self._plot000001 = PlotWidget(parent=None, toolbar=True)
        self._plot000010 = PlotWidget(parent=None, toolbar=True)
        self._plot000100 = PlotWidget(parent=None, toolbar=True)
        self._plot001000 = PlotWidget(parent=None, toolbar=True)
        self._plot010000 = PlotWidget(parent=None, toolbar=True)
        self._plot100000 = PlotWidget(parent=None, toolbar=True)
        self._plot111111 = PlotWidget(parent=None, toolbar=True)

        self._grid.addWidget(self._plot000000, 0, 0)
        self._grid.addWidget(self._plot000001, 0, 1)
        self._grid.addWidget(self._plot000010, 0, 2)
        self._grid.addWidget(self._plot000100, 0, 3)
        self._grid.addWidget(self._plot001000, 1, 0)
        self._grid.addWidget(self._plot010000, 1, 1)
        self._grid.addWidget(self._plot100000, 1, 2)
        self._grid.addWidget(self._plot111111, 1, 3)

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

        setup_plot(self._plot000000, self.params[dev_id]['00'])
        setup_plot(self._plot000001, self.params[dev_id]['01'])
        setup_plot(self._plot000010, self.params[dev_id]['02'])
        setup_plot(self._plot000100, self.params[dev_id]['03'])
        setup_plot(self._plot001000, self.params[dev_id]['10'])
        setup_plot(self._plot010000, self.params[dev_id]['11'])
        setup_plot(self._plot100000, self.params[dev_id]['12'])
        setup_plot(self._plot111111, self.params[dev_id]['13'])

    def clear(self):
        self._plot000000.clear()
        self._plot000001.clear()
        self._plot000010.clear()
        self._plot000100.clear()
        self._plot001000.clear()
        self._plot010000.clear()
        self._plot100000.clear()
        self._plot111111.clear()

    def plot(self, dev_id=0):
        print('plotting att response')
        self.clear()
        self._init(dev_id)

        freqs = self._result.freqs
        s21s_ph = self._result.s21_phase_norm

        # TODO rename to result._psm_codes
        n = len(set(self._result._att_codes))

        psm_indices = []
        for i in main_states:
            try:
                psm_indices.append(self._result._phase_codes.index(i))
            except ValueError:
                psm_indices.append(-1)
        psm_indices = [idx for idx in psm_indices if idx >= 0]

        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        idx = psm_indices[0]
        for xs, ys in zip(itertools.repeat(freqs, n), (chunk[idx] for chunk in chunks(s21s_ph, n))):
            self._plot000000.plot(xs, ys)

        idx = psm_indices[1]
        for xs, ys in zip(itertools.repeat(freqs, n), (chunk[idx] for chunk in chunks(s21s_ph, n))):
            self._plot000001.plot(xs, ys)

        idx = psm_indices[2]
        for xs, ys in zip(itertools.repeat(freqs, n), (chunk[idx] for chunk in chunks(s21s_ph, n))):
            self._plot000010.plot(xs, ys)

        idx = psm_indices[3]
        for xs, ys in zip(itertools.repeat(freqs, n), (chunk[idx] for chunk in chunks(s21s_ph, n))):
            self._plot000100.plot(xs, ys)

        idx = psm_indices[4]
        for xs, ys in zip(itertools.repeat(freqs, n), (chunk[idx] for chunk in chunks(s21s_ph, n))):
            self._plot001000.plot(xs, ys)

        idx = psm_indices[5]
        for xs, ys in zip(itertools.repeat(freqs, n), (chunk[idx] for chunk in chunks(s21s_ph, n))):
            self._plot010000.plot(xs, ys)

        idx = psm_indices[6]
        for xs, ys in zip(itertools.repeat(freqs, n), (chunk[idx] for chunk in chunks(s21s_ph, n))):
            self._plot100000.plot(xs, ys)

        idx = psm_indices[7]
        for xs, ys in zip(itertools.repeat(freqs, n), (chunk[idx] for chunk in chunks(s21s_ph, n))):
            self._plot111111.plot(xs, ys)

    def save(self, img_path='./image'):
        try:
            os.makedirs(img_path)
        except OSError as ex:
            if ex.errno != errno.EEXIST:
                raise IOError('Error creating image dir.')

        for plot, name in zip([self._plot000000, self._plot000001, self._plot000010, self._plot000100], ['stats.png', 'cutoff.png', 'delta.png', 'double-triple.png']):
            plot.savefig(img_path + name, dpi=400)


