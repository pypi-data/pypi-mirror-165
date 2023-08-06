from xmlrpc.client import DateTime
from .frigel_report_creator import FrigelReportCreator
from .consts import *
from .translations import Translations
from .charts.charts import ChartPieWithLegend, ChartBar, PieChartWorkingModes, HBarChartValueAxisNegLabels

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Circle, Drawing, Polygon
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT


from typing import Union
from io import BytesIO
from datetime import datetime, timedelta
import numpy as np

class SyncroReportWeeklyCreator(FrigelReportCreator):
    '''
    Class for the creation of Syncro RS reports
    '''
    
    def __init__(self, operation_hours: list, operation_hours_prev: list, working_modes_hours: dict, working_modes_hours_prev: dict, info_machine: dict, molds_info: dict, start_date: datetime):
        '''
        input:
            operation_hours (list): list with the operation hours of the week,
            operation_hours_prev (list): list with the operation hours of the previous week,
            working_modes_hours (dict): {'standard': [10, 20,..], 'production': [10, 20,..], 'maintenance': [10, 20,..]},
            info_machine = {'sn': '234985', 'name': 'pippo', 'model': 'RSY', 'ref_period': '2022-08-10 - 2022-08-17'},
            molds_info (dict):  {'name_mold': {'recipes: {'name_recipe': 86.78106666666667,...}, 
                                                'original_cycle': '-', 'on': 111.0573682054, 'average_cycle': 236.0401693610941, 
                                                'energy_consumption_syncro': 0, 'material_produced_syncro': 0, 'energy_consumption_standard': 0, 
                                                'material_produced_standard': 0}, ...}, 
            start_date (datetime): starting day
        '''
        self.operation_hours = operation_hours
        self.total_operation_hours = np.sum([0 if x == None else x for x in self.operation_hours])
        self.operation_hours_prev = operation_hours_prev
        self.total_operation_hours_prev = None if all(x is None for x in self.operation_hours_prev) else np.sum([0 if x == None else x for x in self.operation_hours_prev])
        self.working_modes_hours = working_modes_hours
        self.working_modes_hours_prev = working_modes_hours_prev
        self.working_modes_trend = [np.sum([0 if x == None else x for x in self.working_modes_hours[mode]])/np.sum([0 if x == None else x for x in self.working_modes_hours_prev[mode]])-100 if np.sum(0 if x == None else x for x in self.working_modes_hours_prev[mode])>0 else None\
            for mode in WORKING_MODE_TYPES]
        self.molds_info = molds_info
        self.start_date = start_date
        self.info_machine = info_machine
        FrigelReportCreator.__init__(self)
        
           
    def generatePDF(self, dest_path=None, language: str='en') -> Union[BytesIO, str]:
        '''
        generate PDF file
        
        input:
            dest_path (str): save path, if None the PDF will be saved into a ByetsIO buffer
            
        output:
            dest_path if is not None, else the buffer containing the PDF
        '''
        if dest_path:
            pdf_file = dest_path
        else:
            pdf_file = BytesIO()
    
        self.canvas = canvas.Canvas(pdf_file , pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.width, self.height = A4
        self.organization = 'Frigel Firenze S.p.A.'
        self.logoPositionX = 5
        self.logoPositionY = 0
        self.horizontalMargin = 10
        self.lastPositionX = 0
        self.lastPositionY = DEFAULT_STARTING_POSITION
        
        self.translations = Translations(language)
        
        self.drawLogo()
        self.__add_title_report()
        self.drawMachine()
        self.__add_info_machine()
        
        self.addSpacing(DEFAULT_SPACING)
        self.__add_machine_operation_paragraph()
        self.__add_operation_hours_pie()
        #self.__add_working_hours_paragraph()
        #self.__add_working_hours_chart()

        self.newPage()
        
        #add check
        recipe = False
        # for key_mold in self.molds_info:
        #     if self.molds_info[key_mold]:
        #         for key in self.molds_info[key_mold]['recipes']:
        #             key_recipe.append(key)
        # print(key_recipe)
        if self.molds_info:
            self.__add_performance_overview_paragraph()
            self.__add_performance_overview_data()
            self.addSpacing(-35)

            self.__add_cycle_time_paragraph()
            self.__add_cycle_time_bar()
            
            list_key = self.molds_info.keys()
            for key in list_key:
                if self.molds_info[key]['recipes']:
                    recipe = True
            if recipe:
                self.addSpacing(-60)
                self.__add_recipe_for_mold_paragraph()
                self.__add_recipe_for_mold_data()
                
        
            self.newPage()
        
        self.__add_working_modes_paragraph()
        self.__add_working_modes_data()
        
        self.__add_modes_hours_paragraph()
        self.__add_modes_hours_chart()

        
        self.canvas.save()
        
        return pdf_file
    
    # helper functions to create syncro PDF report
    #----------------------------------------------------------------------
    def __add_title_report(self):
        text_machine = """<font size="28">
        {}
        </font>
        """.format(self.translations.getTranslation('Syncro performance report'))
        self.addSpacing(24)
        titleStyle = ParagraphStyle(text_machine,
                           fontName=DEFAULT_FONT_BOLD,
                           parent=self.styles["Heading1"],
                           alignment=TA_CENTER)

        p_machine = Paragraph(text_machine, titleStyle)
        self.drawOnCanvas(p_machine, -10, -5)

    def __add_machine_operation_paragraph(self):
        text_machine = """<font size="24">
        {}
        </font>
        """.format(self.translations.getTranslation('Machine operation'))
        self.addSpacing(50)
        p_machine = Paragraph(text_machine, self.styles["Heading1"])
        self.drawOnCanvas(p_machine, 10, 0)

    def __add_info_machine(self):
        table_data_machine = Table(data=[[self.translations.getTranslation('Machine SN:'), self.info_machine['sn']],
                                         [self.translations.getTranslation('Custom name:'), self.info_machine['name']],
                                         [self.translations.getTranslation('Model:'), self.info_machine['model']],
                                         [self.translations.getTranslation('Reference period:'), 'from {}'.format(self.info_machine['from'])],
                                         ['','to   {}'.format(self.info_machine['to'])]],  rowHeights=[None, None, 20, None, None])
        table_data_machine.setStyle([("FONTSIZE",  (0,0), (-1,-1), 16),
                                ("FONTNAME", (0,0), (-1,-1), DEFAULT_FONT_BOLD),
                                ("VALIGN", (0,0), (-1,-1), 'BOTTOM'),
                                ("ALIGN", (0,0), (-1,-1), "LEFT")])
        _, table_height = table_data_machine.wrap(0, 0)
        self.drawOnCanvas(table_data_machine, 90, table_height -20)
        
        
    def __add_operation_hours_pie(self):
        pie_table_width = self.width/2-self.horizontalMargin - 20
        drawing_circle = Drawing(CIRCLE_SIZE,CIRCLE_SIZE)
        drawing_circle.add(Circle(CIRCLE_SIZE,CIRCLE_SIZE,CIRCLE_SIZE, fillColor=DEFAULT_ON_COLOR, strokeColor=DEFAULT_STROKE_COLOR))
        
        table_on_time = Table(data=[[drawing_circle, self.translations.getTranslation('ON Time')]], colWidths=[CIRCLE_SIZE+8, None])
        table_on_time.setStyle([("FONTSIZE", (1,0), (1,0), 12),
                                ("FONTNAME", (1,0), (1,0), DEFAULT_FONT_BOLD),
                                ("VALIGN", (0,0), (-1,-1), 'BOTTOM')])
        table_on_hours = Table(data=[['{} h'.format(int(self.total_operation_hours))]])
        table_on_hours.setStyle([("FONTSIZE", (0,0), (0,0), 32),
                                 ("FONTSIZE", (1,0), (1,0), 12),
                                 ("FONTNAME", (0,0), (-1,-1), DEFAULT_FONT),
                                 ("VALIGN", (0,0), (-1,-1), 'BOTTOM')])

        percentage_hours = int(100-self.total_operation_hours_prev*100/self.total_operation_hours) if self.total_operation_hours_prev != None and self.total_operation_hours_prev > 0 else None
        drawing_triangle = Drawing(3,3) 
        if percentage_hours and percentage_hours > 0 :
            drawing_triangle.add(Polygon(
                    strokeColor = DEFAULT_ON_COLOR,
                    fillColor = DEFAULT_ON_COLOR,
                    points=[4, 6+(5/2), 4-(5/2), 6-(5/2), 4+(5/2), 6-(5/2), 4, 6+(5/2)] #Structure [(x1,y1),(x2,y2),...]
                ))
        elif percentage_hours:
            drawing_triangle.add(Polygon(
                    strokeColor = DEFAULT_NEGATIVE_COLOR,
                    fillColor = DEFAULT_NEGATIVE_COLOR,
                    points=[4, 6-(5/2), 4+(5/2), 6+(5/2), 4-(5/2), 6+(5/2), 4, 6-(5/2)] 
                ))
        data_table_right = [[table_on_time],
                            [table_on_hours],
                            [Table(data=[[drawing_triangle, self.translations.getTranslation('{}% (prev week)').format(abs(percentage_hours))]], colWidths=[10, 2])] if percentage_hours else []]
                            #[self.translations.getTranslation('vs {}h (prev week)').format(round(self.total_operation_hours_prev/60,2))] if self.total_operation_hours_prev != None else '']
        table_pie_right = Table(data_table_right, colWidths=pie_table_width, rowHeights=[None, None, 35])
        table_pie_right.setStyle([("ALIGN", (0,0), (-1,-1), "LEFT"),
                                  ("FONTSIZE", (0,0), (0,0), 12),
                                  ("FONTSIZE", (0,1), (0,1),  32),
                                  ("FONTNAME", (0,0), (-1,-1), DEFAULT_FONT),
                                  ("FONTSIZE", (0,2), (0,2), 10)])
        
        hours_on_percentage = round(self.total_operation_hours*100/(24*7), 1)
        pie_data = [hours_on_percentage, 100-hours_on_percentage]
        pie_chart_hours = ChartPieWithLegend(data=pie_data, seriesNames=[self.translations.getTranslation('ON'), self.translations.getTranslation('OFF')], _colors=[DEFAULT_ON_COLOR, DEFAULT_OFF_COLOR])
        
        data_pie_hours = [[pie_chart_hours, table_pie_right]]
        table_pie_hours = Table(data_pie_hours, colWidths=pie_table_width)
        table_pie_hours.setStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                            ("ALIGN", (1,0), (1,0), "CENTRE")])
        _, table_height = table_pie_hours.wrap(0, 0)
        self.addSpacing(DEFAULT_SPACING)
        self.drawOnCanvas(table_pie_hours, 10, table_height/3)
        #self.drawOnCanvas(table_pie_hours, 80, table_height/3 - 20 )
        
    # remove ----------------    
    def __add_working_hours_paragraph(self):
        text_machine = """<font size="24">
        {}
        </font>
        """.format(self.translations.getTranslation('Working hours'))
        self.addSpacing(-15)
        p_machine = Paragraph(text_machine, self.styles["Heading1"])
        self.drawOnCanvas(p_machine, 10 + TA_LEFT, 10)
        
        
    def __add_working_hours_chart(self):
        chart_data = [tuple(self.operation_hours), tuple(24-x if x != None else 0 for x in self.operation_hours)]
        chart_working_hours = ChartBar(data=chart_data,
                                       category_names=[(self.start_date+timedelta(days=x)).strftime("%d / %m") for x in range(7)],
                                       colors=[DEFAULT_ON_COLOR, DEFAULT_OFF_COLOR])
        self.addSpacing(DEFAULT_SPACING)
        self.drawOnCanvas(chart_working_hours, 10, chart_working_hours.height/3)
    #--------------------------  
        
    def __add_working_modes_paragraph(self):
        text_machine = """<font size="24">
        {}
        </font>
        """.format(self.translations.getTranslation('Working modes'))
        self.addSpacing(DEFAULT_SPACING)
        p_machine = Paragraph(text_machine, self.styles["Heading1"])
        self.drawOnCanvas(p_machine, 10 + TA_LEFT, 5)
        
        
    def __add_working_modes_data(self):
        data_pie = [np.sum(0 if x is None else x for x in self.working_modes_hours[mode]) for mode in WORKING_MODE_TYPES]
        working_total = sum(data_pie)
        percentage_working_mode = ['{} %'.format(round(value*100/working_total,1)) for value in data_pie] 
        pie_working_modes = PieChartWorkingModes(data=data_pie,
                                                 label_percentage = percentage_working_mode,
                                                 data_trend=self.working_modes_trend,
                                                 header_names=(self.translations.getTranslation('Phases'), 
                                                               self.translations.getTranslation('Time'),
                                                               self.translations.getTranslation('Trend (prev. week)'),),
                                                 series_names=[self.translations.getTranslation('Standard'),
                                                               self.translations.getTranslation('Production'),
                                                               self.translations.getTranslation('Maintenance')],)
        self.drawOnCanvas(pie_working_modes, 10, pie_working_modes.height/3)
        
    def __add_modes_hours_paragraph(self):
        text_machine = """<font size="24">
        {}
        </font>
        """.format(self.translations.getTranslation('Phases hours'))
        p_machine = Paragraph(text_machine, self.styles["Heading1"])
        self.addSpacing(-10)
        self.drawOnCanvas(p_machine, 10, 0)
        
    def __add_modes_hours_chart(self):
        chart_data = [self.working_modes_hours[mode] for mode in WORKING_MODE_TYPES]
        list_working_hours = [0,0,0,0,0,0,0]
        for mode in WORKING_MODE_TYPES:
            list_working_hours = np.add(list_working_hours,self.working_modes_hours[mode])
        list_off_hours = []
        for element in list_working_hours:
            list_off_hours.append(24-element)
        chart_data.append(list_off_hours)
        chart_working_hours = ChartBar(data=chart_data,
                                       category_names=[(self.start_date+timedelta(days=x)).strftime("%d / %m") for x in range(7)],
                                       colors=WORKING_MODES_COLORS,
                                       legend = True,
                                       series_names=[self.translations.getTranslation('Standard'),
                                                     self.translations.getTranslation('Production'),
                                                     self.translations.getTranslation('Maintenance'),
                                                     self.translations.getTranslation('OFF')],)
        
        self.addSpacing(DEFAULT_SPACING)
        self.drawOnCanvas(chart_working_hours, 10, chart_working_hours.height/3)

    def __add_performance_overview_paragraph(self):
        text_machine = """<font size="24">
        {}
        </font>
        """.format(self.translations.getTranslation('Performance Overiew'))
        self.addSpacing(DEFAULT_SPACING)
        p_machine = Paragraph(text_machine, self.styles["Heading1"])
        self.drawOnCanvas(p_machine, 10 + TA_LEFT, 5)

    def __add_performance_overview_data(self):
        table_width = self.width/6-self.horizontalMargin -10
        list_key = self.molds_info.keys()
        list_molds = [[self.translations.getTranslation('Mold'),self.translations.getTranslation('Time ON'),
                        self.translations.getTranslation('Std cycle time'),self.translations.getTranslation('Sync cycle time'), 
                        self.translations.getTranslation('KPI sync'),self.translations.getTranslation('KPI std')]]
        
        styleN = self.styles['Normal']
        styleN.wordWrap = 'CJK'
        styleN.fontName = DEFAULT_FONT_BOLD
        styleN.fontSize = 12
        table_style = [("ALIGN", (0,0), (0,-1), "LEFT"),
                        ("ALIGN", (2,0), (-1,-0), "CENTER"),
                        ("ALIGN", (1,0), (5,0), "RIGHT"),
                        ("ALIGN", (1,1), (5,-1), "RIGHT"),
                        ("FONTNAME", (0,0), (-1,-0), DEFAULT_FONT_BOLD),
                        ("FONTNAME", (0,0), (0,-1), DEFAULT_FONT_BOLD),
                        ("TEXTCOLOR", (0,1), (0,-1), '#000000'),
                        ("FONTSIZE", (0,0), (0,-1), 12),
                        ("FONTSIZE", (0,0), (-1,0), 12),
                        ]

        for key in list_key:
            mold_name = Paragraph(key, styleN)
            list_molds.append([mold_name, '{} h {} min'.format(int(self.molds_info[key]['on']/60) if type(self.molds_info[key]['on']) == float else self.molds_info[key]['on'], int(self.molds_info[key]['on']) - int(self.molds_info[key]['on']/60)*60 if type(self.molds_info[key]['on']) == float else self.molds_info[key]['on'] ), 
                            '{} {}'.format(round(self.molds_info[key]['original_cycle'],2) if type(self.molds_info[key]['original_cycle']) == float else '500' if self.molds_info[key]['original_cycle'] == '-' else self.molds_info[key]['original_cycle'], 'sec'),
                            '{} {}'.format(round(self.molds_info[key]['average_cycle'],2) if type(self.molds_info[key]['average_cycle'])== float else self.molds_info[key]['average_cycle'], 'sec'), 
                            '{} {}'.format(round(self.molds_info[key]['energy_consumption_syncro']/self.molds_info[key]['material_produced_syncro'],2) if self.molds_info[key]['material_produced_syncro']> 0 else 0, 'kWh/kg'),
                            '{} {}'.format(round(self.molds_info[key]['energy_consumption_standard']/self.molds_info[key]['material_produced_standard'],2) if self.molds_info[key]['material_produced_standard']> 0 else 0, 'kWh/kg')])
            
        data_performance_overview = list_molds
        table_performance_overview = Table(data_performance_overview, colWidths=table_width)
        for i, row in enumerate(data_performance_overview):
            standard_time =  row[2].split(' ')[0]
            syncro_time = row[3].split(' ')[0]
            table_style.append(('LINEABOVE',(0,1),(-1,-1),.5,colors.black)),
            if i>0 and float(syncro_time)<float(standard_time if standard_time != '-' else 500):
                table_style.append(('BACKGROUND',(3,i),(3,i), DEFAULT_ON_COLOR))
            elif i>0:
                table_style.append(('BACKGROUND',(2,i),(2,i), DEFAULT_NEGATIVE_COLOR ))

        table_performance_overview.setStyle(table_style)
        _, table_height = table_performance_overview.wrap(0, 0)
        self.addSpacing(4)
        self.drawOnCanvas(table_performance_overview, 10, table_height/3)

    def __add_recipe_for_mold_paragraph(self):
        text_machine = """<font size="24">
        {}
        </font>
        """.format(self.translations.getTranslation('Recipes'))
        self.addSpacing(DEFAULT_SPACING)
        p_machine = Paragraph(text_machine, self.styles["Heading1"])
        self.drawOnCanvas(p_machine, 10 + TA_LEFT, 5)
    
    def __add_recipe_for_mold_data(self):
        table_width = self.width/3.15-self.horizontalMargin -20
        list_key = self.molds_info.keys()
        list_recipes = [[self.translations.getTranslation('Mold'), self.translations.getTranslation('Recipe name'),self.translations.getTranslation('Time ON')]]
        

        table_style = [("ALIGN", (0,0), (0,-1), "LEFT"),
                        ("ALIGN", (2,0), (-1,-0), "CENTER"),
                        ("ALIGN", (1,0), (5,0), "RIGHT"),
                        ("ALIGN", (1,1), (5,-1), "RIGHT"),
                        ("FONTNAME", (0,0), (-1,-0), DEFAULT_FONT_BOLD),
                        ("FONTNAME", (0,0), (0,-1), DEFAULT_FONT_BOLD),
                        ("TEXTCOLOR", (0,1), (0,-1), '#000000'),
                        ("FONTSIZE", (0,0), (0,-1), 12),
                        ("FONTSIZE", (0,0), (-1,0), 12),
                        ]

        for key in list_key:
            for k,value in self.molds_info[key]['recipes'].items():
                list_recipes.append([key, k, '{} h {} min'.format(round(value) if type(value) == float else value, int((value - int(value))*60))])

            
        data_recipes = list_recipes
        table_recipes = Table(data_recipes, colWidths=table_width, rowHeights=18)
        name_mold = ''
        start_row = 0
        end_row = 0
        for i, row in enumerate(data_recipes):
            if row[0] != name_mold and i > 0: 
                table_style.append(('SPAN',(0,start_row),(0,end_row))),
                table_style.append(('LINEABOVE',(0,start_row if start_row!= 0 else start_row+1),(3, -1), .5, colors.black))
                name_mold = row[0]
                start_row = i
                end_row = i
            else:
                end_row = i         
            if i == len(data_recipes)-1 and row[0] == name_mold:
                end_row = i if i == len(data_recipes)-1 else end_row
                table_style.append(('SPAN',(0,start_row),(0,end_row))),
                table_style.append(('LINEABOVE',(0,start_row),(0,end_row), .5, colors.black))

        table_recipes.setStyle(table_style)
        _, table_height = table_recipes.wrap(0, 0)
        #self.addSpacing(DEFAULT_SPACING)
        self.drawOnCanvas(table_recipes, 10, table_height/4 + 10 )

    def __add_cycle_time_paragraph(self):
        text_machine = """<font size="24">
        {}
        </font>
        """.format(self.translations.getTranslation('Cycle time'))
        p_machine = Paragraph(text_machine, self.styles["Heading1"])
        self.drawOnCanvas(p_machine, 10 + TA_LEFT, 5)

    def __add_cycle_time_bar(self):
        list_key = self.molds_info.keys()
        list_molds = []
        chart_data = []
        for key in list_key:
            list_molds.append(key)
            diff_cycle_time = self.molds_info[key]['original_cycle'] - self.molds_info[key]['average_cycle']if type(self.molds_info[key]['original_cycle']) == float else 500 - self.molds_info[key]['average_cycle'] 
            chart_data.append(diff_cycle_time)

        chart_working_hours = HBarChartValueAxisNegLabels(data= [tuple(chart_data)], category_names=list_molds)
        self.drawOnCanvas(chart_working_hours, 0, chart_working_hours.height/3)
            
    
    #----------------------------------------------------------------------