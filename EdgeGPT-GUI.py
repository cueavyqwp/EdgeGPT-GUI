import tkinter.messagebox as tkmsg 
import tkinter.scrolledtext
import tkinter as tk
import threading
import warnings
import locale
import time
import pip

while 1 :
    try:
        import ttkbootstrap as ttk
        import EdgeGPT #EdgeGPT 原地址 https://github.com/acheong08/EdgeGPT
        import emoji
        break
    except:
        pip.main( [ "install" , "ttkbootstrap" ] )
        pip.main( [ "install" , "EdgeGPT" ] )
        pip.main( [ "install" , "emoji" ] )

json = EdgeGPT.json
os = EdgeGPT.os

warnings.filterwarnings("ignore",category=DeprecationWarning)

language_file = locale.getdefaultlocale()
language_file = language_file[0].lower() + ".json"
if not os.path.exists(f"lang/{language_file}") : language_file = "en_us.json"
language_file = "lang/" + language_file

with open( language_file , "r" , encoding = "utf-8" ) as lang_file : language = json.load(lang_file)

font = ( "Arial" , 14 , "bold" )
root = ttk.Window()
root.geometry( "1200x800" )
root.title( "EdgeGPT-GUI" )
root.attributes( "-toolwindow" , 2 ) #只保留退出键
can_chat = True #确保用户不会在Bing回答时输入内容a
root.resizable ( 0 , 233333333 ) #禁止横向拉长窗口 你问我既然可以竖向拉为什么不能横向拉? 因为有BUG _(:з」∠)_
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
    tkmsg.showerror( language[ "wrong" ] , language[ "can_not_to_read" ] )
    exit()

bot = EdgeGPT.Chatbot( cookies = cookies )

the_text = ""
the_chat_text = ""

def show_count( *args ): #统计字数
    global the_text
    the_text = text.get( "1.0" , "end" ) [:-1]
    language_word = language[ "word" ]
    count_label.config( text = f" { language_word } 2000/{ len( the_text ) }" )
    count_label.place(
        x=root.winfo_width() - count_label.winfo_width() - send_button.winfo_width() - 18 ,
        y=root.winfo_height() - 20
        )
    root.after(1,show_count)

def show_GUI(*args): #显示GUI
    text.config(
        width = root.winfo_width()
    )

    chat_text.config(
        height = ( root.winfo_height() - text.winfo_height() - 36 ) // 22 + 1 ,
        width = ( root.winfo_width() - 25 ) // 11
        )
    root.after( 2000 , show_GUI ) #每两秒执行一次 无需过快

def add_chat_message( message , enter = True ): #往聊天内容里添加内容
    chat_text.config( state = tk.NORMAL )
    chat_text.insert( tk.END , message + ( "" , "\n" ) [enter] )
    chat_text.config( state = tk.DISABLED )

def Bing_s_message( future ):
    global can_chat
    if future.result() ["item"] ["result"] ["value"] == "InternalError" :
        tkmsg.showerror( language[ "network_error" ] , language[ "network_error_message" ] )
        can_chat = True
    else:
        message = future.result() ["item"] ["messages"] [1] ["adaptiveCards"] [0] ["body"] [0] ["text"]
        with open( File_name , "a" , encoding = "utf-8" ) as File :
            File.write( f"## `Bing`\n\n___\n\n{message}\n\n" )
        message_with_no_emoji = emoji.demojize( message )#因为处理不了emoji,所以需要把它们解码
        add_chat_message( f"{message_with_no_emoji}\nUser:\n" )
        text.delete(0.0,"end")
        can_chat = True

def send( *args ):
    global can_chat
    if not can_chat :
        tkmsg.showinfo( language[ "info" ] , language[ "wait" ] )
    elif not the_text or "".join( the_text.split() ) == "" :
        tkmsg.showerror( language[ "wrong" ] , language[ "empty_content" ] )
    elif len( the_text ) > 2000 :
        tkmsg.showinfo( language[ "info" ] , language[ "words_too_more" ] )
    elif len( the_text ) <= 2000 and can_chat :
        can_chat = False
        with open( File_name , "a" , encoding = "utf-8" ) as File :
            File.write( f"___\n\n## `User`\n\n___\n\n{the_text}\n___\n\n" )
        add_chat_message( f"{the_text}\n\nBing:\n" )
        future = EdgeGPT.asyncio.run_coroutine_threadsafe( ask() , loop )
        future.add_done_callback( Bing_s_message )

async def ask( *args ) : return await bot.ask( prompt = the_text )

async def reset( *args ) : await bot.reset()

loop = EdgeGPT.asyncio.get_event_loop()
loop_thread = threading.Thread( target = loop.run_forever )
loop_thread.start()

chat_text = tkinter.scrolledtext.ScrolledText(
    root ,
    width = root.winfo_width() ,
    height = 1000,
    state = tk.DISABLED , #交互框不需要也不能编辑
    tabs = ( "1c" ) ,
    undo = True ,
    font = font
    )

chat_text.place(anchor=tk.NW)

add_chat_message( language[ "welcome" ] )

send_button = tk.Button( root , text = language[ "send" ] , command = send , width = 6 , height = 5 , font = font ) 
send_button.pack( side = tk.RIGHT , anchor = tk.S )

text = tkinter.scrolledtext.ScrolledText(
    root ,
    width = root.winfo_width() // 10 ,
    height = 5,
    tabs = ( "1c" ) ,
    undo = True ,
    font = font
    )

text.pack( side = tk.LEFT , anchor = tk.S )
text.update()

count_label = tk.Label( root )

root.after( 1 , show_count )
root.after( 2000 , show_GUI )

root.mainloop()

#关闭循环
loop.call_soon_threadsafe( loop.stop )

log_time()