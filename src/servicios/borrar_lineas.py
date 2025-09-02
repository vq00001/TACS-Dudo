def borrar_lineas(num_lines):
    for _ in range(num_lines):
        print("\033[F", end="")  # Move cursor up one line
        print("\033[K", end="")  # Clear from cursor to end of line
       