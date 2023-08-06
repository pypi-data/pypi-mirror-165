#!/usr/bin/env python3
# Author  : Huseyin Gomleksizoglu
# Date    : "26-May-2022"
# Version : quip.py: 20220526
#
# 1.0.0     Huseyin G.    Jun/2/2022    Icon feature added, build option added
#
# Copyright (c) Stonebranch Inc, 2019.  All rights reserved.


import argparse
import os, sys
import yaml
import shutil
import subprocess
import json
import uuid
import re
import logging
from distutils.dir_util import copy_tree
from getpass import getpass
import requests
from shutil import make_archive, unpack_archive, move
import tempfile
from datetime import datetime
import quip.field_builder as fb
from argparse import RawTextHelpFormatter
from colorama import Fore, Style, init

version = "1.4.2"
UPDATE_ACTION = ["update", "u", "up"]
FIELD_ACTION = ["fields", "f", "fi"]
ICON_ACTION = ["icon", "resize-icon", "ri", "resize"]
DELETE_ACTION = ["delete", "d", "del"]
CLONE_ACTION = ["clone", "c", "cl", "copy"]
BOOTSTRAP_ACTION = ["bootstrap", "bs", "boot", "bst", "baseline"]
DOWNLOAD_ACTION = ["download", "pull"]
UPLOAD_ACTION = ["upload", "push"]
BUILD_ACTION = ["build", "b", "dist", "zip"]
init()

def cprint(text, color, end='\n'):
    if len(str(text).strip()) == 0: return
    fore = getattr(Fore, color.upper())
    print('{0}{1}{2}'.format(fore, text, Style.RESET_ALL), end=end)

def color(text, color, style='Normal'):
    fore = getattr(Fore, color.upper())
    style = getattr(Style, style.upper())
    return '{0}{1}{2}{3}'.format(fore, style, text, Style.RESET_ALL)

