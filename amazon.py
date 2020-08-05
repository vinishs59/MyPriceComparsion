from selectorlib import Extractor
import requests
import json
from json2html import *
from time import sleep
import streamlit as st
import pandas as pd

import streamlit_theme as stt

stt.set_theme({'primary': '#1b3388'})
st.title('My themed app')


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('Testing.yml')
amazon_ext = Extractor.from_yaml_file('search_results.yml')
#pd.set_option('display.max_colwidth',None)

def scrape(url,str):

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.in/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    if str == 'amazon':
         print("Extracting")
         return amazon_ext.extract(r.text)
    if str == 'flipkart':
         ret = e.extract(r.text)
         if (ret['Products']) is not None:
             return e.extract(r.text)
         else:
             ext =Extractor.from_yaml_file('flipkartNew.yml')
             return ext.extract(r.text)


st.sidebar.header('Price to compare')
key = ""
key = st.sidebar.text_input('Enter the product')
st.write('the selected product is', key)

if key:
    amazon_url= 'https://www.amazon.in/s?k='+str(key)
    flipkat_url = 'https://www.flipkart.com/search?q='+ str(key)

    # product_data = []
    #with open("urls.txt",'r') as urllist, open('output.jsonl','w') as outfile:
    #    for url in urllist.read().splitlines():
    #print("url is %s\n"%amazon_url)
    def make_clickable(link):
        # target _blank to open new window
        # extract clickable text to display for your link
        text = link.split('=')[1]
        return f'<a target="_blank" href="{link}">{text}</a>'

    data = scrape(amazon_url,'amazon')
    #amazon_df
    
    if data['Products'] is not None:
            #json.dump(data,outfile)
            #outfile.write("\n")s
            #infoFromJson = json.loads(data)
        #print(data)
            #print(json2html.convert(json = data))
        #f = open('helloworld.html','w',encoding='utf-8')
        f.write(json2html.convert(json = data))
            #df = pd.DataFrame.from_dict(data)
        df = pd.json_normalize(data['Products'])
        df = df.iloc[:10]
        amazonlink = "https://www.amazon.in"
        df['url'] = amazonlink+df['url'].astype(str)
        df['url'] = df['url'].apply(make_clickable)
        #df = df.to_html(escape=False)

            #df.style.set_properties(subset=['url'], **{'width': '300px'})
        #st.subheader('Amazon rates')
        #st.write(amazon_df, unsafe_allow_html=True)
            #df['url'] = df['url'].str.cat(10)
            #st.table(df)
        f.close()

    fdata = scrape(flipkat_url,'flipkart')
    fp_df = pd.DataFrame()
    if fdata['Products'] is not None:
                #f.write(json2html.convert(json = data))
        #print(fdata)
                #df = pd.DataFrame.from_dict(data)
        fp_df = pd.json_normalize(fdata['Products'])
        fp_df = fp_df.iloc[:10]
        #fp_df = fp_df.iloc[:10]
        link = "https://www.flipkart.com"
        fp_df['url'] = link+fp_df['url'].astype(str)
        fp_df['url'] = fp_df['url'].apply(make_clickable)
        #fp_df = fp_df.to_html(escape=False)

        #df.style.set_properties(subset=['url'], **{'width': '300px'})
    st.subheader('flipkart rates')
    frames= [df,fp_df]
    df_keys = pd.concat([df,fp_df], keys=['Amazon','Flipkart'])
    df_keys = df_keys.to_html(escape = False)
    st.write(df_keys, unsafe_allow_html=True)
                #st.table(data)

                #print ("%s"%json2html.convert(json = infoFromJson))            # sleep(5)
                # if data:
                #     with open('output.jsonl','w') as outfile:
                #         infoFromJson = json.loads(outfile)
                #         json2html.convert(json = infoFromJson)
