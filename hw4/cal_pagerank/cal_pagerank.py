from bs4 import BeautifulSoup
import networkx as nx
import os
import re


def create_urlfile_fileurl(path, id_path):
    fileurl, urlfile = {}, {}
    with open(path,'r') as f:
        i = 0
        for line in f.readlines():
            if i == 0:
                i += 1
                continue
            temp = line.strip().split(sep=',')
            file, url = temp[0], temp[1]
            # url = re.sub(r'^http://|^https://|/$', '', url)
            fileurl[id_path + file] = url
            # if url in urlfile.keys():
            #     print(url)
            #     print(urlfile[url])
            #     print(file)
            urlfile[url] = id_path + file
    return fileurl, urlfile


def get_outgoing_and_create_graph(data_path, filename, graph, urlfile, id_path):
    with open(data_path + '/' + filename, 'rb') as html:
        soup = BeautifulSoup(html, features='html.parser')
        tags = soup.find_all('a')
        for tag in tags:
            link = str(tag.get('href')).strip()
            if link in urlfile.keys():
                graph.add_edge(id_path + filename, urlfile[link])


def writetofile(pagerank, path):
    with open(path, 'w') as f:
        for item in pagerank.items():
            f.write(str(item[0]) + '=' + str(item[1]) + '\n')


if __name__ == '__main__':
    mapping_path = 'URLtoHTML_nytimes_news.csv'
    data_path = 'D:/Master/CSCI572/homework/hw4/data/nytimes/nytimes'
    id_path = '/home/wzm/data/crawl_data/'
    write_path = 'external_pageRankFile'

    # pagerank = {'asdas':1e-06,'ddd':1e-06,'ccc':1e-06}
    # writetofile(pagerank,write_path)

    fileurl, urlfile = create_urlfile_fileurl(mapping_path, id_path)
    graph = nx.DiGraph()
    files = os.listdir(data_path)
    i = 0
    for file in files:
        if not os.path.isdir(file):
            get_outgoing_and_create_graph(data_path, file, graph, urlfile, id_path)
        i += 1
        print(str(i))

    pagerank_dict = nx.pagerank(graph, alpha=0.85, personalization=None, max_iter=30, tol=1.0e-06, nstart=None, weight='weight', dangling=None)
    writetofile(pagerank_dict, write_path)
    pass

