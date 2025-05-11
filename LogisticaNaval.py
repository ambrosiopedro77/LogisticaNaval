import sqlite3
import os
import sys
from datetime import datetime

def fun_data_validade(data_input):
    try:
        # Converte a entrada para objeto de data
 
        data_validade = datetime.strptime(data_input, "%d-%m-%Y").date()
        hoje = datetime.today().date()

        # Comparações
        if data_validade < hoje:
            print("«««««««««««««««« ⚠ O item está vencido! »»»»»»»»»»»»»»»»")
            print("-------------------------------------------------------------------------------")
            voltar = input("Ir ao Menu [Enter]: ")
            if voltar:
                limpar_tela()
                menu()
            else:
                limpar_tela()
                menu()
            
        elif data_validade > hoje:
            dias_restantes = (data_validade - hoje).days
            print(f"✅ O item vencerá em {dias_restantes} dia(s).")
            print("--------------------------------------------------------------------------------")
            
        else:
            print("⚠ O item vence hoje!")
            print("-------------------------------------------------------------------------------")
            voltar = input("Ir ao Menu [Enter]: ")
            if voltar:
                limpar_tela()
                menu()
            else:
                limpar_tela()
                menu()
                
            

    except ValueError:
        print("❌ Data inválida. Use o formato dd-mm-yyyy corretamente.")
        print("--------------------------------------------------------------------------------")
        voltar = input("Sair [0] ?: ")
        if voltar:
            limpar_tela()
            menu()
        else:
            limpar_tela()
            menu()

def conexao_banco():
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()

    #Criação da tabela inventario na base de dado
    executor.execute('''CREATE TABLE IF NOT EXISTS item (
                        id_item INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        nome VARCHAR(45) NOT NULL ,
                        peso FLOAT NOT NULL ,
                        tipo VARCHAR(45) NOT NULL ,
                        qtd INTEGER NOT NULL,
                        data_validade DATE,
                        data_recebido DATE NOT NULL,
                        id_item_fornec INTEGER NOT NULL,
                        status VARCHAR(5) NOT NULL DEFAULT 'N',
                        id_item_categ INTEGER NOT NULL,
                        FOREIGN KEY (id_item_categ) REFERENCES categoria(id_categoria),
                        FOREIGN KEY (id_item_fornec) REFERENCES fornecedor(id_fornec)
                         ) 
                    ''')
    
    executor.execute('''
    
                        CREATE TABLE IF NOT EXISTS fornecedor (
                        id_fornec INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        nome VARCHAR(45) NOT NULL,
                        email VARCHAR(60) NOT NULL,
                        endereco VARCHAR(60) NOT NULL,
                        telefone VARCHAR(9) NOT NULL,
                        nif VARCHAR(25) NOT NULL,
                        status VARCHAR(5) NOT NULL
                        )  
                     
                     ''')
    executor.execute("""
                        CREATE TABLE IF NOT EXISTS categoria (
                        id_categoria INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        nome VARCHAR(100) NOT NULL,
                        status VARCHAR(5) NOT NULL                           
                        )
                     
                        """)
    
    #Delectar a table
    """nome_tabela = "fornecedor"
    executor.execute(f"DROP TABLE IF EXISTS {nome_tabela}")
    conexao.commit()"""
           
    conexao.commit()
    conexao.close()

def adicionar_categoria():
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()
    
    print("---------------------------------- Registrar a Categoria ----------------------------------------------")
    #Cadastrando os itens na base de dados
    nome_categoria       = input("Categoria: ")
    status               = input("Status: ")
    executor.execute("INSERT INTO categoria (nome,status) VALUES (?,?)", (nome_categoria,status))
        
    print("««««« Categoria Registrada com Sucesso! »»»»»")
    conexao.commit()
    conexao.close()
    print("-----------------------------------------------------------------------")    
    voltar = input("Continuar para registrar um item ? [S/N]: ")
    if voltar == "S" or voltar == "s":
            limpar_tela()
            adicionar_Item()
    elif voltar == "N" or voltar == "n":
            limpar_tela()
            menu()
    else:
            print("-------------------------Opção Inválida!--------------------------")
            return False
        #Executar as alterações e fechar a conexão com a base de dados
     
