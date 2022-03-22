from telnetlib import Telnet
from exception.exceptions import *
from datetime import date
import time
import os
from dotenv import load_dotenv
import json

load_dotenv()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

f = open(f'{ROOT_DIR}/equipamentos.json')

equipamentos = json.load(f)['equipamentos']


def main(equipamento):
  
    IP_SERVER_FTP = os.environ.get('IP_SERVER_FTP')
    USER_FTP = os.environ.get('USER_FTP')
    PASS_FTP = os.environ.get('PASS_FTP')
    
    data_atual = date.today()
    data_em_texto ="{}-{}-{}".format(data_atual.day, data_atual.month,data_atual.year)
    r = '\r'
    r = r.encode('ascii')
    try:
        equipamento.connection = Telnet(equipamento.ip, equipamento.port)

        # Realizando Login
        index, match_obj, text = equipamento.connection.expect(["Username:".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError(f"Falha na conexão, EQUIPAMENTO RESPONSE: {text}")

        equipamento.connection.write(f"{equipamento.user}\r".encode('latin-1'))

        index, match_obj, text = equipamento.connection.expect(["Password:".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError(f"Falha no usuário, EQUIPAMENTO RESPONSE: {text}")

        equipamento.connection.write(f"{equipamento.password}\r".encode('latin-1'))
        index, match_obj, text = equipamento.connection.expect([">".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError("Falha ao informar a senha")

        equipamento.connection.write(b"save\r")
        equipamento.connection.write(b"Y\r")
       
        
        index, match_obj, text = equipamento.connection.expect([">".encode('latin-1')], timeout=2)
        print("Acessou o switch.")
        time.sleep(3)
        
        index, match_obj, text = equipamento.connection.expect([">".encode('latin-1')], timeout=2)
        ftp = "ftp -a %s %s"%(equipamento.ip,IP_SERVER_FTP)
        ftp = ftp.encode('ascii')
        equipamento.connection.write(ftp + r)

        index, match_obj, text = equipamento.connection.expect([":".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError("Falha ao executar comando de conectar no ftp ")

        equipamento.connection.write(USER_FTP.encode('ascii') + r)

        index, match_obj, text = equipamento.connection.expect(["password:".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError("Falha ao Acessar o FTP-SERVER verifique a conexão e credenciais")

        equipamento.connection.write(PASS_FTP.encode('ascii') + r)

        index, match_obj, text = equipamento.connection.expect(["[ftp]".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError("Falha ao Acessar o FTP-SERVER")
        equipamento.connection.write(b"binary\r")

        index, match_obj, text = equipamento.connection.expect(["[ftp]".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError("Falha ao mudar ftp para binary")

        equipamento.connection.write(b"cd backups\r")

        index, match_obj, text = equipamento.connection.expect(["[ftp]".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError("Falha ao entrar na pasta Backups")

        equipamento.connection.write(b"cd huawei\r")


        index, match_obj, text = equipamento.connection.expect(["[ftp]".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError("Falha ao Entrar na pasta huawei")

        criarPasta = "mkdir %s"%(equipamento.hostname)
        criarPasta = criarPasta.encode('ascii')
        equipamento.connection.write(criarPasta + r)


        index, match_obj, text = equipamento.connection.expect(["[ftp]".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError("Falha ao Entrar na pasta huawei")            

        pasta = "cd %s"%(equipamento.hostname)
        pasta = pasta.encode('ascii')
        equipamento.connection.write(pasta + r)
    
        index, match_obj, text = equipamento.connection.expect(["[ftp]".encode('latin-1')], timeout=2)

        if not match_obj:
            raise CommandError("Falha ao Entrar na pasta do switch")
        put = "put vrpcfg.zip vrpcfg-%s.zip"%(data_em_texto)
        put = put.encode('ascii')
        equipamento.connection.write(put + r)

        index, match_obj, text = equipamento.connection.expect(["[ftp]".encode('latin-1')], timeout=2)
        if not match_obj:
            raise CommandError("Falha ao salvar o arquivo de configuração no servidor.")
        time.sleep(1.5)
        #print (equipamento.connection.read_eager())
        #print (equipamento.connection.read_all())
        print('BackupFinalizado')
        equipamento.connection.close()

    except:
        equipamento.connection.close()
        raise ConnectionError()

class Equipamento:
    def __init__(self,hostname, ip,port, user, password):
        self.connection = None
        self.hostname = hostname
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password

for switch in equipamentos:
    try:
        USER = os.environ.get('USER')
        PASS = os.environ.get('PASS')
        PORT_TELNET = os.environ.get('PORT_TELNET')
        print(f"Iniciando Backup no Switch {switch['hostname']}")
        equipamento = Equipamento(switch['hostname'],switch['ip'],PORT_TELNET,USER,PASS)
        main(equipamento)
    except:
        pass