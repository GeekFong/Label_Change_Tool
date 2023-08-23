#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
from PIL import Image
import time
from datetime import datetime
import logging
from Label_Model import change_label_progarm

# 创建模型
class Model:
    def __init__(self):
        self.wrong_files = os.getcwd() + r'\wrong_file'
        self.pyqt_config = os.getcwd() + r'\config\config.ini'
        self.file_cnt = 0
        self.thread_flag = 0
        self.delete_files_in_folder(self.wrong_files)

        self.option_map = {
            ("yolo-txt", "pascal-voc"): self.process_txt_voc,
            ("yolo-txt", "精灵标注助手-xml"): self.process_txt_xml,
            ("pascal-voc", "yolo-txt"): self.process_voc_txt,
            ("pascal-voc", "精灵标注助手-xml"): self.process_voc_xml,
            ("精灵标注助手-xml", "yolo-txt"): self.process_xml_txt,
            ("精灵标注助手-xml", "pascal-voc"): self.process_xml_voc,
        }

        # 创建一个字典，将名字改成别名
        self.alias_mapping = {
            "yolo-txt": "txt",
            "pascal-voc": "xml",
            "精灵标注助手-xml": "xml"
        }


        self.error_messages = {
            0:"信息正确",
            -1:"选择的标签相同,请更换标签",
            -2:"缺少分类名",
            -3:"路径错误或图片和转换标签数目不相同,请先校验再进行转换",
            -4:"图片或标签文件没任何数据，请检查",
            -5:"要转换的标签和你文件夹中的标签不一致"
        }


    def get_current_timestamp(self):
        # 获取当前时间戳（秒数）
        timestamp = int(time.time())
        return str(timestamp)
    

    #检测是否所有图片都是jpg
    def check_folder_for_jpg_images(self, folder_path):
        file_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]

        for file_path in file_paths:
            try:
                with Image.open(file_path) as img:
                    if img.format != "JPEG":
                        return -2
            except Exception as e:
                return -2

        return 0

    #每次启动删除文件夹下的所有文件
    def delete_files_in_folder(self, folder_path):
        #print(folder_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)



    #计算文件夹下有多少文件
    def count_files_in_folder(self, folder_path):
        file_names = os.listdir(folder_path)
        return len(file_names)



    #第一个参数是图片的文件夹，只支持jpg
    #第二个参数需要对比的标注信息，
    #标注信息的类型
    def compare_and_move_files(self, pic_folder_path, label_folder_path, type):

        # 检查文件夹是否已存在，不存在则创建
        if not os.path.exists(self.wrong_files):
            os.makedirs(self.wrong_files)


        # 获取文件夹1中的文件名集合（不包括后缀）
        filenames1 = {
            os.path.splitext(filename)[0] for filename in os.listdir(pic_folder_path)
        }

        # 获取文件夹2中的文件名集合（不包括后缀）
        filenames2 = {
            os.path.splitext(filename)[0] for filename in os.listdir(label_folder_path)
        }

        # 找到在文件夹1中存在但在文件夹2中不存在的文件名
        different_filenames1 = filenames1 - filenames2

        # 找到在文件夹2中存在但在文件夹1中不存在的文件名
        different_filenames2 = filenames2 - filenames1

        # 移动文件夹1中不同的文件到目标文件夹
        for filename in different_filenames1:
            file_path = os.path.join(pic_folder_path, f"{filename}.jpg")
            destination_path = os.path.join(self.wrong_files, f"\{filename}.jpg")
            print(destination_path)
            shutil.move(file_path, destination_path)
            print(f"Moved file from {pic_folder_path} to {self.wrong_files}: {filename}")

        # 移动文件夹2中不同的文件到目标文件夹
        for filename in different_filenames2:
            file_path = os.path.join(label_folder_path, f"{filename}.{type}")
            destination_path = os.path.join(self.wrong_files, f"\{filename}.{type}")
            shutil.move(file_path, destination_path)
            print(f"Moved file from {label_folder_path} to {self.wrong_files}: {filename}")
        
        self.file_cnt = self.file_cnt + 1

        return self.count_files_in_folder(self.wrong_files)

    #检查文件数目是否相同
    def compare_folder_files(self, folder1, folder2):
        # 验证传入的路径是否为有效路径
        if not (os.path.exists(folder1) and os.path.exists(folder2)):
            return -1  # 返回-1表示路径无效

        # 获取文件夹1中的文件列表
        files1 = os.listdir(folder1)
        num_files1 = len(files1)

        # 获取文件夹2中的文件列表
        files2 = os.listdir(folder2)
        num_files2 = len(files2)

        # 比较文件数量是否相同
        return 0 if num_files1 == num_files2 else -1 


    #检查两个文件夹是否为空
    def check_folders_for_empty(self, folder1, folder2):
        return -1 if not os.listdir(folder1) or not os.listdir(folder2) else 0


    #检测后缀名是否和传入的一样
    def check_folder_file_extensions(self, folder, extension):
        files = os.listdir(folder)  # 获取文件夹中的文件列表
        for file in files:
            file_extension = os.path.splitext(file)[1]  # 获取文件的后缀名
            if file_extension[1:] == extension:
                return True  # 存在具有相同后缀名的文件
        
        return False  # 不存在具有相同后缀名的文件


    def check_info_label(self,selected_option1, selected_option2, class_type, image_path, label_path):

        if not str(class_type): #监测传入的标签是否为空
            return -2
        if self.compare_folder_files(image_path, label_path) == -1: #检查两个文件夹里的文件数目是否相同
            return -3
        if self.check_folders_for_empty(image_path, label_path) == -1:
            return -4


        return 0


    #记录pyqt的值
    def Write_Record_Pyqt_info(self, recoder_json):
        # 检查文件是否存在，存在则删除
        if os.path.exists(self.pyqt_config):
            os.remove(self.pyqt_config)

        # 获取文件夹路径
        folder_path = os.path.dirname(self.pyqt_config)

        # 创建文件夹（包括父级文件夹）
        os.makedirs(folder_path, exist_ok=True)

        # 写入新的内容
        with open(self.pyqt_config, "w+") as file:
            file.write(recoder_json)


    #读取记录的值
    def Read_Record_Pyqt_info(self):
        try:
            with open(self.pyqt_config, "r") as file:
                if recoder_json := file.read():
                    return eval(recoder_json)
        except FileNotFoundError:
            return -1


    def change_label(self, selected_option1, selected_option2, class_type, images_path, lab_path, custom_folder, View_progressBar):
        # 调用相应的处理函数
        try:
            if (selected_option1, selected_option2) in self.option_map:
                processing_function = self.option_map[(selected_option1, selected_option2)]
                print(f'开始解析文件 —— 解析的文件放到{custom_folder}/{selected_option1}To{selected_option2}')
                print("开始转换 voc标签变为xml标签")
                print(f"标签种类为{class_type}")
                print("请确保标签的位置和数量正确，程序中无法确认你的标签名字和数量是否对应")
                        # 检查文件夹是否已存在，不存在则创建
                if not os.path.exists(f'{custom_folder}/{self.get_current_timestamp()}_{selected_option1}To{selected_option2}'):
                    os.makedirs(f'{custom_folder}/{self.get_current_timestamp()}_{selected_option1}To{selected_option2}')
                processing_function(class_type, images_path, lab_path, 
                    f'{custom_folder}/{self.get_current_timestamp()}_{selected_option1}To{selected_option2}', View_progressBar)  # 传递所需的参数
            else:
                # 处理未找到对应处理函数的情况
                print("未找到匹配的处理函数。")
        except Exception as e:
            print(f'未知错误：{e}')
            return -1

        return 0


    
    def process_txt_voc(self, class_type, images_path, lab_path, custom_folder, View_progressBar):
        change_label_progarm.txt_2_voc(images_path, custom_folder, lab_path, class_type, View_progressBar)


    def process_txt_xml(self, class_type, images_path, lab_path, custom_folder, View_progressBar):
        change_label_progarm.txt_to_xml(lab_path, custom_folder, images_path, class_type, View_progressBar)


    def process_voc_txt(self, class_type, images_path, lab_path, custom_folder,View_progressBar):
        change_label_progarm.convert_voc_to_yolov5(lab_path, custom_folder, images_path, class_type)

    def process_voc_xml(self, class_type, images_path, lab_path, custom_folder, View_progressBar):
        change_label_progarm.convert_voc_to_xml(images_path, lab_path, custom_folder, class_type)


    
    def process_xml_txt(self, class_type, images_path, lab_path, custom_folder,View_progressBar):
        change_label_progarm.xml_to_txt_batch(lab_path, custom_folder, images_path, class_type,View_progressBar)

    def process_xml_voc(self, class_type, images_path, lab_path, custom_folder,View_progressBar):
        change_label_progarm.convert_xml_to_voc_batch(lab_path, custom_folder, images_path, class_type,View_progressBar)




