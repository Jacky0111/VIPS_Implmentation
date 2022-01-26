import os
import json
import time
import functools
from urllib.parse import urlparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from DOM.DomNode import DomNode
from Visualization import Visualization
from VIPS.VisualBlockExtraction import VisualBlockExtraction
from VIPS.SeparatorDetection import SeparatorDetection
from VIPS.SeparatorWeight import SeparatorWeight
from VIPS.ContentStructureConstruction import ContentStructureConstruction


class Vips:
    PDoC = 6  # Permitted Degree of Coherence
    url = None
    output = None
    browser = None
    file_name = None
    window_width = None
    window_height = None
    node_list = []  # To store dom tree

    def __init__(self, url):
        self.url = url
        self.node_list.clear()
        self.setFolderName()
        self.setDriver()
        self.getJavaScript()

    '''
    Execution function for Vips class including:
    1. Visual Block Extraction
    2. Visual Separator Detection
    3. Content Structure Construction
    '''
    def runner(self):
        print('Step 1: Visual Block Extraction---------------------------------------------------------------')
        vbe = VisualBlockExtraction()
        block = vbe.runner(self.node_list)
        block_list = vbe.block_list

        print(f'Number of Block List: {len(block_list)}')
        time.sleep(10)
        self.output.blockOutput(block_list, self.file_name)
        Visualization.textOutput(block_list)

        i = 1
        while True:
            print('Step 2: Separator Detection-------------------------------------------------------------------')
            sd = SeparatorDetection(0, 0, self.window_width, self.window_height)
            horizontal_list = []
            horizontal_list.extend(sd.runner(block_list, 'horizontal'))
            self.output.separatorOutput(horizontal_list, self.file_name, 'horizontal', i)
            vertical_list = []
            vertical_list.extend(sd.runner(block_list, 'vertical'))
            self.output.separatorOutput(vertical_list, self.file_name, 'vertical', i)

            print(f'Number of Horizontal Separator List: {len(horizontal_list)}')
            print(f'Number of Vertical Separator List: {len(vertical_list)}')
            time.sleep(10)

            print('Step 3: Separator Weight----------------------------------------------------------------------')
            hr_list = vbe.hr_list
            sw = SeparatorWeight()
            print('---------------------------------------Horizontal Weight--------------------------------------')
            sw.runner(horizontal_list, hr_list)
            self.output.weightOutput(horizontal_list, self.file_name, 'horizontal_weight', i)
            print('---------------------------------------Vertical Weight----------------------------------------')
            sw.runner(vertical_list, hr_list)
            self.output.weightOutput(vertical_list, self.file_name, 'vertical_weight', i)

            print('Step 4: Content Structure Construction--------------------------------------------------------')
            separator_list = []
            separator_list.extend(horizontal_list)
            separator_list.extend(vertical_list)
            separator_list.sort(key=functools.cmp_to_key(Vips.separatorCompare))
            temp_list = block_list

            csc = ContentStructureConstruction()
            csc.runner(separator_list)

            VisualBlockExtraction.refresh(block)
            block_list.clear()
            vbe.fillPool(block)
            block_list = vbe.block_list

            # Remove the overlapping between new and old blocks
            for new in block_list:
                for old in temp_list:
                    if new.identity == old.identity:
                        block_list.remove(new)
                        break

            i += 1

            print(f'Number of Merged Block List: {len(block_list)}')
            self.output.blockOutput(block_list, self.file_name, i)

            if self.checkDoC(block_list):
                break

    '''
    Each leaf node is checked whether it meets the granularity requirement. The common requirement must be DoC > PDoC
    @param blocks
    @return True if DoC > PDoC, False otherwise.
    '''
    def checkDoC(self, blocks):
        for ele in blocks:
            print(f'ele.DoC: {ele.DoC}, self.PDoC: {self.PDoC}')
            if ele.DoC > self.PDoC:
                print('ele.DoC > self.PDoC')
                return True
        print('ele.DoC < self.PDoC')
        return False

    '''
    Sort the separator list in ascending order.
    @param sep1
    @param sep2
    @return 1 if sep1 > sep2, -1 if sep1 < sep2, 0 otherwise.
    '''
    @staticmethod
    def separatorCompare(sep1, sep2):
        if sep1 < sep2:
            return -1
        elif sep1 > sep2:
            return 1
        else:
            return 0

    '''
    Set the folder name and make directory
    '''
    def setFolderName(self):
        parse_url = urlparse(self.url)
        path = r'Screenshots/' + parse_url.netloc + '_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '/'
        self.file_name = path + parse_url.netloc
        os.makedirs(path)

    '''
    Set driver
    '''
    def setDriver(self):
        option = Options()
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        option.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(chrome_options=option)

    '''
    Retrieve Java Script from the web page
    '''
    def getJavaScript(self):
        self.browser.get(self.url)
        time.sleep(10)

        # Before closing the web server make sure get all the information required
        self.window_width = 1920
        self.window_height = self.browser.execute_script('return document.body.parentNode.scrollHeight')

        self.output = Visualization()
        self.output.screenshotImage(self.browser, self.window_width, self.window_height, self.file_name)

        # Read in DOM java script file as string
        file = open('DOM/dom.js', 'r')
        java_script = file.read()
        with open('first.txt', 'w') as file:
            file.write(java_script)

        # Add additional javascript code to run our dom.js to JSON method
        java_script += '\nreturn JSON.stringify(toJSON(document.getElementsByTagName("BODY")[0]));'
        with open('second.txt', 'w') as file:
            file.write(java_script)

        # Run the javascript
        x = self.browser.execute_script(java_script)

        self.browser.close()
        self.browser.quit()

        self.convertToDomTree(x)

    '''
    Use the JavaScript obtained from getJavaScript() to convert to DOM Tree (Recursive Function)
    @param obj
    @param parentNode 
    @return node
    '''
    def convertToDomTree(self, obj, parentNode=None):
        if isinstance(obj, str):
            # Use json lib to load our json string
            json_obj = json.loads(obj)
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
        # Text Node (Free Text)
        elif node_type == 3:
            node.createTextNode(json_obj['nodeValue'], parentNode)
            if node.parentNode is not None:
                visual_cues = node.parentNode.visual_cues
                if visual_cues is not None:
                    node.setVisualCues(visual_cues)

        self.node_list.append(node)
        if node_type == 1:
            child_nodes = json_obj['childNodes']
            for i in range(len(child_nodes)):
                if child_nodes[i]['nodeType'] == 1:
                    node.appendChild(self.convertToDomTree(child_nodes[i], node))
                    print(f'NODE_{i}\n======\n{node.__str__()}')
                elif child_nodes[i]['nodeType'] == 3:
                    try:
                        if not child_nodes[i]['nodeValue'].isspace():
                            node.appendChild(self.convertToDomTree(child_nodes[i], node))
                            print(f'NODE_{i}\n======\n{node.__str__()}')
                    except KeyError:
                        print('Key Error, abnormal text node')

        return node
