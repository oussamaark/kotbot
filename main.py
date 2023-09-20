import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from lxml import html
from random import randint
from urllib.parse import quote

# Initialize the bot
app = Client(
    "projet test",
    api_id=14699552,
    api_hash='01b99bb6fa0ae3bebad401190697318c',
    bot_token='5824511454:AAETOab3Ixmlr2R8KUn_QCvwrqgzGn4c7tE'
)


#random book message
@app.on_message(filters.command("random") & filters.private)
def random(client, m):
    m.reply("جاري المعالجة ...")
    #random number 100-1500
    j = randint(100, 1500)
    url = f'https://www.kotobati.com/download-book/{j}'
    proxy = {'http': 'http://4.175.121.88:80'}
    headers = {'User-Agent'
    :
    'Mozilla/5.0 (Linux; Android 11; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36'}
    r = requests.get(url, headers=headers, verify=False, proxies=proxy)
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    namm = soup.find('div', class_='media row')
 
    namm = str(namm)
    root = html.fromstring(namm)
    nameb = root.xpath('//h1[@class="download-book-title"]/text()')
    nameb = nameb[0]
    nameb = nameb.replace(" ", "-")
    link = f'https://www.kotobati.com/book/{nameb}'
    
    
    
    msg = get_info(link)

    dlink = get_dlink(link)
    msgg = msg[0]
    img = msg[1]
    
    button = InlineKeyboardButton(text="تحميل", callback_data=f'#{dlink}')
    keyboard = InlineKeyboardMarkup([[button]])
    app.send_photo(chat_id = m.chat.id,photo=f'{img}', caption=f'{msgg}\n id = {j}')
    m.reply_text("-#-#-#-#-#-#-#-#-#", reply_markup=keyboard)
    #############
    
# Start message
@app.on_message(filters.command("start") & filters.private)
def start(client, m):
    button1 = InlineKeyboardButton(text="البحث", callback_data="search")
    button2 = InlineKeyboardButton(text="كتاب عشوائي", callback_data="random")
    button3 = InlineKeyboardButton(text="الاقسام", callback_data="sections")

    keyboard = InlineKeyboardMarkup([[button1 , button2], [button3]])
    m.reply("مرحب بك في بوت كتباتي \n\n البوت خاص بالبحث عن الكتب وتحميلها \n\n اضغط على البحث للبحث عن مؤلف او كتاب او اقسام \n\n اضغط على كتاب عشوائي لتحميل كتاب عشوائي", reply_markup=keyboard)

# Search and download book
@app.on_message(filters.text)
def search_books(client, message):
    
    main_search(client, message)  # Call main_search with client and message as arguments

def main_search(client, message):

    results = []
    title = message.text
    url = f'https://www.kotobati.com/search/result?s={title}'
    encoded_url = quote(url, safe=':/')
    headers = {'User-Agent'
    :
    'Mozilla/5.0 (Linux; Android 11; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36'}
    r = requests.get(url, headers=headers, verify=False)
    
    soup = BeautifulSoup(r.text, 'html.parser')

    boxes = soup.find_all("div", {"class": "book-teaser"})

    for box in boxes:
        link = box.find("a", {"class": "d-inline-block"})["href"]
        title = box.find("h3", {"class": "title"}).text
        img_element = box.find("img", {"class": "img"})
        
        if img_element:
            img = img_element.get("data-src")
        else:
            img = None

        results.append({"link": link, "title": title, "img": img})

    if r.status_code != 200:
        message.reply_text("لم يتم العثور على نتائج")
    else:
        i = 0
        for result in results:
            i += 1
            name = result["title"]
            link = result["link"]
            img_url = result["img"]
            
            # Download the image
            img_url = 'https://www.kotobati.com' + img_url
            link = 'https://www.kotobati.com' + link
            
            response = requests.get(img_url, headers=headers, verify=False)
            msg = message.reply_text(f"جاري المعالجة ... ")
            #delet message reply_text
            time.sleep(1)
            msg.delete()
            titll = name 
            titll = titll.replace(" ", "-")
            img_filename = f"imgfold/{titll}.jpg"
            
            with open(img_filename, 'wb') as f:
                f.write(response.content)
            # Send the image and the book name
            with open(img_filename, 'rb') as f:
                try:
                    button = InlineKeyboardButton(text="التفاصيل", callback_data=f'dl#{titll}')
                    keyboard = InlineKeyboardMarkup([[button]])
                    message.reply_photo(photo=f, caption=name, reply_markup=keyboard)
                except:
                    pass
                
