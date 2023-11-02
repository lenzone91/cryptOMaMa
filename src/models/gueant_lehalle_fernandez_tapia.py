import numpy as np

class GueantLehalleFernandezTapia(object):
    
    def __init__(self):
        pass

    def compute_quotes(self, with_penalty, A, k, q, delta, gamma, sigma, xi):
        if with_penalty:
            if xi == 0:
                bid_quote = (1/k)+((2*q+delta)/2)*np.sqrt((gamma*np.power(sigma,2)*np.exp(1))/(2*A*delta*k))
                ask_quote = (1/k)-((2*q-delta)/2)*np.sqrt((gamma*np.power(sigma,2)*np.exp(1))/(2*A*delta*k))
        return bid_quote, ask_quote