class Quip:
    def __init__(self, log_level=logging.INFO) -> None:
        cprint(f"======= QUIP (v.{version}) =======", color="cyan")
        logging.basicConfig(level=log_level)
        self.in_project_folder = False
        self.args = self.parse_arguments()
        if self.args.debug:
            logging.getLogger().setLevel(logging.DEBUG)
        self.set_global_configs(self.args.name, self.args.config)

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Wrapper for UIP command.', formatter_class=RawTextHelpFormatter)
        subparsers = parser.add_subparsers(dest='action')
        parser.add_argument('--config', '-c', default=None,
                             help='path of the global config. Default is ~/.uip_config.yml')
        parser.add_argument('--debug', '-v', action='store_true',
                            help='show debug logs')

        parser_new = subparsers.add_parser('new', help='Creates new integration')
        parser_new.add_argument('name', help='name of the project')
        parser_new.add_argument('--template', '-t', action='store_true',
                             help='create template instead of extension')

        parser_update = subparsers.add_parser('update', aliases=UPDATE_ACTION[1:], help='Updates existing integration')
        parser_update.add_argument('name', nargs="?", help='name of the project')
        parser_update.add_argument('--uuid', '-u', action='store_true',
                             help='Update UUID of the template')
        parser_update.add_argument('--new-uuid', '-n', action='store_true',
                             help='Update only new_uuid with a valid UUID in the template')
        parser_update.add_argument('--template', '-t', action='store_true',
                             help='create template instead of extension')
        
        parser_fields = subparsers.add_parser('fields', aliases=FIELD_ACTION[1:], help='Updates or dumps template.json fields.')
        parser_fields.add_argument('name', nargs="?", help='name of the project')
        parser_fields.add_argument('--update', '-u', action='store_true',
                             help='Update fields from fields.yml')
        parser_fields.add_argument('--dump', '-d', action='store_true',
                             help='dump fields to fields.yml')
        parser_fields.add_argument('--code', action='store_true',
                            help='Give some code samples')

        parser_delete = subparsers.add_parser('delete', aliases=DELETE_ACTION[1:], help='Deletes the integration folder')
        parser_delete.add_argument('name', help='name of the project')

        parser_clone = subparsers.add_parser('clone', aliases=CLONE_ACTION[1:], help='Clones existing integration with a new name')
        parser_clone.add_argument('name', help='name of the project')
        parser_clone.add_argument('source', help='source project path')
        parser_clone.add_argument('--template', '-t', action='store_true',
                             help='create template instead of extension')

        parser_bootstrap = subparsers.add_parser('bootstrap', aliases=BOOTSTRAP_ACTION[1:], help='Bootstrap new integration from baseline project')
        parser_bootstrap.add_argument('name', nargs="?", help='name of the project')
        parser_bootstrap.add_argument('--template', '-t', action='store_true',
                             help='create template instead of extension')

        parser_upload = subparsers.add_parser('upload', aliases=UPLOAD_ACTION[1:], help='Uploads the template to Universal Controller. (Template Only)')
        parser_upload.add_argument('name', nargs="?", help='name of the project')
        parser_upload.add_argument('--template', '-t', action='store_true',
                             help='create template instead of extension')

        parser_download = subparsers.add_parser('download', aliases=DOWNLOAD_ACTION[1:], help='Download the template from Universal Controller. (Template Only)')
        parser_download.add_argument('name', nargs="?", help='name of the project')
        parser_download.add_argument('--template', '-t', action='store_true',
                             help='create template instead of extension')

        parser_build = subparsers.add_parser('build', aliases=BUILD_ACTION[1:], help='Builds a zip file to import to Universal Controller. (Template Only)')
        parser_build.add_argument('name', nargs="?", help='name of the project')
        parser_build.add_argument('--template', '-t', action='store_true',
                             help='create template instead of extension')

        parser_icon = subparsers.add_parser('icon', aliases=ICON_ACTION[1:], help='Resize the images to 48x48 in src/templates/')
        parser_icon.add_argument('name', nargs="?", help='name of the project')
        parser_icon.add_argument('--generate', '-g', action='store_true',
                             help='generate new icon')

        parser_icon = subparsers.add_parser('config', help='show the configuration')

        args = parser.parse_args()
        print(args)

        if args.action is None:
            parser.print_help()
            sys.exit(0)
        
        if args.action in ["config"]:
            # give a fake name because name is mandatory
            args.name = ""

        if args.name is None:
            current_folder = os.getcwd()
            template_path = os.path.join(current_folder, "src", "templates", "template.json")
            if os.path.exists(template_path):
                _json = self.read_template_json(template_path=template_path)
                args.name = _json["name"]
                self.in_project_folder = True
            else:
                logging.error("You are not in a project folder. Please specify the project name.")
        return args
    
    def main(self):
        action = self.args.action
        if action == "new":
            if self.args.template:
                logging.info("creating new template")
                self.new_template()
            else:
                self.new_project()
                self.dump_fields(write=True)
            self.create_icon_safe()
        elif action in ICON_ACTION:
            if self.args.generate:
                self.create_icon()
            else:
                self.update_icon()
        elif action in FIELD_ACTION:
            if self.args.update:
                self.update_fields(self.args.code)
            elif self.args.dump:
                self.dump_fields(write=True)
        elif action in UPDATE_ACTION:
            self.update_project(self.args.uuid, self.args.new_uuid)
        elif action in DELETE_ACTION:
            self.delete_project()
        elif action in CLONE_ACTION:
            self.clone_project(self.args.source)
            self.dump_fields(write=True)
        elif action in BOOTSTRAP_ACTION:
            if self.args.template:
                self.bootstrap_template()
            else:
                self.bootstrap_project()
            self.dump_fields(write=True)
            self.create_icon_safe()
        elif action in UPLOAD_ACTION:
            if not self.args.template:
                logging.error("This action only possible with --template option. For extensions use 'uip push' command.")
                sys.exit(1)
            self.upload_template()
        elif action in DOWNLOAD_ACTION:
            if not self.args.template:
                logging.error("This action only possible with --template option. For extensions use 'uip pull' command.")
                sys.exit(1)

            if os.path.exists(self.project_name) or self.in_project_folder:
                self.download_template()
            else:
                self.bootstrap_template(ask_for_upload=False)
                self.download_template()
            self.dump_fields(write=True)
        elif action == "build":
            if not self.args.template:
                logging.error("This action only possible with --template option. For extensions use 'uip build' command.")
                sys.exit(1)
            self.build_zip(self.project_name)
        elif action == "config":
            if not self.uip_global_config.get("new", False):
                QuipGlobalConfig().check_config(self.uip_global_config)
            sys.exit(0)

    def set_global_configs(self, project_name, config_path=None):
        if config_path is not None:
            logging.info(f"Using config from file : {config_path}")
        self.uip_global_config = QuipGlobalConfig(config_file=config_path).conf
        logging.debug(self.uip_global_config)

        self._global_conf_defaults = self.uip_global_config.get("defaults", {})
        self._global_conf_extension = self.uip_global_config.get("extension.yml", {})
        self._global_conf_uip = self.uip_global_config.get("uip.yml", {})
        self.default_template = self._global_conf_defaults.get("template", "ue-task")
        self.project_name = self.format_ext_name(project_name)
        self.template_name = self.titleize(project_name)
        logging.debug(f"Project Name: {self.project_name}")
        logging.debug(f"Template Name: {self.template_name}")

    def new_template(self):
        logging.info(f"creating new template {self.template_name}")
        if os.path.exists(self.project_name):
            logging.error("Folder already exists")
            sys.exit(1)

        os.makedirs(self.project_name)
        os.makedirs(self.join_path("src"))
        os.makedirs(self.join_path("src", "templates"))

    def new_project(self):
        logging.info(f"creating new extension {self.template_name}")
        if os.path.exists(self.project_name):
            print("ERROR: Folder already exists")
            sys.exit(1)
        
        os.makedirs(self.project_name)
        self.uip_init(self.project_name, self.default_template)
        self.update_extension_yaml(self.project_name)
        self.update_uip_config(self.project_name)
        self.update_template_json(self.project_name)

    def update_project(self, update_uuid=False, update_new_uuid=False):
        logging.info(f"Updating extension {self.template_name}")
        if not self.args.template:
            self.update_extension_yaml(self.project_name)
            self.update_uip_config(self.project_name)
        self.update_template_json(self.project_name, update_uuid, update_new_uuid)

    def update_icon(self):
        from PIL import Image
        import PIL

        logging.info(f"Updating icon for {self.template_name}")
        template_path = self.join_path("src", "templates")
        converted = []
        for path in os.scandir(template_path):
            logging.debug(f"Scanning file : {path}")
            if path.is_file():
                if path.name in ["template_icon.png"]:
                    continue
                if path.name.lower().endswith("48x48.png"):
                    continue
                filename = self.join_path("src", "templates", path.name)
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    logging.debug(f"Image file : {filename}")
                    output_file = os.path.splitext(filename)[0] + "_48x48.png"
                    converted.append(output_file)
                    logging.debug(f"Output Image file : {output_file}")
                    with Image.open(filename) as im:
                        im_resized = im.resize((48, 48), resample=PIL.Image.LANCZOS)
                        im_resized.save(output_file, "PNG")
        if len(converted) == 1:
            logging.info(f"Updating icon file {converted[0]} => template_icon.png")
            shutil.copy2(converted[0], os.path.join(template_path, "template_icon.png"))
        elif len(converted) == 0:
            logging.info(f"Nothing to convert. Put an image file under templates folder and make sure the file name is not 'template_icon.png'")

    def create_icon_safe(self, message=None):
        try:
            self.create_icon(message=message)
        except Exception as ex:
            logging.error(f"WARNING: Couldn't create a new ICON")
            logging.error(f"Error: {ex}")
            return

    def create_icon(self, message=None):
        try:
            from PIL import Image, ImageDraw, ImageFont
        except Exception as ex:
            logging.error(f"WARNING: PIL module is missing. Install it using 'pip install Pillow'")
            logging.error(f"WARNING: Couldn't create a new ICON")
            return

        logging.info(f"Creating a new icon based on the name of the template/extension.")

        width = 48
        height = 48
        if message is None:
            message = self.get_icon_message(self.template_name)
        logging.info(f"Text in the ICON will be '{message}'")
        font_size = 38
        correction_x = 3
        correction_y = -5
        if len(message) == 1:
            font_size = 38
            correction_x = 3
            correction_y = -7
        elif len(message) == 2:
            font_size = 24
            correction_x = 3
            correction_y = -5
        elif len(message) == 3:
            font_size = 18
            correction_x = 3
            correction_y = -5
        
        font_name = self._global_conf_defaults.get("icon_font", "cour.ttf")
        font = ImageFont.truetype(font_name, size=font_size)
        img = Image.new('RGBA', (width, height), (255, 0, 0, 0))
        imgDraw = ImageDraw.Draw(img)

        textWidth = font.getbbox(message)[2]
        textHeight = font.getbbox(message)[3]
        xText = (width - textWidth + correction_x) / 2
        yText = (height - textHeight + correction_y) / 2

        imgDraw.ellipse((4, 4, 44, 44), outline=(50, 110, 230), fill=(50, 110, 230))
        imgDraw.text((xText, yText), message, font=font, fill='white', stroke_width=1)

        template_path = self.join_path("src", "templates")
        img.save(os.path.join(template_path, "template_icon.png"))
    
    def get_icon_message(self, message):
        result = []
        message = message.replace("-", " ")
        message = message.replace("  ", " ").upper()
        words = message.split(" ")
        if len(words[-1]) < 4:
            return words[-1]
        else:
            for word in words:
                result.append(word[0])
        
        if len("".join(result)) < 3:
            match = re.search("(\d+)$", words[-1])
            if match is not None:
                result.append(match.group(0))

        return "".join(result)[:3]

    def delete_project(self):
        logging.info(f"Deleting extension {self.template_name}")
        if not os.path.exists(self.project_name):
            logging.error("Folder doesn't exist")
            sys.exit(1)

        shutil.rmtree(self.project_name)

    def clone_project(self, from_project_path, all_files=False, exclude_list=None):
        if not os.path.exists(from_project_path):
            logging.error(f"From path does NOT exists. {from_project_path}")
            sys.exit(1)
        
        from_project_src_path = os.path.join(from_project_path, "src")
        if not os.path.exists(from_project_src_path):
            logging.error("From path is not a extension path")
            sys.exit(1)

        if os.path.exists(self.project_name):
            logging.error("Folder already exists")
            sys.exit(1)
        
        os.makedirs(self.project_name)
        if not self.args.template:
            self.uip_init(self.project_name, self.default_template)

        if not all_files:
            files = copy_tree(from_project_src_path, self.join_path("src"))
        else:
            source_files = os.listdir(from_project_path)
            if exclude_list is not None:
                logging.info(f"Ignoring following items: {exclude_list}")
                source_files = list(set(source_files) - set(exclude_list))
            for source_file in sorted(source_files):
                source_file_path = os.path.join(from_project_path, source_file)
                if os.path.isdir(source_file_path):
                    files = copy_tree(source_file_path, self.join_path(source_file))
                    for f in files:
                        logging.info(f"Copying file {f}")
                else:
                    shutil.copy2(source_file_path, self.join_path(source_file))
                    logging.info(f"Copying file {source_file}")
        
        self.update_project(update_uuid=True, update_new_uuid=True)

    def bootstrap_project(self):
        # get bootstrap source
        from_project_path = self._global_conf_defaults.get("bootstrap", {}).get("source", None)
        if from_project_path is None:
            logging.error("Bootstrap source not found. Please check the config file.")
            sys.exit(2)
        
        exclude_list = self._global_conf_defaults.get("bootstrap", {}).get("exclude", None)
        
        self.clone_project(from_project_path, all_files=True, exclude_list=exclude_list)

    def bootstrap_template(self, ask_for_upload=True):
        # get bootstrap source
        from_project_path = self._global_conf_defaults.get("bootstrap", {}).get("template_source", None)
        if from_project_path is None:
            logging.error("Bootstrap template source not found. Please check the config file.")
            sys.exit(2)
        
        exclude_list = self._global_conf_defaults.get("bootstrap", {}).get("template-exclude", None)
        
        self.clone_project(from_project_path, all_files=True, exclude_list=exclude_list)
        if ask_for_upload:
            answer = self.yes_or_no("Do you want to push the template to controller? ", default=True)
            if answer == True:
                self.upload_template()

    def upload_template(self):
        zip_file_path = self.build_zip(self.project_name)

        uac_user = self._global_conf_uip.get("userid", "ops.admin")
        # uac_pass = input(f"Enter password for {uac_user}: ")
        uac_pass = getpass(prompt=f"Enter password for {uac_user}: ")
        if len(uac_pass) == 0:
            logging.debug("Using password from config")
            uac_pass = self._global_conf_defaults.get("uac_password")
            logging.debug(f"Password is {uac_pass}")

        uac_url = self._global_conf_uip.get("url", "http://localhost:8080/uc")
        template_url = uac_url + "/resources/universaltemplate/importtemplate"
        logging.info(f"Uploading to controller ({uac_url})")
        with open(zip_file_path, "rb") as zipfile:
            zipfile_data = zipfile.read()
        result = requests.post(template_url, data=zipfile_data, auth=(uac_user, uac_pass), verify=False)
        if result.ok:
            logging.info(f"Template {self.template_name} pushed to {uac_url}")
        else:
            logging.error(f"Error while pushing {self.template_name} to {uac_url}")
            logging.error(f"Error detail: {result.text}")
            sys.exit(3)

    def upload_template_json(self):
        uac_user = self._global_conf_uip.get("userid", "ops.admin")
        uac_url = self._global_conf_uip.get("url", "http://localhost:8080/uc")
        template_url = uac_url + "/resources/universaltemplate"
        logging.info(f"Uploading to controller ({uac_url})")
        uac_pass = input(f"Enter password for {uac_user}: ")
        if len(uac_pass) == 0:
            logging.debug("Using password from config")
            uac_pass = self._global_conf_defaults.get("uac_password")
            logging.debug(f"Password is {uac_pass}")
        payload = self.merge_template_scripts(self.project_name)
        logging.debug(f"Payload = {self.format_json(payload)}")
        
        answer = self.yes_or_no("Are you updating existing template? ", default=True)
        if answer == True:
            logging.info("Updating existing template")
            result = requests.put(template_url, json=payload, auth=(uac_user, uac_pass), verify=False)
        else:
            logging.info("Creating new template")
            result = requests.post(template_url, json=payload, auth=(uac_user, uac_pass), verify=False)
        
        if result.ok:
            logging.info(f"Template {self.template_name} pushed to {uac_url}")
        else:
            logging.error(f"Error while pushing {self.template_name} to {uac_url}")
            logging.error(f"Error detail: {result.text}")
            sys.exit(3)
        
        logging.info("Uploading icon")
        template_icon_url = uac_url + "/resources/universaltemplate/seticon?templatename=" + self.template_name
        # application/octet-stream, image/png
        headers = {"content-type": "image/png", "Accept": "plain/text"}
        with open(self.join_path("src", "templates", "template_icon.png"), "rb") as icon:
            icon_data = icon.read()
        icon_result = requests.post(template_icon_url, data=icon_data, auth=(uac_user, uac_pass), verify=False)
        
    def download_template(self, template_name=None):
        uac_user = self._global_conf_uip.get("userid", "ops.admin")
        uac_url = self._global_conf_uip.get("url", "http://localhost:8080/uc")
        logging.info(f"Downloading template from controller ({uac_url})")
        uac_pass = getpass(prompt=f"Enter password for {uac_user}: ")
        if len(uac_pass) == 0:
            logging.debug("Using password from config")
            uac_pass = self._global_conf_defaults.get("uac_password")
            logging.debug(f"Password is {uac_pass}")

        if template_name is None:
            template_name = self.template_name

        #template_url = uac_url + "/resources/universaltemplate?templatename=" + self.template_name
        #headers = {"content-type": "application/json", "Accept": "application/json"}
        #logging.debug(f"Template URL is {template_url}")
        #result = requests.get(template_url, auth=(uac_user, uac_pass), headers=headers, verify=False)
        
        logging.info("Downloading template zip")
        template_url = uac_url + "/resources/universaltemplate/exporttemplate?templatename=" + self.template_name
        headers = {"Accept": "application/octet-stream"}
        logging.debug(f"Template URL is {template_url}")
        result = requests.get(template_url, auth=(uac_user, uac_pass), headers=headers, verify=False, allow_redirects=True)
        if result.ok:
            with tempfile.TemporaryDirectory() as tmpdirname:
                with open(os.path.join(tmpdirname, "template.zip"), "wb") as f:
                    f.write(result.content)
                download_folder = self.join_path("downloads")
                if not os.path.exists(download_folder):
                    os.makedirs(download_folder)
                shutil.copy2(os.path.join(tmpdirname, "template.zip"), os.path.join(download_folder, "template.zip"))
                logging.info(f"Download file archived in download folder {download_folder}")
                logging.info("Unpacking the zip file")
                unpack_archive(os.path.join(tmpdirname, "template.zip"), extract_dir=tmpdirname, format="zip")
                with open(os.path.join(tmpdirname, "template.json")) as json_f:
                    json_data = json_f.read()
                if os.path.exists(os.path.join(tmpdirname, "template_icon.png")):
                    logging.info("Icon updated from zip file")
                    shutil.copy2(os.path.join(tmpdirname, "template_icon.png"), self.join_path("src", "templates", "template_icon.png"))
                else:
                    logging.warn("Icon file is missing")
            
            self.split_template_scripts(json.loads(json_data))
        else:
            logging.error(f"Error while downloading {self.template_name} from {uac_url}")
            logging.error(f"Error detail: {result.text}")
            sys.exit(3)

    def update_fields(self, code=False):
        fields_path = self.join_path("fields.yml")
        if os.path.exists(fields_path):
            with open(fields_path) as f:
                conf = yaml.safe_load(f)
                new_fields = conf.get("fields", [])
                logging.debug("FIELDS: ", new_fields)
                fields_dict = fb.prepare_fields(new_fields, code)
            
            logging.info("Updating template.json file")
            template = self.join_path("src", "templates", "template.json")
            if os.path.exists(template):
                with open(template, "r") as f:
                    template_content = f.read()
                    
                with open(template, "w") as f:
                    _json = json.loads(template_content)
                    _json["fields"] = fields_dict
                    f.write(self.format_json(_json))
                    logging.debug("template.json file is updated")
                
                self.dump_fields(write=True)
                logging.debug("fields.yml updated")
            else:
                logging.error(f"ERROR: template.json file is missing! Path= {template}")
                sys.exit(1)
        else:
            logging.error(f"fields.yml file is missing")
            sys.exit(4)

    def dump_fields(self, write=False):
        logging.info("Writing fields to fields.yml file")
        template = self.join_path("src", "templates", "template.json")
        if os.path.exists(template):
            with open(template, "r") as f:
                template_content = f.read()
                _json = json.loads(template_content)
                fields_dict = fb.dump_fields(_json.get("fields"))
                yaml_dump = yaml.dump(fields_dict, Dumper=MyDumper, default_flow_style=False, sort_keys=False)
                if not write:
                    print(yaml_dump)
                else:
                    fields_path = self.join_path("fields.yml")
                    with open(fields_path, "w") as f:
                        f.write(yaml_dump)
        else:
            logging.error(f"ERROR: template.json file is missing! Path= {template}")
            sys.exit(1)

    def build_zip(self, project_name):
        with tempfile.TemporaryDirectory() as tmpdirname:
            logging.debug(f"Created temporary directory {tmpdirname}")
            payload = self.merge_template_scripts(self.project_name)
            template = os.path.join(tmpdirname, "template.json")
            with open(template, "w") as f:
                f.write(self.format_json(payload))
            template_icon = self.join_path("src", "templates", "template_icon.png")
            shutil.copy2(template_icon, os.path.join(tmpdirname, "template_icon.png"))
            if os.path.exists("script.yml"):
                with open("script.yml") as f:
                    conf = yaml.safe_load(f)
                    version = conf.get("script", []).get("version")
            else:
                version = datetime.now().strftime("%Y%m%d")

            archive_name = f"unv-tmplt-{project_name}-{version}"
            new_archive_file = make_archive(archive_name, "zip", root_dir=tmpdirname)
            logging.info(f"Archive file created. File name is {archive_name}.zip")
            build_folder = self.join_path("build")
            if not os.path.exists(build_folder):
                os.makedirs(build_folder)
            move(new_archive_file, os.path.join(build_folder, archive_name + ".zip"))
            logging.debug(f"Archive file {archive_name}.zip moved to {build_folder}")
        return os.path.join(build_folder, archive_name + ".zip")

    def yes_or_no(self, question, default=None):
        if default == True:
            options = "(Y/n)"
        elif default == False:
            options = "(y/N)"
        else:
            options = "(y/n)"
            default = None

        while True:
            answer = input(question + options + ": ").lower().strip()
            
            if len(answer) == 0 and default is not None:
                return default
            elif answer[0] in  ["y", "yes"]:
                return True
            elif answer[0] in  ["n", "no"]:
                return False

    def titleize(self, name):
        if name[:3] in ["ue-", "ut-"]:
            name = name[3:]
        elif name.lower() != name:
            # if name has uppercase than use it as-is
            return name
        name = name.replace("_", " ")
        name = name.replace("-", " ")
        name = name.replace("/", "")
        return name.title()

    def format_ext_name(self, name):
        name = name.replace("_", "-")
        name = name.replace(" ", "-")
        name = name.replace("/", "")
        return name.lower()

    def join_path(self, *paths):
        if self.in_project_folder:
            return os.path.join(os.getcwd(), *paths)
        else:
            return os.path.join(self.project_name, *paths)

    def uip_init(self, project_name, default_template):
        # run uip init command
        command = f'''uip init -t {default_template} {project_name}'''
        logging.info(f"Initializing the extension with command {command}")
        command = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if command.returncode != 0:
            logging.error("UIP Init command failed.")
            logging.error(f"ERROR: Command is {command}")
            logging.error(f"ERROR: Return code is {command.returncode}")
            sys.exit(command.returncode)

    def update_extension_yaml(self, project_name):
        logging.info("Updating extension.yml file")
        extension_config = self.join_path("src", "extension.yml")
        if os.path.exists(extension_config):
            with open(extension_config, "w") as f:
                _extension_config = self._global_conf_extension
                _extension_config["extension"]["name"] = project_name
                yaml.dump(_extension_config, f, sort_keys=False)
                logging.debug("extension.yml file is updated")
        else:
            logging.error(f"ERROR: extension.yml file is missing! Path= {extension_config}")
            sys.exit(1)

    def update_uip_config(self, project_name):
        logging.info("Updating uip.yml file")
        config = self.join_path(".uip", "config", "uip.yml")
        if os.path.exists(config):
            with open(config, "w") as f:
                _config = self._global_conf_uip
                _config["template-name"] = self.template_name
                yaml.dump(_config, f, sort_keys=False)
                logging.debug("uip.yml file is updated")
        else:
            logging.error(f"ERROR: uip.yml file is missing! Path= {config}")
            sys.exit(1)

    def read_template_json(self, template_path):
        logging.info("Reading template.json file")
        
        if os.path.exists(template_path):
            with open(template_path, "r") as f:
                template_content = f.read()
                return json.loads(template_content)
        else:
            logging.error(f"ERROR: template.json file is missing! Path= {template_path}")
            sys.exit(1)

    def update_template_json(self, project_name, update_uuid=False, update_new_uuid=False):
        logging.info("Updating template.json file")
        template = self.join_path("src", "templates", "template.json")
        if os.path.exists(template):
            with open(template, "r") as f:
                template_content = f.read()
                if update_uuid:
                    logging.info("Updating SysIds in template.json")
                    template_content = self.update_all_sysid_values(template_content)
                if update_new_uuid:
                    logging.info("Updating new_uuid with a valid SysIds in template.json")
                    template_content = self.update_new_uuid_values(template_content)

            with open(template, "w") as f:
                _json = json.loads(template_content)
                if "extension" in _json and _json["extension"] is not None:
                    _json["extension"] = project_name
                _json["name"] = self.template_name
                f.write(self.format_json(_json))
                logging.debug("template.json file is updated")
        else:
            logging.error(f"ERROR: template.json file is missing! Path= {template}")
            sys.exit(1)
    
    def merge_template_scripts(self, project_name):
        logging.info("Merging scripts to template.json file")
        template = self.join_path("src", "templates", "template.json")
        if os.path.exists(template):
            with open(template, "r") as f:
                template_content = f.read()

            _json = json.loads(template_content)
            if _json["useCommonScript"]:
                script_path = self.join_path("src", "templates", "script")
                script_content = self.read_file_content(script_path)
                _json["script"] = r"""{}""".format(script_content)
                _json["scriptUnix"] = None
                _json["scriptWindows"] = None
            else:
                _json["script"] = None
                if _json["agentType"] in ["Linux/Unix", "Any"]:
                    script_unix_path = self.join_path("src", "templates", "scriptUnix")
                    script_unix_content = self.read_file_content(script_unix_path)
                    _json["scriptUnix"] = script_unix_content #.replace('\n', '\\n')

                if _json["agentType"] in ["Windows", "Any"]:
                    script_windows_path = self.join_path("src", "templates", "scriptWindows")
                    script_windows_content = self.read_file_content(script_windows_path)
                    _json["scriptWindows"] = script_windows_content #.replace('\n', '\\n')
            
            if "iconFilename" not in _json:
                icon_file = self.join_path("src", "templates", "template_icon.png")
                if os.path.exists(icon_file):
                    logging.info("Icon fields are added to the template.json payload.")
                    _json["iconDateCreated"] = "2022-06-23 15:37:45"
                    _json["iconFilename"] = "template_icon.png"
                    _json["iconFilesize"] = os.path.getsize(icon_file)

            # Remove new fields to it can be imported to 7.1
            if "events" in _json:
                del _json["events"]
            if "sendVariables" in _json:
                del _json["sendVariables"]

            return _json
        else:
            logging.error(f"ERROR: template.json file is missing! Path= {template}")
            sys.exit(1)

    def split_template_scripts(self, payload_json):
        if payload_json["useCommonScript"]:
            script_path = self.join_path("src", "templates", "script")
            self.write_to_file(script_path, payload_json["script"])
        else:
            if payload_json["agentType"] in ["Linux/Unix", "Any"]:
                script_unix_path = self.join_path("src", "templates", "scriptUnix")
                self.write_to_file(script_unix_path, payload_json["scriptUnix"])
            if payload_json["agentType"] in ["Windows", "Any"]:
                script_windows_path = self.join_path("src", "templates", "scriptWindows")
                self.write_to_file(script_windows_path, payload_json["scriptWindows"])

        payload_json["script"] = None
        payload_json["scriptUnix"] = None
        payload_json["scriptWindows"] = None

        # Remove new fields to it can be imported to 7.1
        del payload_json["events"]
        del payload_json["sendVariables"]

        template = self.join_path("src", "templates", "template.json")
        with open(template, "w") as f:
            f.write(self.format_json(payload_json))
            logging.debug("template.json file is updated")
    
    def format_json(self, json_obj):
        json_string = json.dumps(json_obj, indent=4, sort_keys=True)
        json_string = re.sub(r"\n\s*\{", " {", json_string)
        json_string = re.sub(r"\n\s*\]", " ]", json_string)
        json_string = re.sub(r"\[\],", "[ ],", json_string)
        json_string = re.sub(r"\":(\s*[^\n]+)", "\" :\\1", json_string)
        return json_string

    def read_file_content(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()
        else:
            logging.error(f"ERROR: file is missing! Path= {file_path}")
            sys.exit(1)

        return content

    def write_to_file(self, file_path, content):
        try:
            short_file_path = file_path.replace(os.getcwd(), "")
            if content is None:
                logging.warn(f"Script Content for {short_file_path} is empty.")
                return

            if os.path.exists(file_path):
                if not self.yes_or_no(f"Do you want to overwrite the script file? ({short_file_path}): ", default=False):
                    logging.info(f"Script file NOT updated.")
                    return None
            
            logging.info(f"Script file updated: {short_file_path}")
            with open(file_path, "w") as f:
                f.write(content)
        except Exception as ex:
            logging.error(f"ERROR: While writing to file! Path= {file_path}")
            logging.error(f"ERROR: {ex}")
            sys.exit(1)

    def update_all_sysid_values(self, template_content):
        regex = re.compile(r"""\"sysId\"\s*:\s*\"([0-9a-f]{32})\"""")
        matches = regex.finditer(template_content)
        olds = set()
        for match in matches:
            old = match.group(1)
            if old in olds:
                continue

            new = str(uuid.uuid4()).replace("-","")
            logging.info(f"Updating SysID: {old} => {new}")
            template_content = template_content.replace(old, new)
            olds.add(old)
        
        return template_content

    def update_new_uuid_values(self, template_content):
        old = '"new_uuid"'
        for i in range(template_content.count(old)):
            new = "\"{}\"".format(str(uuid.uuid4()).replace("-",""))
            logging.info(f"Updating SysID: {old} => {new}")
            template_content = template_content.replace(old, new, 1)
        
        return template_content

class QuipGlobalConfig:
    def __init__(self, config_file=None) -> None:
        self.conf = {}
        self.new_config = False
        if config_file is None:
            config_file = self.find_config_path()
        
        if config_file is not None:
            with open(config_file) as f:
                self.conf = yaml.safe_load(f)
            if self.new_config:
                self.conf["new"] = True

    def find_config_path(self, config_path=None):
        home_folder = os.path.expanduser("~")
        config_file = config_file_home = os.path.join(home_folder, ".uip_config.yml")
        if not os.path.exists(config_file):
            config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".uip_config.yml")
        
        if os.path.exists(config_file):
            logging.info(f"Using config from file : {config_file}")
            return config_file
        else:
            logging.warn(f"Not using any config file. {config_file_home} or {config_file}")
            config_file = self.setup_config(config_file_home)
            self.new_config = True
            return config_file
    
    def yes_or_no(self, question, default=None):
        if default == True:
            options = "(Y/n)"
        elif default == False:
            options = "(y/N)"
        else:
            options = "(y/n)"
            default = None

        while True:
            answer = input(question + options + ": ").lower().strip()
            
            if len(answer) == 0 and default is not None:
                return default
            elif answer[0] in  ["y", "yes"]:
                return True
            elif answer[0] in  ["n", "no"]:
                return False
    
    def setup_config(self, config_file):
        logging.info("You don't have any config file. I think this is the first time you are running this tool.")
        if self.yes_or_no(f"Do you want to download sample quip config? (Destination: {config_file}): ", default=True):
            response = requests.get("https://stb-se-dev.s3.amazonaws.com/quip/.uip_config.yml.sample")
            if response.ok:
                conf = yaml.safe_load(response.text)
                owner_name = input(f"Enter your name: ")
                conf["extension.yml"]["owner"]["name"] = owner_name

            with open(config_file, "w") as f:
                yaml.dump(conf, f, sort_keys=False)
            
            logging.info(f"Config file created. Check {config_file}")
            cprint("You need to pull the baseline projects. Use the following command.", color="cyan")
            cprint("git clone https://gitlab.stonebranch.com/integration-prototypes/ue-baseline.git", color="cyan")
            cprint("git clone https://gitlab.stonebranch.com/integration-prototypes/ut-baseline.git", color="cyan")
            
            self.check_config(conf)

            return config_file
        return None
    
    def check_config(self, conf):
        print(yaml.dump(conf, sort_keys=False))
        # check defaults
        if "defaults" not in conf:
            cprint("Defaults section is missing", color="red")
        else:
            if "template" not in conf["defaults"]:
                cprint("Defaults>template tag is missing", color="red")
            elif len(conf["defaults"]["template"]) == 0:
                cprint("Defaults>template value is empty.", color="red")
            
            if "bootstrap" not in conf["defaults"]:
                cprint("Defaults>bootstrap tag is missing", color="red")
            else:
                if "source" not in conf["defaults"]["bootstrap"]:
                    cprint("Defaults>bootstrap>source tag is missing", color="red")
                else:
                    if not os.path.exists(conf["defaults"]["bootstrap"]["source"]):
                        cprint("Defaults>bootstrap>source path is missing.", color="red")
                        cprint("Be sure you use full path of the ue-baseline project. You can clone the project by using the following command.", color="red")
                        cprint("git clone https://gitlab.stonebranch.com/integration-prototypes/ue-baseline.git\n", color="green")

                if "template_source" not in conf["defaults"]["bootstrap"]:
                    cprint("Defaults>bootstrap>template_source tag is missing", color="red")
                else:
                    if not os.path.exists(conf["defaults"]["bootstrap"]["template_source"]):
                        cprint("Defaults>bootstrap>template_source path is missing.", color="red")
                        cprint("Be sure you use full path of the ut-baseline project. You can clone the project by using the following command.", color="red")
                        cprint("git clone https://gitlab.stonebranch.com/integration-prototypes/ut-baseline.git\n", color="green")



            
        


class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 2:
            super().write_line_break()

def run():
    _quip = Quip(log_level=logging.INFO)
    _quip.main()

if __name__ == '__main__':
    _quip = Quip(log_level=logging.INFO)
    _quip.main()
