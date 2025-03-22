import os
import glob
import json
import re
path_main = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_each = os.path.join(path_main, 'BookSources', 'each')
path_booksource_info = os.path.join(path_main, 'BookSources', 'bookSource.json')
path_booksource_list = os.path.join(path_main, 'src','config','booksources_list.json')
print('[info] pythoFileBasePath: '+path_main)

bookSources = []
booksource_info = []
booksource_list = []

def jsonMerged():
    for i in glob.glob(os.path.join(path_each, '*.json')):
        print('-'*50)
        print('[info] Merging:           '+i)
        with open(i,'r',encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                data = data[0]
            jsonFileName = i.replace(path_each+'\\','')
            bookSourceName = data.get('bookSourceName')
            bookSourceName = re.search(r'【(.*?)】', bookSourceName).group(1)
            bookSourceUrl = data.get('bookSourceUrl')
            if bookSourceUrl.endswith('/'):
                bookSourceUrl = bookSourceUrl[:-1]
            print('[info] jsonFileName:      '+jsonFileName)
            print('[info] bookSourceName:    '+bookSourceName)
            print('[info] bookSourceUrl:     '+bookSourceUrl)
            booksource_info.append(data)
            booksource_list.append({'bookSourceNameCH':bookSourceName,
                                    'bookSourceJson': jsonFileName,
                                      'bookSourceUrl': bookSourceUrl})
    with open(path_booksource_info, 'w', encoding='utf-8') as file:
        json.dump(booksource_info, file, indent=4, ensure_ascii=False)
    with open(path_booksource_list, 'w', encoding='utf-8') as file:
        json.dump(booksource_list, file, indent=4, ensure_ascii=False)
    print('[info] Done!')

def jsonSplit():
    booksource_list = []
    with open(path_booksource_info, 'r', encoding='utf-8') as f:
        for data in json.load(f):
            #print(json.dumps(data, indent=4, ensure_ascii=False))
            bookSourceName = data.get('bookSourceName')
            bookSourceName = re.search(r'【(.*?)】', bookSourceName).group(1)
            bookSourceUrl = data.get('bookSourceUrl')
            if bookSourceUrl.endswith('/'):
                bookSourceUrl = bookSourceUrl[:-1]
            jsonFileName = bookSourceUrl.replace('https://','')+'.json'
            booksource_list.append({'bookSourceNameCH':bookSourceName,
                                    'bookSourceJson': jsonFileName,
                                    'bookSourceUrl': bookSourceUrl})
            print('-'*50)
            print('[info] jsonFileName:      '+jsonFileName)
            print('[info] bookSourceName:    '+bookSourceName)
            print('[info] bookSourceUrl:     '+bookSourceUrl)
            with open(path_each+'\\'+jsonFileName, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
    with open(path_booksource_list, 'w', encoding='utf-8') as file:
        json.dump(booksource_list, file, indent=4, ensure_ascii=False)
    booksource_list = []
    with open(path_booksource_list, 'r', encoding='utf-8') as f:
        for data in json.load(f):
            booksource_list.append(data.get('bookSourceJson'))
    for i in glob.glob(os.path.join(path_each, '*.json')):
        if i.split('\\')[-1] not in booksource_list:
            os.remove(i)
            print('[info] Removed----:    '+i.split('\\')[-1])
    print('[info] Done!')
if __name__ == '__main__':
    # jsonSplit()       # Split bookSource.json to each json file
    jsonMerged()        # Merge each json file to bookSource.json

