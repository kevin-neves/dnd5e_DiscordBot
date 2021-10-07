import requests
import json

''' Version 1.0.0
This is the first version of the API requests functions.
In order for this to work, you need to install the requests and json packages.
'''

''' Setup some usesful variables '''
api = "https://www.dnd5eapi.co/api"
bmab = 'https://www.buymeacoffee.com/kevinneves'

spell_pop_list = ['Index', 'School index', 'School name', 'School url', 'Url', 'Dc dc_type url']
equipment_pop_list = ['Index', 'Equipment_category index', 'Equipment_category url', 
                    'Damage damage_type index', 'Damage damage_type url', 'Url', 
                    'Equipment_category name', 'Cost quantity', 'Cost unit']
'''End'''

def make_request(parameter, mid_point): # mid_point example '/equipment-categories/'
    index = format_index(parameter)  if type(parameter) == str else parameter
    r = requests.get(f"{api}{mid_point}{index}")
    return json.loads(r.text)

def createList(results, first_key_word = 'results', second_key_word = 'name'):
    return list(map(lambda data: data[second_key_word], results[first_key_word]))

def get_list_of(parameter):
    results = make_request(parameter, '/')
    list_data = list(set(createList(results)))
    return format_info_to_discord_chat(list_data)


def get_equipment_list(categorie):
    # Choose between weapon, armor or adventuring-gear
    results = make_request(categorie, '/equipment-categories/')
    list_data = createList(results, 'equipment')
    return format_info_to_discord_chat(list_data)


def get_spell_list(lvl):  # Need the level of the spell (0-9)
    results = make_request(lvl, '/spells?level=')
    list_data = createList(results)
    return(format_info_to_discord_chat(list_data))


def get_monsters_list(nd):  # Add exceptions
    results = make_request(nd, '/monsters?challenge_rating=')
    list_data = createList(results)
    return(format_info_to_discord_chat(list_data))


def get_start_equipment(_class):  # Need some improvments
    r = requests.get(f"{api}/classes/{_class}/starting-equipment")
    list_ = json.loads(r.text)
    print(list_)


'''
def get_rules_sections_list(): 
''' 

def get_spell_info(name):
    info = json_to_dict(make_request(name, '/spells/'))
    
    pop_list(info, spell_pop_list)

    info['Classes'] = createList(info, 'Classes', 'name')
    info['Subclasses'] = createList(info, 'Subclasses', 'name')
    info = format_items_to_dict(info)
    pop_dict(info)
    return format_info_to_discord_chat(info)


def get_feature_info(name):
    index = format_index(name)
    if index == 'berserker-axe':
        return None
    # r = requests.get(f"{api}/features/{index}")
    # inf = json.loads(r.text)

    results = make_request(name, '/features/')
    info = {
        'Name': results['name'],
        'Index': results['index'],
        'Description': remove_all(str(results['desc'])),
        'Classes': remove_all(str(results['class']['name']))
    }
    if 'subclass' in results and results['subclass'] != []:
        info['Subclass'] = remove_all(str(results['subclass']['name']))
    if 'prerequisites' in results and results['prerequisites'] != []:
        info['Prerequisites'] = remove_all(str([x['prerequisites'] for x in
                                                results['prerequisites']]))
    return(info)


def get_index_of(parameter):
    results = make_request(parameter, '/')
    list_data = createList(results, second_key_word='index')
    return list_data


def get_equipment_info(name):
    # Format the index
    results = make_request(name, '/equipment/')
    if results == {'error': 'Not found'}: results = make_request(name, '/magic-items/')
    info = json_to_dict(results)
    try:
        info['Cost'] = str(info['Cost quantity']) + ' ' + info['Cost unit']
    except:
        pass
    
    pop_list(info, equipment_pop_list)
    
    try:
        info['Properties'] = [x['name'] for x in info['Properties']]
    except:
        pass
    info = format_items_to_dict(info)
    pop_dict(info)
    return format_info_to_discord_chat(info)


'''     ----- General useful functions -----     '''

# Remove empty dicts in data
def pop_dict(info):
    pop_list = []
    for i in info:
        if type(info[i]) == dict:
            pop_list.append(i)
        if info[i] == '':
            pop_list.append(i)
    for i in pop_list:
        info.pop(i, None)


def pop_list(data, list_names):
    for i in list_names:
        try:
            data.pop(i)
        except:
            pass

# Remove special caracters when needed
def remove_all(str_):
    chars = '][}\'{"'
    for i in chars:
        str_ = str_.replace(i, '')
    return str_

# 
def format_items_to_dict(dict_):
    for i in dict_.keys():
        if type(dict_[i]) != dict:
            dict_[i] = str(dict_[i])
        try:
            dict_[i] = remove_all(dict_[i])
        except:
            pass
    return dict_


def format_index(str_):
    str_ = str_.lower().strip()
    chars = ' _/'
    for i in chars:
        str_ = str_.replace(i, '-')
    chars2 = '’\',)('
    for i in chars2:
        str_ = str_.replace(i, '')
    str_.replace(' +1, +2, or +3', '')
    return str_


# Important functions!!!
def format_info_to_discord_chat(info):
    msg = str()
    if type(info) is dict:
        for i in info:
            msg = str(msg + '\n' + f'{i}: {info[i]}')
    elif type(info) is list:
        for i in info:
            msg = str(msg + '\n' + i)
    return msg


def json_to_dict(json):
    d = {}
    for i in json:
        if type(json[i]) is dict:
            for x in json[i]:
                if type(json[i][x]) is dict:
                    for n in json[i][x]:
                        d[(i + ' ' + x + ' ' + n).capitalize()] = json[i][x][n]
                else:
                    d[(i + ' ' + x).capitalize()] = json[i][x]
        else:
            d[i.capitalize()] = json[i]
    return d



def main():
    # armors = get_equipment_list('armor')
    # for i in armors:
    #     print(get_equipment_info(i))

    #print(get_equipment_info('Chain Mail'))
    #print(get_spell_info('magic circle'))
    print(get_list_of('Features'))
    #print(get_equipment_list('armor'))
    #print(get_feature_info('Hide in Plain Sight'))
    

if __name__ == '__main__':
    main()