def adicionar_fornecedor():
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()
    
    print("---------------------------------- Registrar o Fornecedor ----------------------------------------------")
    #Cadastrando os itens na base de dados
    nome_fornecedor       = input("Nome do Fornecedor: ")
    email                 = input("E-mail: ")
    endereco              = input("Endereco: ")
    telefone              = input("Telefone: ")
    nif                   = input("NIF: ")
    status_fornecedro     = input("Status: ")
    
    if nome_fornecedor != "" and telefone != "" and endereco != "" and nif != "": 
        executor.execute("INSERT INTO fornecedor (nome,email,endereco,telefone,nif,status) VALUES (?,?,?,?,?,?)",
                          (nome_fornecedor,email,endereco,telefone,nif,status_fornecedro))
        conexao.commit()
        conexao.close()
        print("««««« Fornecedor Registrado com Sucesso! »»»»»")

        print("-----------------------------------------------------------------------")    
        voltar = input("Continuar para registrar um item ? [S/N]: ")
        if voltar == "S" or voltar == "s":
            limpar_tela()
            adicionar_Item()
        elif voltar == "N" or voltar == "n":
            limpar_tela()
            menu()
        else:
            print("-------------------------Opção Inválida!--------------------------")
            return False
        #Executar as alterações e fechar a conexão com a base de dados
        
    else:
        print("««««« Preencha os campos! »»»»»")
        voltar = input("Tentar novamnete ? [S/N]: ")
        if voltar == "S" or voltar == "s":
            limpar_tela()
            adicionar_fornecedor()
        elif voltar == "N" or voltar == "n":
            limpar_tela()
            menu()
        else:
            print("-------------------------Opção Inválida!--------------------------")
            return False
    
    print("-----------------------------------------------------------------------")    
    voltar = input("Continuar para registrar um item ? [S/N]: ")
    if voltar == "S" or voltar == "s":
        limpar_tela()
        adicionar_Item()
    elif voltar == "N" or voltar == "n":
         limpar_tela()
         menu()
    else:
       print("-------------------------Opção Inválida!--------------------------")
       return False

def adicionar_Item():
  
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()
    
    print("---------------------------------- Registra Items ----------------------------------------------")
    #Cadastrando os itens na base de dados
    nome_item       = input("Nome do Item: ")
    tipo_item       = input("Tipo de Item: ")
    peso            = input("Peso do Item (kg / L): ")
    qtd             = input("Quantidade do Item: ")
    data_validade   = input("Data de Validade do Item (DD-MM-YYYY): ")
    data_recebe     = datetime.today().date()
    data_recebido   = data_recebe.strftime('%d-%m-%Y')
    nome_fornecedor = input("Nome do Fornecedor: ")
    status_item     = input("Status do Item [S/N]: ")


    executor.execute("SELECT * FROM categoria")
    categorias = executor.fetchall()
    print(f"Categorias Disponíveis:  ")
    for cat in categorias:
        print(f"{cat[0]} - {cat[1]} | " , end=' ')
    
    categoria = input("\nID da Categoria:  ")
    if categoria == " ":
        print("Prencha o campo: ")
        adicionar_Item()
    fun_data_validade(data_validade)
   
    #Verifica se o fornecedor existe

    executor.execute("SELECT id_fornec FROM fornecedor WHERE nome = ?", (nome_fornecedor,))
    resultado = executor.fetchone()
   
    if resultado:
        id_fornec = resultado[0]
                
        executor.execute("INSERT INTO item (nome,tipo,peso,qtd,data_validade,data_recebido,id_item_fornec,status,id_item_categ) VALUES (?,?, ?, ?, ?,?, ?, ?, ?)", 
                         (nome_item,tipo_item, peso,qtd,data_validade,data_recebido,id_fornec,status_item,categoria))
        
        #Executar as alterações e fechar a conexão com a base de dados
        conexao.commit()
        conexao.close()
         
    
        print("««««« Item Registrado com Sucesso! »»»»»")
        print("--------------------------------------------------------------------------------")    
        voltar = input("Realizar um Novo Registro ? [S/N]: ")
        print("--------------------------------------------------------------------------------")
        if voltar == "S" or voltar == "s":
            limpar_tela()
            adicionar_Item()
        elif voltar == "N" or voltar == "n":
            limpar_tela()
            menu()
        else:
            print("-------------------------Opção Inválida!--------------------------")
        return False
    else:
        print("--------------------------------------------------------------------------------")
        print("««««««««««««««« Fornecedor não encontrado. Por favor, verifique o seu cadastro. »»»»»»»»»»»»»")
        print("--------------------------------------------------------------------------------")
        voltar = input("Cadastrar-se ? [S/N]: ")
        if voltar == "S" or voltar == "s":
            limpar_tela()
            adicionar_fornecedor()
            
        elif voltar == "N" or voltar == "n":
            limpar_tela()
            adicionar_Item()
        else:
            print("-------------------------Opção Inválida!--------------------------")

