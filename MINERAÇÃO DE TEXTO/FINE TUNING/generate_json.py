import json
import os

def generate(data_name: str, data: list) -> None:
    diretorio = os.getcwd()  
    subdir = "FINE TUNING/DATA"
    caminho_subdir = os.path.join(diretorio, subdir)

    if not os.path.exists(caminho_subdir):
        os.makedirs(caminho_subdir)

    nome_file = f"{data_name}.json"
    caminho_file = os.path.join(caminho_subdir, nome_file)

    if os.path.exists(caminho_file):
        with open(caminho_file, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
                if not isinstance(existing_data, list): 
                    raise ValueError("O conteúdo do arquivo JSON não é uma lista.")
            except json.JSONDecodeError: existing_data = []
    else: existing_data = []

    existing_data.extend(data)

    with open(caminho_file, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4) 

    print(f"Arquivo JSON salvo em: {caminho_file}")

def get_id() -> int:
    diretorio = os.getcwd()
    subdir = "FINE TUNING"
    caminho_subdir = os.path.join(diretorio, subdir)
    
    nome_file = f"id_db.txt"
    caminho_file = os.path.join(caminho_subdir, nome_file)
    
    try:
        with open(caminho_file, 'r', encoding='utf-8') as file:
            id = int(file.read().strip())
            id += 1
            
        with open(caminho_file, 'w', encoding='utf-8') as file:
            id = f"{id:05}"
            file.write(str(id))
            
        return id    
        
    except FileNotFoundError:
        print(f"O arquivo {caminho_file} não foi encontrado.")   

answers_list = [{"text":"", "answer_start":"",}]
qas_list     = [{"id":"", "is_impossible":"", "question":"", "answers": ""}]
data         = []

answers_list_template = [{"text": "", "answer_start": ""}]
qas_list_template     = [{"id": "", "is_impossible": "", "question": "", "answers": ""}]
data                  = []

while (context := input("Insira o contexto: ")):
    qas = []
    
    while (question := input("Insira a pergunta: ")):
        answers      = []
        
        text         = input("Insira a resposta: ")
        answer_start = (context.upper()).find(text.upper())
        answer       = {"text":text, "answer_start":answer_start}
        answers.append(answer)
        
        qa = {"id":get_id(), "is_impossible":False, "question":question, "answers":answers}
        qas.append(qa)
        
        print(f"A substring {text} foi encontrada na posição {answer_start}.")
        
    pre_data = {"context": context, "qas": qas}
    data.append(pre_data)

generate("train_data", data)