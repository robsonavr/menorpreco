from bs4 import BeautifulSoup
import requests
import json
import time
import pandas as pd

headers = {
    'Accept' : '*/*',
    'Accept-Encoding' : 'gzip, deflate, br, zstd',
    'Accept-Language' : 'en-US,en;q=0.9,pt;q=0.8,es;q=0.7',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

df = pd.DataFrame()

def get_product_links(query):
    search_url = f'https://menorpreco.notaparana.pr.gov.br/api/v1/produtos?local=6gkzq99z5j5f&termo={query}&offset=0&raio=2&data=-1&ordem=0'
    return search_url


def extract_product_info(url, query):

    global df

    r = requests.get(url=url, headers=headers)
    # print(r.status_code)

    soup = BeautifulSoup(r.content, 'html.parser')

    data_json  = json.loads(soup.text)

    df_json = pd.json_normalize(data_json['produtos'])

    # print(df_json.columns)
    try:
        df_json.drop(columns=['id', 'local', 'valor_desconto', 'valor_tabela', 'tempo', 'nrdoc', 'estabelecimento.nm_fan',
        'estabelecimento.codigo','estabelecimento.complemento', 'estabelecimento.mesoreg', 'estabelecimento.microreg'], inplace=True)
        
        df_json.columns = ['desc', 'ncm', 'cdanp', 'valor', 'datahora', 'distkm', 'gtin',
        'nm_emp', 'tp_logr', 'nm_logr', 'nr_logr', 'bairro', 'mun', 'uf']
        
        df_json['query'] = query

        df = pd.concat([df, df_json], axis=0)

    except Exception as e:
        print(query, ': product not found!')

      
    # filename = 'data.jsonl'
    # if os.path.isfile(filename):
    #     os.remove(filename)

    # for product in data_json['produtos']:
    #     try:
    #         product_info = {
    #             'description' : product['desc'],
    #             # 'ncm' : product['ncm'],
    #             'price' : product['valor'],
    #             'time' : product['tempo'].strip('h\u00e1 '),
    #             'distance' : product['distkm'],
    #             'store' : product['estabelecimento']['nm_emp'],
    #             'street' : product['estabelecimento']['nm_logr'],
    #             'number' : product['estabelecimento']['nr_logr'],
    #             'neighbor' : product['estabelecimento']['bairro'],
    #             'city' : product['estabelecimento']['mun'],
    #             'state' : product['estabelecimento']['uf'],
    #         }
    #     except Exception as e:
    #         product_info = {'error': e}
        
    #     with open(filename, 'a') as f:
    #         f.write(json.dumps(product_info)+',\n')

def main():

    global df

    df_list = pd.read_csv('lista_compra.csv')

    for item in df_list['produtos'].tolist():
        extract_product_info(get_product_links(item), item)
        time.sleep(3)
    
    df['Endereço'] = df[['tp_logr', 'nm_logr']].agg(' '.join, axis=1)
    df['Endereço'] = df[['Endereço', 'nr_logr']].agg(', '.join, axis=1)
    df['Cidade'] = df[['mun', 'uf']].agg('/'.join, axis=1)
    df.drop(columns=['tp_logr', 'nm_logr', 'mun', 'uf', 'nr_logr'], inplace=True)
    df.to_excel('data.xlsx', sheet_name='products', index=False)

if __name__ == "__main__":
    main()