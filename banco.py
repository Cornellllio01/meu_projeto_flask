import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Configuração do banco SQLite
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL
)
''')
conn.commit()

# Funções CRUD

def listar_usuarios():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    for i, usuario in enumerate(usuarios):
        tag = 'par' if i % 2 == 0 else 'impar'
        tree.insert("", tk.END, values=usuario, tags=(tag,))

def cadastrar_usuario():
    nome = entry_nome.get().strip()
    idade = entry_idade.get().strip()

    if not nome or not idade:
        messagebox.showwarning("⚠️ Aviso", "Por favor, preencha nome e idade.")
        return
    if not idade.isdigit():
        messagebox.showwarning("⚠️ Aviso", "Idade deve ser um número.")
        return

    cursor.execute("INSERT INTO usuarios (nome, idade) VALUES (?, ?)", (nome, int(idade)))
    conn.commit()
    messagebox.showinfo("✅ Sucesso", "Usuário cadastrado!")
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    listar_usuarios()

def atualizar_usuario():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("⚠️ Aviso", "Selecione um usuário para atualizar.")
        return
    
    usuario = tree.item(selecionado, 'values')
    user_id = usuario[0]

    novo_nome = simpledialog.askstring("✏️ Atualizar nome", "Novo nome:", initialvalue=usuario[1])
    if novo_nome is None or novo_nome.strip() == "":
        return

    nova_idade = simpledialog.askstring("✏️ Atualizar idade", "Nova idade:", initialvalue=usuario[2])
    if nova_idade is None or not nova_idade.isdigit():
        messagebox.showwarning("⚠️ Aviso", "Idade inválida.")
        return

    cursor.execute("UPDATE usuarios SET nome = ?, idade = ? WHERE id = ?", (novo_nome.strip(), int(nova_idade), user_id))
    conn.commit()
    messagebox.showinfo("✅ Sucesso", "Usuário atualizado!")
    listar_usuarios()

def remover_usuario():
    selecionado = tree.focus()
    if not selecionado:
        messagebox.showwarning("⚠️ Aviso", "Selecione um usuário para remover.")
        return

    usuario = tree.item(selecionado, 'values')
    user_id = usuario[0]
    confirma = messagebox.askyesno("⚠️ Confirmação", f"Remover usuário '{usuario[1]}'?")
    if confirma:
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        conn.commit()
        messagebox.showinfo("✅ Sucesso", "Usuário removido!")
        listar_usuarios()

def sair():
    conn.close()
    root.destroy()

# Interface Tkinter
root = tk.Tk()
root.title("🧑‍💻 Gerenciador Colorido de Usuários")
root.geometry("560x460")
root.configure(bg="#222831")

# Estilos para a Treeview
style = ttk.Style(root)
style.theme_use("clam")

style.configure("Treeview",
                background="#393e46",
                foreground="#eeeeee",
                rowheight=28,
                fieldbackground="#393e46",
                font=("Segoe UI", 11))
style.map('Treeview',
          background=[('selected', '#00adb5')],
          foreground=[('selected', '#222831')])
style.configure("Treeview.Heading",
                background="#00adb5",
                foreground="#eeeeee",
                font=("Segoe UI", 13, "bold"))

# Cores alternadas para linhas
tree_tag_par = "par"
tree_tag_impar = "impar"
style.configure("Treeview", bordercolor="#00adb5", borderwidth=1)
tree_tag_colors = {tree_tag_par: "#222831", tree_tag_impar: "#393e46"}

# Frame para formulário
frame_form = tk.Frame(root, bg="#222831")
frame_form.pack(pady=15)

lbl_nome = tk.Label(frame_form, text="Nome:", bg="#222831", fg="#00adb5", font=("Segoe UI", 14, "bold"))
lbl_nome.grid(row=0, column=0, padx=10, pady=6, sticky='e')
entry_nome = tk.Entry(frame_form, font=("Segoe UI", 13), bg="#393e46", fg="#eeeeee", insertbackground='white', relief='flat')
entry_nome.grid(row=0, column=1, padx=10, pady=6)

lbl_idade = tk.Label(frame_form, text="Idade:", bg="#222831", fg="#00adb5", font=("Segoe UI", 14, "bold"))
lbl_idade.grid(row=1, column=0, padx=10, pady=6, sticky='e')
entry_idade = tk.Entry(frame_form, font=("Segoe UI", 13), bg="#393e46", fg="#eeeeee", insertbackground='white', relief='flat')
entry_idade.grid(row=1, column=1, padx=10, pady=6)

# Botões coloridos
frame_botoes = tk.Frame(root, bg="#222831")
frame_botoes.pack(pady=12)

btn_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=cadastrar_usuario,
                          bg="#00adb5", fg="#222831", font=("Segoe UI", 13, "bold"),
                          activebackground="#00ffcc", activeforeground="#222831",
                          relief="raised", bd=3, width=14)
btn_cadastrar.grid(row=0, column=0, padx=8)

btn_atualizar = tk.Button(frame_botoes, text="Atualizar", command=atualizar_usuario,
                          bg="#ff5722", fg="white", font=("Segoe UI", 13, "bold"),
                          activebackground="#ff784e", activeforeground="#222831",
                          relief="raised", bd=3, width=14)
btn_atualizar.grid(row=0, column=1, padx=8)

btn_remover = tk.Button(frame_botoes, text="Remover", command=remover_usuario,
                        bg="#e53935", fg="white", font=("Segoe UI", 13, "bold"),
                        activebackground="#ff6f60", activeforeground="#222831",
                        relief="raised", bd=3, width=14)
btn_remover.grid(row=0, column=2, padx=8)

btn_sair = tk.Button(frame_botoes, text="Sair", command=sair,
                     bg="#393e46", fg="#eeeeee", font=("Segoe UI", 13, "bold"),
                     activebackground="#222831", activeforeground="#00adb5",
                     relief="raised", bd=3, width=14)
btn_sair.grid(row=0, column=3, padx=8)

# Treeview (tabela) de usuários
tree = ttk.Treeview(root, columns=("ID", "Nome", "Idade"), show="headings", selectmode="browse")
tree.heading("ID", text="ID")
tree.column("ID", width=50, anchor="center")
tree.heading("Nome", text="Nome")
tree.column("Nome", width=320)
tree.heading("Idade", text="Idade")
tree.column("Idade", width=80, anchor="center")
tree.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

# Configurar as cores alternadas
tree.tag_configure(tree_tag_par, background=tree_tag_colors[tree_tag_par])
tree.tag_configure(tree_tag_impar, background=tree_tag_colors[tree_tag_impar])

# Listar usuários ao abrir
listar_usuarios()

root.mainloop()
