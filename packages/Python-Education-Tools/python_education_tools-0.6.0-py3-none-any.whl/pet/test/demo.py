from pet.data import load_data

print(load_data.load_data('tyjhzz.txt'))

df1 = load_data.load_data('ip_address.xlsx')
'''

输入：st.xls -某高校研究生初试成绩。返回：dataframe
输入：ip_address.xlsx  -ip地址分类。返回：dataframe
输入：subway.xlsx  -上海地铁线路数据。返回：dataframe
输入：ddj.txt -道德经文本。返回：字符串。
输入：tyjhzz.txt-《太乙金华宗旨》。返回：字符串。

'''

print(df1)

dffs = load_data.generate_sr(rows=100)
'''
生成一个Series对象，对象内数据条数默认40条，可任意设置。
'''
dfff = load_data.generate_df(rows=200)
'''
生成一个dataframe对象，对象内数据条数默认40条，可任意设置。shape是（n，13），n为数据条数
'''
print(dfff.shape)

print(load_data.votes) #投票文本数据
print(load_data.cookies ) #某cookies数据