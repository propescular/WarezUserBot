# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

# Turhan UserBot - Yusuf Usta


""" Diğer kategorilere uymayan fazlalık komutların yer aldığı modül. """

import os
import time
import asyncio
import shutil
from bs4 import BeautifulSoup
import re
from time import sleep
from html import unescape
from re import findall
from selenium import webdriver
from urllib.parse import quote_plus
from urllib.error import HTTPError

from selenium.webdriver.chrome.options import Options
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError
from urbandict import define
from requests import get
from search_engine_parser import GoogleSearch
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from gtts.lang import tts_langs
from emoji import get_emoji_regexp
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from asyncio import sleep
from userbot import CMD_HELP, BOTLOG, BOTLOG_CHATID, YOUTUBE_API_KEY, CHROME_DRIVER, GOOGLE_CHROME_BIN
from userbot.events import register
from telethon.tl.types import DocumentAttributeAudio
from userbot.modules.upload_download import progress
from userbot.google_images_download import googleimagesdownload

CARBONLANG = "auto"
TTS_LANG = "tr"
TRT_LANG = "tr"



import subprocess

import asyncio
import time
from userbot.events import register
import glob
import os

@register(outgoing=True, pattern="^.song(?: |$)(.*)")
async def port_song(event):
    if event.fwd_from:
        return
    
    cmd = event.pattern_match.group(1)
    if len(cmd) < 1:
        await event.edit("`Kullanım: .song şarkı ismi/youtube url/spotify url`") 

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
        
    await event.edit("`Şarkı aranıyor ve indiriliyor lütfen bekleyin!`")  
    dosya = os.getcwd() 
    os.system(f"spotdl --song {cmd} -f {dosya}")
    await event.edit("`İndirme işlemi başarılı lütfen bekleyiniz.`")    

    l = glob.glob("*.mp3")
    if l[0]:
        await event.edit("Şarkı yükleniyor!")
        await event.client.send_file(
            event.chat_id,
            l[0],
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id
        )
        await event.delete()
    else:
        await event.edit("`Aradığınız şarkı bulunamadı! Üzgünüm.`")   
        return 
    os.system("rm -rf *.mp3")
    subprocess.check_output("rm -rf *.mp3",shell=True)


@register(outgoing=True, pattern="^.ceviri")
async def ceviri(e):
    # http://www.tamga.org/2016/01/web-tabanl-gokturkce-cevirici-e.html #
    await e.edit("`Çeviriliyor...`")
    textx = await e.get_reply_message()
    pcode = e.text
    if pcode[8:]:
        pcode = str(pcode[8:])
    elif textx:
        pcode = str(textx.message)  # Girilen metin, modüle aktarılıyor.
    code = quote_plus(pcode)  # Çözülmüş url'ye dönüştürülüyor.
    url = "http://www.tamga.org/2016/01/web-tabanl-gokturkce-cevirici-e.html"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER,
                              options=chrome_options)
    driver.get(url)
    Latin = driver.find_element_by_name("Latin_Metin").send_keys(pcode)
    Turk = driver.find_element_by_name("Göktürk_Metin").get_attribute("value")
    e.edit(Turk)


@register(outgoing=True, pattern="^.img (.*)")
async def img_sampler(event):
    """ .img komutu Google'da resim araması yapar. """
    await event.edit("İşleniyor...")
    query = event.pattern_match.group(1)
    lim = findall(r"lim=\d+", query)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 5
    response = googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory"
    }

    # passing the arguments to the function
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst)
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()


@register(outgoing=True, pattern="^.currency (.*)")
async def moni(event):
    input_str = event.pattern_match.group(1)
    input_sgra = input_str.split(" ")
    if len(input_sgra) == 3:
        try:
            number = float(input_sgra[0])
            currency_from = input_sgra[1].upper()
            currency_to = input_sgra[2].upper()
            request_url = "https://api.exchangeratesapi.io/latest?base={}".format(
                currency_from)
            current_response = get(request_url).json()
            if currency_to in current_response["rates"]:
                current_rate = float(current_response["rates"][currency_to])
                rebmun = round(number * current_rate, 2)
                await event.edit("{} {} = {} {}".format(
                    number, currency_from, rebmun, currency_to))
            else:
                await event.edit(
                    "`Yazdığın şey uzaylıların kullandığı bir para birimine benziyor, bu yüzden dönüştüremiyorum.`"
                )
        except Exception as e:
            await event.edit(str(e))
    else:
        await event.edit("`Sözdizimi hatası.`")
        return


