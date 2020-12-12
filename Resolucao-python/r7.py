import sys

sys.stdout.write('Digite a primeira nota: ')
sys.stdout.flush()
nA = float(sys.stdin.readline())
sys.stdout.write('Digite a segunda nota: ')
sys.stdout.flush()
nB = float(sys.stdin.readline())
sys.stdout.write(
    'a media entre {} e {} é de {:.1f}'.format(
        nA, nB, (nA + nB) / 2
        )
    )