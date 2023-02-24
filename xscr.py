import requests
from bs4 import BeautifulSoup
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Scrapping"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS news_storage(id INT AUTO_INCREMENT PRIMARY KEY, con_url VARCHAR(255), Heading VARCHAR(255), image_link TEXT, paragraph TEXT , publish_date VARCHAR(255), updated_date VARCHAR(255))")


urls = 'https://www.jagran.com/news/national-news-hindi.html?itm_medium=national&itm_source=dsktp&itm_campaign=navigation'

r = requests.get(urls)
soup = BeautifulSoup(r.content,'html.parser')

i=1
all_links = soup.find_all('div',{'class':'pagination border0'})
for links in all_links:
    links = soup.find_all('a')
    for bt_url in links:
        # if page_url.has_attr('href') 
        
        if bt_url.has_attr('href') and '/news/national-news-hindi-page' in bt_url['href']:    # Button url links 
            page_url =  "https://www.jagran.com" + bt_url['href']
            print("Buttton linked page content ------------------------------------------------------------")
            # print(page_url)
            if page_url:
                print("Paginated Button Page Url:  ",page_url)
                print("----------------------------")
                url = requests.get(page_url)
                page_soup = BeautifulSoup(url.content,'html.parser')

                content_link = page_soup.find_all('article',{'class':'topicBox'})
                for link in content_link:
                    print("Content url")

                    link = page_soup.find_all('a')
                    for url in link:
                        if url.has_attr('href') and '/news/national-news-hindi' in url['href']:
                            pass
                        elif url.has_attr('href') and '/news/national' in url['href']:  # button has content url link only  
                            con_url = "https://www.jagran.com" + url['href']
                            # print(con_url)
                            if con_url:         # now extracting the content from the content url link
                                print(" Content Url:  ",con_url)
                                print("------------------------------------------------------------------------------------------------------")
                                link_resp=requests.get(con_url)
                                link_soup=BeautifulSoup(link_resp.content,'html.parser')

                                # Heading of the content
                                head = None
                                title=link_soup.find_all('div',{'class':'articleHd'})
                                for head in title:
                                    head=link_soup.find('h1')
                                    print("Heading -----",head.text)
                                    
                                
                                # paragraph of the content
                                link_parag=link_soup.find_all('p')
                                paragraph =[]
                                for p in link_parag:
                                    paragraph.append(p.text.strip())
                                print('----Full paragraph is here :', paragraph)  #full paragraph of the content
                                

                                #image link of the content
                                link_image = link_soup.find('figure',{'class':'bodySummery'})
                                image_link = []
                                for url in link_image:
                                    url = link_soup.find_all('img')
                                    for image_url in url:
                                        try:
                                            # print("Content Image url --- ",image_url['src'])
                                            image_link.append(image_url['src'])
                                        except KeyError:
                                            pass
                                print("Image url ==",image_link)


                                #Publish date & update date
                                publish_date = None
                                updated_date = None
                                link_date=link_soup.find_all('span',{'class':'date'})
                                for span in link_date:
                                    text = span.get_text()
                                    if 'Publish Date:' in text:
                                        publish_date = text.replace('Publish Date:','').strip()
                                        print('Publish Date:', publish_date)
                                    elif 'Updated Date:' in text:
                                        updated_date = text.replace('Updated Date:','').strip()
                                        print('Updated Date:', updated_date)
                                    else:
                                        publish_date =text
                                        updated_date = None
                                print("=====================================================================================================")

                                sql = "INSERT INTO news_storage(con_url, Heading, image_link, paragraph, publish_date, updated_date) VALUES (%s, %s, %s, %s, %s, %s)"
                                val = (con_url, head.text if head else None, '\n\n '.join(image_link)  , '\n\n '.join(paragraph), publish_date, updated_date)
                                mycursor.execute(sql, val)
                                mydb.commit()
                                print("the " , i ," th data is inserted------")
                                i=i+1


        #by default page 1 (Home page contents.......)
        elif bt_url.has_attr('href') and '/news/national-' in bt_url['href']:   # bydefault page1 url links
            print("Page 1 -----------------------------------------")
            con_url = "https://www.jagran.com" + bt_url['href']
            print("by default page 1 content =------------------------------------------")
            print("Page 1 content")
            if con_url:         # now extracting the content from the content url link
                print(" Content Url:  ",con_url)
                print("------------------------------------------------------------------------------------------------------")
                link_resp=requests.get(con_url)
                link_soup=BeautifulSoup(link_resp.content,'html.parser')

                # Heading of the content
                head = None
                title=link_soup.find_all('div',{'class':'articleHd'})
                for head in title:
                    head=link_soup.find('h1')
                    print("Heading -----",head.text)
                    # Heading=head.text.strip()
            

                                
                # paragraph of the content
                link_parag=link_soup.find_all('p')
                paragraph =[]
                for p in link_parag:
                    # print("linked Paragraph :  ", p.text)
                    paragraph.append(p.text.strip())
                print('----Full paragraph is here :', paragraph)  #full paragraph of the content
                                
                # import ipdb;ipdb.set_trace()
                # image link of the content
                link_image = link_soup.find_all('figure',{'class':'bodySummery'})
                image_link = []
                for link in link_image:
                    link = link_soup.find_all('img')
                    for image_url in link:
                        try:
                        # print("Content Image url --- ",image_url['src'])
                            image_link.append(image_url['src'])
                        except KeyError:
                            pass
                print("Image url ==",image_link)
                # image_link = link_soup.find_all('img')
                # print(image_link['src'])
                

                #Publish date & update date
                publish_date = None
                updated_date = None
                link_date=link_soup.find_all('span',{'class':'date'})
                for span in link_date:
                    text = span.get_text()
                    if 'Publish Date:' in text:
                        publish_date = text.replace('Publish Date:','').strip()
                        print('Publish Date:', publish_date)
                    elif 'Updated Date:' in text:
                        updated_date = text.replace('Updated Date:','').strip()
                        print('Updated Date:', updated_date)
                    else:
                        publish_date =text
                        updated_date = None
                print("=====================================================================================================")
                # import ipdb;ipdb.set_trace()
                sql = "INSERT INTO news_storage(con_url, Heading, image_link, paragraph, publish_date, updated_date) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (con_url, head.text if head else None, '\n\n '.join(image_link)  , '\n\n '.join(paragraph), publish_date, updated_date)
                mycursor.execute(sql, val)
                mydb.commit()
                print("the ", i ," th data is inserted------")
                i=i+1

        

print("Data Inserted Successfullyyyy.................. Value of data is ", i)    

        