def remover_Item():
    limpar_tela()
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()
    
    print("---------------------------------- Remover Items Cadastrados  ----------------------------------------------")
   
    # Recupera todas as inventario da tabela
    executor.execute("SELECT * FROM item")
    item = executor.fetchall()
    
    # Exibe as Itens da Categoria abastecimento Geral
    print("Itens cadastradaos: \n")
    for item in item:
         print(f"ID: {item[0]} | Nome: {item[1]} | Peso: {item[2]} | Tipo:  {item[3]} | QTD: {item[4]} | Data de recepção: {item[6]} | Status: {item[8]}  ")
    
    #Solicitar o codigo do item na tablea inventario geral para eliminar o item

    print("------------------------------------------------------------------------------------------------------------------")
    id_remover = input("Informe o ID do item que deseja remover: ")

    #Remove o item do banco
    executor.execute(f"DELETE FROM item WHERE id_item = {id_remover} ")
    conexao.commit()
    limpar_tela()
    

    # Exibe as Itens da Categoria inventario Geral
    print("Itens cadastradaos Actualizados: \n")
    executor.execute("SELECT * FROM item")
    item = executor.fetchall()
    for item in item:
         print(f"ID: {item[0]} | Nome: {item[1]} | Tipo: {item[2]} | Peso: {item[3]} | QTD: {item[4]}   | Data de Recepção: {item[6]} | Status: {item[8]}     ")
    
    # Fecha a conexão
    conexao.close()

    print(f"«««««««««« Item removido com sucesso! »»»»»»»»»»")
    print("------------------------------------------------------------------------------------------------------------------")


    continuar = input("Desejas Voltar [S/N] ? ")
    #print("------------------------------------------------------------")
    if continuar == "S" or continuar == "s":
        limpar_tela()
        menu()
    elif continuar == "N" or continuar == "n":
        limpar_tela()
        remover_Item()
    else:
        print("-------------------------Opção Inválida!--------------------------")
        flat = False  

def listar_item():
    limpar_tela()
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()   

    print("----------------------------------Listar Todos Item Registrados ----------------------------------------------")  

    # Recupera todas as pessoas da tabela
    executor.execute("SELECT * FROM item")
    item = executor.fetchall()
    
    # Exibe as pessoas
    print("Itens cadastrados: \n")
    for item in item:
         print(f"ID: {item[0]} | Nome: {item[1]} | Peso: {item[2]} | Tipo: {item[3]} | QTD: {item[4]} | Data de Expiração: {item[5]}| Data de recepção: {item[6]} | Status: {item[8]}    ")
    
     

    # Fecha a conexão
    conexao.close()
    print("------------------------------------------------------------------------------------------------------------------")
    continuar = input("Desejas Voltar [S/N] ? ")
    #print("------------------------------------------------------------")
    if continuar == "S" or continuar == "s":
        limpar_tela()
        menu()
    elif continuar == "N" or continuar == "n":
        limpar_tela()
        listar_item()
    else:
        print("-------------------------Opção Inválida!--------------------------")
        flat = False  

