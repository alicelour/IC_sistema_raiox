# Sistema para diagnóstico de doenças com base em IA 
Esse sistema, que está sendo desenvolvido em uma iniciação cientifica utiliza inteligência artificial para auxiliar no diagnóstico de doenças pulmonares a partir de radiografias de tórax.
Ao receber uma imagem no formato DICOM, 
o sistema converte o arquivo para PNG e processa a imagem por meio de uma rede neural treinada para identificar padrões associados a diferentes condições médicas.

O diagnóstico gerado pela IA é automaticamente armazenado em um banco de dados SQLite, permitindo acesso rápido e organizado às informações. 
Além disso, os resultados são exibidos em uma interface web desenvolvida com Flask, garantindo praticidade para profissionais de saúde que desejam visualizar e analisar os laudos diretamente pelo sistema.

Essa solução tem como objetivo otimizar o tempo de análise, reduzindo a carga de trabalho de especialistas e aumentando a eficiência na detecção precoce de doenças respiratórias.

### Desenvolvimento:
**Primeiro Passo:** Sistema ainda não reconhece todas as doenças que deveriam ser diagnósticadas, apenas a chance de ter uma doença no raiox. Identificando um raiox por vez.

**Segundo Passo:** Ainda sem reconhecer as doenças, porém mais automatizado, rodando várias imagens de uma vez. (**Atualmente aqui**)

**Terceiro Passo:** Rodar várias imagens de uma vez, mas sem tanta lentidão. E o site com mais funções como a opção de retirar o paciente da fila e fazer essa integração com o banco de dados.  

**Quarto Passo:** Reconhecer mais doenças e mais funções no site.

**Quinto Passo:** Realizar melhorias e um possivel app.

### Recursos Utilizados:

- Python
- Flask
- Sqlite3
- HTML5
- CSS3

  
