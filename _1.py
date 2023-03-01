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
mycursor.execute("CREATE TABLE IF NOT EXISTS NEWS_storage(id INT AUTO_INCREMENT PRIMARY KEY, Content_url VARCHAR(255), Title VARCHAR(255), Image_url VARCHAR(255), Paragraph TEXT , Publish_date VARCHAR(255), Updated_date VARCHAR(255))")

def ExtractInfo(Content_url):
    print("--------------------------------------------------------------------")
    print("Content Urls-----" , Content_url)
    Link_response = requests.get(Content_url)
    Link_Soup = BeautifulSoup(Link_response.content, 'html.parser')

    #Title of the Content
    Title = Link_Soup.find('h1')
    print("Title of the Content is---",Title.text)

    #Main Body-Paragraph of Content
    Link_para=Link_Soup.find_all('p')
    Paragraph =[]
    for p in Link_para:
        Paragraph.append(p.text.strip())
    print('Full paragraph is here ----:', Paragraph)

    #Main Image of Content Only
    Image_url = set()
    url = Link_Soup.find_all('img')
    for link in url:
        if link.has_attr('src') and 'http' in link['src']:
            pass
        else:
            try:
                Image_url = 'https:' + link['src']
            except KeyError:
                pass
    print("Image url is---- ",Image_url)

    #Publish And Updated Date
    Publish_date = None
    Updated_date = None
    Link_date=Link_Soup.find_all('span',{'class':'date'})
    for span in Link_date:
        text = span.get_text()
        if 'Publish Date:' in text:
            Publish_date = text.replace('Publish Date:','').strip()
            print('Publish Date:', Publish_date)
        elif 'Updated Date:' in text:
            Updated_date = text.replace('Updated Date:','').strip()
            print('Updated Date:', Updated_date)
        else:
            Publish_date =text
            Updated_date = None
    print("==============================================================")

    sql = "INSERT INTO NEWS_storage(Content_url, Title, Image_url, Paragraph, Publish_date, Updated_date) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (Content_url, Title.text if Title else None, Image_url , '\n\n '.join(Paragraph), Publish_date, Updated_date)
    mycursor.execute(sql, val)
    mydb.commit()
    
urls = 'https://www.jagran.com/news/national-news-hindi.html?itm_medium=national&itm_source=dsktp&itm_campaign=navigation'

r = requests.get(urls)
soup = BeautifulSoup(r.content,'html.parser')

Page_urls = soup.find_all('a')
for Main_urls in Page_urls:
    if Main_urls.has_attr('href') and '/news/national-news-hindi-page' in Main_urls['href']:
        Urls = "https://www.jagran.com" + Main_urls['href']
        print("Button Urls Are --", Urls)                                            #Button Url Done
        if Urls:
            link = requests.get(Urls)
            link_soup = BeautifulSoup(link.content,'html.parser')

            Content_link = link_soup.find_all('ul',{'class':'topicList'})
            for url in Content_link:
                url = link_soup.find_all('a')
                for link in url:
                    if link.has_attr('href') and '/news/national-news-' in link['href']:
                        pass                                                            #pass the default page and button url to fetch only con url
                    elif link.has_attr('href') and '/news/national' in link['href']:
                        Content_url = "https://www.jagran.com" + link['href']              #button page has content url
                        # print("Button's content url ",Content_url)         
                        if Content_url:
                            ExtractInfo(Content_url)       #calling Info function for Extract all the details           

    elif Main_urls.has_attr('href') and '/news/national-news-hindi.html' in Main_urls['href']:
        pass                                                                         #pass the default home urls
    elif Main_urls.has_attr('href') and '/news/national' in Main_urls['href']:
        Content_url = "https://www.jagran.com" + Main_urls['href']                   #Content Url of Home Page
        # print("Content Urls --", Content_url) 
        if Content_url:
            ExtractInfo(Content_url)                #calling Info function for Extract all the details 
                                                          

        