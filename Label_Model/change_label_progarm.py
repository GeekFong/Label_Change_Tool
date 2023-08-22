import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from PIL import Image
import time
import logging
from xml.dom import minidom
import glob

class Xml_make(object):
    def __init__(self):
        super().__init__()
        
    def __indent(self, elem, level=0):
        i = "\n" + level*"\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.__indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def _imageinfo(self, list_top):
        annotation_root = ET.Element('annotation')
        annotation_root.set('verified', 'no')
        tree = ET.ElementTree(annotation_root)
        '''
        0:xml_savepath 1:folder,2:filename,3:path
        4:checked,5:width,6:height,7:depth
        ''' 
        folder_element = ET.Element('folder')      
        folder_element.text = list_top[1]
        annotation_root.append(folder_element)

        filename_element = ET.Element('filename')
        filename_element.text = list_top[2]
        annotation_root.append(filename_element)

        path_element = ET.Element('path')
        path_element.text = list_top[3]
        annotation_root.append(path_element)
        
        checked_element=ET.Element('checked')
        checked_element.text=list_top[4]
        annotation_root.append(checked_element)

        source_element=ET.Element('source')
        database_element=SubElement(source_element,'database')
        database_element.text='Unknown'
        annotation_root.append(source_element)   

        size_element=ET.Element('size')
        width_element=SubElement(size_element,'width')
        width_element.text=str(list_top[5])
        height_element=SubElement(size_element,'height')
        height_element.text=str(list_top[6])
        depth_element=SubElement(size_element,'depth')
        depth_element.text=str(list_top[7])
        annotation_root.append(size_element) 

        segmented_person_element=ET.Element('segmented')
        segmented_person_element.text='0'
        annotation_root.append(segmented_person_element) 

        return tree,annotation_root

    def _bndbox(self, annotation_root, list_bndbox):
        for i in range(0, len(list_bndbox), 9):
            object_element = ET.Element('object')
            name_element = SubElement(object_element, 'name')
            name_element.text = list_bndbox[i]

            flag_element = SubElement(object_element, 'flag')
            flag_element.text = list_bndbox[i + 1]   

            pose_element = SubElement(object_element, 'pose')
            pose_element.text = list_bndbox[i + 2]   

            truncated_element = SubElement(object_element, 'truncated')
            truncated_element.text = list_bndbox[i + 3] 

            difficult_element = SubElement(object_element, 'difficult')
            difficult_element.text = list_bndbox[i + 4]   

            bndbox_element = SubElement(object_element, 'bndbox')
            xmin_element = SubElement(bndbox_element, 'xmin')
            xmin_element.text = str(list_bndbox[i + 5])

            ymin_element = SubElement(bndbox_element, 'ymin')
            ymin_element.text = str(list_bndbox[i + 6])

            xmax_element = SubElement(bndbox_element, 'xmax')
            xmax_element.text = str(list_bndbox[i + 7])

            ymax_element = SubElement(bndbox_element, 'ymax')
            ymax_element.text = str(list_bndbox[i + 8])

            annotation_root.append(object_element)

        return annotation_root

    def txt_to_xml(self, list_top, list_bndbox):
        tree,annotation_root = self._imageinfo(list_top)
        annotation_root = self._bndbox(annotation_root, list_bndbox)
        self.__indent(annotation_root)
        tree.write(list_top[0], encoding='utf-8', xml_declaration=True)
        

def txt_2_xml(source_path, xml_save_dir, txt_dir, class_type):

    
    #class_type = class_type.split(",")
    #print(class_type)
    COUNT = 0
    print(f'{os.path.dirname(txt_dir)}->路径->{os.path.dirname(xml_save_dir)}')
    print("开始转换")
    time.sleep(2)
    try:
        for folder_path_tuple, folder_name_list, file_name_list in os.walk(source_path):
            for file_name in file_name_list:
                file_suffix = os.path.splitext(file_name)[-1]
                if file_suffix != '.jpg':
                    continue
                list_top = []
                list_bndbox = []
                path = os.path.join(folder_path_tuple, file_name)
                xml_save_path = os.path.join(xml_save_dir, file_name.replace(file_suffix, '.xml'))
                txt_path = os.path.join(txt_dir, file_name.replace(file_suffix, '.txt'))
                filename = os.path.splitext(file_name)[0]
                checked = 'NO'
                im = Image.open(path)
                im_w = im.size[0]
                im_h = im.size[1]
                width = str(im_w)
                height = str(im_h)
                depth = '3'
                flag = 'rectangle'
                pose = 'Unspecified'
                truncated = '0'
                difficult = '0'
                list_top.extend([xml_save_path, folder_path_tuple, filename, path, checked,
                                width, height, depth])
                for line in open(txt_path, 'r'):
                    line = line.strip()
                    info = line.split(' ')
                    
                    name = info[0]
                    print(name)
                    print(class_type)
                    classs = class_type[int(name)]
                    print(classs)
                    x_cen = float(info[1]) * im_w
                    y_cen = float(info[2]) *im_h
                    w = float(info[3]) * im_w
                    h = float(info[4]) * im_h
                    xmin = int(x_cen - w/2)
                    ymin = int(y_cen - h/2)
                    xmax = int(x_cen + w/2)
                    ymax = int(y_cen + h/2)
                    list_bndbox.extend([classs, flag, pose, truncated, difficult,
                                        str(xmin), str(ymin), str(xmax), str(ymax)])
                    #print(list_bndbox)
                Xml_make().txt_to_xml(list_top, list_bndbox)
                COUNT += 1
                logging.info(f'{os.path.basename(txt_path)}转化为{os.path.basename(xml_save_path)}')
                #print(COUNT, xml_save_path)     
                #print(COUNT)
                time.sleep(0.025)                         
    except Exception as e:
        print(e)


