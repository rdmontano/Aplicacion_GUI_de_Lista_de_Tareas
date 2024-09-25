import tkinter as tk
from tkinter import messagebox, ttk

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LISTA DE TAREAS")
        self.root.geometry("500x400")
        self.tasks = []

        # Colores para sombreado
        self.completed_bg = "lightgreen"  # Verde claro para tareas completadas
        self.pending_bg = "lightcoral"    # Rojo claro para tareas pendientes

        # Marco principal
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(pady=10)

        # Entrada de texto para agregar nuevas tareas
        self.task_entry = tk.Entry(frame, width=35, font=("Arial", 12))
        self.task_entry.grid(row=0, column=0, padx=5, pady=10)
        self.task_entry.bind('<Return>', self.add_task)

        # Botón de añadir tarea
        add_button = tk.Button(frame, text="➕ Añadir Tarea", command=self.add_task, width=15)
        add_button.grid(row=0, column=1, padx=5)

        # Botón de marcar como completada
        complete_button = tk.Button(frame, text="✔️ Marcar Completada", command=self.mark_completed, width=20)
        complete_button.grid(row=1, column=0, padx=5, pady=5)

        # Botón de eliminar tarea
        delete_button = tk.Button(frame, text="🗑️ Eliminar Tarea", command=self.delete_task, width=15)
        delete_button.grid(row=1, column=1, padx=5, pady=5)

        # Treeview para mostrar las tareas con sombreado
        self.task_tree = ttk.Treeview(self.root, columns=("task",), show="headings", height=10)
        self.task_tree.heading("task", text="TAREAS")
        self.task_tree.column("task", width=450)
        self.task_tree.pack(pady=10)

        # Aplicar estilos de fondo
        self.style = ttk.Style()
        self.style.map('Treeview', background=[('selected', 'blue')])  # Color de selección
        self.style.layout('Treeview', [('Treeview.treearea', {'sticky': 'nswe'})])

        # Manejo de eventos para un clic y doble clic
        self.task_tree.bind('<Double-1>', self.edit_task)

    def add_task(self, event=None):
        #Agregar una nueva tarea desde el campo de entrada.
        task = self.task_entry.get()
        if task:
            self.tasks.append({"task": task, "completed": False})
            self.task_tree.insert("", tk.END, values=(task,), tags=("pending",))
            self.task_entry.delete(0, tk.END)
            self.apply_colors()  # Aplicar el sombreado
        else:
            messagebox.showwarning("Advertencia", "La tarea no puede estar vacía.")

    def mark_completed(self):
        #Marcar una tarea seleccionada como completada o pendiente.
        try:
            selected_item = self.task_tree.selection()[0]
            task_index = self.task_tree.index(selected_item)
            task = self.tasks[task_index]

            # Cambiar el estado de la tarea y actualizar visualmente
            if not task["completed"]:
                task["completed"] = True
                self.task_tree.item(selected_item, tags=("completed",))
            else:
                task["completed"] = False
                self.task_tree.item(selected_item, tags=("pending",))

            self.apply_colors()  # Reaplicar el sombreado después del cambio
        except IndexError:
            messagebox.showwarning("Advertencia", "Seleccione una tarea para marcar como completada.")

    def delete_task(self):
        #Eliminar la tarea seleccionada.
        try:
            selected_item = self.task_tree.selection()[0]
            task_index = self.task_tree.index(selected_item)
            self.task_tree.delete(selected_item)
            self.tasks.pop(task_index)
        except IndexError:
            messagebox.showwarning("Advertencia", "Seleccione una tarea para eliminar.")

    def edit_task(self, event=None):
        #Editar una tarea al hacer doble clic.
        try:
            selected_item = self.task_tree.selection()[0]
            task_index = self.task_tree.index(selected_item)
            task = self.tasks[task_index]

            # Mostrar la tarea en el Entry para su edición
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(tk.END, task["task"])

            # Borrar la tarea de la lista mientras se edita
            self.task_tree.delete(selected_item)
            self.tasks.pop(task_index)
        except IndexError:
            pass

    def apply_colors(self):
        #Aplicar los colores de fondo a las tareas según su estado.
        for index, task in enumerate(self.tasks):
            item_id = self.task_tree.get_children()[index]
            if task["completed"]:
                self.task_tree.tag_configure("completed", background=self.completed_bg, foreground="black")
            else:
                self.task_tree.tag_configure("pending", background=self.pending_bg, foreground="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