def editar_Item():
    limpar_tela()
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()
    
    print("---------------------------------- Editar informações dos Item ----------------------------------------------")
   
    
    #Consulta que junta as duas tabelas
    consulta = '''
        SELECT  item.id_item,item.nome,item.tipo, item.peso,item.qtd, item.data_validade, item.data_recebido,item.status,
                fornecedor.nome, fornecedor.nif , categoria.nome
        FROM item
        INNER JOIN fornecedor ON item.id_item_fornec = fornecedor.id_fornec
        INNER JOIN categoria ON item.id_item_categ = categoria.id_categoria
        '''
    executor.execute(consulta)
    resultado = executor.fetchall()

    print("Itens cadastrados: \n")
    for id_item,nome,tipo,peso,qtd,data_validade,data_recebido,status, fornecedor,nif,categoria in resultado:
            print(f"ID: {id_item} | Item: {nome} | Categoria: {categoria} | Tipo: {tipo} | Peso: {peso} | QTD:  {qtd} | Data de Exp: {data_validade} | Data de Recep: {data_recebido} | Status: {status} | Fornecedor: {fornecedor} | NIF: {nif} ")
        
    print("------------------------------------------------------------------------------------------------------------------")
    id_editar = input("Informe o ID do item que deseja editar: ")
    print("------------------------------------------------------------------------------------------------------------------")


    #Solicitar os novos dados 
    novo_nome       = input("Novo nome do item: ")
    novo_tipo       = input("Novo tipo de Item: ")
    novo_peso       = input("Novo peso (kg / L): ")
    nova_qtd        = input("Nova quantidade: ")
    nova_validade   = input("Nova Data de Validade (DD-MM-YYYY): ")
    novo_fornecedor = input("Novo nome do fornecedor: ")
    novo_status     = input("Novo Status do Item [S/N]: ")
    
    executor.execute("SELECT * FROM categoria")
    categorias = executor.fetchall()
    print(f"Categorias Disponíveis: ")
    for cat in categorias:
        print(f"{cat[0]} - {cat[1]} |" , end=' ')
    
    novo_categoria = input("\nID da Categoria:  ")

    fun_data_validade(nova_validade)

    #Verifica se o fornecedor existe
    executor.execute("SELECT id_fornec FROM fornecedor WHERE nome = ?", (novo_fornecedor,))
    resultado = executor.fetchone()

    if resultado:
        id_fornec = resultado[0]
        executor.execute("""UPDATE item SET 
                            nome = ?, 
                            tipo = ?,
                            peso = ?, 
                            qtd = ?, 
                            id_item_fornec = ?, 
                            data_validade = ?, 
                            status = ?,
                            id_item_categ = ?
                            WHERE id_item = ?  """, 
                            (novo_nome, novo_tipo, novo_peso, nova_qtd,id_fornec, nova_validade, novo_status,novo_categoria, id_editar))
        conexao.commit()
        limpar_tela()
    

        # Exibe as Itens da Categoria inventario Geral    
        """executor.execute("SELECT * FROM item")
        inventario = executor.fetchall()
        """

            
        #Consulta que junta as duas tabelas
        consulta = '''
        SELECT  item.id_item,item.nome,item.tipo, item.peso,item.qtd, item.data_validade,item.status,
                fornecedor.nome,fornecedor.nif, categoria.nome
        FROM item
        INNER JOIN fornecedor ON item.id_item_fornec = fornecedor.id_fornec
        INNER JOIN categoria ON item.id_item_categ = categoria.id_categoria
        '''
        executor.execute(consulta)
        resultados = executor.fetchall()

        print("Itens cadastrados: \n")
        for id_item,nome,tipo,peso,qtd,data_validade,status, fornecedor,nif,categoria in resultados:
            print(f"ID: {id_item} | Item: {nome} | Tipo: {tipo} | Categoria: {categoria} | Peso: {peso} | QTD:  {qtd} | Data de Exp: {data_validade} | Status: {status} | Fornecedor: {fornecedor} ! NIF: {nif} ")
        


        print("\n «««««««««««« Item atualizado/editado com sucesso! »»»»»»»»»»»»»»")
        conexao.close
        print("------------------------------------------------------------------------------------------------------------------")


        continuar = input("Desejas realizar nova edicão [S/N] ? ")
        #print("------------------------------------------------------------")
        if continuar == "S" or continuar == "s":
            limpar_tela()
            editar_Item()
        
        elif continuar == "N" or continuar == "n":
            limpar_tela()
            menu()
        else:
            print("-------------------------Opção Inválida!--------------------------")
            flat = False    
    else:
        print("--------------------------------------------------------------------------------")
        print("««««««««««««««« Fornecedor não encontrado. Por favor, verifique o nome do fornecedor. »»»»»»»»»»»»»")
        print("--------------------------------------------------------------------------------")
        voltar = input("Tentar novamente ? [S/N]: ")
        if voltar == "S" or voltar == "s":
            limpar_tela()
            editar_Item()
        elif voltar == "N" or voltar == "n":
            limpar_tela()
            menu()
        else:
            print("-------------------------Opção Inválida!--------------------------")
        return False

