"""Executa casos congelados do protocolo1.0 contra nginx/API reais.

Não importa o parser para gerar esperados. Critérios: gramática do projeto,
lista de casos da Tarefa4 e três oráculos independentes fixados em 18/11/2026.
"""
import argparse,csv,hashlib,json,re,subprocess,time
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request,build_opener,ProxyHandler
from zoneinfo import ZoneInfo

cli=argparse.ArgumentParser(description=__doc__)
cli.add_argument('--raiz',type=Path,default=Path(__file__).resolve().parents[1])
cli.add_argument('--saida',type=Path)
cli.add_argument('--url',default='http://127.0.0.1:8501/api/analisar')
args=cli.parse_args()
ROOT=args.raiz.resolve()
OUT=(args.saida or ROOT/'docs/etapa5/resultados').resolve()
OUT.mkdir(parents=True,exist_ok=True)
CASOS=json.loads((ROOT/'tests/planejamento/etapa4-casos.json').read_text())['casos']
REFERENCIAS={r['caso']:r['subarvore_esperada'] for r in json.loads((ROOT/'tests/planejamento/etapa4-ast-referencias.json').read_text())['referencias']}
HTTP400={'B01','B02','B05'}
SKIP={'L01','L02','L03','B08'}
ERRO={f'S{i:02}' for i in range(1,11)}|{'B03','B07'}
ASTTIPOS={'Programa','Declaracao','Atribuicao','Bloco','Se','Binario','Unario','Identificador','Literal'}
S_ERROS={'S01':('',6,';'),'S02':('{',11,')'),'S03':('',9,'}'),'S04':(';',9,'LITERAL_INTEIRO'),
'S05':('else',1,'if'),'S06':('*',13,'LITERAL_INTEIRO'),'S07':('if',5,'IDENTIFICADOR'),
'S08':('',8,'LITERAL_INTEIRO'),'S09':(',',6,';'),'S10':('(',7,'=')}
L_ERROS={'L01':('@',1),'L02':('1.2.3',7),'L03':('/* aberto',8),'B08':('@',1)}
http=build_opener(ProxyHandler({}))


def requisitar(codigo):
 req=Request(args.url,data=json.dumps({'codigo':codigo}).encode(),headers={'Content-Type':'application/json'})
 try:
  with http.open(req,timeout=20) as r:return r.status,json.loads(r.read())
 except HTTPError as e:return e.code,json.loads(e.read())


def sem_posicoes(x):
 if isinstance(x,dict):return {k:sem_posicoes(v) for k,v in x.items() if k not in {'inicio','fim'}}
 if isinstance(x,list):return [sem_posicoes(v) for v in x]
 return x


def nos(ast):
 pilha=[ast]
 while pilha:
  n=pilha.pop()
  if isinstance(n,list):pilha.extend(n)
  elif isinstance(n,dict):
   if n.get('tipo') in ASTTIPOS:yield n
   pilha.extend(n.values())


def validar_ast(ast,tokens,codigo):
 assert ast['tipo']=='Programa' and ast['comandos']
 linhas=codigo.replace('\r\n','\n').replace('\r','\n').split('\n')
 folhas={(t['lexema'],t['linha'],t['coluna']) for t in tokens}
 for no in nos(ast):
  assert no['tipo'] in ASTTIPOS
  for p in (no['inicio'],no['fim']):
   assert 1<=p['linha']<=len(linhas)
   assert 1<=p['coluna']<=len(linhas[p['linha']-1])+1
  assert (no['inicio']['linha'],no['inicio']['coluna']) < (no['fim']['linha'],no['fim']['coluna'])
  if no['tipo'] in {'Literal','Identificador'}:
   texto=no.get('lexema',no.get('nome'))
   assert (texto,no['inicio']['linha'],no['inicio']['coluna']) in folhas
   assert no['fim']['coluna']-no['inicio']['coluna']==len(texto)


