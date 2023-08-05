# -*- coding:utf-8 -*-
#!/usr/bin/env python

'''
    text_markup_language_utility.py - 文本标记语言通用方法集
'''

import os, codecs,json
from typing import List, Dict, Union, AnyStr
from io import StringIO
from pathlib import Path
from dataclasses import dataclass
from attrbox import AttrDict,AttrList

try:
    import toml
except:
    toml = None

try:
    import yaml
except:
    yaml = None

from ...definations.tml import TmlDefs
from ...dataclasses.c.err import ErrorDefs,DyError

@dataclass
class TmlConf(object):
    lan: TmlDefs
    file_ext_names: List[str]

class TmlUtl(object):
    @staticmethod
    def walk_conf():
        for _, en in TmlDefs.__members__.items():
            yield TmlConf(lan = en, file_ext_names = [ nm.lower() for nm in en.value.split(":") if nm ])

    @staticmethod
    def guess_file(file_path: Union[Path,AnyStr]) -> TmlDefs:
        pos = file_path.rfind('.')
        if 0 > pos: 
            return None

        for tml_conf in TmlUtl.walk_conf():
            if file_path[pos + 1:].lower() in tml_conf.file_ext_names:
                return tml_conf.lan

        return None

    @staticmethod
    def suffix_extend_names(file_basename:str, *lans:List[TmlDefs]) -> List[str]:
        file_names = []
        for tml_conf in TmlUtl.walk_conf():
            if tml_conf.lan in lans:
                file_names.extend([ f"{file_basename}.{file_ext_name}" for file_ext_name in tml_conf.file_ext_names ])
        return file_names

    @staticmethod
    def loads(text: str, lan:TmlDefs, input_encoding:str = None, *args, **kwargs) -> Union[Dict,List]:
        if text is None:
            raise DyError(ErrorDefs.ARGS_MUSTBE_EXIST.value, title = "No argument exist", error_messsage = "Miss 'text' argument").as_exception()
        if lan is None:
            raise DyError(ErrorDefs.ARGS_MUSTBE_EXIST.value, title = "No argument exist", error_messsage = "Miss 'lan' argument").as_exception()

        if not input_encoding: input_encoding = 'utf-8'
        input_str = text.encode(input_encoding).decode('utf-8') if 'utf-8' != codecs.lookup(input_encoding).name else text

        if TmlDefs.JSON == lan:
            return json.loads(input_str, *args, **kwargs)
        elif TmlDefs.TOML == lan:
            if toml is None:
                raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", error_messsage = "Can't import 'toml' module").as_exception()
            return toml.loads(input_str)
        elif TmlDefs.YAML == lan:
            if yaml is None:
                raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", error_messsage = "Can't import 'yaml' module").as_exception()
            return yaml.load(input_str, Loader = yaml.Loader)
        else:
            raise DyError(ErrorDefs.UNSUPPORTED_CONFIGURATION_FORMAT.value, title = "Unsupport", error_message = f"Unsupported configuration format: {lan or 'None'}").as_exception()

    @staticmethod
    def loads_attr(text: str, lan:TmlDefs, input_encoding:str = None, *args, **kwargs) -> Union[AttrDict,AttrList]:
        rv = TmlUtl.loads(text, lan, input_encoding, *args, **kwargs)
        return AttrList(rv) if isinstance(rv, list) else AttrDict(rv)

    @staticmethod
    def dumps(o: dict, lan:TmlDefs = None, output_encoding:str = None, *args, **kwargs) -> str:
        if lan is None:
            raise DyError(ErrorDefs.ARGS_MUSTBE_EXIST.value, title = "No argument exist", error_messsage = "Miss 'lan' argument").as_exception()

        if not output_encoding: output_encoding = 'utf-8'
        with StringIO() as sio:
            with codecs.EncodedFile(sio, "utf-8", output_encoding) as ef:
                if TmlDefs.JSON == lan:
                    json.dump(o, ef, *args, **kwargs)
                elif TmlDefs.TOML == lan:
                    if toml is None:
                        raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", message = "Can't import 'toml' module").as_exception()
                    toml.dump(o, ef) 
                elif TmlDefs.YAML == lan:
                    if yaml is None:
                        raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", message = "Can't import 'yaml' module").as_exception()
                    yaml.dump(o, ef, *args, **kwargs)
                else:
                    raise DyError(ErrorDefs.UNSUPPORTED_CONFIGURATION_FORMAT.value, title = "Unsupport", error_message = f"Unsupported configuration format: {lan or 'None'}").as_exception()

        sio.seek(0)
        return sio.read()

    @staticmethod
    def load(file_path: Union[Path,AnyStr], lan:TmlDefs = None, input_encoding:str = None, *args, **kwargs) -> dict:
        if not os.path.exists(file_path):
            raise DyError(ErrorDefs.NO_FILE_FOUND.value, title = "No fild found", error_message = f"Lost file '{file_path}'").as_exception()

        lan_en = TmlUtl.guess_file(file_path) if not lan else lan

        if not input_encoding: input_encoding = 'utf-8'
        with codecs.open(file_path, 'r', encoding = input_encoding) as f:
            if TmlDefs.JSON == lan_en:
                return json.load(f, *args, **kwargs)
            elif TmlDefs.TOML == lan_en:
                if toml is None:
                    raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", message = "Can't import 'toml' module").as_exception()
                return toml.load(f)
            elif TmlDefs.YAML == lan_en:
                if yaml is None:
                    raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", message = "Can't import 'yaml' module").as_exception()
                return yaml.load(f, Loader = yaml.Loader)
            else:
                raise DyError(ErrorDefs.UNSUPPORTED_CONFIGURATION_FORMAT.value, title = "Unsupport", error_message = f"Unsupported configuration format: {lan or 'None'}").as_exception()

    @staticmethod
    def load_attr(file_path: Union[Path,AnyStr], lan:TmlDefs = None, input_encoding:str = None, *args, **kwargs) -> Union[AttrDict,AttrList]:
        rv = TmlUtl.load(file_path, lan, input_encoding, *args, **kwargs)
        return AttrList(rv) if isinstance(rv, list) else AttrDict(rv)

    @staticmethod
    def dump(o: dict, file_path: Union[Path,AnyStr], lan:TmlDefs = None, output_encoding:str = None, *args, **kwargs):
        lan_en = TmlUtl.guess_file(file_path) if not lan else lan

        if not output_encoding: output_encoding = 'utf-8'
        with open(file_path, 'w', encoding = output_encoding) as f:
            with codecs.EncodedFile(f, "utf-8", output_encoding) as ef:
                if TmlDefs.JSON == lan_en:
                    json.dump(o, ef, *args, **kwargs)
                elif TmlDefs.TOML == lan_en:
                    if toml is None:
                        raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", error_message = "Can't import 'toml' module").as_exception()
                    toml.dump(o, ef) 
                elif TmlDefs.YAML == lan_en:
                    if yaml is None:
                        raise DyError(ErrorDefs.UNDEFINED_ERROR.value, title = "No Module", error_message = "Can't import 'yaml' module").as_exception()
                    yaml.dump(o, ef, *args, **kwargs)
                else:
                    raise DyError(ErrorDefs.UNSUPPORTED_CONFIGURATION_FORMAT.value, title = "Unsupport", error_message = f"Unsupported configuration format: {lan or 'None'}").as_exception()
