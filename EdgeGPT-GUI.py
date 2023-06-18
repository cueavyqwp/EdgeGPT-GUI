import tkinter.messagebox as tkmsg
import tkinter.scrolledtext
import tkinter as tk
import threading
import traceback
import warnings
import asyncio
import logging
import json
import time
import pip
import os

#===================================#
font = ( "Consolas" , 18 , "bold" ) # 自定义字体
cookies_path = "cookies.json"       # cookies文件位置 
chat_logs = "chat_logs"             # 聊天记录位置
logs = "logs"                       # 日志文件位置
save_logs_file = True               # 是否保存日志
show_links = True                   # 是否在GUI上显示链接
show_suggest = True                 # 是否在GUI上显示建议
#===================================#

file_name = os.path.join( str( time.strftime( "%Y-%m-%d" , time.localtime() ) ) )
logs_name = os.path.join( logs , file_name + ".log" )
chat_logs_name = os.path.join( chat_logs , file_name + ".md" )

if not os.path.exists( logs ) :
    os.mkdir( logs )
if not os.path.exists( chat_logs ) :
    os.mkdir( chat_logs )

logger = logging.getLogger( "EdgeGPT-GUI" )
logger.setLevel( logging.DEBUG )

formatter = logging.Formatter( "[%(asctime)s] [%(levelname)s] %(message)s" , "%Y-%m-%d %H:%M:%S" )

if save_logs_file :
    file_log = logging.FileHandler( logs_name , encoding = "utf-8" )
    file_log.setLevel( logging.DEBUG )
    file_log.setFormatter(formatter)
    logger.addHandler(file_log)

log = logging.StreamHandler()
log.setLevel( logging.DEBUG )
log.setFormatter(formatter)
logger.addHandler(log)

for i in range(5,0,-1) :
    try :
        import EdgeGPT
        # from EdgeGPT import EdgeGPT # https://github.com/acheong08/EdgeGPT
        import langful # https://github.com/cueavy/langful
        break
    except ModuleNotFoundError as e :
        logger.warning( "-" * 30 + "\n" + str(e) )
        logger.warning( "-" * 30 )
        pip.main( [ "install" , "-r" , "requirements.txt" ] )
        logger.info( "install finish" )
        pass
if ( i - 1 ) < 1 :
    logger.error( "Can't to import or install the module" )
    exit()

can_chat = True # 确保用户不会在Bing回答时输入内容
lang = langful.lang( change = "@" )
root = tk.Tk()
root.geometry( "1200x800" )
root.title( "EdgeGPT-GUI" )

try :
    with open( cookies_path ) as file :
        cookie = json.load(file)
    bot = EdgeGPT.Chatbot( cookies = cookie )
except json.decoder.JSONDecodeError :
    logger.error( "can't to load cookie file" )
    tkmsg.showerror( lang.get( "wrong" ) , lang.get( "can_not_to_read" ) )
    quit()
except EdgeGPT.httpx.ConnectError as e :
    tkmsg.showerror( "错误" , f":(\n{e}\n这个错误主要是因为没开代理\n若没有代理,请放弃尝试" )
    quit()

warnings.simplefilter( "ignore" , DeprecationWarning ) # 防止出现警告
with warnings.catch_warnings() :
    loop = asyncio.get_event_loop()
loop_thread = threading.Thread( target = loop.run_forever )
loop_thread.start()

the_text = the_text_old = the_chat_text = ""

with open( "format.md" , encoding = "utf-8" ) as f :
    file = f.read()
    md_texts = {}
    md_texts[ "user" ] = file.split("<!--User-->")[1][1:-1]
    md_texts[ "bing" ] = file.split("<!--Bing-->")[1][1:-1]
    md_texts[ "start" ] = file.split("<!--Time_start-->")[1][1:-1]
    md_texts[ "reset" ] = file.split("<!--Time_reset-->")[1][1:-1]
    md_texts[ "end" ] = file.split("<!--Time_end-->")[1][1:-1]

def md_text( key , value ) :
    i = md_texts[ key ].split( "<!--value-->" )
    return i[0] + value + i[1] 

def md_file() :
    return open( chat_logs_name , "a" , encoding = "utf-8" )

def log_time( type ) :
    with md_file() as file :
        Now_time = time.strftime( "%Y-%m-%d %H:%M:%S" , time.localtime() )
        file.write( md_text( type , Now_time ) )
        logger.info( f"Log time [{type}] [ {Now_time} ]" )

def reset( *args ) :
    global bot , loop , loop_thread
    if can_chat :
        logger.info( f"open new topic" )
        bot = EdgeGPT.Chatbot( cookies = cookies_path )
        loop.call_soon_threadsafe( loop.stop )
        loop = asyncio.get_event_loop()
        loop_thread = threading.Thread( target = loop.run_forever )
        loop_thread.start()
        chat_text.config( state = tk.NORMAL )
        chat_text.delete( "0.0" , tk.END )
        chat_text.config( state = tk.DISABLED )
        chat_text.see( tk.END )
        message_user()
        log_time( "reset" )
    else :
        tkmsg.showinfo( lang.get( "info" ) , lang.get( "wait" ) )

def show_count( *args ) : # 统计字数
    global the_text
    the_text = text.get( "1.0" , "end" ) [:-1]
    root.title( lang.str_replace ( f"EdgeGPT-GUI [ { lang.get( 'word' ) } 2000/{ len( the_text ) } ] " + lang.replace( "help" , [ "[ " , " ] [ " , " ]" ] ) ) )
    root.after( 1 , show_count )

