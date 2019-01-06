def mkdir(path):
    file = open(path,'w')
    file.close()

if __name__ == '__main__':
    list = ['bbc.log','donews.log','douban.log','economist.log','fortune.log','huanqiu.log','netease.log','phoenix.log','sina.log','slashdot.log','souhu.log','tencent.log','tieba.log','time.log','wired.log','xinhua.log','zhihu.log']
    for li in list:
        li = "log/" + li
        mkdir(li)