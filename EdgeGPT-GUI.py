import tkinter.messagebox as tkmsg
import tkinter.scrolledtext
import tkinter as tk
import threading
import traceback
import warnings
import logging
import json
import time
import pip
import os

#==================================#
font = ( "Consolas" , 18 , "bold" )
cookies = "cookies.json"
chat_logs = "chat_logs"
logs = "logs"
#==================================#

file_name = os.path.join( str( time.strftime( "%Y-%m-%d" , time.localtime() ) ) )
logs_name = os.path.join( logs , file_name + ".log" )
chat_logs_name = os.path.join( chat_logs , file_name + ".md" )

logger = logging.getLogger( "EdgeGPT-GUI" )
logger.setLevel( logging.DEBUG )

formatter = logging.Formatter( "[%(asctime)s] [%(levelname)s] %(message)s" , "%Y-%m-%d %H:%M:%S" )

file_log = logging.FileHandler( logs_name )
file_log.setLevel( logging.DEBUG )
file_log.setFormatter(formatter)
logger.addHandler(file_log)

log = logging.StreamHandler()
log.setLevel( logging.DEBUG )
log.setFormatter(formatter)
logger.addHandler(log)

while 1 :
    try:
        import EdgeGPT #https://github.com/acheong08/EdgeGPT
        import langful
        break
    except:
        logger.warning( "module not find" )
        logger.info( "install 'langful'" )
        pip.main( [ "install" , "langful" ] )
        logger.info( "install 'EdgeGPT'" )
        pip.main( [ "install" , "EdgeGPT" ] )
        logger.info( "install finish" )

if not os.path.exists( logs ) :
    os.mkdir( logs )
if not os.path.exists( chat_logs ) :
    os.mkdir( chat_logs )

can_chat = True #确保用户不会在Bing回答时输入内容
lang = langful.lang( change = "@" )
root = tk.Tk()
root.geometry( "1200x800" )
root.title( "EdgeGPT-GUI" )

try :
    bot = EdgeGPT.Chatbot( cookie_path = cookies )
except json.decoder.JSONDecodeError :
    logger.error( "can't to load cookie file" )
    tkmsg.showerror( lang.get( "wrong" ) , lang.get( "can_not_to_read" ) )
    quit()

warnings.simplefilter( "ignore" , DeprecationWarning ) # 防止出现警告
with warnings.catch_warnings() :
    loop = EdgeGPT.asyncio.get_event_loop()
loop_thread = threading.Thread( target = loop.run_forever )
loop_thread.start()

the_text = the_text_old = the_chat_text = ""

with open( "format.md" , encoding = "utf-8" ) as f :
    file = f.read()
    md_texts = {}
    md_texts[ "user" ] = file.split("<!--User-->")[1][1:-1]
    md_texts[ "bing" ] = file.split("<!--Bing-->")[1][1:-1]
    md_texts[ "time" ] = file.split("<!--Time-->")[1][1:-1]

def md_text( key , value ) :
    i = md_texts[ key ].split( "<!--value-->" )
    return i[0] + value + i[1] 

def log_time() :
    with open( chat_logs_name , "a" , encoding = "utf-8" ) as File :
        Now_time = time.strftime( "%Y-%m-%d %H:%M:%S" , time.localtime() )
        File.write( md_text( "time" , Now_time ) )
        logger.info( f"Log time [ {Now_time} ]" )

def reset( *args ) :
    global bot , loop , loop_thread
    if can_chat :
        logger.info( f"open new topic" )
        bot = EdgeGPT.Chatbot( cookie_path = cookies )
        loop.call_soon_threadsafe( loop.stop )
        loop = EdgeGPT.asyncio.get_event_loop()
        loop_thread = threading.Thread( target = loop.run_forever )
        loop_thread.start()
        add_chat_message( lang.replace( "new_topic" , [ f"{ '=' * 60 }\n" , f"\n{ '=' * 60 }\n" ] ) )
        message_user()
        log_time()
    else :
        tkmsg.showinfo( lang.get( "info" ) , lang.get( "wait" ) )

def show_count( *args ): #统计字数
    global the_text
    the_text = text.get( "1.0" , "end" ) [:-1]
    root.title( lang.str_replace ( f"EdgeGPT-GUI [ { lang.get( 'word' ) } 2000/{ len( the_text ) } ] " + lang.replace( "help" , [ "[ " , " ] [ " , " ]" ] ) ) )
    root.after( 1 , show_count )

def add_chat_message( message , enter = True ): #往聊天内容里添加内容
    chat_text.config( state = tk.NORMAL )
    chat_text.insert( tk.END , message + ( "" , "\n" ) [enter] )
    chat_text.config( state = tk.DISABLED )
    chat_text.see( tk.END )

def Bing_s_message( future ):
    global text , can_chat , the_text_old
    try :
        message = future.result() ["item"] ["messages"] [1] ["adaptiveCards"] [0] ["body"] [0] ["text"]
        with open( chat_logs_name , "a" , encoding = "utf-8" ) as File :
            File.write( md_text( "bing" , message ) )
        add_chat_message( f"{message}" )
        message_user()
    except Exception :
        traceback.print_exc()
        tkmsg.showerror( lang.get( "wrong" ) , lang.get( "some_error" ) )
        text.insert( tk.END , the_text_old )
    can_chat = True

def send( *args ):
    global the_text_old , can_chat

    if not can_chat :
        tkmsg.showinfo( lang.get( "info" ) , lang.get( "wait" ) )

    elif not the_text or "".join( the_text.split() ) == "" :
        tkmsg.showerror( lang.get( "wrong" ) , lang.get( "empty_content" ) )

    elif len( the_text ) > 2000 :
        tkmsg.showinfo( lang.get( "info" ) , lang.get( "words_too_more" ) )

    elif len( the_text ) <= 2000 and can_chat :
        can_chat = False
        with open( chat_logs_name , "a" , encoding = "utf-8" ) as File :
            File.write( md_text( "user" , the_text ) )
        add_chat_message( f"{the_text}" )
        add_chat_message( "\nBing:\n" )
        the_text_old = the_text
        text.delete( 0.0 , "end" )
        future = EdgeGPT.asyncio.run_coroutine_threadsafe( ask() , loop )
        future.add_done_callback( Bing_s_message )

def close() :
    root.destroy()
    loop.call_soon_threadsafe( loop.stop ) # 关闭循环
    log_time()
    logger.info( "'EdgeGPT-GUI' stop" )
    logger.info( "-" * 30 )

def message_user() :
    add_chat_message( "User:\n" )

async def ask( *args ) :
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
logger.debug( f"'cookies' file at '{os.path.abspath( cookies )}'" )
logger.debug( f"'chat_logs' file at '{os.path.abspath( chat_logs )}'" )
logger.debug( f"'logs' file at '{os.path.abspath( logs )}'" )

log_time()
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