def yolov5_to_xml_batch(folder_path, xml_output_path, image_path, class_label):
    print(class_label)
    if not os.path.exists(xml_output_path):
        os.makedirs(xml_output_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            yolov5_annotation_file = os.path.join(folder_path, filename)
            image_filename = os.path.splitext(filename)[0] + '.jpg'
            image_file_path = os.path.join(image_path, image_filename)
            xml_output_file = os.path.join(xml_output_path, os.path.splitext(filename)[0] + '.xml')
            with open(yolov5_annotation_file, 'r') as f:
                lines = f.readlines()
            
            root = ET.Element('doc')
            folder = ET.SubElement(root, 'folder')
            folder.text = os.path.dirname(image_file_path)

            filename = ET.SubElement(root, 'filename')
            filename.text = os.path.basename(image_file_path)

            path = ET.SubElement(root, 'path')
            path.text = image_file_path

            outputs = ET.SubElement(root, 'outputs')
            object_elem = ET.SubElement(outputs, 'object')

            image = Image.open(image_file_path)
            image_width, image_height = image.size

            for line in lines:
                print(line)
                print(len(line.split()))
                class_id, x_center, y_center, width, height = line.split()
                print(class_id)
                if int(class_id) >= len(class_label):
                    continue
                class_label_name = class_label[int(class_id)]
                print(class_label_name)
                # Convert relative coordinates to absolute coordinates
                x_min = int(float(x_center) * image_width - float(width) * image_width / 2)
                y_min = int(float(y_center) * image_height - float(height) * image_height / 2)
                x_max = int(float(x_center) * image_width + float(width) * image_width / 2)
                y_max = int(float(y_center) * image_height + float(height) * image_height / 2)

                item = ET.SubElement(object_elem, 'item')
                name = ET.SubElement(item, 'name')
                name.text = class_label_name
                bndbox = ET.SubElement(item, 'bndbox')
                xmin = ET.SubElement(bndbox, 'xmin')
                xmin.text = str(x_min)
                ymin = ET.SubElement(bndbox, 'ymin')
                ymin.text = str(y_min)
                xmax = ET.SubElement(bndbox, 'xmax')
                xmax.text = str(x_max)
                ymax = ET.SubElement(bndbox, 'ymax')
                ymax.text = str(y_max)

            labeled = ET.SubElement(root, 'labeled')
            labeled.text = 'true'

            size = ET.SubElement(root, 'size')
            width = ET.SubElement(size, 'width')
            width.text = str(image_width)
            height = ET.SubElement(size, 'height')
            height.text = str(image_height)
            depth = ET.SubElement(size, 'depth')
            depth.text = '3'

            # Create a formatted XML string
            xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
            logging.info(xml_output_file)
            with open(xml_output_file, 'w') as f:
                f.write(xml_str)
            time.sleep(0.025)

def get_image_size(image_path):
    image = Image.open(image_path)
    width, height = image.size
    return width, height


def convert_coordinates(size, box):
    image_width, image_height = size[0], size[1]
    x_min, y_min, x_max, y_max = box[0], box[1], box[2], box[3]

    # 归一化处理
    x = (x_min + x_max) / (2.0 * image_width)
    y = (y_min + y_max) / (2.0 * image_height)
    w = (x_max - x_min) / image_width
    h = (y_max - y_min) / image_height

    return x, y, w, h


def pascal_voc_to_yolov5(xml_path, txt_path, image_path, classes):
    image_width, image_height = get_image_size(image_path)

    tree = ET.parse(xml_path)
    root = tree.getroot()
    with open(txt_path, 'w') as txt_file:
        logging.info(txt_path)
        #time.sleep(0.1)
        for obj in root.findall('object'):
            name = obj.find('name').text.replace(' ', '')
            bbox = obj.find('bndbox')
            xmin = float(bbox.find('xmin').text)
            ymin = float(bbox.find('ymin').text)
            xmax = float(bbox.find('xmax').text)
            ymax = float(bbox.find('ymax').text)

            # 转换为YOLOv5格式的坐标
            x, y, w, h = convert_coordinates((image_width, image_height), (xmin, ymin, xmax, ymax))

            # 获取类别索引
            class_index = classes.index(name)

            txt_file.write(f"{class_index} {x} {y} {w} {h}\n")
        time.sleep(0.025) 


def convert_voc_to_yolov5(xml_dir, txt_dir, image_dir, classes):
    # 创建保存txt文件的目录
    os.makedirs(txt_dir, exist_ok=True)

    # 遍历目录中的每个.xml文件并进行转换
    for filename in os.listdir(xml_dir):
        if filename.endswith('.xml'):
            xml_path = os.path.join(xml_dir, filename)
            txt_filename = f'{os.path.splitext(filename)[0]}.txt'
            txt_path = os.path.join(txt_dir, txt_filename)
            image_filename = f'{os.path.splitext(filename)[0]}.jpg'
            image_path = os.path.join(image_dir, image_filename)
            pascal_voc_to_yolov5(xml_path, txt_path, image_path, classes)

def convert_voc_to_xml(src_img_dir, src_txt_dir, src_xml_dir, classes):
    def convert_annotation(voc_path, image_id):
        logging.info(f"已转换:{image_id}")
        in_file = open(voc_path + '/%s.xml' % (image_id), 'rb')
        # 解析xml文件
        tree = ET.parse(in_file)
        # 获得对应的键值对
        root = tree.getroot()

        bbox = []  # 初始化
        cls_id = []
        for obj in root.iter('object'):
            # 获得difficult
            difficult = obj.find('difficult').text
            # 获得类别 =string 类型
            cls = obj.find('name').text
            try:
                cls_id.append(classes.index(cls))
            except ValueError:
                raise ValueError(f"类别 {cls} 未找到对应的索引值")
                return -1
            # 找到bndbox 对象
            xmlbox = obj.find('bndbox')
            # 获取对应的bndbox的数组 = ['xmin','xmax','ymin','ymax']
            bbox.append(
                [xmlbox.find('xmin').text, xmlbox.find('ymin').text, xmlbox.find('xmax').text, xmlbox.find('ymax').text])
        return bbox, cls_id

    img_Lists = glob.glob(src_img_dir + '/*.jpg')

    img_basenames = []
    for item in img_Lists:
        img_basenames.append(os.path.basename(item))

    img_names = []
    for item in img_basenames:
        temp1, temp2 = os.path.splitext(item)
        img_names.append(temp1)

    # 创建目标文件夹
    os.makedirs(src_xml_dir, exist_ok=True)

    for img in img_names:
        img_path = src_img_dir + '/' + img + '.jpg'
        im = Image.open(img_path)
        width, height = im.size

        gt, cls_id = convert_annotation(src_txt_dir, img)

        xml_file = open((src_xml_dir + '/' + img + '.xml'), 'w')
        xml_file.write('<?xml version="1.0" ?>\n')
        xml_file.write('<doc>\n')
        xml_file.write(f'<folder>{src_img_dir}</folder>\n')
        xml_file.write(f'<filename>{img}.jpg</filename>\n')
        xml_file.write('    <path>' + img_path + '</path>\n')
        xml_file.write('    <outputs>\n')
        xml_file.write('        <object>\n')

        count = 0
        for spt in gt:
            xml_file.write('            <item>\n')
            xml_file.write(f'                <name>{classes[int(cls_id[count])]}</name>\n')
            xml_file.write('                <bndbox>\n')
            xml_file.write('                    <xmin>' + spt[0] + '</xmin>\n')
            xml_file.write('                    <ymin>' + spt[1] + '</ymin>\n')
            xml_file.write('                    <xmax>' + spt[2] + '</xmax>\n')
            xml_file.write('                    <ymax>' + spt[3] + '</ymax>\n')
            xml_file.write('                </bndbox>\n')
            xml_file.write('            </item>\n')
            count += 1
        xml_file.write('        </object>\n')
        xml_file.write('    </outputs>\n')
        xml_file.write('    <labeled>true</labeled>\n')
        xml_file.write('    <size>\n')
        xml_file.write('        <width>' + str(width) + '</width>\n')
        xml_file.write('        <height>' + str(height) + '</height>\n')
        xml_file.write('        <depth>3</depth>\n')
        xml_file.write('    </size>\n')
        xml_file.write('</doc>')
    
        time.sleep(0.02)

def yolov5_to_txt_batch(folder_path, txt_output_path, image_path, class_label):
    if not os.path.exists(txt_output_path):
        os.makedirs(txt_output_path)

    for filename in os.listdir(folder_path):
        if filename.endswith('.xml'):
            xml_file = os.path.join(folder_path, filename)
            image_filename = os.path.splitext(filename)[0] + '.jpg'
            image_file_path = os.path.join(image_path, image_filename)
            txt_output_file = os.path.join(txt_output_path, os.path.splitext(filename)[0] + '.txt')

            tree = ET.parse(xml_file)
            root = tree.getroot()

            image = Image.open(image_file_path)
            image_width, image_height = image.size
            logging.info(txt_output_file)
            with open(txt_output_file, 'w') as f:
                for item in root.findall('outputs/object/item'):
                    name = item.find('name').text
                    xmin = int(item.find('bndbox/xmin').text)
                    ymin = int(item.find('bndbox/ymin').text)
                    xmax = int(item.find('bndbox/xmax').text)
                    ymax = int(item.find('bndbox/ymax').text)

                    class_id = class_label.index(name)
                    x_center = (xmin + xmax) / 2 / image_width
                    y_center = (ymin + ymax) / 2 / image_height
                    width = (xmax - xmin) / image_width
                    height = (ymax - ymin) / image_height

                    line = f"{class_id} {x_center} {y_center} {width} {height}"
                    f.write(line + '\n')
            time.sleep(0.02)
                    
def convert_xml_to_voc_batch(xml_folder, dest_folder, image_path, class_labels):
    os.makedirs(dest_folder, exist_ok=True)

    for filename in os.listdir(xml_folder):
        if filename.endswith('.xml'):
            xml_file_path = os.path.join(xml_folder, filename)
            dest_xml_path = os.path.join(dest_folder, os.path.splitext(filename)[0] + '.xml')

            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            annotation = ET.Element('annotation')
            annotation.set('verified', 'no')

            folder = ET.SubElement(annotation, 'folder')
            folder.text = root.find('folder').text

            filename_elem = ET.SubElement(annotation, 'filename')
            filename_elem.text = os.path.splitext(root.find('filename').text)[0]

            path = ET.SubElement(annotation, 'path')
            path.text = os.path.join(image_path, filename_elem.text + '.jpg')

            checked = ET.SubElement(annotation, 'checked')
            checked.text = 'NO'

            source = ET.SubElement(annotation, 'source')
            database = ET.SubElement(source, 'database')
            database.text = 'Unknown'

            size = ET.SubElement(annotation, 'size')
            width = ET.SubElement(size, 'width')
            width.text = root.find('size/width').text
            height = ET.SubElement(size, 'height')
            height.text = root.find('size/height').text
            depth = ET.SubElement(size, 'depth')
            depth.text = root.find('size/depth').text

            segmented = ET.SubElement(annotation, 'segmented')
            segmented.text = '0'

            objects = root.findall('outputs/object')
            for obj in objects:
                item = obj.find('item')
                name = item.find('name').text
                bndbox = item.find('bndbox')

                object_elem = ET.SubElement(annotation, 'object')

                name_elem = ET.SubElement(object_elem, 'name')
                if name in class_labels:
                    name_elem.text = name
                else:
                    raise ValueError(f"类别 {name} 未找到对应的索引值")

                flag = ET.SubElement(object_elem, 'flag')
                flag.text = 'rectangle'

                pose = ET.SubElement(object_elem, 'pose')
                pose.text = 'Unspecified'

                truncated = ET.SubElement(object_elem, 'truncated')
                truncated.text = '0'

                difficult = ET.SubElement(object_elem, 'difficult')
                difficult.text = '0'

                bndbox_elem = ET.SubElement(object_elem, 'bndbox')

                xmin = ET.SubElement(bndbox_elem, 'xmin')
                xmin.text = bndbox.find('xmin').text

                ymin = ET.SubElement(bndbox_elem, 'ymin')
                ymin.text = bndbox.find('ymin').text

                xmax = ET.SubElement(bndbox_elem, 'xmax')
                xmax.text = bndbox.find('xmax').text

                ymax = ET.SubElement(bndbox_elem, 'ymax')
                ymax.text = bndbox.find('ymax').text

            new_tree = ET.ElementTree(annotation)
            new_tree.write(dest_xml_path, encoding='utf-8', xml_declaration=True)

            logging.info(dest_xml_path)
            # 使用minidom重新解析XML文件并设置格式为一行行
            dom = minidom.parse(dest_xml_path)
            with open(dest_xml_path, 'w') as f:
                dom.writexml(f, addindent='', newl='\n')
            time.sleep(0.025)