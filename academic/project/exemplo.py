"""Exemplo básico do Prof. Luan."""

import tkinter as tk
from pathlib import Path
from tkinter import messagebox

if Path('lista_de_tarefas.txt').is_file():
    with Path('lista_de_tarefas.txt').open('w') as arquivo:
        arquivo.write('')


# Função para adicionar uma nova tarefa à lista
def adicionar_tarefa():
    """Adicionar tarefa."""
    tarefa = entry_tarefa.get()
    if tarefa:
        lista_tarefas.insert(tk.END, tarefa)
        entry_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning('Aviso', 'Por favor, insira uma tarefa válida.')


# Função para editar a tarefa selecionada
def editar_tarefa():
    """Editar tarefa."""
    selecao = lista_tarefas.curselection()
    if selecao:
        indice = selecao[0]
        nova_tarefa = entry_tarefa.get()
        if nova_tarefa:
            lista_tarefas.delete(indice)
            lista_tarefas.insert(indice, nova_tarefa)
            entry_tarefa.delete(0, tk.END)
        else:
            messagebox.showwarning(
                'Aviso',
                'Por favor, insira uma tarefa válida.',
            )
    else:
        messagebox.showwarning('Aviso', 'Selecione uma tarefa para editar.')


# Função para excluir a tarefa selecionada
def excluir_tarefa():
    """Excluir tarefa."""
    selecao = lista_tarefas.curselection()
    if selecao:
        indice = selecao[0]
        lista_tarefas.delete(indice)
        entry_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning('Aviso', 'Selecione uma tarefa para excluir.')


# Função para salvar a lista de tarefas em um arquivo de texto
def salvar_lista():
    """Salvar lista."""
    tarefas = lista_tarefas.get(0, tk.END)
    with Path('lista_de_tarefas.txt').open('w') as arquivo:
        for tarefa in tarefas:
            arquivo.write(tarefa + '\n')
    lista_tarefas.delete(0, tk.END)


# Função para carregar a lista de tarefas de um arquivo de texto
def carregar_lista():
    """Carregar lista."""
    lista_tarefas.delete(0, tk.END)
    try:
        with Path('lista_de_tarefas.txt').open() as arquivo:
            for linha in arquivo:
                lista_tarefas.insert(tk.END, linha.strip())
    except FileNotFoundError:
        pass


# Configuração da janela principal
root = tk.Tk()
root.title('Lista de Tarefas')
# dimensões da janela
root.geometry('300x200+100+100')

# Criando e configurando a lista de tarefas
lista_tarefas = tk.Listbox(root, selectmode=tk.SINGLE)
lista_tarefas.pack(pady=10)

# Criando e configurando a entrada de texto para adicionar/editar tarefas
entry_tarefa = tk.Entry(root)
entry_tarefa.pack(pady=5)

# Botões
btn_adicionar = tk.Button(
    root,
    text='Adicionar Tarefa',
    command=adicionar_tarefa,
)
btn_editar = tk.Button(root, text='Editar Tarefa', command=editar_tarefa)
btn_excluir = tk.Button(root, text='Excluir Tarefa', command=excluir_tarefa)
btn_salvar = tk.Button(root, text='Salvar Lista', command=salvar_lista)
btn_carregar = tk.Button(root, text='Carregar Lista', command=carregar_lista)

btn_adicionar.pack()
btn_editar.pack()
btn_excluir.pack()
btn_salvar.pack()
btn_carregar.pack()

# Carregar a lista de tarefas do arquivo (se existir)
carregar_lista()

# Iniciar o loop da aplicação
root.mainloop()
