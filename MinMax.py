import math
import matplotlib.pyplot as plt
# Se define el tamaño del tablero
N = 3

# Se definen los jugadores
X = 'X'
O = 'O'
EMPTY = '-'

# Función para imprimir el tablero
def print_board(board):     #Se llama a board (tablero)  
    for row in board:       #row representa cada fila de la matriz
        print(' '.join(row))    #Se imprime cada fila representando el tablero 
    print()
    
# Función para mostrar el tablero como un gráfico de dispersión
def plot_board(board, title):
    plt.figure()
    plt.title(title)
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'X':
                plt.text(j, i, 'X', fontsize=50, color='blue', ha='center', va='center')
            elif board[i][j] == 'O':
                plt.text(j, i, 'O', fontsize=50, color='red', ha='center', va='center')
            else:
                plt.text(j, i, ' ', fontsize=50, color='green', ha='center', va='center')
    plt.xticks(range(len(board[0])))
    plt.yticks(range(len(board)))
    plt.gca().invert_yaxis()
    plt.grid()
    plt.show()

# Función para verificar si hay un ganador
def winner(board):
    # Verificar filas
    for row in board:   
        if row.count(row[0]) == len(row) and row[0] != EMPTY: #cuenta cuántas veces aparece el primer elemento de la fila en la lista, si el recuento es igual a la longitud, significa que  los elementos  son iguales, se verifica que el primer elemento no sea una casilla vacía
            return row[0] #Si se cumple la condición mencionada anteriormente, esta línea devuelve el símbolo del ganador de la fila.
   
    # Verificar columnas
    for col in range(N):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:  #Se verifica que todos los elementos en la columna sean iguales, revisando que el primer elemento no sea una casialla vacia
            return board[0][col] #Si se cumple la condición mencionada anteriormente, esta línea devuelve el símbolo del ganador de la columna.
    # Verificar diagonales
    #Se verifica que todos los elementos en las diagonales sean iguales, revisando que el primer elemento no sea una casialla vacia
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0] #Si se cumple la condición mencionada anteriormente, esta línea devuelve el símbolo del ganador de la diagonal principal.
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2] #Si se cumple la condición mencionada anteriormente, esta línea devuelve el símbolo del ganador de la otra diagonal.
    return None #Si ninguna de las condiciones anteriores se cumple, significa que no hay un ganador en el tablero y la función devuelve None.

# Función para verificar si el tablero está lleno
def board_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True

# Función para generar todos los movimientos posibles
def generate_moves(board):
    moves = []  #Se crea una lista que almacenará todos los movimientos posibles
    for i in range(N):
        for j in range(N):  #Estos  dos  for anidados  iteran sobre los índices de filas (i) y columnas (j) del tablero. N representa el tamaño del tablero,
            if board[i][j] == EMPTY:    #Se verifica si la casilla en la posición (i, j) del tablero está vacía (EMPTY). Si la casilla está vacía, significa que es un movimiento posible.
                moves.append((i, j)) #Si la casilla en la posición (i, j) está vacía, se agrega esta posición a la lista de movimientos
    return moves

# Función para evaluar el tablero
#Se llama a la función winner(board) para verificar si hay un ganador en el tablero. 
  
def evaluate(board):
    if winner(board) == X:  #Si el jugador X es el ganador (winner(board) == X), la función devuelve 1, indicando que el jugador X tiene una ventaja.
        return 1
    elif winner(board) == O: #Si el jugador O es el ganador (winner(board) == O), la función devuelve -1, indicando que el jugador O tiene una ventaja.
        return -1
    else:
        return 0 #Si no hay un ganador (else), la función devuelve 0, lo que significa que el juego está empatado.

