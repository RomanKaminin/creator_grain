# -*- coding: utf-8 -*-
'''
Created on 03 мар. 2018 г.

@author: r.kaminin
'''
import os, sys
import argparse
import shutil
import xml.etree.ElementTree as ET
import re
from distutils.dir_util import copy_tree

VERSION = "1.0.1"
IMPORTS_FOR_NAVIGATOR = ['#coding: utf-8', 'import json', 'from common.api.datapanels.datapanel import TabOrder',
                         'from common.api.events.action import Action',
                         'from common.api.events.activities import DatapanelActivity',
                         'from common.api.navigator.node import NavigatorNode', '\n'
                         ]
GENERALAPP_PROPERTIES_FILENAME = 'generalapp.properties'
GRAIN_DIRS = ['cards', 'datapanels', 'filters', 'functions',
              'grids', 'selectors', 'toolbars', 'rests'
              ]

class Creator:
    '''
    It`s class for:
        1.Check configuration files from project
        2.Generates a typical structure of files and directories in the granule
        3.Create complete example for quick start of work
    '''
    def __init__(self, name):
        self.grain = name
        self.lines_for_sql =  ["create grain " + self.grain + " version '1.0';", '\n']
        self.lines_for_init = ['#coding: utf-8', 'from common.navigator import navigatorsParts',
                               "navigatorsParts['" + self.grain + "'] = " + self.grain + "Navigator", '\n']
    def createCatalog(self, all_settings):
        dir_module = os.getcwd()
        os.chdir('example')
        dir_module_example = os.getcwd()

        cat_xml = os.path.abspath('catalina.xml')
        exam_xml = os.path.abspath('grainsSettings.xml')
        gen_prop = os.path.abspath(GENERALAPP_PROPERTIES_FILENAME)
        app_prop = os.path.abspath('app.properties')
        exam_card = os.path.abspath('exampleCard.xml')
        login_page = os.path.abspath('login.jsp')
        logo_file = os.path.abspath('logokurs.png')

        os.chdir('example')
        dir_example_grain = os.getcwd()
        os.chdir(dir_module_example)
        dir_upper = dir_module.replace(dir_module.split('\\').pop(), '')
        os.chdir(dir_upper[0:-16])
        dir_project = os.getcwd()
        name_current_dir = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
        result_message = False

        #In project
        self.change_grains_settings(dir_project, exam_xml)
        if bool(all_settings) and name_current_dir == self.grain:
            self.create_catalina_file(cat_xml, dir_project)
            self.create_login_page_file(login_page, dir_project)
            self.change_genproperties(dir_project, gen_prop)
            result_message = True
        if bool(all_settings) and name_current_dir != self.grain and self.grain != 'example':
            print u"""If you want create project with all settings you must rename project directory to '%s' 
                 """ % (self.grain)

        #In granule
        os.chdir('default')
        dir_def = os.getcwd()
        if bool(result_message):
            self.create_logo_file(dir_def, logo_file)
            self.change_appproperties(app_prop, dir_def)
        os.chdir('xforms')
        dir_def_xforms = os.getcwd()
        os.chdir(dir_def)
        os.chdir('score')
        dir_score = os.getcwd()

        #check granule folder in score
        if self.grain in os.listdir(dir_score):
            view = u'second_way'
            return Creator.response_term(self, view)
        if self.grain == u'example':
            if name_current_dir == u'example':
                os.makedirs(self.grain)
                os.chdir(self.grain)
                copy_tree(dir_example_grain, os.getcwd())
                shutil.copy(exam_card, dir_def_xforms)
                view = u'first_way'
                return Creator.response_term(self, view)
            else:
                print u"""
                If you want to see in browser the working example, you must rename main project catalog to 'example' 
                 """
            return
        self.create_dirs_tree_in_score()
        view = u'first_way'
        if bool(result_message):
            return Creator.response_term(self, view)
        else:
            print u"Grain %s, is created!"%(self.grain)

    def create_dirs_tree_in_score(self):
        '''
        1.Create granule directory in score
        2.Create typical structure of files and directories in the granule
        3.Writes some imports in files
        '''
        os.makedirs(self.grain)
        os.chdir(self.grain)
        dir_grain = os.getcwd()
        for dir in GRAIN_DIRS:
            dir_name = dir[:-1]
            files_deeply = ['__init__.py', self.grain + dir_name.title() + '.py']
            files_higher = ['__init__.py', '_' + self.grain + '.sql', 'navigator.py']
            try:
                os.makedirs(dir)
            except:
                print u"Can`t make dir is, %s" % (dir)
            os.chdir(dir)
            for file in files_deeply:
                open(file, 'w')
            os.chdir(dir_grain)

            # check imports in init,navigatot files
            for f in files_higher:
                if f == '__init__.py':
                    lines = self.lines_for_init
                elif f == 'navigator.py':
                    lines = IMPORTS_FOR_NAVIGATOR
                elif f == "_" + self.grain + ".sql":
                    lines = self.lines_for_sql
                else:
                    raise Exception('!!!!!')
                empty_file = open(f, "w")
                for line in lines:
                    empty_file.write(line + "\n")
                empty_file.close()

    def create_logo_file(self, dir_def, logo_file):
        '''
       1.Check logo file in dir login_content
       '''
        os.chdir('resources')
        os.chdir('login_content')
        dir_content = os.getcwd()
        if 'logokurs.png' not in os.listdir(dir_content):
            shutil.copy(logo_file, dir_content)
        os.chdir(dir_def)

    def create_catalina_file(self, cat_xml, dir_project):
        '''
        1.Check present file for_catalina.xml in dir project
        2.Remove old file
        3.Create new file with setting for start project
        '''
        try:
            os.remove('for_catalina.xml')
        except Exception:
            pass
            #print u"With delete file 'for_catalina.xml' has problem"
        way_to_project = dir_project.replace("\\", '\\\\')
        way_to_project = way_to_project.replace(way_to_project[0], way_to_project[0].lower())
        if 'for_catalina.xml' not in os.listdir(dir_project):
            shutil.copy(cat_xml, dir_project)
            os.rename('catalina.xml', 'for_catalina.xml')
        root = ET.parse('for_catalina.xml')
        param_tag = root.find('Parameter')
        param_tag.set('value', way_to_project)
        root.write('for_catalina.xml', encoding=None, xml_declaration=True)

    def create_login_page_file(self, login_page, dir_project):
        '''
       1.Check present file login.jsp in dir project
       2.Create new file from module
       '''
        if 'login.jsp' not in os.listdir(dir_project):
            shutil.copy(login_page, dir_project)


    def change_grains_settings(self, dir_project, exam_xml):
        '''
        1.Check the setting name new grain in grainsSettings.xml
        2.If not pesent then add name
        '''
        if 'grainsSettings.xml' not in os.listdir(dir_project):
            shutil.copy(exam_xml, dir_project)
        if 'grainsSettings.xml' in os.listdir(dir_project):
            root = ET.parse('grainsSettings.xml')
            names_exists_grains = []
            for item in root.findall('.//userdata'):
                for subelem in item:
                    title = subelem.text
                    names_exists_grains.append(title)
                if self.grain not in names_exists_grains:
                    new_tag = ET.SubElement(root.find('.//userdata'), 'group')
                    new_tag.text = self.grain
                    new_tag.tail = "\n                "
                else:
                    print u"""Grain %s, already added in grainsSettings.xml""" % (self.grain)
            root.write('grainsSettings.xml', encoding='utf-8', xml_declaration=True)

    def change_appproperties(self, app_prop, dir_def):
        '''
        1.Change settings, name title in file app.properties
        '''
        if "app.properties" in os.listdir(dir_def):
            os.remove('app.properties')
            shutil.copy(app_prop, os.getcwd())
            new_properties = open("new.properties", 'w')
            with open('app.properties', 'r') as old_properties:
                for string in old_properties.readlines():
                    if re.match(r"(^index.title)", string):
                        string = string.replace(string, 'index.title = ' + self.grain + '\n')
                    new_properties.write(string)
            new_properties.close()
            os.remove('app.properties')
            os.rename('new.properties', 'app.properties')

    def change_genproperties(self, dir_project, gen_prop):
        '''
        1.Create file if not present file generalapp.properties in dir project
        2.Change settings, name title page, name for bd connection in file generalapp.properties
        '''
        if GENERALAPP_PROPERTIES_FILENAME not in os.listdir(dir_project):
            shutil.copy(gen_prop, dir_project)
        if GENERALAPP_PROPERTIES_FILENAME in os.listdir(dir_project):
            new_properties = open("new.properties", 'w')
            with open(GENERALAPP_PROPERTIES_FILENAME, 'r') as old_properties:
                for string in old_properties.readlines():
                    if re.match(r"(^login.title)", string):
                        string = string.replace(string, 'login.title=' + self.grain + '\n')
                    if re.match(r"(^rdbms.connection.url)", string):
                        string = string.replace(string,
                                                'rdbms.connection.url=jdbc:postgresql://localhost:5432/' + self.grain + '\n')
                    new_properties.write(string)
            new_properties.close()
            os.remove(GENERALAPP_PROPERTIES_FILENAME)
            os.rename('new.properties', GENERALAPP_PROPERTIES_FILENAME)

    def response_term(self, view):
        if view == u'first_way':
            print u"""
            Grain %s, is created!
        1) Copy file '.war' from last release and paste to 'Tomcat 8.5\webapps' with name '%s'
        2) Copy catalog 'mellophone' from last release and paste to 'Tomcat 8.5\webapps' with name mellophone
        3) Copy file 'for_catalina.xml' from project catalog, to 'Tomcat 8.5\conf\Catalina\localhost' with name %s.xml
        4) Create database in localhost PostgresSQL with name '%s' 
        After star Tomcat server your can open http://localhost:8080/%s/ in browser
        """ %(self.grain, self.grain, self.grain, self.grain, self.grain)
        elif view == u'second_way':
            print u"""Grain %s, already exist!""" %(self.grain)


