# agregar una variable de entorno
import os

def add_var_env(name_variable, value_variable):

    os.environ[name_variable] = value_variable
    return f'Variable {name_variable}: {value_variable}'

if __name__ == "__main__":
    name_variable = input('Nombre de la variable:')
    value_variable = input('Valor de la variable:')
    add_var_env(name_variable, value_variable)