def consultar_Item_fornecedor():
    limpar_tela()
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()   

    print("----------------------------------Consultar pelo Fornecedor ---------------------------------------------- \n")  

    consul_fornecedor = input("Inforne o nome do Fornecedor para a consulta: ")
    print("-----------------------------------------------------------------------------------------------------------") 

    executor.execute("SELECT id_fornec FROM fornecedor WHERE LOWER(nome) = ?", (consul_fornecedor,))
    resultado = executor.fetchone()

    if resultado:
        id_fornec = resultado[0]

        executor.execute(''' SELECT nome,tipo,peso,qtd,data_validade,data_recebido,status FROM item WHERE id_item_fornec = ?   ''', (id_fornec,))

        #Coleta os resultados
        resultados = executor.fetchall()
        for item in resultados:
                print(f"- Nome do Item: {item[0]} | Tipo de Item: {item[1]} |  Peso: {item[2]} | QTD: {item[3]} | Data de Expiração: {item[4]}| Data de Recepção: {item[5]} | Status do Item: {item[6]}")
        
        #Fecha a conexão
        conexao.close()

        print("------------------------------------------------------------------------------------------------------------------")


        continuar = input("Desejas realizar nova consulta [S/N] ? ")
        #print("------------------------------------------------------------")
        if continuar == "S" or continuar == "s":
            limpar_tela()
            consultar_Item_fornecedor()
        
        elif continuar == "N" or continuar == "n":
            limpar_tela()
            consultar()
        else:
            print("-------------------------Opção Inválida!--------------------------")
            flat = False
    else:
        print("Nenhum item encontrado para esse fornecedor.")

        print("------------------------------------------------------------------------------------------------------------------")


        continuar = input("Desejas realizar nova consulta [S/N] ? ")
        #print("------------------------------------------------------------")
        if continuar == "S" or continuar == "s":
            limpar_tela()
            consultar_Item_fornecedor()
        
        elif continuar == "N" or continuar == "n":
            limpar_tela()
            consultar()
        else:
            print("-------------------------Opção Inválida!--------------------------")
            flat = False

def consultar_Item_tipo():
    limpar_tela()
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()   


    print("----------------------------------Consultar pelo Tipo de Item ---------------------------------------------- \n")  

    consul_tipo = input("Inforne o Tipo do Item para a consulta: ")

    print("-----------------------------------------------------------------------------------------------------------") 

    executor.execute(""" SELECT nome, peso,qtd,data_validade,data_recebido,status FROM item WHERE LOWER(tipo) = ? AND status = ? """, (consul_tipo,'S'))

    #Coleta os resultados
    resultados = executor.fetchall()
 
    #Exibe os resultados
    if resultados:
        print(f"\nItens Do Tipo: {consul_tipo}: \n")
        for item in resultados:
            print(f"- Nome do Item: {item[0]} |  Peso: {item[1]} | QTD: {item[2]} | Data de Expiração: {item[3]} | Data de Recepção: {item[4]} | Status do Item: {item[5]} ")
    else:
        print("Nenhum item encontrado para esse item.")

    #Fecha a conexão
    conexao.close()

    print("------------------------------------------------------------------------------------------------------------------")


    continuar = input("Desejas realizar nova consulta [S/N] ? ")
    #print("------------------------------------------------------------")
    if continuar == "S" or continuar == "s":
        limpar_tela()
        consultar_Item_tipo()
       
    elif continuar == "N" or continuar == "n":
        limpar_tela()
        consultar()
    else:
        print("-------------------------Opção Inválida!--------------------------")
        flat = False

def consultar():
    print("----------------------------- Consulta de Items por Critério Específico-----------------------------------------------")
    print("1 - Pelo nome do fornecedor ")
    print("2 - Pelo tipo de item ")
    print("0 - Voltar ")


    print("-----------------------------------------------------------------------------------------------") 
       
    opcao_categoria = input("Selecione a opcção: ") 

    if opcao_categoria == "1":
        limpar_tela()
        consultar_Item_fornecedor()
        flat = False
    elif opcao_categoria == "2":
        limpar_tela()
        consultar_Item_tipo()
        flat = False
    
    elif opcao_categoria == "0":
        limpar_tela()
        menu()          
    else:
        print("----------------------------------Comando Inválido-------------------------------------------")
        flat = False

