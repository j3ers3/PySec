def init():
    data = []

    with open('data/cms.txt') as f:
        for line in f:
            str = line.strip().split(" ")
            ls_data = {}
            if len(str) == 3:
                ls_data["url"] = str[0]
                ls_data["name"] = str[1]
                ls_data["md5"] = str[2]
                data.append(ls_data)


