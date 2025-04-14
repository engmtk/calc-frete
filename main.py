import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import requests

# Comando para a Criação da tabela caso na exista! Vai facilitar a sua vida, acredite!


def inicializar_banco():
    with sqlite3.connect('frete.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CADASTRO_FRETE (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origem TEXT,
                destino TEXT,
                distancia_km REAL,
                tipo_combustivel TEXT,
                consumo_medio REAL,
                valor_combustivel REAL,
                litros_usados REAL,
                valor_combustivel_total REAL,
                pedagios REAL,
                valor_pedagios_total REAL,
                lucro REAL,
                valor_total REAL,
                data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Função auxiliar para geocodificar o endereço -> coordenadas


def geocodificar(endereco):
    url = f"https://nominatim.openstreetmap.org/search"
    params = {
        'q': endereco,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'frete-calculadora-app'
    }

    resposta = requests.get(url, params=params, headers=headers)
    dados = resposta.json()

    if dados:
        lat = float(dados[0]['lat'])
        lon = float(dados[0]['lon'])
        return lat, lon
    else:
        raise Exception(f"Endereço não encontrado: {endereco}")

# Função para calcular distância real com OSRM


def calcular_distancia_km(origem, destino):
    try:
        lat1, lon1 = geocodificar(origem)
        lat2, lon2 = geocodificar(destino)

        url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
        resposta = requests.get(url)
        rota = resposta.json()

        distancia_metros = rota['routes'][0]['distance']
        distancia_km = distancia_metros / 1000
        return round(distancia_km, 2)

    except Exception as e:
        print(f"[Erro na rota]: {e}")
        messagebox.showwarning(
            "Atenção", "Erro ao obter distância. Usando valor padrão.")
        return 100.0  # fallback

# Função principal que realiza o cálculo do frete


def calcular_frete():
    try:
        origem = entry_origem.get()
        destino = entry_destino.get()
        tipo_combustivel = combo_combustivel.get()
        consumo = float(entry_consumo.get())
        valor_combustivel = float(entry_valor_combustivel.get())
        lucro = float(entry_lucro.get())

        distancia_km = calcular_distancia_km(origem, destino)

        # Aqui eu inclui os Pedágios (simulado)
        pedagios = 2
        valor_pedagios_total = 15.00 * pedagios

        litros_usados = distancia_km / consumo
        valor_combustivel_total = litros_usados * valor_combustivel
        valor_total = valor_combustivel_total + valor_pedagios_total + lucro

        # Grava no banco local com segurança as informações inseridas na console do usuário (sem travar porque é uma caracteristica do SQLite :D)
        with sqlite3.connect('frete.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO CADASTRO_FRETE (
                    origem, destino, distancia_km, tipo_combustivel, consumo_medio,
                    valor_combustivel, litros_usados, valor_combustivel_total,
                    pedagios, valor_pedagios_total, lucro, valor_total
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                origem, destino, distancia_km, tipo_combustivel, consumo,
                valor_combustivel, litros_usados, valor_combustivel_total,
                pedagios, valor_pedagios_total, lucro, valor_total
            ))
            conn.commit()

        messagebox.showinfo("Frete Calculado", f"Distância: {distancia_km} km\n"
                                               f"Litros: {litros_usados:.2f} L\n"
                                               f"Total: R$ {valor_total:.2f}")

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# GUI com Tkinter
root = tk.Tk()
root.title("Cálculo de Frete")
root.geometry("400x400")

tk.Label(root, text="Origem:").pack()
entry_origem = tk.Entry(root, width=40)
entry_origem.pack()

tk.Label(root, text="Destino:").pack()
entry_destino = tk.Entry(root, width=40)
entry_destino.pack()

tk.Label(root, text="Tipo de Combustível:").pack()
combo_combustivel = ttk.Combobox(
    root, values=["Gasolina", "Álcool", "Diesel", "Gás"])
combo_combustivel.pack()

tk.Label(root, text="Consumo Médio (km/l):").pack()
entry_consumo = tk.Entry(root)
entry_consumo.pack()

tk.Label(root, text="Valor do Combustível (R$):").pack()
entry_valor_combustivel = tk.Entry(root)
entry_valor_combustivel.pack()

tk.Label(root, text="Lucro desejado (R$):").pack()
entry_lucro = tk.Entry(root)
entry_lucro.pack()

tk.Button(root, text="Calcular Frete", command=calcular_frete).pack(pady=10)

# Inicializa o banco!
inicializar_banco()

root.mainloop()
