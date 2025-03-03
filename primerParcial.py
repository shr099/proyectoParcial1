from sys import stdin

# Diccionario para almacenar los valores de verdad de los atomos
valores = dict()

# Convertir una cadena en una lista
def str_a_lista(s: str, ignorar: set) -> list[str]:
    ans = []
    for car in s:
        if car not in ignorar:
            ans.append(car)
    return ans

# PUNTO A

# Verifica si la fórmula es válida
def es_formula_valida(formula: list) -> bool:
    valida = True
    # Verifica que todos los atomos en la formula estén definidos
    for car in formula:
        if car.isalpha() and car not in valores:  # .isalpha() verifica si es un atomo
            valida = False

    # Verificar que los paréntesis esten balanceados
    cnt = 0
    for car in formula:
        if car == '(':
            cnt += 1
        elif car == ')':
            cnt -= 1
        if cnt < 0:
            valida = False
    return valida and cnt == 0

# Evalua una formula logica (Función recursiva)
def evaluar_formula(formula: list, inicio: int, fin: int) -> bool:
    resultado = False
    if inicio == fin:
        resultado = valores[formula[inicio]]
    elif formula[inicio] == '!':
        resultado = not evaluar_formula(formula, inicio + 1, fin)
    elif formula[inicio] == '(' and formula[fin] == ')':
        cnt = 0
        i = inicio + 1
        operadorPrincipal = -1
        while i < fin and operadorPrincipal == -1:
            if formula[i] == '(':
                cnt += 1
            elif formula[i] == ')':
                cnt -= 1
            if formula[i] in {'&', '|'} and cnt == 0:
                operadorPrincipal = i
            i += 1
 
        if operadorPrincipal != -1:
            if formula[operadorPrincipal] == '&':
                resultado = evaluar_formula(formula, inicio  + 1, operadorPrincipal - 1) and evaluar_formula(formula, operadorPrincipal + 1, fin - 1)
            elif formula[operadorPrincipal] == '|':
                resultado = evaluar_formula(formula, inicio + 1, operadorPrincipal - 1) or evaluar_formula(formula, operadorPrincipal + 1, fin - 1)
    return resultado


# PUNTO B

# Genera todas las combinaciones de valores de verdad
def generar_combinaciones(atomos: list, posicion: int, valorActual: dict, combinaciones: list):
    if posicion == len(atomos):
        combinaciones.append(valorActual.copy()) 
        return
    valorActual[atomos[posicion]] = True
    generar_combinaciones(atomos, posicion + 1, valorActual, combinaciones)
    valorActual[atomos[posicion]] = False
    generar_combinaciones(atomos, posicion + 1, valorActual, combinaciones)

# Determina si una formula es tautología, contradicción o contingencia
def tipo_formula(formula: list, atomos: list) -> int:
    combinaciones = []
    generar_combinaciones(atomos, 0, {}, combinaciones)
    
    resultados = []
    for combinacion in combinaciones:
        for atomo, valor in combinacion.items():
            valores[atomo] = valor
        resultados.append(evaluar_formula(formula, 0, len(formula) - 1))
    
    if all(resultados):
        return 1  # Tautología
    elif not any(resultados):
        return 0  # Contradicción
    else:
        return -1  # Contingencia

# Función principal
def main():
    # Lee el numero de átomos
    numeroAtomos = int(stdin.readline().strip())
    for i in range(numeroAtomos):
        nombreAtomo, valor = stdin.readline().split()
        valores[nombreAtomo] = bool(int(valor))
    
    # Lee el numero de formulas a evaluar (parte A)
    numeroFormulas_A = int(stdin.readline().strip())
    for i in range(numeroFormulas_A):
        formula = str_a_lista(stdin.readline().strip(), {' '})
        # Verifica si la fórmula es valida
        if not es_formula_valida(formula):
            print("-1")  
        else:
            # Evaluar la formula con la valoración
            resultado = evaluar_formula(formula, 0, len(formula) - 1)
            if resultado:
                print("1")   # Si resultado es True
            else:
                print("0")   # Si resultado es False
    
    # Lee el numero de formulas a evaluar (parte B)
    numeroFormulas_B = int(stdin.readline().strip())
    for i in range(numeroFormulas_B):
        formula = str_a_lista(stdin.readline().strip(), {' '})
        # Obtiene los atomos unicos en la fórmula
        atomos = []
        for car in formula:
            if car.isalpha():
                atomos.append(car)
        atomos_formula = list(set(atomos))
        # Determinar el tipo de fórmula
        tipo = tipo_formula(formula, atomos_formula)
        print(tipo)

main()