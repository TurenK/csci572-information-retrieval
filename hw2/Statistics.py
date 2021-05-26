import pandas as pd

fetch = pd.read_csv("fetch_wsj.csv")
visit = pd.read_csv("visit_wsj.csv")
urls = pd.read_csv("urls_wsj.csv", encoding='utf-8')

# calculate fetches attempted, succeeded and failed or aborted
attempted = fetch.shape[0]
succeeded = fetch[fetch[fetch.columns[1]] < 300].shape[0]
failedOrAborted = fetch[fetch[fetch.columns[1]] >= 300].shape[0]

# Outgoing URLs
total_extracted = visit[visit.columns[2]].sum()
drop_dup_data = urls.drop_duplicates(urls.columns[0])
unique_extracted = drop_dup_data.shape[0]
unique_within = drop_dup_data[drop_dup_data[drop_dup_data.columns[1]] == "OK"].shape[0]
uinque_outside = drop_dup_data[drop_dup_data[drop_dup_data.columns[1]] == "N_OK"].shape[0]

# status dict -- use in for key in status_dict
status_dict = fetch.groupby(fetch.columns[1]).count().to_dict()
status_res = {200: '200 OK', 301: '301 Moved Permanently', 302: '302 Found', 403: '403 Forbidden',
              404: '404 Not Found', 500: '500 Internal Server Error', 503: '503 Service Unavailable'}
status_dict = status_dict[fetch.columns[0]]

# file sizes in bytes (1024)
less_1kb = visit[visit[visit.columns[1]] < 1024].shape[0]  # < 1KB
less_10kb = visit[(visit[visit.columns[1]] >= 1024) & (visit[visit.columns[1]] < 10 * 1024)].shape[0]
less_100kb = visit[(visit[visit.columns[1]] >= 10 * 1024) & (visit[visit.columns[1]] < 100 * 1024)].shape[0]
less_1mb = visit[(visit[visit.columns[1]] >= 100 * 1024) & (visit[visit.columns[1]] < 1024 * 1024)].shape[0]
greater_1mb = visit[visit[visit.columns[1]] >= 1024 * 1024].shape[0]  # >= 1MB

# content type
dict_of_ct = visit.groupby(visit.columns[3]).count().to_dict()
dict_of_ct = dict_of_ct[visit.columns[0]]  # Have to clip top 1/2 when outputting to file

# Output to file
out = "Name: Ziming Wang\n"
out += "USC ID: 8219864426\n"
out += "News site crawled: https://www.wsj.com\n"
out += "\n"
out += "Fetch Statistics\n"
out += "================\n"
out += "# fetches attempted: " + str(attempted) + "\n"
out += "# fetches succeeded: " + str(succeeded) + "\n"
out += "# fetches failed or aborted: " + str(failedOrAborted) + "\n"
out += "\n"
out += "Outgoing URLs:\n"
out += "==============\n"
out += "Total URLs extracted: " + str(total_extracted) + "\n"
out += "# unique URLs extracted: " + str(unique_extracted) + "\n"
out += "# unique URLs within News Site: " + str(unique_within) + "\n"
out += "# unique URLs outside News Site: " + str(uinque_outside) + "\n"
out += "\n"
out += "Status Codes:\n"
out += "=============\n"
for key in status_dict:
    if key in status_res:
        temp_k = status_res[key]
        out += temp_k + ": " + str(status_dict[key]) + "\n"
    else:
        out += str(key) + ": " + str(status_dict[key]) + "\n"
out += "\n"
out += "File Sizes:\n"
out += "===========\n"
out += "< 1KB: " + str(less_1kb) + "\n"
out += "1KB ~ <10KB: " + str(less_10kb) + "\n"
out += "10KB ~ <100KB: " + str(less_100kb) + "\n"
out += "100KB ~ <1MB: " + str(less_1mb) + "\n"
out += ">= 1MB: " + str(greater_1mb) + "\n"
out += "\n"
out += "Content Types:\n"
out += "==============\n"
for key in dict_of_ct:
    out += key + ": " + str(dict_of_ct[key]) + "\n"

out = out[:-1]  # Cut the last new-line

with open('CrawlReport_wsj.txt', 'w') as fp:
    fp.write(out)