def verificar(caso,status,r):
 id=caso['id']; codigo=caso['codigo']
 if id in HTTP400:
  assert status==400 and r['recebido'] is False
  assert r['erro']=='entrada_invalida'
  assert all(k not in r for k in ['tokens','sintatica'])
  return
 assert status==200 and r['recebido'] is True
 assert r['total_caracteres']==len(codigo)
 assert r['total_linhas']==len(codigo.splitlines())
 assert r['sucesso']==(not r['erros'])
 assert all(t['tipo']!='EOF' for t in r['tokens'])
 s=r['sintatica']
 if id in SKIP:
  assert r['sucesso'] is False
  assert s=={'estado':'nao_executada','sucesso':None,'motivo':'erros_lexicos','ast':None,'erros':[]}
  lexema,coluna=L_ERROS[id]
  assert len(r['erros'])==1 and (r['erros'][0]['lexema'],r['erros'][0]['linha'],r['erros'][0]['coluna'])==(lexema,1,coluna)
  assert r['tokens'], 'Tokens válidos devem ser preservados'
  return
 assert r['sucesso'] is True and r['erros']==[]
 if id in ERRO:
  assert s['estado']=='erro' and s['sucesso'] is False and s['ast'] is None and s['erros']
  if id in S_ERROS:
   lexema,coluna,esperado=S_ERROS[id]
   e=s['erros'][0]
   assert (e['lexema'],e['linha'],e['coluna'])==(lexema,1,coluna)
   assert esperado in e['esperado']
   assert e['encontrado']==('EOF' if lexema=='' else 'PALAVRA_RESERVADA' if lexema in {'if','else'} else 'OPERADOR' if lexema=='*' else 'DELIMITADOR')
  if id=='B03':assert r['tokens']==[] and s['erros'][0]['encontrado']=='EOF' and 'Programa vazio' in s['erros'][0]['mensagem']
  if id=='B07':assert s['erros'][0]['codigo']=='limite_profundidade'
  return
 assert s['estado']=='sucesso' and s['sucesso'] is True and s['erros']==[]
 ast=s['ast'];validar_ast(ast,r['tokens'],codigo);comandos=ast['comandos']
 if id=='V01':assert comandos[0]['tipo']=='Declaracao' and comandos[0]['nome']=='x' and comandos[0]['tipoDado']=='int' and comandos[0]['inicializador'] is None
 if id=='V02':assert comandos[0]['tipoDado']=='float' and sem_posicoes(comandos[0]['inicializador'])=={'tipo':'Literal','categoria':'real','lexema':'7.5'}
 if id=='V03':assert [n['tipo'] for n in comandos]==['Declaracao','Atribuicao'] and comandos[1]['alvo']['nome']=='x' and comandos[1]['valor']['lexema']=='10'
 if id in REFERENCIAS:assert sem_posicoes(comandos[0]['inicializador'])==REFERENCIAS[id]
 if id=='V07':
  expr=comandos[0]['inicializador']; assert expr['operador']=='*'
  assert expr['esquerda']['tipo']=='Unario' and expr['esquerda']['operador']=='-' and expr['esquerda']['operando']['lexema']=='2'
  assert expr['direita']['tipo']=='Unario' and expr['direita']['operador']=='+' and expr['direita']['operando']['lexema']=='3'
 if id in {'V08','V09'}:
  cond=comandos[1]; assert cond['tipo']=='Se' and cond['entao']['tipo']=='Bloco' and cond['entao']['comandos'][0]['tipo']=='Atribuicao'
  if id=='V08':assert cond['senao'] is None and cond['condicao']['operador']=='>='
  else:assert cond['senao']['tipo']=='Bloco' and cond['senao']['comandos'][0]['valor']['lexema']=='2' and cond['condicao']['operador']=='!='
 if id=='V10':assert comandos[0]['tipo']=='Bloco' and comandos[0]['comandos'][1]['tipo']=='Bloco' and comandos[0]['comandos'][1]['comandos'][0]['tipoDado']=='float'
 if id=='V11':assert {n['tipo'] for n in nos(ast)}=={'Programa','Declaracao'}
 if id=='V12':assert len(comandos)==1 and comandos[0]['tipo']=='Bloco' and comandos[0]['comandos']==[]
 if id=='B04':assert len(codigo)==10000 and comandos[0]['tipo']=='Declaracao'
 if id=='B06':
  atual=comandos[0];quantidade=0
  while atual['tipo']=='Bloco':quantidade+=1;atual=atual['comandos'][0]
  assert quantidade==64 and atual['tipo']=='Declaracao'


