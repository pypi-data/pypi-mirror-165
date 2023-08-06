def desc(data, number=None, df=None):
    import pandas as pd
    # 第一
    all_data = []
    for i in range(1, data.shape[1] + 1):
        all_data.append(len(data))

    null_n = list(data.isnull().sum())

    null_b = []
    for i in null_n:
        if i == 0:
            null_b.append('0%')
        else:
            n_b = i / len(data) * 100
            n_b = '%.2f' % n_b
            null_b.append(str(n_b) + '%')

    dfr = []
    for i in list(data):
        dfr.append(len(data[i].unique()))

    lists = [
        all_data,
        null_n,
        null_b,
        dfr,
    ]

    df1 = pd.DataFrame(data=lists, index=['数据总数', '空值个数', '空值比例', '不同值个数'],
                       columns=[list(data)])

    # 第二
    listss = list(data.describe())
    listssa = []
    for i in listss:
        mean = data[i].describe()[1]
        std = data[i].describe()[2]
        min_ = data[i].describe()[3]
        max_ = data[i].describe()[-1]
        M_3 = data[i].describe()[1] - 3 * std
        M3 = data[i].describe()[1] + 3 * std

        j = [min_, max_, mean, std, M_3, M3]
        listssa.append(j)
    df2 = pd.DataFrame(data=listssa, index=listss, columns=['MIN', 'MAX', 'Mean', 'Std', 'M-3std', 'M+3std'])

    # 第三
    listsa = []
    list_b = []
    if number == None:
        number = 20
    else:
        number
    data_na = data.fillna(0)
    for i in list(data_na):
        if len(list(set(data_na[i]))) <= number:
            list_b.append(i)
    for b in list_b:

        listda = []
        sumx = []
        lista = []
        lists = list(set(data_na[b]))
        for i in list(set(data_na[b])):
            lista.append((data_na[b] == i).sum())
        for i in lista:
            sumx.append(str("%.0f" % ((i / sum(lista)) * 100) + '%'))
        a = 0
        for x in lists:
            listda.append(str(x) + '(' + sumx[a] + ')')
            a += 1

        listsa.append(listda)
        listsa.append(lista)
    x = []
    for b in list_b:
        x.append(b)
        x.append(' ')
    df3 = pd.DataFrame(data=listsa, index=x)

    writer = pd.ExcelWriter('数据质量.xlsx')
    df1.to_excel(writer, '空值')
    df2.to_excel(writer, '数值')
    df3.to_excel(writer, '类别')
    writer.save()

    if df == 2:
        return df2
    elif df == 3:
        return df3
    else:
        return df1
