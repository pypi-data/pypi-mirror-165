MISSING_STRING = '__missing__'
AVAILABLE_LANGUAGES = ['en']

REPORT_TRANSLATIONS ={
    'Syncro performance report': {
        'en': 'Syncro performance report'
    },

    'Machine operation': {
        'en': 'Machine operation'
    },
    
    'ON Time': {
        'en': 'ON Time'
    },
    
    'vs {}h (prev week)': {
        'en': 'vs {}h (prev week)'
    },
    
    '{}% (prev week)': {
        'en': '{}% (prev week)'
    },

    'ON': {
        'en': 'ON'
    },
    
    'OFF': {
        'en': 'OFF'
    },
 
    'Working hours': {
        'en': 'Working hours'
    },
    
    'Working modes': {
        'en': 'Working modes'
    },

    'Phases': {
        'en': 'Phases'
    },
    
    'Time': {
        'en': 'Time'
    },
    
    'Trend (prev. week)': {
        'en': 'Trend (prev. week)'
    },
    
    'Standard': {
        'en': 'Standard'
    },
    
    'Production': {
        'en': 'Production'
    },
    
    'Maintenance': {
        'en': 'Maintenance'
    },
    
    'Phases hours': {
        'en': 'Phases hours'
    },
    'Performance Overiew':{
         'en': 'Performance Overiew'
    },
    'Mold':{
         'en': 'Mold'
    }, 
    'Time ON':{
         'en': 'Time ON'
    },
    'Std cycle time':{
         'en': 'Std cycle time'
    },
    'Sync cycle time':{
         'en': 'Sync cycle time'
    }, 
    'KPI sync':{
         'en': 'KPI sync'
    },
    'KPI std':{
         'en': 'KPI std'
    },
    'Recipes':{
         'en': 'Recipes'
    },
    'Recipe name':{
         'en': 'Recipe name'
    },
    'Machine SN:':{
         'en': 'Machine SN:'
    },
    'Custom name:':{
         'en': 'Custom name:'
    },
    'Model:':{
         'en': 'Model:'
    },
    'Reference period:':{
         'en': 'Reference period:'
    },
    'Cycle time':{
         'en': 'Cycle time'
    },

}



class Translations():
    
    def __init__(self, language):
        '''
        
        '''
        self.language = language
        
    def getTranslation(self, id) -> str:
        try:
            return REPORT_TRANSLATIONS[id][self.language]
        except:
             try:
                 return REPORT_TRANSLATIONS[id][self.language]
             except:
                 return MISSING_STRING