def versao_checkout():
 r=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True)
 return r.stdout.strip() if r.returncode==0 else 'sem metadados Git; conferir hashes dos artefatos e versão informada'


def main():
 inicio=datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat();rows=[];semantic=[]
 for c in CASOS:
  t=time.perf_counter(); r=None;status=None;falha=''
  try:
   status,r=requisitar(c['codigo']);verificar(c,status,r)
   passou=True
  except Exception as e:passou=False;falha=f'{type(e).__name__}: {e}'
  s=(r or {}).get('sintatica',{})
  row={'id':c['id'],'categoria':c['categoria'],'codigo':c['codigo'],'geracao_da_entrada':c.get('geracao_da_entrada'),'resultado_esperado':c['resultado_esperado'],
   'http_observado':status,'estado_sintatico_observado':s.get('estado'),'sucesso_lexico_observado':(r or {}).get('sucesso'),
   'numero_tokens':len((r or {}).get('tokens',[])),'erros_lexicos':(r or {}).get('erros',[]),'erros_sintaticos':s.get('erros',[]),
   'tipo_raiz_ast':(s.get('ast') or {}).get('tipo'),'resultado':'aprovado' if passou else 'reprovado',
   'falha':falha,'duracao_ms_observada':round((time.perf_counter()-t)*1000,3),'resposta_observada':r}
  if c['id'].startswith('M'):
   row['resultado_semantico']='pendente_nao_implementado';row['observacao']='A aprovação refere-se somente à sintaxe. Não foi executada verificação de declaração/redeclaração/tipos.';semantic.append(row)
  else:rows.append(row)
  print(c['id'],row['resultado'],status,s.get('estado'),falha,flush=True)
 total=len(rows);ap=sum(r['resultado']=='aprovado' for r in rows);execu=sum(r['http_observado'] is not None for r in rows)
 report={'protocolo_origem':'1.0, definido em18/11/2026 antes do parser','inicio':inicio,'fim':datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(),
 'commit':versao_checkout(),'url_alvo':args.url,
 'fixture_sha256':hashlib.sha256((ROOT/'tests/planejamento/etapa4-casos.json').read_bytes()).hexdigest(),
 'planejados_aplicaveis':total,'executados':execu,'aprovados':ap,'reprovados':sum(r['resultado']=='reprovado' for r in rows),'nao_executados':total-execu,
 'cobertura_execucao_percentual':100*execu/total,'aprovacao_percentual':100*ap/execu if execu else None,'prontidao_percentual':100*ap/total,
 'cobertura_de_codigo':'não medida nesta rodada; cobertura de casos não equivale à cobertura de linhas/ramos',
 'casos':rows,'controles_sintaticos_de_casos_semanticos_futuros':semantic,'casos_semanticos_executados':0,'casos_semanticos_pendentes':3,'avaliacao_humana_executada':False}
 (OUT/'casos_funcionais.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 campos=['id','categoria','codigo_resumo','resultado_esperado','http_observado','estado_sintatico_observado','sucesso_lexico_observado','numero_tokens','erros_lexicos','erros_sintaticos','tipo_raiz_ast','resultado','falha']
 with (OUT/'casos_funcionais.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=campos);w.writeheader()
  for r in rows:
   d={k:r.get(k) for k in campos};d['codigo_resumo']=r['geracao_da_entrada'] or r['codigo'];d['erros_lexicos']=json.dumps(r['erros_lexicos'],ensure_ascii=False);d['erros_sintaticos']=json.dumps(r['erros_sintaticos'],ensure_ascii=False);w.writerow(d)
 with (OUT/'casos_semanticos_pendentes.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['id','codigo','resultado_esperado','controle_sintatico_observado','avaliacao_semantica']);w.writeheader()
  for r in semantic:w.writerow({'id':r['id'],'codigo':r['codigo'],'resultado_esperado':r['resultado_esperado'],'controle_sintatico_observado':r['estado_sintatico_observado'],'avaliacao_semantica':'pendente; não implementada'})
 print('RESUMO',ap,'/',total,'aprovados;',execu,'executados; semântica0/3',flush=True)
 return int(ap!=total)

if __name__=='__main__':raise SystemExit(main())
