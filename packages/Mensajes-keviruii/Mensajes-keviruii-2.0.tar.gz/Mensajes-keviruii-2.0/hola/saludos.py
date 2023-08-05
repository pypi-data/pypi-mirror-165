import numpy as np

def saludar():
    print("hola")

def generar_array(numeros):
	return np.arange(numeros)


class Saludo():

	def __init__(self):
		
		print("Hola, te estoy saludando desde el __init__ de la clase Saludo")




if __name__ == '__main__':
    print(generar_array(5))