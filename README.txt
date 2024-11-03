### Grupo: SO-TI-18
# Aluno 1: Luís Lima (fc62214)
# Aluno 2: Gonçalo Seguro (fc62252)
# Aluno 3: Dinis Garcia (fc62269)


###Resumo

O pword.py é um programa Python, com um script Bash auxiliar (pword), que permite contar as ocorrências de uma palavra específica 
em arquivos .txt. As contagens podem ser feitas de três modos diferentes: contagem total de ocorrências, contagem de ocorrências isoladas
e contagem das linhas distintas onde a palavra aparece.


### Exemplos de comandos para executar o pword.py:
1) ./pword -m c -w exemplo -p 2 file1.txt file2.txt
2) ./pword -m l -w teste -p 1 file3.txt
3) ./pword -m i -w palavra -p 3 file4.txt


### Limitações da implementação:

- Divisão desigual, uma vez que a divisão dos arquivos pelos processos é feita por linhas, 
o que pode resultar num processamento desigual, pois as linhas podem ter tamanhos diferentes. 
Isso pode fazer com que o tempo de execução de cada processo seja ligeiramente diferente.

- Não considera a pontuação na totalidade, já que o programa ignora pontuações básicas ao ir buscar a palavra isolada, 
certos caracteres podem ser considerados parte da palavra. 
A função count_isolated lida com isso ao ir buscar a palavra entre delimitadores como espaços e sinais de pontuação comuns.


### Abordagem para a divisão dos ficheiros:

- Colocamos todas as linhas de todos os ficheiros numa lista, onde cada linha é um elemento da lista.
- Dividimos a lista das linhas pelos processos, dividindo o tamanho total desta pelo número de processos.
- Esta abordagem não divide uniformemente os ficheiros pelos processos, pois as linhas têm tamanhos diferentes, mas é uma abordagem mais simples e fácil de implementar.


### Outras informações pertinentes:

- O programa considera uma palavra como qualquer sequência de caracteres separado por espaços brancos.
- Os resultados foram comparados aos de comandos como o grep e o "Ctrl + F" do VSCode, então a implementação segue a mesma destes comandos.
- Os resultados e tempo de execução de cada processo é exibido juntamente com o resultado da contagem. Esse tempo é medido internamente para cada processo.