d = [{'username': 'asish', 'id': 232}, {'username': 'shaji',
                                        'id': 4545}, {'username': 'thomas', 'id': 64545}]

ids = [232, 4545, 64545]


for id in ids:
    l = list(filter(lambda user: user['id'] == 4545, d))
    print(l[0])

    break
