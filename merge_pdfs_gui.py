import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class PDFMergerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Mesclador de PDFs by Luis")
        self.root.geometry("600x400")
        self.pdf_files = []

        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial, 12"))

        # Titulo
        self.label_title = ttk.Label(root, text="Mesclador de PDFs", font=("Arial", 16, "bold"))
        self.label_title.pack(pady=10)

        # Botão para adicionar PDFs
        self.btn_add = ttk.Button(root, text="Adicionar PDFs", command=self.add_pdfs)
        self.btn_add.pack(pady=5)

        # Botão para remover PDF selecionado
        self.btn_remove = ttk.Button(root, text="Remover PDF Selecionado", command=self.remove_pdf)
        self.btn_remove.pack(pady=5)

        # Lista para exibir PDFs selecionados
        self.listbox = tk.Listbox(root, height=10, width=50, font=("Arial", 10))
        self.listbox.pack(pady=10)

        # Botão para mesclar PDFs
        self.btn_merge = ttk.Button(root, text="Mesclar PDFs", command=self.merge_pdfs)
        self.btn_merge.pack(pady=10)

        # Label de status
        self.status_label = ttk.Label(root, text="Nenhum arquivo selecionado", wraplength=500)
        self.status_label.pack(pady=10)

    def add_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Selecione os arquivos PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))
        self.update_status()

    def remove_pdf(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.listbox.delete(index)
            self.pdf_files.pop(index)
            self.update_status()

    def update_status(self):
        if self.pdf_files:
            self.status_label.config(text=f"{len(self.pdf_files)} arquivo(s) selecionado(s)")
        else:
            self.status_label.config(text="Nenhum arquivo selecionado")

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showinfo("Informação", "Nenhum arquivo PDF selecionado.")
            return
        
        output_file = filedialog.asksaveasfilename(
            title="Salvar PDF mesclado como",
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if not output_file:
            messagebox.showinfo("Informação", "Nenhum nome de arquivo de saída fornecido.")
            return
        
        merger = PyPDF2.PdfMerger()
        try:
            for pdf in self.pdf_files:
                if not os.path.exists(pdf):
                    raise FileNotFoundError(f"O arquivo {pdf} não foi encontrado")
                merger.append(pdf)
            with open(output_file, 'wb') as output_file_handle:
                merger.write(output_file_handle)
            messagebox.showinfo("Sucesso", f"PDFs mesclados com sucesso em {output_file}")
            self.pdf_files.clear()
            self.listbox.delete(0, tk.END)
            self.update_status()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao mesclar PDFs: {str(e)}")

def main():
        root = tk.Tk()
        app = PDFMergerApp(root)
        root.mainloop()

if __name__ == "__main__":
        main()

