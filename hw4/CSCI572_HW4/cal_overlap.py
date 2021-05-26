from urllib import request
import simplejson


def writetocsv(query,default,pagerank,overlap_num,t_path,o_path):
    if '+' in query:
        temp = query.split(sep='+')
        query = temp[0] + temp[1]
    with open(t_path, 'a') as f1:
        f1.write(query + ',default,pagerank\n')
        for i in range(len(default)):
            f1.write(str(i) + ',' + default[i] + ',' + pagerank[i] + '\n')

    with open(o_path, 'a') as f2:
        f2.write(query + ',' + str(overlap_num) + '\n')


def query_solr(query):
    first_connection = request.urlopen(
        'http://localhost:8983/solr/myexample/select?q=' + query)
    response = simplejson.load(first_connection)
    print(query + ' default ' + str(response['response']['numFound']) + " documents found.")

    i = 0
    d_urls = []
    for doc in response['response']['docs']:
        i += 1
        if 'og_url' in doc.keys():
            d_urls.append(doc['og_url'][0])

    second_connection = request.urlopen('http://localhost:8983/solr/myexample/select?q='+query+'&sort=pageRankFile+desc')
    response = simplejson.load(second_connection)
    print(query + ' pagerank ' + str(response['response']['numFound']) + " documents found.")

    i = 0
    pr_urls = []
    for doc in response['response']['docs']:
        i += 1
        if 'og_url' in doc.keys():
            pr_urls.append(doc['og_url'][0])

    overlap_num = len(list(set(d_urls).intersection(set(pr_urls))))

    return pr_urls, d_urls, overlap_num


if __name__ == '__main__':
    queries = ['Cannes', 'Congress', 'Democrats', 'Patriot+Movement', 'Republicans', 'Senate', 'Olympics+2020', 'Stock', 'Virus']
    t_path = 'table.csv'
    o_path = 'overlap.csv'

    for query in queries:
        pr_urls, d_urls, overlap_num = query_solr(query)
        writetocsv(query,d_urls,pr_urls,overlap_num,t_path,o_path)



