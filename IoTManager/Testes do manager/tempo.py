import requests
import time
url = ""
payload = [ 
    "/1.1/2.1/3.1/4.2",
    "/1.1/2.1/3.2/4.3", "/1.1/2.1/3.2/4.4",
    "/1.1/2.2/3.3/4.5", "/1.1/2.2/3.3/4.6",
    "/1.1/2.2/3.4/4.7", "/1.1/2.2/3.4/4.8"
        ]
def fazer_requisicao(i):
    global url, payload
    url = "http://172.19.62.174:9008/search"
   
    headers = {"Content-Type": "text/plain"}

    start_time = time.time()
    response = requests.post(url, data=payload[i], headers=headers)
    end_time = time.time()

    tempo_resposta = (end_time - start_time) * 1000

    return tempo_resposta, response

def salvar_em_txt(tempo_resposta,i):
    global payload
    with open("tempo.txt", "a") as arquivo:
        arquivo.write(f"{payload[i]} : {tempo_resposta:.6f}\n")

if __name__ == "__main__":
    
    for k in range(len(payload)):
        print(payload[k])
        for i in range(10):
            tempo_resposta, response = fazer_requisicao(k)
            if response.status_code == 200:
                print(f"\n\n{i+1} -\tRequisição realizada com sucesso!")
                print(response.content)
                salvar_em_txt(tempo_resposta,k)
            else:
                print(f"Falha na requisição. Código de status: {response.status_code}")
                break
                
            time.sleep(3)


