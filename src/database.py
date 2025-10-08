"""
database.py
--------
Este arquivo contém anotações e instruções (apenas comentários) para guiá-lo
passo a passo sobre como integrar a parte de "salvar planilhas geradas" na
interface gráfica — especificamente, como exibir as planilhas geradas dentro
do frame com scroll que fica no lado direito da aplicação (o "frame scroll da direita").

IMPORTANTE: conforme pedido, este arquivo não implementa a funcionalidade,
ele apenas ensina o que você precisa fazer. Use as instruções abaixo como um
checklist quando for implementar.

Passos gerais (visão de alto nível)
1) Identificar o frame scroll direito na sua View (provavelmente em
	 `src/conciliador/ui/main_window.py`). Esse frame deve ser um container
	 (por exemplo, um CTkFrame) que contém um Canvas + Scrollbar para exibir
	 vários elementos dinamicamente.

2) Definir um contract/contrato entre a camada de serviços e a UI:
	 - Quando o serviço gera uma planilha (output_generator), ele deve retornar
		 o caminho do arquivo salvo (str). A UI será responsável por ler esse
		 arquivo e renderizá-lo no frame.

3) Na UI (controller), depois de gerar a planilha, abra o arquivo com pandas
	 (pd.read_excel) e crie uma visualização tabular dentro do frame scroll.
	 - Convertendo o DataFrame para uma sequência de widgets (Labels ou uma
		 CTkTable se tiver disponível), cada linha vira uma linha de widgets.

4) Para que o frame seja atualizado dinamicamente:
	 - Limpe o conteúdo atual do frame (destroy/forget widgets) antes de
		 inserir a nova tabela.
	 - Use `canvas.create_window` para inserir um frame interno que contém a
		 grelha com todas as linhas e configure o scrollregion.

Detalhamento técnico (passo a passo)
- Localize o frame: abra `main_window.py` e encontre o container do lado direito
	que deve receber a lista de arquivos/visualizações.

- Pseudocódigo da rotina de renderização (implementação na UI):
	1. def renderizar_planilha_no_frame(df, container_frame):
		 - Limpar container_frame: para child in container_frame.winfo_children(): child.destroy()
		 - Criar um frame interno `inner = CTkFrame(container_frame)`
		 - Para cada coluna do df: criar um Label com o nome da coluna na primeira linha
		 - Para cada linha do df: criar Labels para cada célula e colocá-los com grid(row=i, column=j)
		 - Inserir `inner` no canvas do container (ou empacotar diretamente se não usar canvas)

- Se a planilha for muito grande, considere usar paginação (mostrar as primeiras N linhas)
	ou virtualização (carregar apenas as linhas visíveis). Isso melhora performance.

Como integrar com o pipeline existente
- No controller (UIController), onde você chama `output_generator.gerar_planilha(...)`:
	- Receba o caminho retornado e, em seguida, chame pandas.read_excel(caminho)
	- Passe o DataFrame para `renderizar_planilha_no_frame(df, container_frame_direito)`

Sobre persistência e histórico
- Armazene metadados (nome do arquivo, timestamp, template usado) em uma pequena
	tabela (JSON ou SQLite) se quiser listar as planilhas geradas na UI com histórico.

Erros e mensagens ao usuário
- Mostre mensagens amigáveis se ocorrer erro ao ler o arquivo (arquivo corrompido,
	formato inválido, etc.). Use try/except e exiba um alerta modal ou um label de erro.

Segurança e permissões
- No Windows, caminhos longos ou permissões podem bloquear a escrita/abertura. Se
	planeja distribuir o app, trate exceções e mostre instruções ao usuário.

Referências rápidas
- tkinter Canvas + Scrollbar patterns: inserir um frame dentro de um canvas para
	permitir scroll vertical de widgets.
- pandas.read_excel para carregar o arquivo salvo em DataFrame.

Quando quiser que eu implemente essas instruções em código (renderização, leitura
e integração), eu posso fazê-lo — mas por enquanto deixei apenas as orientações
como você pediu.
"""