@register(outgoing=True, pattern=r"^.google (.*)")
async def gsearch(q_event):
    """ .google komutu ile basit Google aramaları gerçekleştirilebilir """
    match = q_event.pattern_match.group(1)
    page = findall(r"page=\d+", match)
    try:
        page = page[0]
        page = page.replace("page=", "")
        match = match.replace("page=" + page[0], "")
    except IndexError:
        page = 1
    search_args = (str(match), int(page))
    gsearch = GoogleSearch()
    gresults = await gsearch.async_search(*search_args)
    msg = ""
    for i in range(10):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await q_event.edit("**Arama Sorgusu:**\n`" + match + "`\n\n**Sonuçlar:**\n" +
                       msg,
                       link_preview=False)

    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            match + "`sözcüğü başarıyla Google'da aratıldı!`",
        )


@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """ .wiki komutu Vikipedi üzerinden bilgi çeker. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Belirsiz bir sayfa bulundu.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Aradığınız sayfa bulunamadı.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open("wiki.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "wiki.txt",
            reply_to=wiki_q.id,
            caption="`Sonuç çok uzun, dosya yoluyla gönderiliyor...`",
        )
        if os.path.exists("wiki.txt"):
            os.remove("wiki.txt")
        return
    await wiki_q.edit("**Arama:**\n`" + match + "`\n\n**Sonuç:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"{match}` teriminin Wikipedia sorgusu başarıyla gerçekleştirildi!`")


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """ .tts komutu ile Google'ın metinden yazıya dönüştürme servisi kullanılabilir. """
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit(
            "`Yazıdan sese çevirmek için bir metin gir.`")
        return

    try:
        gTTS(message, lang=TTS_LANG)
    except AssertionError:
        await query.edit(
            'Metin boş.\n'
            'Ön işleme, tokenizasyon ve temizlikten sonra konuşacak hiçbir şey kalmadı.'
        )
        return
    except ValueError:
        await query.edit('Bu dil henüz desteklenmiyor.')
        return
    except RuntimeError:
        await query.edit('Dilin sözlüğünü görüntülemede bir hata gerçekleşti.')
        return
    tts = gTTS(message, lang=TTS_LANG)
    tts.save("h.mp3")
    with open("h.mp3", "rb") as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(message, lang=TTS_LANG)
        tts.save("h.mp3")
    with open("h.mp3", "r"):
        await query.client.send_file(query.chat_id, "h.mp3", voice_note=True)
        os.remove("h.mp3")
        if BOTLOG:
            await query.client.send_message(
                BOTLOG_CHATID, "Metin başarıyla sese dönüştürüldü!")
        await query.delete()



@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]*)")
async def translateme(trans):
    """ .trt komutu verilen metni Google Çeviri kullanarak çevirir. """
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Bana çevirilecek bir metin wer!`")
        return

    try:
        reply_text = translator.translate(deEmojify(message), dest=TRT_LANG)
    except ValueError:
        await trans.edit("Ayarlanan hedef dil geçersiz.")
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f"Şu dilden:**{source_lan.title()}**\nŞu dile:**{transl_lan.title()}:**\n\n{reply_text.text}"

    await trans.edit(reply_text)
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Biraz {source_lan.title()} kelime az önce {transl_lan.title()} diline çevirildi.",
        )


@register(pattern=".lang (trt|tts) (.*)", outgoing=True)
async def lang(value):
    """ .lang komutu birkaç modül için varsayılan dili değiştirir. """
    util = value.pattern_match.group(1).lower()
    if util == "trt":
        scraper = "Translator"
        global TRT_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in LANGUAGES:
            TRT_LANG = arg
            LANG = LANGUAGES[arg]
        else:
            await value.edit(
                f"`Geçersiz dil kodu!`\n`Geçerli dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    elif util == "tts":
        scraper = "Yazıdan Sese"
        global TTS_LANG
        arg = value.pattern_match.group(2).lower()
        if arg in tts_langs():
            TTS_LANG = arg
            LANG = tts_langs()[arg]
        else:
            await value.edit(
                f"`Geçersiz dil kodu!`\n`Geçerli dil kodları`:\n\n`{LANGUAGES}`"
            )
            return
    await value.edit(f"`{scraper} modülü için varsayılan dil {LANG.title()} diline çevirildi.`")
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID,
            f"`{scraper} modülü için varsayılan dil {LANG.title()} diline çevirildi.`")


@register(outgoing=True, pattern="^.yt (.*)")
async def yt_search(video_q):
    """ .yt komutu YouTube üzerinde arama yapar. """
    query = video_q.pattern_match.group(1)
    result = ''

    if not YOUTUBE_API_KEY:
        await video_q.edit(
            "`Hata: YouTube API anahtarı tanımlanmamış!`"
        )
        return

    await video_q.edit("```İşleniyor...```")

    full_response = await youtube_search(query)
    videos_json = full_response[1]

    for video in videos_json:
        title = f"{unescape(video['snippet']['title'])}"
        link = f"https://youtu.be/{video['id']['videoId']}"
        result += f"{title}\n{link}\n\n"

    reply_text = f"**Arama Sorgusu:**\n`{query}`\n\n**Sonuçlar:**\n\n{result}"

    await video_q.edit(reply_text)