def relatorio():
    limpar_tela()
    conexao = sqlite3.connect("Logistica_Naval.db")
    executor = conexao.cursor()   
   
    consul = """
                SELECT nome,tipo, qtd, SUM(qtd * peso) AS peso_total
                FROM item
                GROUP BY nome
                """
    executor.execute(consul)
    resultados = executor.fetchall()
    print("----------------------------------- «« Relatório Geral»»  ------------------------------------------ \n")

    print("\n \n ««««« Relatório: Total por Itens »»»»» \n")
    for nome,tipo, qtd,peso_total in resultados:
        print(f"Nome do Item: {nome} | Tipo de Item: {tipo} |  QTD: {qtd} |  Peso Total ddo Items: {peso_total:.2f} ") 
       




    consulta = """
                SELECT tipo, COUNT(*) as total_item, SUM(qtd * peso) AS peso_total
                FROM item
                GROUP BY tipo
                """
    executor.execute(consulta)
    resultados = executor.fetchall()

    print("\n1n «««« Relatório: Total de Itens por Tipo »»»» \n")
    for tipo, total_item,peso_total in resultados:
        print(f"Tipo de Item: {tipo} |  Total de Items: {total_item} |  Total de Peso: {peso_total:.2f} ") 
       
    # Recupera todas as pessoas da tabela
    executor.execute("SELECT * FROM fornecedor")
    fornecedor = executor.fetchall()
    
    # Exibe as pessoas

    print("\n\n «««« Fornecedores cadastrados »»»»\n")
    for fornecedor in fornecedor:
         print(f"ID: {fornecedor[0]} | Fornecedor: {fornecedor[1]} | E-mail: {fornecedor[2]} | Endereço: {fornecedor[3]} | Telefone: {fornecedor[4]}     ")
    
    # Recupera todas as pessoas da tabela
    executor.execute("SELECT * FROM categoria")
    categoria = executor.fetchall()
    
    # Exibe as pessoas

    print("\n\n«««« Categorias cadastrados »»»»\n")
    for categoria in categoria:
         print(f"ID: {categoria[0]} | Categoria: {categoria[1]}   ")
    
     
    conexao.commit()
    conexao.close()


    print("------------------------------------------------------------------------------------------------------------------")

    continuar = input("Deseja voltar ?  [S/N] ? ")
    #print("------------------------------------------------------------")
    if continuar == "S" or continuar == "s":
        limpar_tela()
        menu()
       
    elif continuar == "N" or continuar == "n":
        limpar_tela()
        relatorio()
    else:
        print("-------------------------Opção Inválida!--------------------------")
        flat = False

def menu():
    conexao_banco()
    limpar_tela()
    flat = True
    while flat:
        print("-----------------------------------MENU PRINCIPAL------------------------------------------")
        print("1 - Adicionar um item ao inventario")
        print("2 - Editar as informações de um item existente")
        print("3 - Remover um item do inventário")
        print("4 - Listar todos os itens armazenados")
        print("5 - Consultar os itens por critérios específicos")
        print("6 - Gerar relatórios básicos (ex.: total de itens por tipo ou peso total dos itens armazenados);")
        print("7 - Cadastrar  Fornecedores")
        print("8 - Cadastrar  categoria")
        print("0 - Sair do programa")
        print("--------------------------------------------------------------------------------")

        opcao = input("Selecione uma opcção: ")
       
        if opcao == "1":
            limpar_tela()
            adicionar_Item() 
            break
        elif opcao == "2":
             limpar_tela()
             editar_Item()
             break
        elif opcao == "3":
            limpar_tela()
            remover_Item()
            break
        elif opcao == "4":
            limpar_tela()
            listar_item()
            break        
        elif opcao == "5":
            limpar_tela()
            consultar()
            break
        elif opcao == "6":
            limpar_tela()
            relatorio()
            break
        elif opcao == "7":
            limpar_tela()
            adicionar_fornecedor()
            break
        elif opcao == "8":
            limpar_tela()
            adicionar_categoria()
            break
        elif opcao == "0": 
             flat = False
             sys.exit()
        else:
            print("------------------Erro! Opção invalida!----------------------")
            continuar = input("Desejas Continuar [S/N] ? ")
            #print("------------------------------------------------------------")
            if continuar == "S" or continuar == "s":
                flat = True
                limpar_tela()
            elif continuar == "N" or continuar == "n":
                flat = False
                break
            else:
                print("-------------------------Opção Inválida!--------------------------")
                break

def limpar_tela():
    # Verifica o sistema operacional
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux ou Mac
        os.system('clear')

menu()