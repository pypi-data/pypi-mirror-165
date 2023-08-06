from reportlab.lib.colors import HexColor
import pathlib
from os import path

# import font Calibri 
#---------------------------------------------
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

CALIBRI_FONT = path.join(pathlib.Path(__file__).parent.resolve(), 'assets', 'Calibri.ttf')
CALIBRI_BOLD_FONT = path.join(pathlib.Path(__file__).parent.resolve(), 'assets', 'Calibri-Bold.ttf')

pdfmetrics.registerFont(TTFont('Calibri', CALIBRI_FONT))
pdfmetrics.registerFont(TTFont('Calibri-Bold', CALIBRI_BOLD_FONT))
#---------------------------------------------

DEFAULT_SPACING = 8
DEFAULT_STARTING_POSITION = 24
CIRCLE_SIZE = 4

DEFAULT_FONT = 'Calibri' #'Helvetica'
DEFAULT_FONT_BOLD = 'Calibri-Bold' #'Helvetica-Bold'

DEFAULT_LOGO_PATH = path.join(pathlib.Path(__file__).parent.resolve(), 'assets', 'frigel_logo.png')
DEFAULT_MACHINE_PATH = path.join(pathlib.Path(__file__).parent.resolve(), 'assets', 'RSY_con_display.jpeg')

WORKING_MODE_TYPES = ['standard', 'production', 'maintenance']

DEFAULT_ON_COLOR = HexColor("#B9E0A1")
DEFAULT_OFF_COLOR = HexColor("#CECECE")
DEFAULT_NEGATIVE_COLOR = HexColor("#4E70AB")
DEFAULT_STROKE_COLOR = HexColor("#E9E9E9")
WORKING_MODES_COLORS = (HexColor("#6BCE70"), HexColor("#BEDAA4"), HexColor("#4E70AB"), HexColor("#CECECE"))