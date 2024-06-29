import tkinter as tk
from tkinter import messagebox, ttk
import ipaddress

def subnetear_red():
    try:
        # Obtener los valores de las entradas
        input_ip = entry_ip.get()
        num_subnets = int(entry_subnets.get())

        # Crear un objeto IPv4Network
        red = ipaddress.IPv4Network(input_ip, strict=False)

        # Calcular el nuevo prefijo
        prefix_length = red.prefixlen + num_subnets.bit_length()

        # Calcular las subredes resultantes
        subnets = list(red.subnets(new_prefix=prefix_length))

        # Mostrar la ventana de información detallada
        mostrar_info(subnets[:num_subnets], red)

    except ValueError as e:
        messagebox.showerror("Error", "Ingreso equivocado. Modelo de ingreso esperado: 192.168.0.0/24")

def mostrar_info(subnets, red):
    # Crear la ventana para mostrar la información detallada
    info_window = tk.Toplevel(root)
    info_window.title("Información Detallada de Subredes")
    info_window.geometry("1000x600")  # Tamaño inicial grande de la ventana

    # Crear un Frame para la información de la red original
    frame_original = tk.Frame(info_window, bg="lightblue", padx=10, pady=10)
    frame_original.pack(pady=10, padx=10, fill=tk.BOTH)

    # Mostrar la información de la red original en el marco superior central
    info_original = f"Información de la red original:\n"
    info_original += f"Red: {red.network_address}\n"
    info_original += f"Máscara de red: {red.netmask}\n"
    info_original += f"Dirección de broadcast: {red.broadcast_address}\n"
    info_original += f"Rango de direcciones IP disponibles: {red.network_address + 1} a {red.broadcast_address - 1}\n\n"

    label_original = tk.Label(frame_original, text=info_original, justify=tk.LEFT)
    label_original.pack()

    # Crear un Canvas para contener las subredes y permitir el desplazamiento
    canvas = tk.Canvas(info_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Añadir un scrollbar vertical al canvas
    scrollbar_vertical = ttk.Scrollbar(info_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar_vertical.set)

    # Crear el frame_subred que contendrá la información de las subredes
    frame_subred = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_subred, anchor=tk.NW)

    # Colores alternados para las filas de la tabla
    colors = ["#FFCDD2", "#B3E5FC", "#C8E6C9", "#F8BBD0"]  # Colores claros para fondo

    # Mostrar la información de las subredes en una tabla de 3 columnas
    for i, subred in enumerate(subnets, 1):
        info_subred = f"Información de la subred {i}:\n"
        info_subred += f"Red: {subred.network_address}\n"
        info_subred += f"Máscara de red: {subred.netmask}\n"
        info_subred += f"Dirección de broadcast: {subred.broadcast_address}\n"
        info_subred += f"Rango de direcciones IP disponibles: {subred.network_address + 1} a {subred.broadcast_address - 1}\n"

        # Calcular la cantidad de hosts (equipos) en la subred
        num_hosts = subred.num_addresses - 2  # Restamos la red y el broadcast
        info_subred += f"Cantidad de equipos: {num_hosts}\n\n"

        # Colorear filas alternas
        bg_color = colors[(i - 1) % len(colors)]

        # Crear el marco para cada celda de la tabla
        subred_frame = tk.Frame(frame_subred, bg=bg_color, padx=10, pady=10)
        subred_frame.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=10, pady=5, sticky=tk.W)

        label_subred = tk.Label(subred_frame, text=info_subred, justify=tk.LEFT, bg=bg_color)
        label_subred.pack()

    # Ajustar el tamaño del canvas
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Ajustar el tamaño de la ventana según el contenido
    info_window.geometry(f"{info_window.winfo_reqwidth()}x{info_window.winfo_reqheight()}")

# Crear la ventana principal
root = tk.Tk()
root.title("Subneteo de Redes")
root.configure(bg="green")

# Ajustar el tamaño de la ventana principal y centrarla
root.geometry("600x500")
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
position_top = int(window_height / 2 - 500 / 2)
position_right = int(window_width / 2 - 600 / 2)
root.geometry(f"+{position_right}+{position_top}")

# Crear el título de la ventana principal
label_title = tk.Label(root, text="Subneteo de Redes", bg="green", fg="lightblue", font=("Helvetica", 16, "bold"))
label_title.pack(pady=10)

# Crear y colocar las etiquetas y entradas
label_ip = tk.Label(root, text="Dirección IP y máscara en CIDR:", bg="green", fg="lightblue")
label_ip.pack(pady=5)

entry_ip = tk.Entry(root)
entry_ip.pack(pady=5)

label_subnets = tk.Label(root, text="Cantidad de subredes deseadas:", bg="green", fg="lightblue")
label_subnets.pack(pady=5)

entry_subnets = tk.Entry(root)
entry_subnets.pack(pady=5)

# Crear y colocar el botón para calcular las subredes
button_calculate = tk.Button(root, text="Calcular Subredes", command=subnetear_red)
button_calculate.pack(pady=20)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
