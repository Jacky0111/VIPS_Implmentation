import os
import json
import time
import functools
from urllib.parse import urlparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from CssBox import CssBox
from DomNode import DomNode
from Visualization.Output import Output
from VariationOrder.BlockVO import BlockVO
from VariationOrder.SeparatorVO import SeparatorVO
from VIPS.VisualBlockExtraction import VisualBlockExtraction
from VIPS.SeparatorDetection import SeparatorDetection
from VIPS.SeparatorWeight import SeparatorWeight
from VIPS.ContentStructureConstruction import ContentStructureConstruction


class Vips:
    PDoC = 1 # Permitted Degree of Coherence
    round = 1

    url = None
    html = None
    output = None
    browser = None
    file_name = None

    node_list = []
    css_box_list = dict()

    def __init__(self, url_str):
        self.setUrl(url_str)
        self.setDriver()
        self.output = Output()
        self.output.imageOutput(self.browser, self.url, self.file_name)
        self.getDomTree()

    def service(self):
        print('-----------------------------Visual Block Extraction------------------------------------')
        vbe = VisualBlockExtraction()
        block = vbe.service(self.node_list)
        block_list = vbe.block_list

        i = 0
        while self.checkDoC(block_list) and i < self.round:
            print(f'Size of Block List: {len(block_list)}')
            self.output.blockOutput(block_list, self.file_name, i)
            Output.textOutput(self.file_name, block_list, i)

            print(f'-----------------------------Separator Detection---------------------------------{str(i)}')
            sd = SeparatorDetection(self.browser.get_window_size()['width'], self.browser.get_window_size()['height'])
            vertical_list = []
            vertical_list.extend(sd.service(block_list, SeparatorVO.TYPE_VERTICAL))
            self.output.separatorOutput(vertical_list, self.file_name, '_vertica_', i)
            horizontal_list = []
            horizontal_list.extend(sd.service(block_list, SeparatorVO.TYPE_HORIZONTAL))
            self.output.separatorOutput(horizontal_list, self.file_name, '_horizontal_', i)

            print(f'-----------------------------Separator Weight---------------------------------{str(i)}')
            hr_list = vbe.hr_list
            sw = SeparatorWeight(self.node_list)
            sw.service(horizontal_list, hr_list)
            sw.service(vertical_list, hr_list)

            print(f'-----------------------Content Structure Construction----------------------------{str(i)}')
            separator_list = []
            separator_list.extend(horizontal_list)
            separator_list.extend(vertical_list)
            separator_list.sort(key=functools.cmp_to_key(Vips.separatorCompare))
            temp_list = block_list
            csc = ContentStructureConstruction()
            csc.service(separator_list, block)
            BlockVO.refreshBlock(block)
            block_list.clear()
            vbe.fillList(block)
            block_list = vbe.block_list

            for new in block_list:
                for old in temp_list:
                    if new.identity == old.identity:
                        block_list.remove(new)
                        break
            i += 1
        self.browser.quit()

    def checkDoC(self, blocks):
        for block_vo in blocks:
            if block_vo.DoC < self.PDoC:
                return True
        return False

    @staticmethod
    def separatorCompare(separator1, separator2):
        if separator1 < separator2:
            return -1
        elif separator1 > separator2:
            return 1
        else:
            return 0

    def setUrl(self, url_str):
        try:
            if url_str.startswith('https://') or url_str.startswith('http://'):
                self.url = url_str
            else:
                self.url = 'http://' + url_str
            parse_object = urlparse(self.url)
            new_path = r'Screenshots/' + parse_object.netloc + '_'+str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) +'/'
            self.file_name = new_path + parse_object.netloc
            os.makedirs(new_path)
        except TypeError:
            print(f'Invalid Address: {str(url_str)}')
        except AttributeError:
            print(f'Invalid Address: {str(url_str)}')

    def setDriver(self):
        option = Options()
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        option.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(chrome_options=option)

    def convertToDomTree(self, obj, parentNode=None):
        if isinstance(obj, str):
            json_obj = json.loads(obj)  # Use json lib to load our json string
        else:
            json_obj = obj
        node_type = json_obj['nodeType']
        node = DomNode(node_type)
        # Element Node
        if node_type == 1:
            node.createElement(json_obj['tagName'])
            attributes = json_obj['attributes']
            if attributes is not None:
                node.setAttributes(attributes)
            visual_cues = json_obj['visual_cues']
            if visual_cues is not None:
                node.setVisualCues(visual_cues)
        elif node_type == 3:
            node.createTextNode(json_obj['nodeValue'], parentNode)
            if node.parentNode is not None:
                visual_cues = node.parentNode.visual_cues
                if visual_cues is not None:
                    node.setVisualCues(visual_cues)
        else:
            return node

        self.node_list.append(node)
        if node_type == 1:
            child_nodes = json_obj['childNodes']
            for i in range(len(child_nodes)):
                if child_nodes[i]['nodeType'] == 1:
                    node.appendChild(self.convertToDomTree(child_nodes[i], node))
                if child_nodes[i]['nodeType'] == 3:
                    try:
                        if not child_nodes[i]['nodeValue'].isspace():
                            node.appendChild(self.convertToDomTree(child_nodes[i], node))
                    except KeyError:
                        print('Abnormal text node')

        return node

    def getDomTree(self):
        self.browser.get(self.url)
        time.sleep(5)

        # Read in DOM jva script file as string
        file = open('DOM.js', 'r')
        java_script = file.read()

        # Add additional javascript code to run our DOM js toJSON method
        java_script += '\nreturn JSON.stringify(toJSON(document.getElementsByTagName("BODY")[0]));'

        # Finally run the javascript, and wait for it to finish and call the someCallback function.
        x = self.browser.execute_script(java_script)
        print(x)
        self.convertToDomTree(x)

    def setRound(self, r):
        self.round = r