def add_chat_message( message = "" , enter = True ) : # 往聊天内容里添加内容
    chat_text.config( state = tk.NORMAL )
    chat_text.insert( tk.END , message + ( "" , "\n" ) [enter] )
    chat_text.config( state = tk.DISABLED )
    chat_text.see( tk.END )

def Bing_s_message( future ) :
    global text , can_chat , the_text_old
    try :
        data = future.result()
        if not ( len( data["item"]["messages"] ) -1 ) :
            tkmsg.showerror( lang.get( "wrong" ) , lang.get( "can_not_get_message" ) )
        messages = data["item"]["messages"][1]
        message = messages["text"]
        message = message.replace( "[^" , "[" ).replace( "^]" , "]" )
        links = messages["sourceAttributions"]
        logger.info("Finish to get message")
        if len( links ) :
            link_text = ""
            for i in range( len( links ) ) :
                if links[i] :
                    link_text += f"""[{i+1}] {links[i]["seeMoreUrl"]}\n"""
                    with md_file() as file :
                        file.write( f"""[{i+1}]: {links[i]["seeMoreUrl"]}\n""" )
            link_text = link_text[:-1]
            if show_links :
                link_text = f"""\n{"-" * 30}\n{link_text}\n{"-" * 30}"""
                add_chat_message( link_text )
        elif show_links :
            add_chat_message()
        suggested_responses = data["item"]["messages"][1]["suggestedResponses"]
        with md_file() as file :
            file.write( md_text( "bing" , message ) )
        if not ( show_suggest and len( suggested_responses ) ) :
            message += "\n"
        add_chat_message( message )
        if len( suggested_responses ) :
            suggest_text = ""
            for i in suggested_responses :
                if i :
                    suggest_text += i[ "text" ] + "\n"
            suggest_text = suggest_text[:-1]
            logger.info( "-" * 30 + "\n" + suggest_text )
            logger.info( "-" * 30 )
            if show_suggest :
                suggest_text = f"""{"-" * 30}\n{suggest_text}\n{"-" * 30}\n"""
                add_chat_message( suggest_text )
        message_user()
    except :
        logger.error("Fail to get message")
        error = traceback.format_exc()[:-1]
        tkmsg.showerror( lang.get( "wrong" ) , error )
        logger.error( f"{'-' * 30}\n{error}" )
        logger.error( "-" * 30 )
        try :
            logger.debug(data)
        except :
            logger.error("Chan't save chat data")
            error = traceback.format_exc()[:-1]
            logger.error( f"{'-' * 30}\n{error}" )
            logger.error( "-" * 30 )
        text.insert( tk.END , the_text_old )
    can_chat = True

def send( *args ) :
    global the_text_old , can_chat
    if not can_chat :
        tkmsg.showinfo( lang.get( "info" ) , lang.get( "wait" ) )
    elif not the_text or "".join( the_text.split() ) == "" :
        tkmsg.showerror( lang.get( "wrong" ) , lang.get( "empty_content" ) )
    elif len( the_text ) > 2000 :
        tkmsg.showinfo( lang.get( "info" ) , lang.get( "words_too_more" ) )
    elif len( the_text ) <= 2000 and can_chat :
        can_chat = False
        with md_file() as file :
            file.write( md_text( "user" , the_text ) )
        add_chat_message( f"{the_text}" )
        if show_links :
            add_chat_message( "\nBing:" )
        else :
            add_chat_message( "\nBing:\n" )
        the_text_old = the_text
        text.delete( 0.0 , "end" )
        future = asyncio.run_coroutine_threadsafe( ask() , loop )
        future.add_done_callback( Bing_s_message )

def close() :
    root.destroy()
    loop.call_soon_threadsafe( loop.stop ) # 关闭循环
    log_time( "end" )
    logger.info( "'EdgeGPT-GUI' stop" )
    logger.info( "-" * 30 + "\n" )

def message_user() :
    add_chat_message( "User:\n" )

async def ask() :
    return await bot.ask( prompt = the_text )

paned = tk.PanedWindow( root, orient = tk.VERTICAL )
paned.pack( fill = tk.BOTH, expand = True )

chat_text = tkinter.scrolledtext.ScrolledText(
    root ,
    tabs = ( "1c" ) ,
    undo = True ,
    font = font
    )

text = tkinter.scrolledtext.ScrolledText(
    root ,
    tabs = ( "1c" ) ,
    undo = True ,
    font = font
    )

paned.add( chat_text )
paned.add( text )

text.bind( "<Shift-Return>" , send )
text.bind( "<Control-s>" , send )
text.bind( "<F9>" , send )

text.bind( "<Control-r>" , reset )
text.bind( "<Control-n>" , reset )
text.bind( "<F12>" , reset )

root.protocol( "WM_DELETE_WINDOW" , close )
root.after( 1 , show_count )

logger.info( "-" * 30 )
logger.info( "'EdgeGPT-GUI' run" )
logger.debug( f"'font' info [ {font} ]" )
logger.debug( f"'cookies' file at '{os.path.abspath( cookies_path )}'" )
logger.debug( f"'chat_logs' dir at '{os.path.abspath( chat_logs )}'" )
logger.debug( f"'logs' dir at '{os.path.abspath( logs )}'" )

log_time( "start" )
message_user()

try :
    root.mainloop()
except :
    logger.error( "The program abnormally exits" )
    error = traceback.format_exc()[:-1]
    logger.error( f"{'-' * 30}\n{error}" )
    logger.error( "-" * 30 )
    tkmsg.showerror( lang.get( "wrong" ) , error )
    close()
