import random

# Falta: 
#  Validacion -> Comprobar que los datos fueron ingresados correctamente
#  Cantidad de Corridas -> Las veces que se ejecutara el programa, 
#  tambien es un parametro
#  Consola -> Pasar el programa para que funcione en consola
#  Graficas con matplotlib

# Sera un parametro pasado por consola
numero_seleccionado = int(input('Ingrese numero: '))

# Sera un parametro pasado por consola
tiradas_ruleta = int(input('Ingrese el numero de tiradas de la ruleta: '))

coincidencias = 0
valor_acumulado = 0

for n in range(tiradas_ruleta):
    resultado = random.randint(1, 36)
    valor_acumulado += resultado
    if resultado == numero_seleccionado:
        print('Numeros iguales')
        print('Elegido: ', numero_seleccionado, ' Resultado: ', resultado)
        coincidencias += 1
    else:
        print('Numeros diferentes')
        print('Elegido: ', numero_seleccionado, ' Resultado: ', resultado)

print('Coincidencias - Frecuencia Absoluta: ', coincidencias)
print('Frecuencia Relativa Esperada: ', 1/36)
print('Frecuencia Relativa: ', coincidencias/tiradas_ruleta)
# No se si es correcto esto
print('Valor Promedio Esperado: ', 18)
print('Valor Promedio: ', valor_acumulado/tiradas_ruleta)