def get_dlink(link):
    url = f'{link}'
    encoded_url = quote(url, safe=':/')
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.46'}
    r = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    element = soup.find('div', class_='col-md-12')
    if element:
        element = str(element)
        tree = html.fromstring(element)
        download_link = tree.xpath('//a[@class="btn btn-icon btn-1 download"]/@href')
        if download_link:
            download_url = download_link[0]
        else:
            download_url = ""
        url = f'https://www.kotobati.com{download_url}'
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.46'}
        r = requests.get(url, headers=headers, verify=False)
        
        soup = BeautifulSoup(r.text, 'html.parser')

        dl_url = soup.find('div', class_='download-block')
        dl_url = str(dl_url)
        tree = html.fromstring(dl_url)
        dl_link = tree.xpath('//div[@class="download-block"]//div[@id="downloadProgressDynamic"]/@data-src')
        return f'/book/download/{dl_link[0]}'
    else:
        return False 
def get_info(book_link):

    url = f'{book_link}'
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.46'}
    
    r = requests.get(url , headers=headers, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    abouts = soup.find_all("div", {"class": "row py-4"})
    info_place = soup.find("div", {"class": "media-body col-md-10"})
    try:
      book_title = info_place.find("h2").text
    except:
      book_title = 'القصة غير متوفرة'
    try:
        book_author = info_place.find("p").text
    except:
        book_author = 'المؤلف غير متوفر'
    try:
        book_theme = soup.find_all('p', class_='book-p-info')[1].find('a').get_text(strip=True)
    except:
        book_theme = 'النوع غير متوفر'

    element = soup.find_all('div', class_='media-body col-md-10')
    # array to string
    element = ''.join([str(elem) for elem in element])
    

    root = html.fromstring(element)
    
    # Use XPath to extract the desired text
    try:
        page_count = root.xpath('//li[contains(@class, "nav-item")]/p[text()="الصفحات"]/following-sibling::p/span[@class="numero"]/text()')
        page_count = ''.join(page_count)
    except:
        page_count = 'غير متوفر'
    try:
        language = root.xpath('//li[@class="nav-item"]/p[text()="اللغة"]/following-sibling::p/text()')[0].strip() if root.xpath('//li[@class="nav-item"]/p[text()="اللغة"]') else ""
    except:
        language = 'غير متوفر'
    try:
        size_text = root.xpath('//li[contains(p, "الحجم")]/p/text()[normalize-space()]')[1]
        size = root.xpath('//li[@class="nav-item"]/p[text()="الحجم"]/following-sibling::p/span[@class="numero"]/text()')
    except:
        size_text = 'غير متوفر'
        size = 'غير متوفر'
    #Test get img
    element1 = soup.find_all('div', class_='image')
    element1 = ''.join([str(elem) for elem in element1])
    

    root = html.fromstring(element1)
    img1 = root.xpath('//div[@class="image"]/img/@data-src')
    img1 = ''.join(img1)
    img1 = 'https://www.kotobati.com' + img1
    response = requests.get(img1, headers=headers, verify=False)
    titll = book_title.replace(" ", "-")
    img_filename = f"imgfold/{titll}.jpg"
    with open(img_filename, 'wb') as f:
        f.write(response.content)
    with open(img_filename, 'rb') as f:
        try:
            i = 1+1
        except:
            pass


    #list to string
    file_size = ''.join(size)
    file_size = file_size + size_text
    

    titll = book_title.replace(" ", "-")
    book_img = f'imgfold/{titll}.jpg'
    msg = []
    info = f"العنوان: {book_title} \n\n المؤلف: {book_author} \n\n النوع: {book_theme} \n\n الصفحات: {page_count} \n\n اللغة: {language} \n\n الحجم: {file_size} \n\n نوع الملف: pdf \n\n "
    msg.append(info)
    msg.append(book_img)
    return msg

    

# Callback query handling
@app.on_callback_query()
def callback_query(client, query):
    if query.data == "search":
        query.message.delete()
        query.message.reply_text("ارسل اسم الكتاب")
    elif query.data == "sections":
        query.message.delete()
        topics_and_books = {
        "الأدب والرواية": ["روايات", "مجموعة قصص", "الشعر"],
        "الدراسات الإسلامية": ["العلوم الإسلامية", "التفاسير", "السيرة النبوية"],
        "الفلسفة وعلم المنطق": ["الفلسفة والمنطق"],
        "تطوير الذات": ["التنمية البشرية وتطوير الذات"],
        "السياسة": ["السياسة"],
        "البحث والدراسات": ["دراسات وبحوث"],
        "الفنون والمسرح": ["مسرحيات وفنون"],
        "كتب الأطفال": ["الأطفال"],
        "النقد الأدبي والتحليل": ["الأدب", "نصوص وخواطر"],
        "السير الذاتية والمذكرات": ["مذكرات وسير ذاتية"],
        "التاريخ والحضارات": ["التاريخ والحضارات", "سيرة الخلفاء والتابعين"],
        "ثقافة المرأة": ["ثقافة المرأة"],
        "علم النفس": ["علم النفس"],
        "التعليم": ["التعليم والتربية"],
        "العلوم والفيزياء الحديثة": ["الفيزياء والعلوم الحديثة"],
        "تعلم اللغة": ["تعلم اللغة العربية", "تعلم اللغة الإنجليزية", "تعلم اللغة الفرنسية", "تعلم اللغة الإسبانية"],
        "الاقتصاد": ["الاقتصاد"],
        "الطب والتمريض": ["الطب والتمريض", "التغذية"],
        "القانون": ["القانون"],
        "الأعشاب والطب البديل": ["الأعشاب والطب البديل"],
        "الاتصال ووسائل الإعلام": ["التواصل والإعلام"],
        "الرياضة": ["الرياضة"],
        "التصوير الفوتوغرافي": ["التصوير الفوتوغرافي"],
        "الحواسيب والبرمجة": ["الحواسيب", "البرمجة"],
        "الطهي": ["الطبخ"],
        "تفسير الأحلام": ["تفاسير الأحلام"],
        "الديانة": ["الأديان", "قصص الأنبياء", "المصاحيف"],
        "العلوم الاجتماعية": ["علم الاجتماع"]}

        # Create an empty string to store the output
        output_text = ""

        # Iterate through the dictionary and build the output string
        for topic, books in topics_and_books.items():
            output_text += f"{topic}:\n"
            for book in books:
                output_text += f"{book}\n"
            output_text += "\n"
        query.message.reply_text(f'{output_text}')
    elif query.data.startswith("dl#"):
        link = query.data.split("#", 1)[1]
        query.message.delete()

        client.answer_callback_query(query.id, 'انتضر قليلا جاري معالجة الطلب...', show_alert=True)
        slink = link
        link = f'https://www.kotobati.com/book/{link}'
        msg = get_info(link)
        dlink = get_dlink(link)
        dlink = f'https://www.kotobati.com{dlink}'
        msg = msg[0]
        
        
        client.send_photo(chat_id=query.message.chat.id, photo=f'imgfold/{slink}.jpg', caption=msg)
        app.send_document(chat_id=query.message.chat.id, document=f'{dlink}')
    elif query.data == "random":
        query.message.delete()
        query.message.reply_text("جاري المعالجة ...")
        #random number 100-1500

        j = randint(100, 3000)
        try:
            url = f'https://www.kotobati.com/download-book/{j}'
            headers = {'User-Agent'
            :
            'Mozilla/5.0 (Linux; Android 11; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36'}
            r = requests.get(url, headers=headers, verify=False)
            
            soup = BeautifulSoup(r.text, 'html.parser')
            namm = soup.find('div', class_='media row')
            namm = str(namm)
            root = html.fromstring(namm)
            nameb = root.xpath('//h1[@class="download-book-title"]/text()')
            nameb = nameb[0]
            nameb = nameb.replace(" ", "-")
            link = f'https://www.kotobati.com/book/{nameb}'
            
            
            
            msg = get_info(link)

            dlink = get_dlink(link)
            msgg = msg[0]
            img = msg[1]
            button = InlineKeyboardButton(text="تحميل", callback_data=f'#{dlink}')
            keyboard = InlineKeyboardMarkup([[button]])
            query.message.reply_photo(photo=f'{img}', caption=f'{msgg}\n id = {j}')
            query.message.reply_text("-#-#-#-#-#-#-#-#-#", reply_markup=keyboard)

            #app.send_document(chat_id=query.message.chat.id, document=f'{dlink}')
        except:
            query.message.reply_text(" حدث خطأ مااعد المحاولة\n /random")
    elif query.data.startswith("#"):
        query.message.delete()
        
        dlink = query.data.split("#", 1)[1]
        dlink = f'https://www.kotobati.com{dlink}'
        app.send_document(chat_id=query.message.chat.id, document=f'{dlink}')
        

# Run the bot
if __name__ == "__main__":
    app.run()
