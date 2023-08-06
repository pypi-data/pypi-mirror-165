from django.template.loader import render_to_string
from pathlib import Path

import shutil
import os
import traceback

from .memory import dinamic

BASE_DIR = Path(__file__).resolve().parent

class Template:

    PYTHON_FILE = 'py'
    HTML_FILE = 'html'

    def __init__(self, app_name, model_name, template_name, ext='py', do_replace=False, 
                 final_template_name=None):
        self.app_name = app_name.strip() if app_name else app_name
        self.model_name = model_name.strip() if model_name else model_name
        self.template_name = template_name
        self.ext = ext
        self.current_path = os.path.abspath(os.getcwd())
        self.do_replace = do_replace
        self.final_template_name = final_template_name

    def create_dir(self, dirname, secondary='', third=''):
        try:
            path = os.path.join(self.current_path, dirname, secondary, third)
            if not os.path.isdir(path):
                os.mkdir(path)
        except:
            pass

    def render(self):
        """
        Renderiza el template dado en el archivo solicitado
        """
        try:
            template_file = '%s_template.html' % self.template_name
            destiny_name = self.final_template_name\
                if self.final_template_name else self.template_name

            if self.ext == self.PYTHON_FILE:
                self.create_dir(self.app_name)
                rendered = render_to_string(template_file, {'app_name': self.app_name, 
                                                            'model_name': self.model_name})
                to_path = os.path.join(self.current_path, self.app_name,
                    '%s.py' % ("__init__" if  destiny_name == 'init' else destiny_name))
                
                print('- Creando archivo Python:', destiny_name)
                
                with open(to_path, 'w') as f:
                    f.write(rendered)
            else:
                
                from_path = os.path.join(BASE_DIR, 'templates', template_file)
                if destiny_name in ['login','logout']:
                    self.create_dir(self.app_name, 'templates', 'account')
                    to_path = os.path.join(self.current_path, self.app_name, 'templates', 
                        'account', '%s.html' % destiny_name)
                elif destiny_name in ['list','form']:
                    self.create_dir(self.app_name, 'templates', self.app_name)
                    to_path = os.path.join(self.current_path, self.app_name, 'templates', 
                        self.app_name, '%s_%s.html' % (self.model_name, destiny_name))
                else:
                    self.create_dir(self.app_name, 'templates')
                    to_path = os.path.join(self.current_path, self.app_name, 'templates', 
                        '%s.html' % destiny_name)
                    
                print('- Creando archivo HTML:', destiny_name)
                
                shutil.copyfile(from_path, to_path)
                
                if self.do_replace:
                    self.replace_html_var(to_path)
        except Exception as e:
            print('Generation Error:',e)
            traceback.print_exc()
            
    def replace_html_var(self, final_path):
        dinamic.replace_html(final_path, '[ITEM]', self.model_name)

class Generator:

    def __init__(self, app_name, model_name=None):
        self.app_name = app_name
        self.model_name = model_name

class AppGenerator(Generator):

    def generate(self):
        Template(self.app_name, self.model_name, 'init').render()
        Template(self.app_name, self.model_name, 'apps').render()
        Template(self.app_name, self.model_name, 'admin').render()
        Template(self.app_name, self.model_name, 'models').render()
        Template(self.app_name, self.model_name, 'signals').render()
        Template(self.app_name, self.model_name, 'tests').render()
        Template(self.app_name, self.model_name, 'urls').render()
        Template(self.app_name, self.model_name, 'views').render()
        Template(self.app_name, self.model_name, 'forms').render()
        Template(self.app_name, self.model_name, 'locustfile').render()

class AppTemplatesGenerator(Generator):

    def generate(self):
        Template(self.app_name, None, 'base', 'html').render()
        Template(self.app_name, None, 'header', 'html').render()
        Template(self.app_name, None, 'footer', 'html').render()
        Template(self.app_name, None, 'login', 'html').render()
        Template(self.app_name, None, 'logout', 'html').render()
        Template(self.app_name, None, 'home', 'html').render() 
        Template(self.app_name, None, 'messages', 'html').render()
        
        if self.model_name:
            Template(self.app_name, self.model_name, 'list', 'html', do_replace=True).render()
            Template(self.app_name, self.model_name, 'form', 'html', do_replace=True).render()
            Template(self.app_name, self.model_name, 'menulist', 'html', 
                     do_replace=True, final_template_name='menu').render()
        else:
            Template(self.app_name, None, 'menu', 'html').render()    
            
class AppSettingsModifier:
    
    def get_settings_lines(self, app_name):
        return [
            "\n\nimport os\n",
            "INSTALLED_APPS.append('{}')\n".format(app_name),
            "TEMPLATES[0]['DIRS'].append(os.path.join(BASE_DIR, '{}', 'templates'))\n".format(app_name),
            "LOGIN_REDIRECT_URL = '/'"
        ]
    
    def get_urls_lines(self, app_name):
        return [
            "\n\nfrom django.urls import include\n",
            "urlpatterns.extend([\n",
            "    path('', include('{}.urls')),\n".format(app_name),
            "    path('accounts/', include('allauth.urls')),\n",
            "    path('dwll/', include('dwll.urls'))\n",
            "])"
        ]
    
    def modify(self, app_name_str):
        if not app_name_str:
            print('Imposible generar codigo en sus archivos sin el nombre de la aplicacion')
            return
        
        from django.conf import settings
        
        target_dir = settings.BASE_DIR
        app_name = app_name_str.strip().lower()
        proj_name = os.path.basename(target_dir)
        
        print('Actualizando archivo settings.py para el proyecto', proj_name)
        if os.path.exists(os.path.join(proj_name, 'settings.py')):
            settings_path = os.path.join(target_dir, proj_name, 'settings.py')
            with open(settings_path, 'a') as f:
                f.writelines(self.get_settings_lines(app_name))
        else:
            print('Archivo no existe en la ubicacion', os.path.join(proj_name, 'settings.py'))

        print('Actualizando archivo urls.py para el proyecto', proj_name)
        if os.path.exists(os.path.join(proj_name, 'urls.py')):
            urls_path = os.path.join(target_dir, proj_name, 'urls.py')
            with open(urls_path, 'a') as f:
                f.writelines(self.get_urls_lines(app_name))
        else:
            print('Archivo no existe en la ubicacion', os.path.join(proj_name, 'urls.py'))
        
        print('Todos sus archivos han sido generados y actualizados para el proyecto', proj_name)
        

def run_generator_engine(option, app_name, model_name):
    if option == 'app':
        if app_name:
            AppGenerator(app_name, model_name).generate()
            AppTemplatesGenerator(app_name, model_name).generate()

def update_settings_file(app_name=None):
    AppSettingsModifier().modify(app_name)
