import time
from PIL import Image, ImageDraw, ImageFont


class Output:
    @staticmethod
    def imageOutput(browser, url, screenshot_path='screenshot.png'):
        default_width = 1920
        default_height = 1080
        print('1. Getting Dimension')
        browser.set_window_size(default_width, default_height)
        browser.get(url)
        total_height = browser.execute_script("return document.body.parentNode.scrollHeight")

        print('2. Getting Screenshot')
        browser.set_window_size(default_width, total_height)
        browser.get(url)
        time.sleep(5)
        browser.save_screenshot(screenshot_path + '.png')
        print('Done')

    @staticmethod
    def blockOutput(block, file_name, i=0):
        image = Image.open(file_name + 'png')
        draw = ImageDraw.Draw(image)
        for block_vo in block:
            if block_vo.isVisualBlock:
                # Rectangle
                coordinate = (block_vo.x, block_vo.y, block_vo.x + block_vo.width, block_vo.y + block_vo.height)
                line = (coordinate[0], coordinate[1], coordinate[0], coordinate[3])
                draw.line(line, fill='red', width=1)
                line = (coordinate[0], coordinate[1], coordinate[2], coordinate[1])
                draw.line(line, fill='red', width=1)
                line = (coordinate[0], coordinate[3], coordinate[2], coordinate[3])
                draw.line(line, fill='red', width=1)
                line = (coordinate[2], coordinate[1], coordinate[2], coordinate[3])
                draw.line(line, fill='red', width=1)

                font = ImageFont.truetype("arial.ttf", 15)
                draw.text((block_vo.x, block_vo.y), block_vo.id, (255, 0, 0), font=font)

            path = f'{file_name}_Block_{str(i)}.png'
            image.save(path)

    @staticmethod
    def separatorOutput(List, file_name, direction, i=0):
        if direction == '_vertica_':
            image = Image.open(f'{file_name}_Block_{str(i)}.png')
        elif direction == '_horizontal_':
            image = Image.open(f'{file_name}_vertica_{str(i)}.png')
        draw = ImageDraw.Draw(image)

        for separator in List:
            draw.rectangle(((separator.x, separator.y),
                            (separator.x + separator.width, separator.y + separator.height)
                            ), fill='blue')
        path = f'{file_name}{direction}{str(i)}.png'
        image.save(path)

    @staticmethod
    def textOutput(file_name, block_list, i=0):
        f = open(f'{file_name}_text_output_{str(i)}.txt', 'a')  # , encoding= 'utf-8'
        for block_vo in block_list:
            write_line = str('\n=============================================================\nBlock-' + str(block_vo.id) + '\n')
            text_content = ''
            for box in block_vo.boxes:
                writable = False
                if box.nodeType == 3:
                    if (box.parentNode.nodeName != "script" and
                            box.parentNode.nodeName != "noscript" and
                            box.parentNode.nodeName != "style"):
                        if not box.nodeValue.isspace() or box.nodeValue == None:
                            text_content += str(box.nodeValue + '\n')
                            writable = True
                write_line += text_content + str('\n=============================================================\n')
                if writable:
                    try:
                        f.write(write_line)
                    except UnicodeEncodeError:
                        f.write(str(write_line.encode('utf-8').decode('utg-8')))
                        print(block_vo.id)
            f.close()
