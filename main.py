import PySimpleGUI as sg
import pyodbc

class app:
    def __init__(self):
        sg.theme('LightBrown5')
        self.dados = (
            "Driver={SQL Server};"
            "Server=REIFFERPC\SQLEXPRESS;"
            "Database=filmes"
        )
        self.conexao = pyodbc.connect(self.dados)
        self.cursor = self.conexao.cursor()


    def TelaPrincipal(self):
        buttons = [[sg.Button('Filmes Assistidos',size=(20,1)),sg.Button('Filmes Para Assistir',size=(20,1)),sg.Button('Adicionar Filme',size=(20,1))]]
        layout = [
            [sg.Image(r'download.png', size=(800, 200))],
            [sg.Text('')],
            [sg.Column(buttons,justification='center')]
        ]

        return sg.Window('App de Filmes',layout=layout,finalize=True)



    def TelaAssistidos(self):
        assistidos = self.cursor.execute("SELECT assistidos FROM filmes WHERE assistidos IS NOT NULL")
        assistidos = self.cursor.fetchall()

        layout = [
            [sg.Text('Lista de Filmes Assistidos',size=(74,1)),sg.Image('check.png')],
            [sg.Listbox(assistidos,size=(100,20),key='filmesassistidos')],
            [sg.Button('Remover Filme',size=(20,3)),sg.Button('Voltar',size=(20,3))]

        ]

        return sg.Window('Filmes Assistidos',layout=layout,finalize=True,element_justification='center')


    def TelaParaAssistir(self):
        assistirr = self.cursor.execute("SELECT para_assistir FROM filmes WHERE para_assistir IS NOT NULL")
        assistir = self.cursor.fetchall()

        layout = [
            [sg.Text('Lista de Filmes Para Assistir',size=(74,1)),sg.Image('not a check.png')],
            [sg.Listbox(assistir,size=(100,20),key='listaassitir')],
            [sg.Button('Filme Já Assistido',size=(20,3)),sg.Button('Remover Filme',size=(20,3)),sg.Button('Voltar',size=(20,3))]
        ]

        return sg.Window('Filmes Assistidos',layout=layout,finalize=True,element_justification='center')


    def TelaAdicionarFilme(self):
        layout = [
            [sg.Text('Nome do Novo Filme')],
            [sg.InputText('',key='filme',do_not_clear=False)],
            [sg.Button('Adicionar Filme',size=(20,2)),sg.Button('Voltar',size=(20,2))]
        ]

        return sg.Window('Adicionar Novo Filme',layout=layout,finalize=True,element_justification='center')



    def ChamarTelas(self):
        self.janela1, self.janela2,self.janela3,self.janela4 = self.TelaPrincipal(),None,None,None
        while True:
            window , event , values = sg.read_all_windows()
            if window == self.janela1 and event == sg.WINDOW_CLOSED:
                break
            elif window == self.janela1 and event == 'Filmes Assistidos':
                self.janela2 = self.TelaAssistidos()
                self.janela1.close()
            elif window == self.janela2 and event == sg.WINDOW_CLOSED:
                self.janela2.close()
                self.janela1 = self.TelaPrincipal()
            elif window == self.janela2 and event == 'Voltar':
                self.janela2.close()
                self.janela1 = self.TelaPrincipal()
            elif window == self.janela2 and event == 'Remover Filme':
                if values["filmesassistidos"] == []:
                    sg.popup_auto_close('Selecione um filme para Excluí-lo!')
                else:
                    remover = values["filmesassistidos"]
                    self.cursor.execute(f"DELETE FROM filmes where assistidos = '{remover[0][0]}'")
                    self.conexao.commit()
                    self.janela2['filmesassistidos'].update()
                    self.janela2.close()
                    self.janela2 = self.TelaAssistidos()
            elif window == self.janela1 and event == 'Filmes Para Assistir':
                self.janela1.close()
                self.janela3 = self.TelaParaAssistir()
            elif window == self.janela3 and event == sg.WINDOW_CLOSED:
                self.janela3.close()
                self.janela1 = self.TelaPrincipal()
            elif window == self.janela3 and event == 'Voltar':
                self.janela3.close()
                self.janela1 = self.TelaPrincipal()
            elif window == self.janela3 and event == 'Filme Já Assistido':
                if values['listaassitir'] == []:
                    sg.popup_auto_close('Selecione um Filme para marca-lo como assistido!')
                else:
                    ja_visto = values['listaassitir']
                    self.cursor.execute(f"INSERT INTO filmes(assistidos) VALUES('{ja_visto[0][0]}')")
                    self.conexao.commit()
                    self.cursor.execute(f"DELETE FROM filmes WHERE para_assistir = '{ja_visto[0][0]}'")
                    self.conexao.commit()
                    sg.popup_auto_close('Filme Marcado como Assistido!')
                    self.janela3['listaassitir'].update()
                    self.janela3.close()
                    self.janela3 = self.TelaParaAssistir()
            elif window == self.janela3 and event == 'Remover Filme':
                if values["listaassitir"] == []:
                    sg.popup_auto_close('Selecione um filme para Excluí-lo!')
                else:
                    remover = values["listaassitir"]
                    self.cursor.execute(f"DELETE FROM filmes where para_assistir = '{remover[0][0]}'")
                    self.conexao.commit()
                    self.janela3['listaassitir'].update()
                    self.janela3.close()
                    self.janela3 = self.TelaParaAssistir()
            elif window == self.janela1 and event == 'Adicionar Filme':
                self.janela1.close()
                self.janela4 = self.TelaAdicionarFilme()
            elif window == self.janela4 and event == sg.WINDOW_CLOSED:
                self.janela4.close()
                self.janela1 = self.TelaPrincipal()
            elif window == self.janela4 and event == 'Voltar':
                self.janela4.close()
                self.janela1 = self.TelaPrincipal()
            elif window == self.janela4 and event == 'Adicionar Filme':
                if values['filme'] == '':
                    sg.popup_auto_close('Digite um nome de filme!')
                else:
                    filme = values['filme']
                    self.cursor.execute(f"INSERT INTO filmes(para_assistir) VALUES ('{filme}')")
                    self.conexao.commit()
                    sg.popup_auto_close('Filme adicionado com sucesso',auto_close_duration=0.8)

app = app()
app.ChamarTelas()