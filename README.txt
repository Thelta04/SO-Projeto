### Grupo: SO-TI-18
# Aluno 1: Luís Lima (fc62214)
# Aluno 2: Gonçalo Seguro (fc62252)
# Aluno 3: Dinis Garcia (fc62269)


###Resumo

O pword.py é um programa Python, com um script Bash auxiliar (pword), que permite contar as ocorrências de uma palavra específica 
em arquivos .txt. As contagens podem ser feitas de três modos diferentes: contagem total de ocorrências, contagem de ocorrências isoladas
e contagem das linhas distintas onde a palavra aparece.

### Exemplos de comandos para executar o pword.py:
1) ./pword -m i -p 2 -w exemplo file1.txt file2.txt -> Contagem isolada da palavra "exemplo" nos ficheiros 1 e 2, com dois processos.
2) ./pword -m l -w teste file3.txt -> Contagem das linhas da palavra "teste" no ficheiro 3, com um processo (omissão).
3) ./pword -w word file4.txt -> Contagem total (omissão) da palavra "word" no ficheiro 4, com um processo (omissão).
4) ./pword -d out.txt -i 1 -w copy ficheiros_teste/file1.txt -> A cada 1 segundo, mete no ficheiro "out.txt" os resultados parciais.

5) ./pword -w erro -> Erro: "The arguments must include a -w word argument and a .txt argument."
6) ./pword -> Erro: "You need to provide arguments."
7) ./pword -m i -p 3 -w copy ficheiros_teste/file1.txt ficheiros_teste/file4.txt -> Erro: "For multiple files, the number of processes can't be greater that the number of files. Redefining number of processes to be the number of files."

### Limitações da implementação:

- Divisão desigual, uma vez que a divisão dos arquivos pelos processos é feita por linhas, 
o que pode resultar num processamento desigual, pois as linhas podem ter tamanhos diferentes. 
Isso pode fazer com que o tempo de execução de cada processo seja ligeiramente diferente.

- Não é confirmada se a soma dos counts no Array e os resultados no Queue são iguais.


### Abordagem para a divisão dos ficheiros:

- Colocamos todas as linhas de todos os ficheiros numa lista, onde cada linha é um elemento da lista.
- Dividimos a lista das linhas pelos processos, dividindo o tamanho total desta pelo número de processos.
- Esta abordagem não divide uniformemente os ficheiros pelos processos, pois as linhas têm tamanhos diferentes, mas é uma abordagem mais simples e fácil de implementar.


### Outras informações pertinentes:

- O programa considera uma palavra como qualquer sequência de caracteres separado por espaços brancos.
- Os resultados foram comparados aos de comandos como o grep e o "Ctrl + F" do VSCode, então a implementação segue a mesma destes comandos.
- Os resultados e tempo de execução de cada processo é exibido juntamente com o resultado da contagem. Esse tempo é medido internamente para cada processo.
- Mesmo não sendo específicado no enuniciado, o Ctrl+C revela também resultados parciais.