# Función para minimax
def minimax(board, depth, is_max): #board, que es una lista de listas que representa el estado actual del tablero del juego, depth, que representa la profundidad actual en el árbol de búsqueda, y is_max, un booleano que indica si es el turno del jugador Max
    score = evaluate(board) #Se calcula la puntuación del estado actual del tablero llamando a la función evaluate(board)

    # Caso base: si hay un ganador o el tablero está lleno
    if score == 1 or score == -1: #Si es 1, significa que (X) ha ganado; si es -1, significa que (O) ha ganado. 
        return score

    if board_full(board): #Si el tablero está lleno pero no hay un ganador, se considera un empate y se devuelve 0  
        return 0

    if is_max: #Si is_max es True, significa que es el turno del jugador Max 
        best_score = -math.inf #inicializamos best_score con infinito negativo para encontrar el máximo.
        for move in generate_moves(board): #se recorren todos los movimientos posibles para el jugador Max (X) llamando a la función generate_moves(board)
            board[move[0]][move[1]] = X #Se simula el movimiento del jugador Max en el tablero.    
            #print("Tablero simulado después del movimiento de X:")
            #print_board(board) 
            score = minimax(board, depth + 1, False) #se llama recursivamente a minimax para evaluar el estado resultante después del movimiento del jugador Max, pero con is_max establecido en False, ya que ahora es el turno del jugador Min.
            board[move[0]][move[1]] = EMPTY #Se deshace el movimiento del jugador Max para explorar otras posibilidades.
            best_score = max(score, best_score) #Se actualiza best_score con el máximo entre el puntaje actual y el mejor puntaje encontrado hasta ahora.
        return best_score #Se devuelve el mejor puntaje encontrado para el jugador Max
    else: #Si is_max es False, significa que es el turno del jugador Min (O) y se realiza el mismo proceso que con Max(X), solo que buscando el valor más pequeño
        best_score = math.inf #inicializamos best_score con infinito positivo para encontrar el mínimo.
        for move in generate_moves(board):
            board[move[0]][move[1]] = O
            #print("Tablero simulado después del movimiento de X:")
            #print_board(board) 
            score = minimax(board, depth + 1, True)
            board[move[0]][move[1]] = EMPTY
            best_score = min(score, best_score)
        return best_score

# Función para obtener el mejor movimiento
def get_best_move(board): #toma un argumento llamado board, que se espera que sea una lista de listas que representa el estado actual del tablero del juego.
    best_score = -math.inf #best_escore se establece en infinito negativo para que cualquier puntuación que se encuentre sea mejor que esta
    best_move = None #best_move se establece en None para almacenar el mejor movimiento encontrado hasta ahora.
    for move in generate_moves(board): #Se itera sobre todos los movimientos posibles en el tablero, obtenidos
        board[move[0]][move[1]] = X #Se simula el movimiento del jugador Max en el tablero.
        score = minimax(board, 0, False) #se llama a la función minimax para evaluar el estado del tablero después del movimiento de X. La profundidad se establece en 0 y is_max se establece en False porque ahora es el turno del jugador Min (O) en la llamada a minimax
        board[move[0]][move[1]] = EMPTY #Se deshace el movimiento simulado para volver al estado original del tablero.
        if score > best_score:#Si la puntuación obtenida en este movimiento es mejor que la mejor puntuación encontrada hasta ahora (best_score)
            best_score = score #se actualiza best_score con la nueva puntuación y 
            best_move = move #best_move con el movimiento correspondiente.
    return best_move #la función devuelve el mejor movimiento encontrado

# Función principal
def main():
    # Estado inicial del tablero
    initial_board = [
        ['X', EMPTY, EMPTY],
        ['O', EMPTY, EMPTY],
        ['O', 'X', EMPTY]
    ]

    print("Estado inicial del tablero:")
    print_board(initial_board)

    # Mostrar el tablero inicial
    plot_board(initial_board, 'Tablero Inicial')

    while not board_full(initial_board) and not winner(initial_board):
        # Movimiento del jugador X (Max)
        x, y = get_best_move(initial_board)
        initial_board[x][y] = X
        print("Jugador X (Max) movió a:", (x, y))
        print_board(initial_board)

        if winner(initial_board) == X:
            print("¡El jugador X (Max) gana!")
            break

        if board_full(initial_board):
            print("¡Empate!")
            break

        # Movimiento del jugador O (Min)
        x, y = get_best_move(initial_board)
        initial_board[x][y] = O
        print("Jugador O (Min) movió a:", (x, y))
        print_board(initial_board)

        if winner(initial_board) == O:
            print("¡El jugador O (Min) gana!")
            break

        if board_full(initial_board):
            print("¡Empate!")
            break

    # Mostrar el tablero final
    plot_board(initial_board, 'Tablero Final')

if __name__ == "__main__":
    main()