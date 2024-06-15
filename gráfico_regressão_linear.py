from lib.regressão_linear import *

# Gráfico do ajuste linear com parâmetros
plt.scatter(x, y, label='Dados Observados')
plt.plot(x, resultado.predict(X), label='Ajuste Linear', color='red')

# Adicionando os parâmetros da equação da reta no gráfico
equacao_reta = f'Reta de Ajuste:\nY = {resultado.params[1]:.4f}X + {resultado.params[0]:.4f}'
plt.annotate(equacao_reta, xy=(0.5, 0.9), xycoords='axes fraction', ha='center', fontsize=10, color='blue')

# Configurações do gráfico
plt.xlabel('Raio (arcsec)')
plt.ylabel('Temperatura (keV)')
plt.legend()
plt.title('Ajuste Linear com Erro Associado')
plt.grid(True)

# Mostrando o gráfico
plt.show()