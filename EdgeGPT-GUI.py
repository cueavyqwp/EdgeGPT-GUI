import tkinter.messagebox as tkmsg
import tkinter.scrolledtext
import tkinter as tk
import traceback
import threading
import json
import time
import pip

while 1 :
    try:
        import EdgeGPT #https://github.com/acheong08/EdgeGPT
        import langful
        break
    except:
        pip.main( [ "install" , "langful==0.17" ] )
        pip.main( [ "install" , "EdgeGPT==0.1.4" ] )

lang = langful.lang()

font = ( "Consolas" , 18 , "bold" )
root = tk.Tk()
root.geometry( "1200x800" )
root.title( "EdgeGPT-GUI" )
can_chat = True #确保用户不会在Bing回答时输入内容
root.update()

File_name = str( time.strftime( "%Y-%m-%d" , time.localtime() ) ) + ".md" #储存对话
def log_time():
    with open( File_name , "a" , encoding = "utf-8" ) as File :
        Now_time = time.strftime( "%Y-%m-%d %H:%M:%S" , time.localtime() )
        File.write( f"___\n\n# `{Now_time}`\n\n" )

log_time()

#测试能否读取cookie文件
try:
    with open( 'cookies.json', 'r' ) as f : cookies = json.load( f )
except:
    tkmsg.showerror( lang.replace( "wrong" ) , lang.get( "can_not_to_read" ) )
    exit()

with open( 'cookies.json', 'r' ) as f : cookies = json.load( f )

bot = bot = EdgeGPT.Chatbot( cookies = cookies )
loop = EdgeGPT.asyncio.get_event_loop()
loop_thread = threading.Thread( target = loop.run_forever )
loop_thread.start()

the_text = ""
the_text_old = ""
the_chat_text = ""

def reset( *args ) :
    global bot , loop , loop_thread
    if can_chat :
        bot = EdgeGPT.Chatbot( cookies = cookies )
        loop.call_soon_threadsafe( loop.stop )
        loop = EdgeGPT.asyncio.get_event_loop()
        loop_thread = threading.Thread( target = loop.run_forever )
        loop_thread.start()
        add_chat_message( lang.replace(
f"""{ '=' * 60 }
%new_topic%
{ '=' * 60 }

You:
"""
    )
        )
        log_time()
    else :
        tkmsg.showinfo( lang.get( "info" ) , lang.get( "wait" ) )

def show_count( *args ): #统计字数
    global the_text
    the_text = text.get( "1.0" , "end" ) [:-1]
    root.title( lang.replace ( f"EdgeGPT-GUI [ %word% 2000/{ len( the_text ) } ] [ %f9_send% ] [ %f12_reload% ]" ) )
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
        with open( File_name , "a" , encoding = "utf-8" ) as File :
            File.write( f"## `Bing`\n\n___\n\n{message}\n\n" )
        add_chat_message( f"{message}\nUser:\n" )
    except Exception as error :
        print( '=' * 60 )
        traceback.print_exc()
        print( '=' * 60 )
        tkmsg.showerror( lang.get( "wrong" ) , lang.get( "network_error_message" ) )
        text.insert( tk.END , the_text_old )
    can_chat = True

def send( *args ):
    global can_chat , the_text_old
    if not can_chat :
        tkmsg.showinfo( lang.get( "info" ) , lang.get( "wait" ) )
    elif not the_text or "".join( the_text.split() ) == "" :
        tkmsg.showerror( lang.get( "wrong" ) , lang.get( "empty_content" ) )
    elif len( the_text ) > 2000 :
        tkmsg.showinfo( lang.get( "info" ) , lang.get( "words_too_more" ) )
    elif len( the_text ) <= 2000 and can_chat :
        can_chat = False
        with open( File_name , "a" , encoding = "utf-8" ) as File :
            File.write( f"___\n\n## `User`\n\n___\n\n{the_text}\n___\n\n" )
        add_chat_message( f"{the_text}\n\nBing:\n" )
        the_text_old = the_text
        text.delete(0.0,"end")
        future = EdgeGPT.asyncio.run_coroutine_threadsafe( ask() , loop )
        future.add_done_callback( Bing_s_message )

async def ask( *args ) : return await bot.ask( prompt = the_text )

chat_text = tkinter.scrolledtext.ScrolledText(
    root ,
    height = root.winfo_height() ,
    width = root.winfo_width() ,
    state = tk.DISABLED ,
    tabs = ( "1c" ) ,
    undo = True ,
    font = font
    )

add_chat_message( lang.replace(
f"""{ '-' * 60 }
%f9_send%
%f12_reload%
{ '-' * 60 }

You:
"""))

text = tkinter.scrolledtext.ScrolledText(
    root ,
    width = root.winfo_width() ,
    tabs = ( "1c" ) ,
    undo = True ,
    height = 5,
    font = font
    )

text.pack(side=tk.BOTTOM , anchor=tk.SW)

text.bind( "<F9>" , send ) #绑定事件
text.bind( "<F12>" , reset ) #绑定事件

chat_text.pack(side=tk.TOP , anchor=tk.N)


root.after( 1 , show_count )

root.mainloop()

#关闭循环
loop.call_soon_threadsafe( loop.stop )

log_time()