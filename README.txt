### Grupo: SO-TI-18
# Aluno 1: Luís Lima (fc62214)
# Aluno 2: Gonçalo Seguro (fc62252)
# Aluno 3: Dinis Garcia (fc62269)

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
- Esta abordagem não divide uniformemente os ficheiros pelos processos, pois as linhas têm tamanhos diferentes, mas é uma abordagem mais simples e fácil de implementar.

### Outras informações pertinentes:
- O programa considera uma palavra como qualquer sequência de caracteres separado por espaços brancos.
- Os resultados foram comparados aos de comandos como o grep e o "Ctrl + F" do VSCode, então a implementação segue a mesma destes comandos.
