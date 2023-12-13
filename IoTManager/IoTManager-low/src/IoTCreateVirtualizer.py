import socket, requests, json, traceback
from IoTManager import portF
from urllib3 import HTTPConnectionPool


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
    print(f"\033[1m[IoTCreateVirtualizer]:\033[0m\t\tLISTURL:\n\t\t{listUrl}\n")
    headers = {'Content-Type': 'application/json'}
    sums_by_url = {}

    for url in listUrl:
        pinglist = [u for u in listUrl if u != url]
        msg['pinglist'] = pinglist

        try:
            print(f"\033[1m[IoTCreateVirtualizer]:\033[0m\t\t{url}/ping:")
            print(f"\033[1m[IoTCreateVirtualizer]:\033[0m\t\tPINGLIST:\n\t\t\t\t{pinglist}\n")

            response = requests.post(f"{url}/ping", data=json.dumps(msg), headers=headers)

            print(f"\033[1m[IoTCreateVirtualizer]:\033[0m\t\t{url}/ping RETURN:\n\t\t\t\t{response.json()}\n")
 
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
    #print(sums_by_url)
    if sums_by_url:
        min_sum_url = min(sums_by_url, key=lambda x: sums_by_url[x]["sum"])
        returne = sums_by_url[min_sum_url]["address"]
        print(f"\033[1m[IoTCreateVirtualizer]:\033[0m\t\tBest address is: \"{returne}\"\n")
        return sums_by_url[min_sum_url]["address"]
    else:
        return None     

def latencyApproximate(Json):
    delay = 1
    num_requests = 10
    if "delay" in Json["rules"]["settings"]:
        delay = Json["rules"]["settings"]["delay"]
    if "requests" in Json["rules"]["settings"]:
        num_requests = Json["rules"]["settings"]["requests"]


    enderecos = []
    dic_pings = {}
    for Cap in Json["sensors"]["capabilities"]:
        enderecos.append(Cap["address"])

    # Constrói listas_enderecos usando o campo "address" do JSON
    listas_enderecos = [endereco["address"].split("/") for endereco in Json["sensors"]["capabilities"]]

    # Transforma listas_enderecos em um dicionário usando o campo "addr" do JSON
    dic_enderecos = {endereco_dict["address"]: {"url": endereco_dict["addr"], "split": tuple(endereco)} for endereco, endereco_dict in zip(listas_enderecos, Json["sensors"]["capabilities"])}

    menor_comprimento = min(len(lista) for lista in listas_enderecos)

    pais_comuns = []

    for i in range(menor_comprimento):
        if all(lista[i] == listas_enderecos[0][i] for lista in listas_enderecos):
            pais_comuns.append(listas_enderecos[0][i])
        else:
            break

    print(f"Os pais comuns são: {pais_comuns}")
    print(dic_enderecos)

    headers = {'Content-Type': 'application/json'}
    msg = {
        "delay": delay,
        "requests": num_requests
    }
    while dic_enderecos:
        chave = next(iter(dic_enderecos))
        valor = dic_enderecos.pop(chave)
        if(valor["split"] != pais_comuns):
            url = valor["url"]
            
            parent_addr = chave
            while parent_addr.split("/") != pais_comuns or parent_addr not in dic_pings:
                chave = parent_addr
                response = requests.post(f"{url}/pingParent", data=json.dumps(msg), headers=headers)
                if response.status_code == 200 and response is not None:
                    data = response.json()
                    for response_data in data:
                        parent_url = response_data.get('parent_url')
                        parent_addr = response_data.get('tree_addr')
                        latency = response_data.get('latency')
                    
                else:
                    print(f"\033[1m[MANAGER-LOW - latencyApproximate]:\033[0m\tERROR")
                    break
                url = parent_url
                novo_item = {chave:latency}
                dic_pings.update(novo_item)



            
    

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
    
def pingUrl(url, delay, times):

    global porttest
    tempos_resposta = []
    port = porttest
    print(porttest)
    porttest = portF + 1

    connection_pool = HTTPConnectionPool(host=url, maxsize=100)
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100, pool_block=connection_pool)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    #print(f"\tPing \"{url}:{port}\"")

    for _ in range(times):
        try:
            for _ in range(3):
                try:
                    
                    resposta = session.get(f"{url}")
                    break
                except requests.exceptions.RequestException as e:
                    print(f"\t\tErro ao fazer requisição para a porta {port}: {e}")
                    port = porttest
                    porttest = portF + 1

            tempo_resposta = resposta.elapsed.total_seconds() * 1000  # Converte para milissegundos
            tempos_resposta.append(tempo_resposta)
            print(f"\tPing \"{url}:{port}\"\t{tempo_resposta}")
            time.sleep(delay)
        except requests.exceptions.RequestException as e:
            print(f"\t\tErro ao fazer requisição: {e}")
        finally:
            # Fechar a sessão após cada solicitação
            # session.close()
            pass
    session.close()

    if tempos_resposta:
        media = sum(tempos_resposta) / len(tempos_resposta)
        print(f"\tMEDIA:\t\"{url}\"\t{media} ms\n")
        return(media)
    else:
        return("ERRO")

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

