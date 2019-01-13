#!/usr/bin/env python3
#!-*- coding:utf-8 -*-

import json
import xml.etree.ElementTree as etree


class JSONDataExtractor:
    '''
    从json文件读取数据，并反序列化为字典对象
    '''
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
    @property
    def parsed_data(self):
        return self.data


class XMLDataExtractor:
    '''
    从xml文件读取数据，并反序列化为ElementTree对象
    '''
    def __init__(self, filepath):
        self.tree = etree.parse(filepath)
    
    @property
    def parsed_data(self):
        return self.tree


def data_extraction_factory(filepath):
    '''工厂模式方法
    根据文件拓展名返回 JSONDataExtractor 或 XMLDataExtractor实例
    '''
    if filepath.endswith('json'):
        extractor = JSONDataExtractor
    elif filepath.endswith('xml'):
        extractor = XMLDataExtractor
    else:
        raise ValueError(f'Cannot extract data from {filepath}')
    
    return extractor(filepath)

def extract_data_from(filepath):
    '''包裹data_extraction_factory函数，添加异常处理
    '''
    factory_obj = None
    try:
        factory_obj = data_extraction_factory(filepath)
    except ValueError as e:
        print(e)
    return factory_obj


if __name__ == '__main__':
    sqlite_factory = extract_data_from('./data/person.sqlite')
    print()

    #解析json文件
    json_factory = extract_data_from('./data/movies.json')
    json_data = json_factory.parsed_data
    print(f'Found: {len(json_data)} movies.')
    for movie in json_data:
        print(f'Title: {movie.get("title")}')
        print(f'Year: {movie.get("year")}')
        print(f'Director: {movie.get("director")}')
        print(f'Genre: {movie.get("genre")}')
        print()
    
    #解析xml文件
    xml_factory = extract_data_from('./data/person.xml')
    xml_data = xml_factory.parsed_data
    liars = xml_data.findall(f'.//person[lastName="Liar"]') #use XPath
    print(f'Found: {len(liars)} persons')
    for liar in liars:
        first_name = liar.find('firstName').text
        last_name = liar.find('lastName').text
        print(f'first name: {first_name}, last name: {last_name}')
        [print(f'phone number: ({p.attrib["type"]}): ', p.text)
        for p in liar.find('phoneNumbers')]
        print()