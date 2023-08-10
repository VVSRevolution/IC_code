import requests
import time
url = ""
payload = ""
def fazer_requisicao():
    global url, payload
    url = "http://172.31.95.68:9007/search"
    payload = "/1.1/2.2/3.3/4.6"
    headers = {"Content-Type": "text/plain"}

    start_time = time.time()
    response = requests.post(url, data=payload, headers=headers)
    end_time = time.time()

    tempo_resposta = (end_time - start_time) * 1000

    return tempo_resposta, response

def salvar_em_txt(tempo_resposta):
    global payload
    with open("tempo.txt", "a") as arquivo:
        arquivo.write(f"{payload} : {tempo_resposta:.6f}\n")

if __name__ == "__main__":
    for i in range(10):
        tempo_resposta, response = fazer_requisicao()
        if response.status_code == 200:
            print(f"\n\n{i+1} -\tRequisição realizada com sucesso!")
            print(response.content)
            salvar_em_txt(tempo_resposta)
        else:
            print(f"Falha na requisição. Código de status: {response.status_code}")
        time.sleep(5)
