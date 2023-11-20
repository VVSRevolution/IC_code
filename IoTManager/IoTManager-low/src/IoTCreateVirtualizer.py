import socket, requests, json

def latencyTest(list):
    menor_tempo = float('inf')
    url_menor_ping = None
    print(f"\033[1m[MANAGER-LOW]:\033[0m\tTeste de Lantencia:")
    for url in list:
        media_tempo_resposta = pingUrl(url)
        if media_tempo_resposta is not None and media_tempo_resposta < menor_tempo:
            menor_tempo = media_tempo_resposta
            url_menor_ping = url
    print(f"\tMenor:\t{url_menor_ping}\t{menor_tempo}ms")
    return url_menor_ping
        
def latencyPrecision(Json):
    delay = 0
    requests = 10
    if "delay" in Json["rules"]["settings"]:
        delay = Json["rules"]["settings"]["delay"]
    if "requests" in Json["rules"]["settings"]:
        requests = Json["rules"]["settings"]["requests"]
    listUrl = [capability["addr"] for capability in Json["sensors"]["capabilities"]]
    print (listUrl)
    msg = {
        "pinglist":listUrl,
        "delay":delay,
        "requests":requests
    }
    headers = {'Content-Type': 'application/json'}
    sums_by_url = {}
    for url in listUrl:
        pinglist = [u for u in listUrl if u != url]
        msg['pinglist'] = pinglist
        
        response = requests.post(url, data=json.dumps(msg), headers=headers)
   
        if response.status_code == 200:
            data = response.json()

            response_url = data.get('url')
            latency = data.get('latency')

            if response_url not in sums_by_url:
                sums_by_url[response_url] = 0

            sums_by_url[response_url] += latency
            
    min_sum_url = min(sums_by_url, key=sums_by_url.get)

    return min_sum_url        



def pingUrl(url):
    tempos_resposta = []
    print(f"\tPing \"{url}\"")

    for _ in range(10):
        try:
            resposta = requests.get(url)
            tempo_resposta = resposta.elapsed.total_seconds() * 1000  # Converte para milissegundos
            tempos_resposta.append(tempo_resposta)
            print(f"\t\t{tempo_resposta}")
        except requests.exceptions.RequestException as e:
            print(f"\t\tErro ao fazer requisição: {e}")

    if tempos_resposta:
        media = sum(tempos_resposta) / len(tempos_resposta)
        print(f"\tMedia:\t{media} ms\n")
        return media
    else:
        return None


def cadastrarCap(msg,url):
    headers= {'Content-type': 'application/json',}
    print(f"\033[1m[MANAGER-LOW]:\033[0m\tCadastrando Capability")
    try:
            print(f"Cadastrado:\n{msg}")
            requests.post (f'http://{url}/capabilities', data = json.dumps(msg),headers=headers)
    except:
        print(f"\033[1m[MANAGER-LOW]:\033[0m\tNão foi possivel cadastrar:\n{msg}")
        #erroMsg1 = f"\033[1m[MANAGER-LOW]:\033[0m\tNão foi possivel cadastrar {capabiliteNome}"
        #return redirect(url_for('erro_m',erroMsg=erroMsg1))

def cadastrarRec(msg,url):
    headers= {'Content-type': 'application/json',}
    print(f"\033[1m[MANAGER-LOW]:\033[0m\tCadastrando Recurso")
    try:
            print(f"Cadastrado:\n{msg}")
            requests.post (f'http://{url}/resources', data = json.dumps(msg),headers=headers)
    except:
        print(f"\033[1m[MANAGER-LOW]:\033[0m\tNão foi possivel cadastrar:\n{msg}")
        #erroMsg1 = f"\033[1m[MANAGER-LOW]:\033[0m\tNão foi possivel cadastrar {capabiliteNome}"
        #return redirect(url_for('erro_m',erroMsg=erroMsg1))

