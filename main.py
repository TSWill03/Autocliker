import customtkinter
import pydirectinput
import keyboard
from time import sleep

nome_arquivo = "pos_mouse.txt"
hook_ativo = False


def click(x, y, delay=0):
    pydirectinput.click(x, y)
    sleep(delay)


def comecar_autoclick():
    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            valores = linha.split()
            if len(valores) == 3:
                x, y, delay = map(int, valores)
                click(x, y, delay)
        rodar_eterno_check = checkbox.get()
        if rodar_eterno_check == "infinito":
            delay_eterno = delay_rodar_eterno.get()
            sleep(float(delay_eterno))
            rodar_eterno()


def arquivo_posicoes(nome_arquivo, informacao):
    try:
        with open(nome_arquivo, 'a') as arquivo:
            # Abre o arquivo no modo de escrita para adicionar uma nova linha
            arquivo.write('\n' + informacao)

    except FileNotFoundError:
        # Se o arquivo não existe, cria o arquivo e adiciona a informação
        with open(nome_arquivo, 'w') as arquivo:
            arquivo.write(informacao)


def pegar_ultima_linha():
    try:
        with open(nome_arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
            if linhas:
                return linhas[-1].strip()
            else:
                return None
    except FileNotFoundError:
        return None  # Retorna None se o arquivo não existir


def mostrar_posicao_tempo():
    posicao = pegar_ultima_linha()
    if posicao is not None:
        x, y, delay = posicao.split()
        mensagem = f"O click foi marcado na posicao x={x} y={y} com {delay} segundos de delay"
        posicao_label.configure(text=mensagem)
        janela.after(1000, lambda: posicao_label.configure(text=""))


def validar_numeros(char):
    return char.isdigit()


def Registrar_Clique():
    global hook_ativo

    def detectar_tecla_c(e):
        if e.event_type == keyboard.KEY_DOWN and e.name == 'c':
            if hook_ativo:
                x, y = pydirectinput.position()
                delay_cliq = delay_texto.get().strip()  # Remove espaços em branco
                delay_cliq = ''.join(filter(validar_numeros, delay_cliq))
                delay_texto.insert(0, delay_cliq)
                delay_cliq = 0 if not delay_cliq or delay_cliq == '' else int(delay_cliq)
                xy = f"{x} {y} {delay_cliq}"
                delay_texto.delete(0, "end")
                arquivo_posicoes(nome_arquivo, xy)

                mostrar_posicao_tempo()

    # Conecta o evento de detecção da tecla 'c'
    keyboard.hook(detectar_tecla_c)
    hook_ativo = True


def Parar_Registrar():
    global hook_ativo
    if hook_ativo:
        keyboard.unhook_all()
        hook_ativo = False


def rodar_eterno():
    delay = int(delay_rodar_eterno.get())
    while True:
        comecar_autoclick()
        sleep(delay)  # Garante que o delay não seja negativo


# Criação da janela
janela = customtkinter.CTk()
janela.geometry("650x450")
janela.title("WyllyCliker")

# Criação do Entry
validacao_numeros = janela.register(validar_numeros)  # Registra a função de validação
delay_texto = customtkinter.CTkEntry(janela, width=90, height=30, validate="key",
                                     validatecommand=(validacao_numeros, "%S"))
delay_texto.place(x=190, y=50)

# Criação dos botões
botao_Registrar_Clique = customtkinter.CTkButton(janela, text="Registrar Clique", command=Registrar_Clique)
botao_Registrar_Clique.place(x=20, y=50)

botao_Parar_Registrar = customtkinter.CTkButton(janela, text="Parar de Registrar", command=Parar_Registrar)
botao_Parar_Registrar.place(x=20, y=130)

botao_Iniciar_autoclick = customtkinter.CTkButton(janela, text="Iniciar autoclick", command=comecar_autoclick)
botao_Iniciar_autoclick.place(x=20, y=210)

# Criação da label para exibir a última posição
posicao_label = customtkinter.CTkLabel(janela, text="")
posicao_label.place(x=20, y=90)

delay_rodar_eterno = customtkinter.CTkEntry(janela, width=110, height=30, validate="key",
                                            validatecommand=(validacao_numeros, "%S"))
delay_rodar_eterno.place(x=20, y=260)
delay_rodar_eterno_label = customtkinter.CTkLabel(janela, text="Delay para Iniciar novamente\nColoque em segundos",
                                                  justify="left")
delay_rodar_eterno_label.place(x=140, y=260)

checkbox = customtkinter.CTkCheckBox(janela, text="Rodar Eternamente", onvalue="infinito", offvalue="finito")
checkbox.place(x=190, y=210)

janela.mainloop()
