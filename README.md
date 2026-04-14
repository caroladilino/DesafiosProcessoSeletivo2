# Relatório Python Challenge 

**Método de Resolução**

Por não ter experiência usando a biblioteca Pandas anteriormente, comecei resolvendo o desafio sem ela. Meu objetivo com essa estratégia era dedicar toda minha atenção à logica do programa, evitando o esfoço adicional que seria lidar com uma ferramenta com a qual não tinha familiaridade.

Minha solução inicial salvava o conteúdo buscado em arquivos json e realizava as devidas operações dentro deles. Eram usados comandos 'for' aninhados, que iteravam linha por linha do código buscando os dados que queríamos manipular. Foi assim que construí toda a lógica do programa. 

Após conseguir um resultado funcional antes da data limite para a entrega, pesquisei sobre a biblioteca Pandas. Me interessei muito no funcionamento e decidi otimizar meu código alterando o método de resolução. Como a lógica já estava pronta, essa substituição foi simples, apenas mudar o método de armazenar a informação (DataFrames ao invés de arquivos json) e substituir as linhas de código para os comandos do Pandas.

No final, busquei maneiras de otimizar ainda mais o código, e descobri que o método que usei ('for's aninhados) não era o ideal. Soluções como um hashmap e outros comandos da biblioteca Pandas seriam muito melhores em legibilidade e performance. Infelizmente, não tive tempo de implementar essas otimizações, mas a próxima vez que tiver que lidar com problemas similares, essa será a solução que irei adotar.
