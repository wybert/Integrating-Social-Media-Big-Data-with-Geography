import pandas as pd
from pymapd import connect
from os import listdir
import glob
from os.path import isfile, join

import pyarrow as pa;import numpy as np
from datetime import datetime,date


def sjoin_process(input_path,output_path,port,start_date,end_date):

    s1 = set([item.split(".")[0] for item in listdir(input_path) if ".gz" in item ])
    heavyai_storage = ""
    s2 = set()
    for subdir in listdir(heavyai_storage):
        for filename in listdir(heavyai_storage+"/"+subdir):
            item = filename.split(".")[0]
            s2.add(item)
    #s2 =set([item.split(".")[0] for item in listdir(output_path)])
    need_process = s1 - s2
    need_process = [item+".csv.gz" for item in need_process]
    print(len(s1),len(s2),len(need_process))

    # all_files = glob.glob(path + "/*.gz")
    l_gf_ni=[]

    print("Connecting to Omnisci")
    conn=connect(user="", password="", host="localhost", port=port, dbname="") #use your port number
    print("Connected",conn)



    l_ni=[]
    conn.execute("DROP TABLE IF EXISTS geotweets;")
    conn.execute("Drop table if exists geotweets_fips;")


    for filename in need_process:

        [y,m,d,h]=[int(i) for i in filename.split(".")[0].split("_")]
        file_date = datetime(y,m,d,h)
        if not (start_date<=file_date<=end_date):
            continue
    #  break
        print(filename)
        filename = input_path + filename
        try:
            df = pd.read_csv(filename, sep='\t',lineterminator="\n", dtype='unicode',index_col=None,compression='gzip')
        except Exception as e:
            print(e,"can't read!")
            l_ni.append(filename)
            continue

        #df.drop(['geom', 'tags', 'source','place','tweet_favorites','photo_url','quoted_status_id','user_id','user_name','user_location','followers','friends','user_favorites','status','user_lang','data_source'],axis=1, inplace=True) 
        df = df.drop(['geom'], axis = 'columns')
        df.columns=['message_id','tweet_date','tweet_text','tags','tweet_lang','source','place','retweets','tweet_favorite', 'photo_url','quoted_status_id','user_id','user_name','user_location','followers','friends','user_favorites','status','user_lang','latitude','longitude','data_source','GPS','spatialerror'] 
        cols = ['message_id', 'retweets', 'tweet_favorite', 'quoted_status_id', 'user_id',
                'followers','friends', 'user_favorites','status','latitude', 'longitude',
                'spatialerror']
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

        
        df['tweet_date'] = pd.to_datetime(df['tweet_date'], errors='coerce')
        values = {'message_id':0, 'retweets':0, 'tweet_favorites':0, 'quoted_status_id':0, 'user_id':0,
                'followers':0,'friends':0, 'user_favorites':0,'status':0,'latitude':0, 'longitude':0,
                'spatialerror':0}
        df.fillna(value=values, inplace = True)
        sel_cols = ['message_id', 'tweet_date', 'tweet_text', 'tweet_lang', 'place', 'user_id','user_name','user_location','followers','friends','latitude','longitude','GPS','spatialerror']
        df = df[sel_cols]

        #print(df.head())



        conn.execute("Create table IF NOT EXISTS geotweets_fips (message_id BIGINT,tweet_date TIMESTAMP,tweet_text TEXT,tweet_lang TEXT ENCODING DICT(32),place TEXT,user_id BIGINT,user_name TEXT,user_location TEXT,followers BIGINT,friends BIGINT,latitude DOUBLE,longitude DOUBLE,GPS TEXT ENCODING DICT(32),spatialerror DOUBLE,fips TEXT, county TEXT,state TEXT);")

        conn.execute("Create table IF NOT EXISTS geotweets (message_id BIGINT,tweet_date TIMESTAMP,tweet_text TEXT,tweet_lang TEXT ENCODING DICT(32),place TEXT,user_id BIGINT,user_name TEXT,user_location TEXT,followers BIGINT,friends BIGINT,latitude DOUBLE,longitude DOUBLE,GPS TEXT ENCODING DICT(32),spatialerror DOUBLE);")

        try:
            conn.load_table("geotweets",df,create='infer',method='arrow')

        except:
            try:
                conn.execute("Create table IF NOT EXISTS geotweets (message_id BIGINT,tweet_date TIMESTAMP,tweet_text TEXT,tweet_lang TEXT ENCODING DICT(32),place TEXT,user_id BIGINT,user_name TEXT,user_location TEXT,followers BIGINT,friends BIGINT,latitude DOUBLE,longitude DOUBLE,GPS TEXT ENCODING DICT(32),spatialerror DOUBLE);") 
                conn.load_table_columnar("geotweets", df,preserve_index=False) 
        
            except Exception as e:
                print(e,"can't load geotweets!")
                
                l_ni.append(filename)
                
                continue
            #conn.execute("Drop table if exists geotweets_fips")
        try:
        #print("Inside loading geotweets_fips", filename)
            conn.execute("INSERT INTO geotweets_fips (Select a.*,b.fips,b.county,b.state from geotweets a inner join heavyai_us_counties b ON ST_Intersects(b.geom,ST_SetSRID(ST_Point(a.longitude,a.latitude),4326)));")
            #  FIXME: can't save to specific location
            sql = """COPY (SELECT * FROM geotweets_fips) TO '%s%s' WITH (delimiter = '\t', quoted = 'true', header = 'true');"""%(output_path,filename.split("/")[-1].replace('.gz',''))
            conn.execute(sql)
        #coinn.execute("Drop table if exists geotweets;")
        except Exception as e:
            print(e,"Not loaded geotweets_fips")
            l_gf_ni.append(filename)
    #  break
        conn.execute("Drop table if exists geotweets;")
        conn.execute("Drop table if exists geotweets_fips;")
        
    # conn.execute("Select count(*) from geotweets_fips;") 
        #conn.execute("Drop table if exists geotweets;")
    #print(l_gf_ni)
    #print(l_ni)
    #  break


if __name__ == "__main__":
    # year = 2012
    # print(year,"year")
    # start_date = datetime(year,1,1,0)
    # end_date = datetime(year+1,1,1,0)
    # port = 10322  
    for i in range(30):
        try:
            year = 2015
            print(year,"year")
            path = '/%d/'%year
            output_path = ''
            #import os
            #os.makedirs(output_path,exist_ok=True)
            start_date = datetime(year,3,1,0)
            end_date = datetime(year,4,1,0)
            port = 7605
            
            sjoin_process(path,output_path,port,start_date,end_date)
            print("all done!")
            break
        except Exception as e:
            print(e)
            continue

