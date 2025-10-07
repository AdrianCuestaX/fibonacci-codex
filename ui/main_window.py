from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List

from fibonacci import FibonacciSummary, generate_fibonacci, summarize


class FibonacciApp:
    """Main application window for the Fibonacci visualizer."""

    MAX_TERMS = 500

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Fibonacci Studio")
        self.root.geometry("820x560")
        self.root.minsize(720, 520)
        self.root.configure(bg="#f4f6fb")

        self._configure_style()
        self._create_menu()

        self.count_var = tk.IntVar(value=15)
        self.scale_var = tk.DoubleVar(value=15)
        self.status_var = tk.StringVar(value="Ready")
        self.summary_last_var = tk.StringVar(value="-")
        self.summary_sum_var = tk.StringVar(value="0")
        self.summary_ratio_var = tk.StringVar(value="-")
        self.current_sequence: List[int] = []

        self._build_layout()
        self._calculate()

    def run(self) -> None:
        self.root.mainloop()

    # Layout -----------------------------------------------------------------
    def _configure_style(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Root.TFrame",
            background="#f4f6fb",
        )
        style.configure(
            "Header.TLabel",
            background="#f4f6fb",
            font=("Segoe UI Semibold", 18),
            foreground="#1f2933",
        )
        style.configure(
            "SubHeader.TLabel",
            background="#f4f6fb",
            font=("Segoe UI", 11),
            foreground="#52606d",
        )
        style.configure(
            "Card.TLabelframe",
            background="#ffffff",
            foreground="#1f2933",
        )
        style.configure(
            "Card.TLabelframe.Label",
            font=("Segoe UI Semibold", 10),
            foreground="#52606d",
        )
        style.configure(
            "CardValue.TLabel",
            background="#ffffff",
            font=("Segoe UI Semibold", 16),
            foreground="#1f2933",
        )
        style.configure(
            "Action.TButton",
            font=("Segoe UI Semibold", 10),
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI Semibold", 10),
        )
        style.configure(
            "Status.TLabel",
            background="#e4e7eb",
            font=("Segoe UI", 10),
            foreground="#52606d",
            padding=(12, 6),
        )

    def _create_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        help_menu = tk.Menu(menu_bar, tearoff=False)
        help_menu.add_command(label="About Fibonacci Studio", command=self._on_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, style="Root.TFrame")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=16)

        header_frame = ttk.Frame(container, style="Root.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 18))

        ttk.Label(header_frame, text="Fibonacci Studio", style="Header.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header_frame,
            text="Explora y exporta la serie de Fibonacci con estilo profesional.",
            style="SubHeader.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        controls_frame = ttk.Frame(container, padding=(16, 16), style="Root.TFrame")
        controls_frame.pack(fill=tk.X)

        ttk.Label(controls_frame, text="Numero de terminos:", style="SubHeader.TLabel").grid(
            row=0,
            column=0,
            sticky="w",
        )

        spinbox = ttk.Spinbox(
            controls_frame,
            from_=0,
            to=self.MAX_TERMS,
            width=8,
            textvariable=self.count_var,
            command=self._sync_from_spinbox,
            justify="center",
        )
        spinbox.grid(row=0, column=1, padx=(10, 20))
        spinbox.bind("<FocusOut>", lambda _event: self._sync_from_spinbox())

        scale = ttk.Scale(
            controls_frame,
            from_=0,
            to=self.MAX_TERMS,
            variable=self.scale_var,
            command=self._sync_from_scale,
        )
        scale.grid(row=0, column=2, sticky="ew")
        controls_frame.columnconfigure(2, weight=1)

        button_frame = ttk.Frame(controls_frame, style="Root.TFrame")
        button_frame.grid(row=0, column=3, padx=(20, 0))

        ttk.Button(
            button_frame,
            text="Calcular",
            style="Action.TButton",
            command=self._calculate,
        ).pack(side=tk.LEFT)

        ttk.Button(
            button_frame,
            text="Copiar",
            style="Action.TButton",
            command=self._copy_to_clipboard,
        ).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Button(
            button_frame,
            text="Guardar CSV",
            style="Action.TButton",
            command=self._export_csv,
        ).pack(side=tk.LEFT, padx=(10, 0))

        summary_frame = ttk.Frame(container, style="Root.TFrame")
        summary_frame.pack(fill=tk.X, pady=18)

        last_card = ttk.Labelframe(
            summary_frame, text="Ultimo valor", style="Card.TLabelframe", padding=16
        )
        last_card.grid(row=0, column=0, sticky="ew")
        ttk.Label(last_card, textvariable=self.summary_last_var, style="CardValue.TLabel").pack()

        sum_card = ttk.Labelframe(
            summary_frame, text="Suma total", style="Card.TLabelframe", padding=16
        )
        sum_card.grid(row=0, column=1, sticky="ew", padx=18)
        ttk.Label(sum_card, textvariable=self.summary_sum_var, style="CardValue.TLabel").pack()

        ratio_card = ttk.Labelframe(
            summary_frame, text="Proporcion dorada", style="Card.TLabelframe", padding=16
        )
        ratio_card.grid(row=0, column=2, sticky="ew")
        ttk.Label(ratio_card, textvariable=self.summary_ratio_var, style="CardValue.TLabel").pack()

        for index in range(3):
            summary_frame.columnconfigure(index, weight=1)

        table_frame = ttk.Frame(container, style="Root.TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("index", "value", "ratio")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12,
        )
        self.tree.heading("index", text="Indice")
        self.tree.heading("value", text="Valor")
        self.tree.heading("ratio", text="Valor / previo")

        self.tree.column("index", width=100, anchor=tk.CENTER)
        self.tree.column("value", width=200, anchor=tk.CENTER)
        self.tree.column("ratio", width=160, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            style="Status.TLabel",
            anchor="w",
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # Event handlers ----------------------------------------------------------
    def _sync_from_scale(self, raw_value: str) -> None:
        value = int(float(raw_value))
        self.count_var.set(value)

    def _sync_from_spinbox(self) -> None:
        value = max(0, min(self.count_var.get(), self.MAX_TERMS))
        self.count_var.set(value)
        self.scale_var.set(float(value))

    def _calculate(self) -> None:
        count = self.count_var.get()
        if count < 0:
            messagebox.showerror("Valor invalido", "Debes ingresar un numero entero no negativo.")
            return

        self.current_sequence = generate_fibonacci(count)
        summary = summarize(self.current_sequence)
        self._populate_tree(self.current_sequence)
        self._update_summary(summary)

        message = (
            f"Mostrando {summary.count} termino{'s' if summary.count != 1 else ''}."
            if summary.count
            else "No hay terminos para mostrar."
        )
        self.status_var.set(message)

    def _populate_tree(self, sequence: List[int]) -> None:
        self.tree.delete(*self.tree.get_children())
        for index, value in enumerate(sequence):
            ratio = ""
            if index > 0 and sequence[index - 1] != 0:
                ratio = f"{value / sequence[index - 1]:.6f}"
            self.tree.insert("", tk.END, values=(index, value, ratio))

    def _update_summary(self, summary: FibonacciSummary) -> None:
        self.summary_last_var.set(str(summary.last_value) if summary.last_value is not None else "-")
        self.summary_sum_var.set(str(summary.total_sum))
        if summary.golden_ratio is None:
            self.summary_ratio_var.set("-")
        else:
            self.summary_ratio_var.set(f"{summary.golden_ratio:.6f}")

    def _copy_to_clipboard(self) -> None:
        if not self.current_sequence:
            messagebox.showinfo("Serie vacia", "Nada para copiar todavia.")
            return
        text = ", ".join(str(value) for value in self.current_sequence)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Serie copiada al portapapeles.")

    def _export_csv(self) -> None:
        if not self.current_sequence:
            messagebox.showinfo("Serie vacia", "Genera la serie antes de exportar.")
            return
        default_filename = f"fibonacci_{datetime.now():%Y%m%d_%H%M%S}.csv"
        path = filedialog.asksaveasfilename(
            title="Guardar serie de Fibonacci",
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV files", "*.csv"), ("Todos los archivos", "*.*")],
        )
        if not path:
            return

        try:
            with Path(path).open("w", newline="", encoding="utf-8") as file_handle:
                writer = csv.writer(file_handle)
                writer.writerow(["Indice", "Valor", "Valor/Previo"])
                previous = None
                for index, value in enumerate(self.current_sequence):
                    ratio = ""
                    if previous not in (None, 0):
                        ratio = f"{value / previous:.6f}"
                    writer.writerow([index, value, ratio])
                    previous = value
            self.status_var.set(f"Archivo guardado en {path}.")
        except OSError as error:
            messagebox.showerror("Error al guardar", str(error))

    def _on_about(self) -> None:
        messagebox.showinfo(
            "Acerca de Fibonacci Studio",
            "Fibonacci Studio\n\nVisualiza y exporta de forma cuidada la clasica serie matematica.",
        )


def launch() -> None:
    FibonacciApp().run()
