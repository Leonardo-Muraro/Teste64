import json
import os

class Livros:
    def __init__ (self,titulo,autor,isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.status_emprestimo = False
        self.membro_id_emprestado = None
 
 
class Membro:
    def __init__ (self, nome, membro_id):
        self.nome = nome
        self.membro_id = membro_id
       
class Biblioteca:
    def __init__(self):
        # Tenta carregar o acervo de um arquivo, se existir
        try:
            with open("acervo.json", 'r', encoding = 'utf-8') as arquivo:
                # Carrega os dados do arquivo
                dados = json.load(arquivo)
                self.acervo = [] # Limpa antes de carregar
                for livro_data in dados:
                    livro_obj = Livros(livro_data['titulo'], livro_data['autor'], livro_data['isbn'])
                    # Restaurar status e membro ID
                    livro_obj.status_emprestimo = livro_data.get('status_emprestimo', False)
                    livro_obj.membro_id_emprestado = livro_data.get('membro_id_emprestado', None)
                    self.acervo.append(livro_obj)
                    
        except FileNotFoundError:
            # Se o arquivo não existir, inicia com acervo vazio
            self.acervo = []
 
        try:
            with open("membros.json", 'r', encoding = 'utf-8') as arquivo:
                dados = json.load(arquivo)
                self.membros = [Membro(membro["nome"], membro["membro_id"]) for membro in dados]
 
        except FileNotFoundError:
            self.membros = []


    def salvar_membros(self):
 
        dados = [{"nome": membro.nome, "membro_id": membro.membro_id} for membro in self.membros]
   
        with open("membros.json", "w", encoding = 'utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4)
 
   
    def salvar_acervo(self):
        # Converte os objetos Livros para dicionários
        dados = [{'titulo': livro.titulo, 'autor': livro.autor,
                 'isbn': livro.isbn, 'status_emprestimo': livro.status_emprestimo, 'membro_id_emprestado': livro.membro_id_emprestado}
                for livro in self.acervo]
       
        # Salva os dados em um arquivo JSON
        with open('acervo.json', 'w', encoding = 'utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4)


    def adicionar_membro(self):
        nome = input("Digite seu nome: ")
 
        #Gerar ID único para cada membro
        if not self.membros:
            membro_id = 1
        else:
            membro_id = max(membro.membro_id for membro in self.membros) + 1

        novo_membro = Membro(nome, membro_id)
        self.membros.append(novo_membro)
        self.salvar_membros()
 
        print(f"\nO membro {nome} foi adicionado com sucesso! ID: {membro_id}")
        return


    def listar_membros(self):
        if not self.membros:
            print("\nNenhum membro cadastrado.")
            return
        
        print("\n===== LISTA DE MEMBROS =====")
        print(f"Total de membros: {len(self.membros)}\n")
        
        for membro in self.membros:
            print(f"ID: {membro.membro_id} | Nome: {membro.nome}")

        return


    def buscar_membro(self, membro_id=None):
        if membro_id is None:
            membro_id = int(input("Digite o ID do membro: "))
        
        for membro in self.membros:
            if membro.membro_id == membro_id:
                return membro
            
        print(f"\nMembro com ID {membro_id} não encontrado.")
        return None

    def add_livro(self):   ####### ADM #######
        titulo = input("Digite o título do livro: ")
        autor = input("Digite o autor do livro: ")
        isbn = input("Digite o ISBN do livro: ")
       
        novo_livro = Livros(titulo, autor, isbn)
        self.acervo.append(novo_livro)
       
        # Salva o acervo após adicionar um livro
        self.salvar_acervo()
       
        print(f"Livro '{titulo}' adicionado com sucesso ao acervo!")
        return novo_livro


    def remove_livro(self):   ####### ADM #######
 
        remove_isbn = input("Digite o ISBN do livro que quer remover: ")
 
        # Procura o livro pelo ISBN
        livro_encontrado = None
 
        for livro in self.acervo:
            if livro.isbn == remove_isbn:
                livro_encontrado = livro
                break
       
        # Verifica se o livro foi encontrado
        if livro_encontrado is None:
            print(f"Livro com ISBN {remove_isbn} não foi encontrado no acervo.")
            return
       
        # Confirmação antes de remover
        confirmacao = input(f"Tem certeza que deseja remover o livro '{livro_encontrado.titulo}' de {livro_encontrado.autor}? (s/n): ")
       
        if confirmacao.lower() == 's':
            self.acervo.remove(livro_encontrado)
            print(f"Livro '{livro_encontrado.titulo}' removido com sucesso!")
           
            # Salva o acervo após a remoção
            self.salvar_acervo()
        else:
            print("Operação de remoção cancelada.")
           
    def listar_livros(self):   ####### MEMBRO #######   ####### ADM #######
 
        if not self.acervo:  # Verifica se o acervo está vazio
            print("O acervo está vazio. Nenhum livro cadastrado.")
            return
       
        print("\n===== LISTA DE LIVROS NO ACERVO =====")
        print(f"Total de livros: {len(self.acervo)}\n")
 
       
        for i, livro in enumerate(self.acervo, 1):  # Printa cada um dos itens no acervo e enumera a partir de "1"
            status = "Disponível" if not livro.status_emprestimo else "Emprestado"
            print(f"{i}. Título: {livro.titulo}")
            print(f"   Autor: {livro.autor}")
            print(f"   ISBN: {livro.isbn}")
            print(f"   Status: {status}\n")
 
    def emprestar_livro(self):

        membro_id = int(input("Digite o ID do membro: "))
        
        # Busco o membro no sistema
        membro = self.buscar_membro(membro_id)
        if membro is None:
            print("\nEmpréstimo não autorizado: membro não encontrado.")
            return 
        
        # Continuar com o empréstimo
        isbn = input("Digite o ISBN do livro que deseja emprestar: ")
        
        # Encontrar o livro pelo ISBN
        for livro in self.acervo:
            if livro.isbn == isbn:
                if livro.status_emprestimo:
                    print(f"\nO livro '{livro.titulo}' já está emprestado.")
                    return 
                else:
                    confirmacao = input(f"Deseja emprestar o livro {livro.titulo} para '{membro.nome}' de ID '{membro.membro_id}' ? (s/n): ").lower()
                
                    if confirmacao == 's':
                        livro.status_emprestimo = True
                        livro.membro_id_emprestado = membro.membro_id
                        self.salvar_acervo()
                        print(f"\nLivro emprestado com sucesso para {membro.nome}!")
                        return 
                    else:
                        print("\nEmpréstimo cancelado")
                        return 
    
        print("Livro não encontrado no acervo.")
        return 
 
    def devolver_livro(self):   ####### MEMBRO #######
        membro_id = int(input("Digite o ID do membro: "))
            
        # Verificar se o membro existe
        membro = self.buscar_membro(membro_id)
        if membro is None:
            print("\nMembro não encontrado no sistema.")
            return 
            
        livros_emprestados = []
            
            # Encontrar todos os livros emprestados para este membro
        for livro in self.acervo:
            if livro.status_emprestimo and livro.membro_id_emprestado == membro_id:
                livros_emprestados.append(livro)
            
            # Verificar se o membro tem livros emprestados
        if not livros_emprestados:
            print(f"\nO membro {membro.nome} (ID: {membro_id}) não possui livros emprestados.")
            return 
            
            # Lista os livros emprestados para o membro
        print(f"\n===== LIVROS EMPRESTADOS PARA {membro.nome.upper()} =====")
        for i, livro in enumerate(livros_emprestados, 1):
            print(f"{i}. Título: {livro.titulo}. Autor:{livro.autor} (ISBN: {livro.isbn})")
            print("="*40)

        try:
            index_devolver = int(input("Digite o número do livro que deseja devolver (ou 0 para cancelar): "))
            if index_devolver == 0:
                print("\nOperação de devolução cancelada.")
                return
            if not (1 <= index_devolver <= len(livros_emprestados)):
                print("Número inválido.")
                return

            livro_devolvido = livros_emprestados[index_devolver - 1]

            confirmacao = input(f"\nConfirmar a devolução do livro '{livro_devolvido.titulo}'? (s/n): ").lower()

            if confirmacao == 's':
                livro_devolvido.status_emprestimo = False
                livro_devolvido.membro_id_emprestado = None
                self.salvar_acervo()
                print(f"\nLivro '{livro_devolvido.titulo}' devolvido com sucesso!")
            else:
                print("\nOperação de devolução cancelada.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")


    def buscar_livros(self):
        termo = input("Digite o termo de busca: ").lower()
        if not termo:
            print("ERRO")
            print("Termo de busca não pode ser vazio.\n\n")
            return biblioteca.buscar_livros()
        
        
        resultados = []
        
        for livro in self.acervo:
            if (termo in livro.titulo.lower() or 
                termo in livro.autor.lower() or 
                termo in livro.isbn.lower()):
                resultados.append(livro)
        
        if not resultados:
            print("\nNenhum livro encontrado com esse termo de busca.")
            return
        
        print(f"\n===== RESULTADOS DA BUSCA =====")
        print(f"Encontrados {len(resultados)} livros:\n")
        
        for i, livro in enumerate(resultados, 1):
            status = "Disponível" if not livro.status_emprestimo else "Emprestado"
            print(f"{i}. Título: {livro.titulo}")
            print(f"   Autor: {livro.autor}")
            print(f"   ISBN: {livro.isbn}")
            print(f"   Status: {status}\n")
            print("="*40)
 
#############       MENUS          ###############]
 

def captura_input_menu(max_opcao):
    while True:
        try:
            captura = int(input("\nDigite a opção desejada: "))
            if 0 <= captura <= max_opcao:
                print("\n") # Adiciona espaço após input válido
                return captura
            else:
                print(f"Opção inválida. Digite um número entre 0 e {max_opcao}.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
 
 
def menuOpcoes():
    print(" \nMENU ")
    print("0 - Sair ")
    print("1 - Menu Membro")
    print("2 - Menu ADM ")
    print("="*22)
    return captura_input_menu(2)
 

def menu_membro():
    print("\n MENU MEMBRO ")
    print("0 - Voltar ")
    print("1 - Emprestar Livro")
    print("2 - Devolver Livro")
    print("3 - Listar Todos os Livros")
    print("4 - Buscar Livros")
    print("="*22)
    return captura_input_menu(4)


def menu_adm():
    print("\n===== MENU ADM =====")
    print("0 - Voltar ")
    print("1 - Listar Todos os Livros")
    print("2 - Buscar Livros")
    print("3 - Gerenciar Livros")
    print("4 - Gerenciar Membros")
    print("="*22)
    return captura_input_menu(4)


def menu_gerenciar_livros():
    print("\n GERENCIAR LIVROS ")
    print("0 - Voltar ")
    print("1 - Adicionar Livro")
    print("2 - Remover Livro")
    print("3 - Listar Todos os Livros")
    print("="*22)
    return captura_input_menu(3)


def menu_gerenciar_membros():
    print("\n GERENCIAR MEMBROS ")
    print("0 - Voltar ")
    print("1 - Adicionar Membro")
    print("2 - Listar Membros")
    print("3 - Buscar Membro")
    print("="*22)
    return captura_input_menu(3)
 
#############      INÍCIO DO PROGRAMA         ###############
 
if __name__ == "__main__":
    biblioteca = Biblioteca()
    
    while True:
        opcao_digitada = menuOpcoes()
        
        if opcao_digitada == 1: ########################## ENTRANDO NO MENU DO MEMBRO ##########################
            opcao_digitada = menu_membro()
    
            if opcao_digitada == 1: ### --- OPÇÃO 1: EMPRÉSTIMO DE LIVRO --- ###
                os.system("cls")
                biblioteca.emprestar_livro()

            elif opcao_digitada == 2: ### --- OPÇÃO 2: DEVOLUÇÃO DE LIVRO --- ###
                os.system("cls")
                biblioteca.devolver_livro()

            elif opcao_digitada == 3: ### --- OPÇÃO 3: LISTAR LIVROS --- ###
                os.system("cls")
                biblioteca.listar_livros()

            elif opcao_digitada == 4: ### --- OPÇÃO 4: BUSCAR LIVROS --- ###
                os.system("cls")
                biblioteca.buscar_livros()
        
        elif opcao_digitada  == 2: ########################## ENTRANDO NO MENU DO ADM ##########################
            opcao_digitada = menu_adm()
    
            if opcao_digitada == 1: ### --- OPÇÃO 1: LISTAR LIVRO --- ###
                biblioteca.listar_livros()

            elif opcao_digitada == 2: ### --- OPÇÃO 2: BUSCAR DE LIVRO --- ###
                biblioteca.buscar_livros()

            elif opcao_digitada == 3: ### --- OPÇÃO 3: MENU DE GERENCIAMENTO DE LIVROS --- ###
                while True:
                    opcao_membros = menu_gerenciar_livros()
                    
                    if opcao_membros == 0:
                        break
                    elif opcao_membros == 1:
                        biblioteca.add_livro() ### OPÇÃO 1: ADICIONA LIVROS ###
                    elif opcao_membros == 2:
                        biblioteca.remove_livro() ### OPÇÃO 2: REMOVE LIVROS ###
                    elif opcao_membros == 3:
                        biblioteca.listar_livros() ### OPÇÃO 3: LISTA LIVROS ###

            elif opcao_digitada == 4:  ### --- OPÇÃO 4: MENU DE GERENCIAMENTO DE MEMBROS --- ###
                while True:
                    opcao_membros = menu_gerenciar_membros()
                    
                    if opcao_membros == 0:
                        break
                    elif opcao_membros == 1:
                        biblioteca.adicionar_membro() ### OPÇÃO 1: ADCIONA MEMBROS ###
                    elif opcao_membros == 2:
                        biblioteca.listar_membros() ### OPÇÃO 2: lISTA MEMBROS ###
                    elif opcao_membros == 3:
                        membro_buscado = biblioteca.buscar_membro()
                        print(f"\nNome: {membro_buscado.nome} // ID: {membro_buscado.membro_id}")
    
        elif opcao_digitada == 0:
            os.system("cls")
            print("Você encerrou o programa")
            break