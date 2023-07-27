from json import dump


with open('draft_idioms.txt', 'r') as file:
    lines = file.readlines()
    idioms = {}

    for line in lines:
        idiom_en, idiom_ru = line.strip().replace('"', '').replace('-', '****', 1).lower().split(' **** ')
        if idiom_en not in idioms:
            idioms[idiom_en] = idiom_ru

    with open('idioms.json', 'w') as file:
        dump(idioms, file, indent=4, ensure_ascii=False)
