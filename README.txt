### Grupo: SO-TI-XX
# Aluno 1: Nome Apelido (fcXXXXX)
# Aluno 2: Nome Apelido (fcXXXXX)
# Aluno 3: Nome Apelido (fcXXXXX)

### Exemplos de comandos para executar o pwordcount:
1) ./pword -m c ...
2) ./pword -m l ...
3) ./pword -m i ...

### Limitações da implementação:
- ...
- ...

### Abordagem para a divisão dos ficheiros:
- Colocamos todas as linhas de todos os ficheiros numa lista, onde cada linha é um elemento da lista.
- Dividimos a lista das linhas pelos processos, dividindo o tamanho total desta pelo número de processos.
- Esta abordagem não divide uniformemente os ficheiros pelos processos, mas é uma abordagem mais simples e fácil de implementar.

### Outras informações pertinentes:
- O programa considera uma palavra como qualquer sequência de caracteres separado por espaços brancos.
- ...
