import socket, requests, json, traceback

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
    delay = 1
    num_requests = 10
    
    if "delay" in Json["rules"]["settings"]:
        delay = Json["rules"]["settings"]["delay"]
    if "requests" in Json["rules"]["settings"]:
        num_requests = Json["rules"]["settings"]["requests"]
    
    listUrl = [capability["addr"] for capability in Json["sensors"]["capabilities"]]
    print(listUrl)

    msg = {
        "pinglist": listUrl,
        "delay": delay,
        "requests": num_requests
    }
    print(f"\033[1m[CreateVirtualizer]:\033[0m\t\tLISTURL:\n\t\t{listUrl}\n")
    headers = {'Content-Type': 'application/json'}
    sums_by_url = {}

    for url in listUrl:
        pinglist = [u for u in listUrl if u != url]
        msg['pinglist'] = pinglist

        

        try:
            print(f"\033[1m[CreateVirtualizer]:\033[0m\t\t{url}/ping:")
            print(f"\033[1m[CreateVirtualizer]:\033[0m\t\tPINGLIST:\n\t\t{pinglist}\n")
            response = requests.post(f"{url}/ping", data=json.dumps(msg), headers=headers)
            print(f"\033[1m[CreateVirtualizer]:\033[0m\t\t{url}/ping RETURN:")
            print(response.json())

            if response.status_code == 200:
                data = response.json()
                for response_data in data:
                    response_url = response_data.get('url')
                    latency = response_data.get('latency')

                if response_url not in sums_by_url:
                    sums_by_url[response_url] = {"sum": 0, "address": Json["sensors"]["capabilities"][listUrl.index(response_url)]["address"]}

                sums_by_url[response_url]["sum"] += latency

            else:
                print(f"Request to {url} failed with status code {response.status_code}")

        except Exception as e:
            print(f"Error processing {url}: {e}")
            traceback.print_exc()

    if sums_by_url:
        min_sum_url = min(sums_by_url, key=lambda x: sums_by_url[x]["sum"])
        returne = sums_by_url[min_sum_url]["address"]
        print(f"\033[1m[CreateVirtualizer]:\033[0m\t\tBest address is: \"{returne}\"")
        return sums_by_url[min_sum_url]["address"]
    else:
        return None     



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

