from uncertainties import ufloat
from scipy.special import gamma, psi
import numpy as np

def gamma_with_uncertainty(x):
    """
    Calcula a função gamma de um objeto ufloat e propaga a incerteza.
    
    Parameters:
    - x: uncertainties.ufloat, o número flutuante incerto de entrada.

    Returns:
    - uncertainties.ufloat, resultado da função gamma com a incerteza propagada.
    """
    result_nominal = gamma(x.nominal_value)

    # Derivada da função gamma em relação a x
    derivada_gamma = psi(x.nominal_value) * gamma(x.nominal_value)

    # Propagação de erro
    incerteza_gamma = np.abs(derivada_gamma) * x.std_dev

    # Criar um novo objeto ufloat com o resultado e a incerteza propagada
    result_with_uncertainty = ufloat(result_nominal, incerteza_gamma)

    return result_with_uncertainty