async def youtube_search(query,
                         order="relevance",
                         token=None,
                         location=None,
                         location_radius=None):
    """ Bir YouTube araması yap. """
    youtube = build('youtube',
                    'v3',
                    developerKey=YOUTUBE_API_KEY,
                    cache_discovery=False)
    search_response = youtube.search().list(
        q=query,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=10,
        location=location,
        locationRadius=location_radius).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return (nexttok, videos)
    except HttpError:
        nexttok = "last_page"
        return (nexttok, videos)
    except KeyError:
        nexttok = "API anahtarı hatası, lütfen yeniden dene."
        return (nexttok, videos)


@register(outgoing=True, pattern=r".rip(audio|video) (.*)")
async def download_video(v_url):
    """ .rip komutu ile YouTube ve birkaç farklı siteden medya çekebilirsin. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    await v_url.edit("`İndirmeye hazırlanıyor...`")

    if type == "audio":
        opts = {
            'format':
            'bestaudio',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'writethumbnail':
            True,
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl':
            '%(id)s.mp3',
            'quiet':
            True,
            'logtostderr':
            False
        }
        video = False
        song = True

    elif type == "video":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True

    try:
        await v_url.edit("`Veri çekiliyor, lütfen bekleyin...`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`İndirilecek içerik fazla kısa.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Maalesef coğrafi kısıtlamalar sebebiyle bu videoyla işlem yapamazsın.`")
        return
    except MaxDownloadsReached:
        await v_url.edit("`Maksimum indirme limitini aştın.`")
        return
    except PostProcessingError:
        await v_url.edit("`İstek işlenirken bir hata oluştu.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Medya belirtilen dosya formatında mevcut değil.`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`Bilgi çıkarılırken bir hata gerçekleşti.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Şarkı yüklenmeye hazırlanıyor:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(rip_data['duration']),
                                       title=str(rip_data['title']),
                                       performer=str(rip_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Karşıya yükleniyor...",
                         f"{rip_data['title']}.mp3")))
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"`Şarkı yüklenmeye hazırlanıyor:`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Karşıya yükleniyor...",
                         f"{rip_data['title']}.mp4")))
        os.remove(f"{rip_data['id']}.mp4")
        await v_url.delete()


def deEmojify(inputString):
    """ Emojileri ve diğer güvenli olmayan karakterleri metinden kaldırır. """
    return get_emoji_regexp().sub(u'', inputString)


CMD_HELP.update({
    'img':
    '.img <kelime>\
        \nKullanım: Google üzerinde hızlı bir resim araması yapar ve ilk 5 resmi gösterir.'
})
CMD_HELP.update({
    'currency':
    '.currency <miktar> <dönüştürülecek birim> <dönüşecek birim>\
        \nKullanım: Yusufun Türk Lirası Botu gibi, ama boş kaldığında kızlara yazmıyor.'
})

CMD_HELP.update({
    'carbon':
    '.carbon <metin>\
        \nKullanım: carbon.now.sh sitesini kullanarak yazdıklarının aşşşşşşırı şekil görünmesini sağlar.\n.crblang <dil> komutuyla varsayılan dilini ayarlayabilirsin.'
})
CMD_HELP.update(
    {'google': '.google <kelime>\
        \nKullanım: Hızlı bir Google araması yapar.'})
CMD_HELP.update(
    {'wiki': '.wiki <terim>\
        \nKullanım: Bir Vikipedi araması gerçekleştirir.'})
CMD_HELP.update(
    {'ud': '.ud <terim>\
        \nKullanım: Urban Dictionary araması yapmanın kolay yolu?'})
CMD_HELP.update({
    'tts':
    '.tts <metin>\
        \nKullanım: Metni sese dönüştürür.\n.lang tts komutuyla varsayılan dili ayarlayabilirsin. (Türkçe ayarlı geliyor merak etme.)'
})
CMD_HELP.update({
    'trt':
    '.trt <metin>\
        \nKullanım: Basit bir çeviri modülü.\n.lang trt komutuyla varsayılan dili ayarlayabilirsin. (Türkçe ayarlı geliyor merak etme.)'
})
CMD_HELP.update({'yt': '.yt <metin>\
        \nKullanım: YouTube üzerinde bir arama yapar.'})
CMD_HELP.update({'song': 
    '.song <youtube/spotify/şarkı>\
        \nKullanım: Şarkı indirir.\
    .songpl <spotify playlist url>\
        \nKullanım: Spotify playlist indirir.'})

CMD_HELP.update(
    {"imdb": ".imdb <film>\nKullanım: Film hakkında bilgi verir."})
CMD_HELP.update({
    'rip':
    '.ripaudio <bağlantı> veya .ripvideo <bağlantı>\
        \nKullanım: YouTube üzerinden (veya [başka sitelerden](https://ytdl-org.github.io/youtube-dl/supportedsites.html)) video veya ses indirir.'
})
