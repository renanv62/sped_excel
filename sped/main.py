from datetime import datetime
from functools import partial

from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDIconButton
import tkinter.filedialog
import pandas as pd
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from matplotlib.figure import Figure
from kivy.uix.behaviors import DragBehavior
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from kivy.config import Config
from kivy.core.window import Window
import matplotlib.pyplot as plt

Window.maximize()
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class DraggableLabel(DragBehavior, FigureCanvasKivyAgg):
    def __init__(self, figure=None, **kwargs):
        super(DraggableLabel, self).__init__(figure=figure, **kwargs)
        self.bar_chart_id = None
        self._drag_start_x = 0
        self._drag_start_y = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._drag_start_x = touch.x
            self._drag_start_y = touch.y
            return super(DraggableLabel, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.x += touch.x - self._drag_start_x
            self.y += touch.y - self._drag_start_y
            self._drag_start_x = touch.x
            self._drag_start_y = touch.y
            return super(DraggableLabel, self).on_touch_move(touch)


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dataframes_content = None
        self.canvas_widgets = []
        self.selected_y_col = None
        self.column_data_y = None

        self.selected_y_col_2 = None
        self.column_data_y_2 = None

        self.dropdown_btn_update_xAxis_5 = None
        self.dropdown_btn_update_yAxis_5 = None
        self.dropdown_btn_update_yAxis_5A = None

    def build(self):
        return Builder.load_file('main.kv')

    ################ CALL INFO FROM PROCESS FILES INIT ##################
    def call_efd_icms(self,dado):
        from process_sped.process_efd_icms import EFD_ICMS
        filter = "Text File (*.txt)"
        # abre o filedialog
        efd_icms_file_path = tkinter.filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
        # verifica se algum arquivo foi selecionado
        if not efd_icms_file_path:
            return
        # executa a função do backend, que está no arquivo chamado 'process_efd_icms'
        EFD_ICMS(efd_icms_file_path,dado)
        if dado == '1':
            if EFD_ICMS:
                # the error appears to be here
                self.root.ids.screen_manager.current = 'scr 3'
            else:
                return IOError
        else:
            pass
    def call_efd_pis(self,dado):
        from process_sped.process_efd_pis import EFD_PIS
        filter = "Text File (*.txt)"
        efd_pis_file_path = tkinter.filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
        if not efd_pis_file_path:
            return
        # executa a função do backend, que está no arquivo chamado 'process_efd_pis'
        EFD_PIS(efd_pis_file_path,dado)
        if dado == '1':
            if EFD_PIS:
                # the error appears to be here
                self.root.ids.screen_manager.current = 'scr 3'
            else:
                return IOError
        else:
            pass

    def call_ecd_icms(self,dado):
        from process_sped.process_ecd_icms import ECD_ICMS
        filter = "Text File (*.txt)"
        ecd_icms_file_path = tkinter.filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
        if not ecd_icms_file_path:
            return
        ECD_ICMS(ecd_icms_file_path,dado)

    def call_ecd_pis(self,dado):
        from process_sped.process_ecd_pis import ECD_PIS
        filter = "Text File (*.txt)"
        ecd_pis_file_path = tkinter.filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
        if not ecd_pis_file_path:
            return
        ECD_PIS(ecd_pis_file_path,dado)
    ################ CALL INFO FROM PROCESS FILES END ##################

    ################ RETRIEVE INFO FROM PROCESS FILES INIT ##################
    #receive the df's from process python files
    retrieve_list_dict_keys = None
    retrieve_list_dict_values = None
    def receive_df(self,get_all_df,type):
        if type == "0":
            df_info = {
                "000": get_all_df[0],"001": get_all_df[1],"002": get_all_df[2],"005": get_all_df[3],"015": get_all_df[4],"100": get_all_df[5],"150":get_all_df[6],"175":get_all_df[7],"190":get_all_df[8],"200": get_all_df[9],"205":get_all_df[10]
            }
        elif type == "1":
            df_info = {
                "000": get_all_df[0],"0035": get_all_df[1],"0100": get_all_df[2],"C170": get_all_df[3],"0300": "0300","0350": "0350"
            }
        elif type == "2":
            df_info = {
                "000": get_all_df[0], "0150": get_all_df[1], "0200": get_all_df[2], "0250": "0250", "0300": "0300", "0350": "0350"
            }
        elif type == "3":
            df_info = {
                "000": get_all_df[0], "0150": get_all_df[1], "0200": get_all_df[2], "0250": "0250", "0300": "0300", "0350": "0350"
            }
        # Create buttons dynamically based on df_info keys
        for key, df_data in df_info.items():
            setattr(self, key, df_data)
        # Filter out keys with None or empty values
        valid_keys = [key for key, value in df_info.items() if
                      value is not None and (isinstance(value, str) and value != "") or not value.empty]
        #store only the non empty keys names
        self.retrieve_list_dict_keys = valid_keys
        #stores all df_info to filter in the future
        self.retrieve_list_dict_values = df_info
    ################ RETRIEVE INFO FROM PROCESS FILES END ##################

    ################ DROPDOWN LIST RIGHT SIDE POWER BI INIT ##################
    def list_keysDropdown_open(self):
        new_df_info = self.retrieve_list_dict_keys
        # Create menu items for the dropdown
        listKeys_menu_items = [
            {
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda item=f"{i}": self.x_y_selected(item)
            } for i in new_df_info
        ]
        # Create and open the dropdown menu
        self.menu = MDDropdownMenu(
            caller=self.root.ids.list_keys_btn,
            items=listKeys_menu_items,
            width_mult=3,
        ).open()

    def x_y_selected(self,item):
        self.selected_both_item = item
        #update the btn text
        btn = self.root.ids.list_keys_btn
        btn.text = item
    ################ DROPDOWN LIST RIGHT SIDE POWER BI END ##################

    ################ TWO DROPDOWN BELOW THE FIRST ONE INIT ##################
    def xAxis_option_1(self,number_type,blank_instance=None):
        new_df_info = self.retrieve_list_dict_keys
        item = self.selected_both_item
        content_dict = self.retrieve_list_dict_values
        selected_values = content_dict.get(item, None)
        # Create menu items for the dropdown based on columns_list
        columns_list = selected_values.columns.tolist()
        x_menu_items_1 = [
            {
                "text": f"{column}",
                "viewclass": "OneLineListItem",
                "on_release": lambda col_option_1=f"{column}": self.xAxis_item_selected_1(col_option_1, item, number_type)
            } for column in columns_list
        ]
        # identify from where it comes the button


        if number_type == 1:# for bar option 1
            caller_id = self.root.ids.layout_to_list_btn_xAxis_1
        elif number_type == 2:# for bar option 1
            caller_id = self.root.ids.layout_to_list_btn_xAxis_2
        elif number_type == 3:# for bar option 1
            caller_id = self.root.ids.layout_to_list_btn_xAxis_3
        elif number_type == 4:# for bar option 1
            caller_id = self.root.ids.layout_to_list_btn_xAxis_4
        elif number_type == 5:# for update option 1
            caller_id = self.dropdown_btn_update_xAxis_5

        self.menu = MDDropdownMenu(
            caller=caller_id,
            items=x_menu_items_1,
            width_mult=3,
        ).open()

    ################ RECIEVE CONTENT TO 'SEND IT' TO CHART INIT ##################
    def xAxis_item_selected_1(self, col, item, number_type):
        # get the button to update the text from it (these lines do only that)
        if number_type == 1:
            x_axis_down_btn = self.root.ids.layout_to_list_btn_xAxis_1
            x_axis_down_btn.text = str(col)
        elif number_type == 2:
            x_axis_down_btn = self.root.ids.layout_to_list_btn_xAxis_2
            x_axis_down_btn.text = str(col)
        elif number_type == 3:
            x_axis_down_btn = self.root.ids.layout_to_list_btn_xAxis_3
            x_axis_down_btn.text = str(col)
        elif number_type == 4:
            x_axis_down_btn = self.root.ids.layout_to_list_btn_xAxis_4
            x_axis_down_btn.text = str(col)
        elif number_type == 5:
            x_axis_down_btn = self.dropdown_btn_update_xAxis_5
            x_axis_down_btn.text = str(col)
        # get the button to update the text from it (these lines above do only that)
        # get the parameters
        self.selected_x_col_1 = col
        self.selected_x_item_1 = item
        # get the df from dict
        content_dict = self.retrieve_list_dict_values
        # extract the data based on the info
        selected_df = content_dict.get(self.selected_x_item_1, None)
        self.column_data_x_1 = selected_df[self.selected_x_col_1].tolist() if selected_df is not None else []

    ################ TWO DROPDOWN BELOW THE FIRST ONE INIT ##################
    def yAxis_option(self,number_type,blank_instance=None):
        new_df_info = self.retrieve_list_dict_keys
        item = self.selected_both_item
        content_dict = self.retrieve_list_dict_values
        selected_values = content_dict.get(item, None)
        # Create menu items for the dropdown based on columns_list
        columns_list = selected_values.columns.tolist()
        y_menu_items = [
            {
                "text": f"{column}",
                "viewclass": "OneLineListItem",
                "on_release": lambda col=f"{column}": self.yAxis_item_selected(col, item, number_type)
            } for column in columns_list
        ]
        # identify from where it comes the button
        if number_type == 1:
            caller_id = self.root.ids.layout_to_list_btn_yAxis_1
        elif number_type == 2:
            caller_id = self.root.ids.layout_to_list_btn_yAxis_2
        elif number_type == 3:
            caller_id = self.root.ids.layout_to_list_btn_yAxis_3
        elif number_type == 4:
            caller_id = self.root.ids.layout_to_list_btn_yAxis_4
        elif number_type == 5:
            caller_id = self.dropdown_btn_update_yAxis_5
        self.menu = MDDropdownMenu(
            caller=caller_id,
            items=y_menu_items,
            width_mult=3,
        ).open()
    ################ TWO DROPDOWN BELOW THE FIRST ONE INIT ##################
    def yAxis_item_selected(self, col, item, number_type):
        # get the button to update the text from it
        if number_type == 1:
            y_axis_down_btn = self.root.ids.layout_to_list_btn_yAxis_1
            y_axis_down_btn.text = str(col)
        elif number_type == 2:
            y_axis_down_btn = self.root.ids.layout_to_list_btn_yAxis_2
            y_axis_down_btn.text = str(col)
        elif number_type == 3:
            y_axis_down_btn = self.root.ids.layout_to_list_btn_yAxis_3
            y_axis_down_btn.text = str(col)
        elif number_type == 4:
            y_axis_down_btn = self.root.ids.layout_to_list_btn_yAxis_4
            y_axis_down_btn.text = str(col)
        elif number_type == 5:
            y_axis_down_btn = self.dropdown_btn_update_yAxis_5
            y_axis_down_btn.text = str(col)
        # get the parameters
        self.selected_y_col = col
        self.selected_y_item = item
        # get the df from dict
        content_dict = self.retrieve_list_dict_values
        # extract the data based on the info
        selected_df = content_dict.get(self.selected_y_item, None)
        self.column_data_y = selected_df[self.selected_y_col].tolist() if selected_df is not None else []

    def yAxis_option_2(self,number_type,blank_instance=None):
        new_df_info = self.retrieve_list_dict_keys
        item = self.selected_both_item
        content_dict = self.retrieve_list_dict_values
        selected_values = content_dict.get(item, None)
        # Create menu items for the dropdown based on columns_list
        columns_list = selected_values.columns.tolist()
        y_menu_items_2 = [
            {
                "text": f"{column}",
                "viewclass": "OneLineListItem",
                "on_release": lambda col_option_2=f"{column}": self.yAxis_item_selected_2(col_option_2, item, number_type)
            } for column in columns_list
        ]
        # identify from where it comes the button
        if number_type == "1A":  # for bar option 1
            caller_id_2 = self.root.ids.layout_to_list_btn_yAxis_1A
        elif number_type == "2A":  # for bar option 1
            caller_id_2 = self.root.ids.layout_to_list_btn_yAxis_2A
        elif number_type == "3A":  # for bar option 1
            caller_id_2 = self.root.ids.layout_to_list_btn_yAxis_3A
        elif number_type == "4A":  # for bar option 1
            caller_id_2 = self.root.ids.layout_to_list_btn_yAxis_4A
        elif number_type == "5A":  # for bar option 1
            caller_id_2 = self.dropdown_btn_update_yAxis_5A
        self.menu_x = MDDropdownMenu(
            caller=caller_id_2,
            items=y_menu_items_2,
            width_mult=3,
        ).open()

    ################ RECIEVE CONTENT TO 'SEND IT' TO CHART INIT ##################
    def yAxis_item_selected_2(self, col, item, number_type):
        # get the button to update the text from it (these lines do only that)
        if number_type == "1A":
            y_axis_down_btn = self.root.ids.layout_to_list_btn_yAxis_1A
            y_axis_down_btn.text = str(col)
        elif number_type == "2A":
            y_axis_down_btn = self.root.ids.layout_to_list_btn_yAxis_2A
            y_axis_down_btn.text = str(col)
        elif number_type == "3A":
            y_axis_down_btn = self.root.ids.layout_to_list_btn_yAxis_3A
            y_axis_down_btn.text = str(col)
        elif number_type == "4A":
            y_axis_down_btn = self.root.ids.layout_to_list_btn_yAxis_4A
            y_axis_down_btn.text = str(col)
        elif number_type == "5A":
            y_axis_down_btn = self.dropdown_btn_update_yAxis_5A
            y_axis_down_btn.text = str(col)
        # get the button to update the text from it (these lines above do only that)
        # get the parameters
        self.selected_y_col_2 = col
        self.selected_y_item_2 = item
        # get the df from dict
        content_dict = self.retrieve_list_dict_values
        # extract the data based on the info
        selected_df = content_dict.get(self.selected_y_item_2, None)
        self.column_data_y_2 = selected_df[self.selected_y_col_2].tolist() if selected_df is not None else []
    ################ RECIEVE CONTENT TO 'SEND IT' TO CHART END ##################

    def create_bar_chart(self):
        x_label_head_1 = self.selected_x_col_1
        x_label_info_1 = self.column_data_x_1
        split_x_label = []
        y_label_head = self.selected_y_col
        y_label_info = self.column_data_y
        y_label_head_2 = self.selected_y_col_2
        y_label_info_2 = self.column_data_y_2

        if x_label_head_1 and y_label_head:
            fig = Figure(facecolor='none')
            ax = fig.add_subplot(111)
            if "DT" in x_label_head_1:# converter em data
                # Substituir os zeros por barras
                x_label_info_1_formatted = [date[:2] + '/' + date[2:4] + '/' + date[4:] for date in x_label_info_1]
                # Converter as datas
                x_dates = pd.to_datetime(x_label_info_1_formatted, format='%d/%m/%Y', dayfirst=True)
                if self.selected_y_col_2 is not None:#duas informações de valores
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    y_label_info_2 = [int(value) for value in y_label_info_2]
                    # Criar um DataFrame com as informações
                    data = {
                        'Date': x_dates,
                        'y_label_info': y_label_info,
                        'y_label_info_2': y_label_info_2
                    }
                    df = pd.DataFrame(data)
                    # Criar coluna combinando mês e ano
                    df['Month_Year'] = df['Date'].dt.to_period('M')
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Month_Year')['y_label_info'].sum()
                    sum_y_label_info_2 = df.groupby('Month_Year')['y_label_info_2'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    sum_y_label_info_2.index = sum_y_label_info_2.index.astype(str)

                    bar_width = 0.35 #largura da barra
                    ax.bar(sum_y_label_info.index, sum_y_label_info, bar_width, label='y_label_info') #cria barra 1
                    #ax.bar(sum_y_label_info_2.index, sum_y_label_info_2)
                    ax.bar([x + bar_width for x in range(len(sum_y_label_info_2))], sum_y_label_info_2, bar_width,
                           label='y_label_info_2') # cria barra 2 (ao lado)
                    # Adicionar rótulos aos eixos
                    ax.set_xlabel('Mês')
                    ax.set_ylabel('Soma dos Valores')
                else:# uma informação de valor
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    # Criar um DataFrame com as informações
                    data = {
                        'Date': x_dates,
                        'y_label_info': y_label_info
                    }
                    df = pd.DataFrame(data)
                    # Criar coluna combinando mês e ano
                    df['Month_Year'] = df['Date'].dt.to_period('M')
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Month_Year')['y_label_info'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    bar_width = 0.2  # largura da barra
                    ax.bar(sum_y_label_info.index, sum_y_label_info, bar_width, label='y_label_info')  # cria barra 1
                    # Adicionar rótulos aos eixos
                    ax.set_xlabel('Mês')
                    ax.set_ylabel('Soma dos Valores')
            else:# separar por categoria
                if self.selected_y_col_2 is not None: # duas informações
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    y_label_info_2 = [int(value) for value in y_label_info_2]
                    # Criar um DataFrame com as informações
                    data = {
                        'Category': x_label_info_1,  # Nome da coluna com as informações não-datas
                        'y_label_info': y_label_info,
                        'y_label_info_2': y_label_info_2
                    }
                    df = pd.DataFrame(data)
                    # Agrupar os valores de y_label_info por categoria e somar
                    sum_y_label_info = df.groupby('Category')['y_label_info'].sum()
                    sum_y_label_info_2 = df.groupby('Category')['y_label_info_2'].sum()

                    bar_width = 0.2
                    # Plotar os gráficos de barras
                    ax.bar(sum_y_label_info.index, sum_y_label_info, bar_width,  label='y_label_info')
                    ax.bar([x + bar_width for x in range(len(sum_y_label_info_2))], sum_y_label_info_2, bar_width,
                           label='y_label_info_2')  # cria barra 2 (ao lado)

                    # Adicionar rótulos aos eixos
                    ax.set_xlabel('Categoria')
                    ax.set_ylabel('Soma dos Valores')
                else:
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    # Criar um DataFrame com as informações
                    data = {
                        'Category': x_label_info_1,  # Nome da coluna com as informações não-datas
                        'y_label_info': y_label_info
                    }
                    df = pd.DataFrame(data)

                    # Agrupar os valores de y_label_info por categoria e somar
                    sum_y_label_info = df.groupby('Category')['y_label_info'].sum()

                    bar_width = 0.2
                    # Plotar os gráficos de barras
                    ax.bar(sum_y_label_info.index, sum_y_label_info, bar_width, label='y_label_info')

                    # Adicionar rótulos aos eixos
                    ax.set_xlabel('Categoria')
                    ax.set_ylabel('Soma dos Valores')

            canvas = DraggableLabel(figure=fig)
            canvas.size_hint = (0.5, 0.5)
            canvas.bar_chart_id = id(canvas)  # add the id
            self.root.ids.layout_to_show_LF.add_widget(canvas)  # print canvas on layout
            bar_type = "bar"
            self.list_labels(canvas,bar_type)
        else:
            print("Please select both X and Y axis items for Bar Chart.")

    def create_line_chart(self):
        x_label_head_1 = self.selected_x_col_1
        x_label_info_1 = self.column_data_x_1
        split_x_label = []

        y_label_head = self.selected_y_col
        y_label_info = self.column_data_y

        y_label_head_2 = self.selected_y_col_2
        y_label_info_2 = self.column_data_y_2

        if x_label_head_1 and y_label_head:
            fig = Figure(facecolor='none')
            ax = fig.add_subplot(111)
            if "DT" in x_label_head_1:  # separar por data
                # Substituir os zeros por barras
                x_label_info_1_formatted = [date[:2] + '/' + date[2:4] + '/' + date[4:] for date in x_label_info_1]
                # Converter as datas
                x_dates = pd.to_datetime(x_label_info_1_formatted, format='%d/%m/%Y', dayfirst=True)
                if self.selected_y_col_2 is not None:  # duas informações de valores
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    y_label_info_2 = [int(value) for value in y_label_info_2]
                    # Criar um DataFrame com as informações
                    data = {
                        'Date': x_dates,
                        'y_label_info': y_label_info,
                        'y_label_info_2': y_label_info_2
                    }
                    df = pd.DataFrame(data)
                    # Criar coluna combinando mês e ano
                    df['Month_Year'] = df['Date'].dt.to_period('M')
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Month_Year')['y_label_info'].sum()
                    sum_y_label_info_2 = df.groupby('Month_Year')['y_label_info_2'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    sum_y_label_info_2.index = sum_y_label_info_2.index.astype(str)

                    # Plota a linha para y_label_info
                    ax.plot(sum_y_label_info.index, sum_y_label_info,  label='y_label_info')
                    # Plota a linha para y_label_info_2
                    ax.plot(sum_y_label_info_2.index, sum_y_label_info_2,  label='y_label_info_2')

                else: # uma informação de valor
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    # Criar um DataFrame com as informações
                    data = {
                        'Date': x_dates,
                        'y_label_info': y_label_info
                    }
                    df = pd.DataFrame(data)
                    # Criar coluna combinando mês e ano
                    df['Month_Year'] = df['Date'].dt.to_period('M')
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Month_Year')['y_label_info'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    # Plota a linha para y_label_info
                    ax.plot(sum_y_label_info.index, sum_y_label_info, label='y_label_info')
            else:#separar por categoria
                if self.selected_y_col_2 is not None:  # duas informações de valores
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    y_label_info_2 = [int(value) for value in y_label_info_2]
                    # Criar um DataFrame com as informações
                    data = {
                        'Category': x_label_info_1,
                        'y_label_info': y_label_info,
                        'y_label_info_2': y_label_info_2
                    }
                    df = pd.DataFrame(data)
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Category')['y_label_info'].sum()
                    sum_y_label_info_2 = df.groupby('Category')['y_label_info_2'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    sum_y_label_info_2.index = sum_y_label_info_2.index.astype(str)
                    # Plota a linha para y_label_info
                    ax.plot(sum_y_label_info.index, sum_y_label_info, label='y_label_info')
                    # Plota a linha para y_label_info_2
                    ax.plot(sum_y_label_info_2.index, sum_y_label_info_2, label='y_label_info_2')
                else: # uma informação de valor
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    # Criar um DataFrame com as informações
                    data = {
                        'Category': x_label_info_1,
                        'y_label_info': y_label_info
                    }
                    df = pd.DataFrame(data)
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Category')['y_label_info'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    # Plota a linha para y_label_info
                    ax.plot(sum_y_label_info.index, sum_y_label_info, label='y_label_info')
            # finish the process
            canvas = DraggableLabel(figure=fig)
            canvas.size_hint = (0.5, 0.5)
            canvas.bar_chart_id = id(canvas)  # add the id
            self.root.ids.layout_to_show_LF.add_widget(canvas)  # print canvas on layout
            bar_type = "line"
            self.list_labels(canvas,bar_type)
        else:
            print("Please select both X and Y axis items for Bar Chart.")


    def create_pizza_chart(self):
        x_label_head_1 = self.selected_x_col_1
        x_label_info_1 = self.column_data_x_1
        split_x_label = []

        y_label_head = self.selected_y_col
        y_label_info = self.column_data_y

        y_label_head_2 = self.selected_y_col_2
        y_label_info_2 = self.column_data_y_2

        if x_label_head_1 and y_label_head:
            fig = Figure(facecolor='none')
            ax = fig.add_subplot(111)
            if "DT" in x_label_head_1:# separar por data
                # Substituir os zeros por barras
                x_label_info_1_formatted = [date[:2] + '/' + date[2:4] + '/' + date[4:] for date in x_label_info_1]
                # Converter as datas
                x_dates = pd.to_datetime(x_label_info_1_formatted, format='%d/%m/%Y', dayfirst=True)
                if self.selected_y_col_2 is not None:  # duas informações de valores
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    y_label_info_2 = [int(value) for value in y_label_info_2]
                    # Criar um DataFrame com as informações
                    data = {
                        'Date': x_dates,
                        'y_label_info': y_label_info,
                        'y_label_info_2': y_label_info_2
                    }
                    df = pd.DataFrame(data)
                    # Criar coluna combinando mês e ano
                    df['Month_Year'] = df['Date'].dt.to_period('M')
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Month_Year')['y_label_info'].sum()
                    sum_y_label_info_2 = df.groupby('Month_Year')['y_label_info_2'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    sum_y_label_info_2.index = sum_y_label_info_2.index.astype(str)
                    # Plotar o gráfico de pizza para sum_y_label_info
                    ax.pie(sum_y_label_info, labels=sum_y_label_info.index, autopct='%1.1f%%', startangle=140)

                else: # uma informação de valor
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    # Criar um DataFrame com as informações
                    data = {
                        'Date': x_dates,
                        'y_label_info': y_label_info
                    }
                    df = pd.DataFrame(data)
                    # Criar coluna combinando mês e ano
                    df['Month_Year'] = df['Date'].dt.to_period('M')
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Month_Year')['y_label_info'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    # Plotar o gráfico de pizza para sum_y_label_info
                    ax.pie(sum_y_label_info, labels=sum_y_label_info.index, autopct='%1.1f%%', startangle=140)
            else: # separar por categoria
                if self.selected_y_col_2 is not None:  # duas informações de valores
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    y_label_info_2 = [int(value) for value in y_label_info_2]
                    # Criar um DataFrame com as informações
                    data = {
                        'Category': x_label_info_1,
                        'y_label_info': y_label_info,
                        'y_label_info_2': y_label_info_2
                    }
                    df = pd.DataFrame(data)
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Category')['y_label_info'].sum()
                    sum_y_label_info_2 = df.groupby('Category')['y_label_info_2'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    sum_y_label_info_2.index = sum_y_label_info_2.index.astype(str)
                    # Plotar o gráfico de pizza para sum_y_label_info
                    ax.pie(sum_y_label_info, labels=sum_y_label_info.index, autopct='%1.1f%%', startangle=140)
                else: # uma informação de valor
                    # Converter as strings em números inteiros
                    y_label_info = [int(value) for value in y_label_info]
                    # Criar um DataFrame com as informações
                    data = {
                        'Category': x_label_info_1,
                        'y_label_info': y_label_info
                    }
                    df = pd.DataFrame(data)
                    # Agrupar os valores de y_label_info por mês e ano e somar
                    sum_y_label_info = df.groupby('Category')['y_label_info'].sum()
                    # Converter o índice de volta para strings para plotagem
                    sum_y_label_info.index = sum_y_label_info.index.astype(str)
                    # Plotar o gráfico de pizza para sum_y_label_info
                    ax.pie(sum_y_label_info, labels=sum_y_label_info.index, autopct='%1.1f%%', startangle=140)

            canvas = DraggableLabel(figure=fig)
            canvas.size_hint = (0.5, 0.5)
            canvas.bar_chart_id = id(canvas)  # add the id
            self.root.ids.layout_to_show_LF.add_widget(canvas)  # print canvas on layout
            bar_type = "pizza"
            self.list_labels(canvas,bar_type)
        else:
            print("Please select both X and Y axis items for Bar Chart.")

    def create_table_chart(self):
        if self.selected_x_col_1 and self.selected_y_col:
            # close the popup
            popup = self.root.ids.my_popup
            popup.height = 0
            popup.opacity = 0
            print(f"X-Axis Item for Pizza Chart: {self.selected_x_col_1}")
            print('-')
            print(f"Y-Axis Item for Pizza Chart: {self.selected_y_col}")
        else:
            print("Please select both X and Y axis items for Pizza Chart.")


    def list_labels(self,list_canvas,bar_type):
        ###### LIST THE CHARTS ADDED ON THE RIGHT SIDE ######
        gridList_canvas = self.root.ids.list_charts_added  # get the first layout
        # THE LEFT SIDE THAT GOES INSIDE THE LIST CHARTS ADDED
        mdbox_first_layout = MDBoxLayout(id="first_layout_box",
                                         orientation="horizontal")  # get the 2 layouts below id:first_layout_box
        layout_chart_name = MDBoxLayout(orientation="vertical", size_hint_x=.6,
                                        padding=5)  # left layout id:left_label_layout
        # THE RIGHT SIDE THAT GOES INSIDE THE LIST CHARTS ADDED
        layout_for_icons = AnchorLayout(orientation="horizontal", size_hint_x=.4, padding=5,
                                        anchor_x="right")  # right layout id:right_icons_layout
        box_for_icons_on_layout = MDBoxLayout(orientation="horizontal", size_hint=(.5, .5), pos_hint={
            "center_y": .5})  # box inside the right layout id:icons_box_layout

        label = MDLabel(text=f"ID: {list_canvas.bar_chart_id}", size_hint_x=1)  # label
        edit_icon = MDIconButton(icon="lead-pencil", icon_size="16dp")  # icon
        edit_icon.bind(on_release=lambda instance: self.modal_chart(instance, list_canvas, label,bar_type))  # icon action
        trash_icon = MDIconButton(icon="trash-can-outline", icon_size="16dp")  # icon
        # trash_icon.bind(on_release=lambda instance: self.delete_chart(instance, canvas,label)) # icon action
        trash_icon.bind(on_release=lambda instance: self.delete_chart(instance, list_canvas, mdbox_first_layout))

        # set the label and icons to their respective layouts
        layout_chart_name.add_widget(label)
        box_for_icons_on_layout.add_widget(edit_icon)
        box_for_icons_on_layout.add_widget(trash_icon)

        # add the layouts to the main layout
        layout_for_icons.add_widget(box_for_icons_on_layout)
        mdbox_first_layout.add_widget(layout_chart_name)
        mdbox_first_layout.add_widget(layout_for_icons)
        gridList_canvas.add_widget(mdbox_first_layout)
        ###### LIST THE CHARTS ADDED ON THE RIGHT SIDE ######



    def delete_chart(self,blank_instance,canvas_chart,mdbox_layout):
        # get the button layout
        gridList_canvas = self.root.ids.list_charts_added
        gridList_canvas.remove_widget(mdbox_layout)
        # remove the canvas chart
        canvas_chart.parent.remove_widget(canvas_chart)

    def modal_chart(self,blank_instance,canvas,delete_label,bar_type):
        # define and turns on the modal
        update_modal = self.root.ids.my_popup
        update_modal.opacity = 1
        update_modal.height = 200
        #update_modal.clear_widgets()
        # print the buttons according to the chart type
        update_up_box = self.root.ids.popup_content_up
        update_up_box.clear_widgets()
        # create the md grid and the buttons
        if bar_type == "bar":
            gridLayout_for_dropdown = MDGridLayout(cols=3,rows=1,spacing=5)
            self.dropdown_btn_update_xAxis_5 = MDFlatButton(id="dropdown_btn_update_xAxis_5",size_hint=(.2,1),text= 'Categ/Data')
            self.dropdown_btn_update_xAxis_5.bind(on_release=lambda instance: self.xAxis_option_1(5,instance))

            self.dropdown_btn_update_yAxis_5 = MDFlatButton(id="dropdown_btn_update_yAxis_5",size_hint=(.2,1),text= 'Opção 1')
            self.dropdown_btn_update_yAxis_5.bind(on_release=lambda instance: self.yAxis_option(5, instance))

            self.dropdown_btn_update_yAxis_5A = MDFlatButton(id="dropdown_btn_update_yAxis_5A",size_hint=(.2,1),text= 'Opção 2')
            self.dropdown_btn_update_yAxis_5A.bind(on_release=lambda instance: self.yAxis_option_2("5A", instance))

            gridLayout_for_dropdown.add_widget(self.dropdown_btn_update_xAxis_5)
            gridLayout_for_dropdown.add_widget(self.dropdown_btn_update_yAxis_5)
            gridLayout_for_dropdown.add_widget(self.dropdown_btn_update_yAxis_5A)
            update_up_box.add_widget(gridLayout_for_dropdown)
        elif bar_type == "line":
            gridLayout_for_dropdown = MDGridLayout(cols=3, rows=1, spacing=5)
            self.dropdown_btn_update_xAxis_5 = MDFlatButton(id="dropdown_btn_update_xAxis_5", size_hint=(.2, 1),text='Categ/Data')
            self.dropdown_btn_update_xAxis_5.bind(on_release=lambda instance: self.xAxis_option_1(5, instance))

            self.dropdown_btn_update_yAxis_5 = MDFlatButton(id="dropdown_btn_update_yAxis_5", size_hint=(.2, 1),text='Opção 1')
            self.dropdown_btn_update_yAxis_5.bind(on_release=lambda instance: self.yAxis_option(5, instance))

            self.dropdown_btn_update_yAxis_5A = MDFlatButton(id="dropdown_btn_update_yAxis_5A", size_hint=(.2, 1),text='Opção 2')
            self.dropdown_btn_update_yAxis_5A.bind(on_release=lambda instance: self.yAxis_option_2("5A", instance))
            gridLayout_for_dropdown.add_widget(self.dropdown_btn_update_xAxis_5)
            gridLayout_for_dropdown.add_widget(self.dropdown_btn_update_yAxis_5)
            gridLayout_for_dropdown.add_widget(self.dropdown_btn_update_yAxis_5A)
            update_up_box.add_widget(gridLayout_for_dropdown)
        elif bar_type == "pizza":
            gridLayout_for_dropdown = MDGridLayout(cols=2, rows=1, spacing=5)
            self.dropdown_btn_update_xAxis_5 = MDFlatButton(id="dropdown_btn_update_xAxis_5", size_hint=(.2, 1),text='Categ/Data')
            self.dropdown_btn_update_xAxis_5.bind(on_release=lambda instance: self.xAxis_option_1(5, instance))

            self.dropdown_btn_update_yAxis_5 = MDFlatButton(id="dropdown_btn_update_yAxis_5", size_hint=(.2, 1),text='Opção 1')
            self.dropdown_btn_update_yAxis_5.bind(on_release=lambda instance: self.yAxis_option(5, instance))

            gridLayout_for_dropdown.add_widget(self.dropdown_btn_update_xAxis_5)
            gridLayout_for_dropdown.add_widget(self.dropdown_btn_update_yAxis_5)
            update_up_box.add_widget(gridLayout_for_dropdown)
        elif bar_type == "table":
            pass

        # choose the data (for future apply)

        # define and add the button to the bottom of the modal
        update_bottom_box = self.root.ids.popupdown_content_mdgrid
        update_bottom_box.clear_widgets()
        update_button = MDFlatButton(text="Atualizar",size_hint=(None,None))
        close_button = MDFlatButton(text="Fechar",size_hint=(None,None))
        update_button.bind(on_release=lambda instance: self.update_chart(instance, canvas, blank_instance,bar_type))
        close_button.bind(on_release=self.close_modal)
        update_bottom_box.add_widget(update_button)
        update_bottom_box.add_widget(close_button)

    def close_modal(self,instance):
        # define and turns on the modal
        update_modal = self.root.ids.my_popup
        update_modal.opacity = 0
        update_modal.height = 0

    def update_chart(self,instance,canvas, blank_instance,bar_type):
        # define and turns on the modal
        update_modal = self.root.ids.my_popup
        update_modal.opacity = 0
        update_modal.height = 0
        # get the variables points
        x_label_head_1 = self.selected_x_col_1
        x_label_info_1 = self.column_data_x_1
        split_x_label = []
        y_label_head = self.selected_y_col
        y_label_info = self.column_data_y
        y_label_head_2 = self.selected_y_col_2
        y_label_info_2 = self.column_data_y_2

        axes = canvas.figure.get_axes()
        ax = axes[0]
        ax.clear()
        if bar_type == 'bar':
            if x_label_head_1 and y_label_head:
                if "DT" in x_label_head_1:  # separar por data
                    # Substituir os zeros por barras
                    x_label_info_1_formatted = [date[:2] + '/' + date[2:4] + '/' + date[4:] for date in x_label_info_1]
                    # Converter as datas
                    x_dates = pd.to_datetime(x_label_info_1_formatted, format='%d/%m/%Y', dayfirst=True)
                    if self.selected_y_col_2 is not None:  # duas informações de valores
                        pass
                    else: # uma informação de valor
                        ax.set_title("Novo Título")
                else: # separar por categoria
                    if self.selected_y_col_2 is not None: # duas informações de valores
                        pass
                    else: # uma informação de valor
                        pass
        elif bar_type == 'line':
            if x_label_head_1 and y_label_head:
                if "DT" in x_label_head_1:  # separar por data
                    # Substituir os zeros por barras
                    x_label_info_1_formatted = [date[:2] + '/' + date[2:4] + '/' + date[4:] for date in x_label_info_1]
                    # Converter as datas
                    x_dates = pd.to_datetime(x_label_info_1_formatted, format='%d/%m/%Y', dayfirst=True)
                    if self.selected_y_col_2 is not None:  # duas informações de valores
                        pass
                    else:  # uma informação de valor
                        pass
                else:  # separar por categoria
                    if self.selected_y_col_2 is not None:  # duas informações de valores
                        pass
                    else:  # uma informação de valor
                        pass
        elif bar_type == 'pizza':
            if x_label_head_1 and y_label_head:
                if "DT" in x_label_head_1:  # separar por data
                    # Substituir os zeros por barras
                    x_label_info_1_formatted = [date[:2] + '/' + date[2:4] + '/' + date[4:] for date in x_label_info_1]
                    # Converter as datas
                    x_dates = pd.to_datetime(x_label_info_1_formatted, format='%d/%m/%Y', dayfirst=True)
                    if self.selected_y_col_2 is not None:  # duas informações de valores
                        pass
                    else:  # uma informação de valor
                        pass
                else:  # separar por categoria
                    if self.selected_y_col_2 is not None:  # duas informações de valores
                        pass
                    else:  # uma informação de valor
                        pass
        elif bar_type == 'table':
            if x_label_head_1 and y_label_head:
                if "DT" in x_label_head_1:  # separar por data
                    # Substituir os zeros por barras
                    x_label_info_1_formatted = [date[:2] + '/' + date[2:4] + '/' + date[4:] for date in x_label_info_1]
                    # Converter as datas
                    x_dates = pd.to_datetime(x_label_info_1_formatted, format='%d/%m/%Y', dayfirst=True)
                    if self.selected_y_col_2 is not None:  # duas informações de valores
                        pass
                    else: # uma informação de valor
                        pass
                else: # separar por categoria
                    if self.selected_y_col_2 is not None: # duas informações de valores
                        pass
                    else: # uma informação de valor
                        pass
        canvas.draw()

    def get_date(self, date):
        pass
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.get_date)
        date_dialog.open()


if __name__ == '__main__':
    MyApp().run()