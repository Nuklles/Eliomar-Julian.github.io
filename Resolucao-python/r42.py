import time

def progress(espaco, size):
    print(f'\rprogresso: |{"█" * (size // 2)}{" " * (espaco - size // 2)}| {size}%', end='')

buffer = 0
while (buffer <= 100):
    progress(50, buffer)
    time.sleep(0.2)
    buffer += 1
