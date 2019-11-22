from utils import rnd


class Epikouriko:
    def __init__(self, name, penos, petis):
        self.name = name
        self.penos = penos
        self.petis = petis

    def calc_eisfores(self, amount):
        rvl = {
            'epikouriko': self.name,
            'pososto_ergazomenos%': self.penos,
            'pososto_ergodotis%': self.petis,
            'pososto_total': self.penos + self.petis,
            'amount': amount
        }
        rvl['kratiseis_ergazomenou'] = rnd(amount * self.penos / 100.0)
        total = rnd(amount * (self.penos + self.petis) / 100.0)
        rvl['kratiseis_ergodoti'] = total - rvl['kratiseis_ergazomenou']
        rvl['kratiseis_synolika'] = total
        return rvl