def createParser ():
    text_for_description = u'''
    This program automates the next stages of the project development:
    ---------------------------------------------------------------------------
    -Creation of a typical structure of files and directories in the granule 'default';
    ---------------------------------------------------------------------------
    -Making settings in the file 'generalapp.properties', and in the absence of a file in the root of the project, generates it;
    ---------------------------------------------------------------------------
    -Making settings in the file 'grainsSettings.xml' and in the absence of a file in the project root it generates it;
    ---------------------------------------------------------------------------
    -Making settings in the file 'app.properties' in the granule 'default';
    ---------------------------------------------------------------------------
    -Creating the file 'for_catalina.xml' in the root of the project with the correct settings, in the future, to move it to the 'Tomcat 8.5 \ conf \ Catalina \ localhost' directory with the project name;
    ---------------------------------------------------------------------------
    -Creating an example of a finished project with all the settings provided that the project name is 'example';
    ---------------------------------------------------------------------------
    '''
    parser = argparse.ArgumentParser(
        prog='creator_grain',
        description= text_for_description,
        epilog='''(c) Kaminin Roman 2018. Python developer of the company OOO "CURS IT".'''
    )

    parser.add_argument('-n', '--name',
                        default='test',
                        help='Create directory in score with entered name.Create inside standart directorys,files. Change grainsSettings.xml',
                        metavar = ''
                        )
    parser.add_argument('-p', '--project',
                        help='Create for_catalina.xml. Change generalapp.properties, grainsSettings.xml. Create directory in score with entered name.Create inside standart directorys,files.',
                        metavar = ''
                        )
    parser.add_argument('-v', '--version',
                        action='version',
                        help = 'Print number version',
                        version='%(prog)s {}'.format(VERSION))

    return parser



if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.project:
        Creator(namespace.project).createCatalog(all_settings=True)
    elif namespace.name:
        Creator(namespace.name).createCatalog(all_settings=False)
