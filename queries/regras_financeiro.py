

def query_filtro_bradesco(filtro):
    query = f"""
SELECT
    -- PASTAS
    pastas.pasta_id,
    localizador,
    grupo_empresarial,
    cliente_principal,
    tipo_de_pasta,
    numero_subpasta,
    numero_processo,
    numero_cnj,
    parte_contraria,
    orgao_julgador,
    cidade,
    COALESCE(carteira, 'NÃO INFORMADO'),
    COALESCE(portfolio, 'NÃO INFORMADO'),
    portfolio,
    rito,
    COALESCE(motivo_situacao, 'NÃO INFORMADO'),
    tag_controle_grupo,
    valor_condenacao,
    valor_realizado,
    valor_sentenca,
    valor_da_causa,
    valor_acordo,
    valor_alcada,
    valor_honorario,
    valor_provisao,
    valor_realizado, -- Era valor cadastro
    data_encerramento,
    data_recebimento,
    pastas.situacao,
    fase,
    modalidade,
    negociacao_referencia,
    assunto_resumo,
    classf.classificacao_de_servico,
    
    -- TAREFAS 
    tarefas.tarefa_id,
    conteudo,
    evento,
    tarefas.situacao,
    prazo_final,
    data_de_lancamento,
    data_de_atualizacao,
    tipo_evento,
    solicitante,
    tarefas.responsavel,
    COALESCE(data_de_atualizacao, data_de_lancamento) AS data_filtro_tarefas,
    
    -- Financeiro da pasta 
    financeiro_id,
    tipo_plano_contas,
    plano_de_contas,
    documento,
    descricao as "descricao_lancamento",
    financeiro.situacao as "situacao_financeiro",
    data_competencia,
    data_transacao,
    data_referencia,
    valor as "valor_base",
    valor_previsto,
    valor_pago,
    valor_liquido,
    data_vencimento
    
FROM 
    autojur_v2.pastas
LEFT JOIN 
    autojur.pasta_classificacao_servico AS classf 
    ON classf.pasta_id::integer = pastas.pasta_id
RIGHT JOIN -- para ficar só o lado das tarefas
    autojur_v2.tarefas tarefas ON tarefas.cod_pasta = pastas.pasta_id
LEFT JOIN 
    autojur_v2.financeiro_da_pasta financeiro ON financeiro.pasta_id = pastas.pasta_id
    
WHERE 
    --- FILTRO DE PASTAS
    tipo_de_pasta = 'JUDICIAL CíVEL'
    AND grupo_empresarial = 'GRUPO BRADESCO'
    AND (
        (	--- NESSE FILTRO BUSCAMOS PELOS PROCESSOS ANTIGOS DA CLASSIFICACAO 4785
            classf.classificacao_de_servico = '4785 - GES.PROC.JUD.TERCEIR'
            AND carteira != 'PROCESSOS ADMINISTRATIVOS'
            AND data_cadastro < '2024-09-02'
        )
        OR
        (	--- NESSE FILTRO BUSCAMOS PELOS PROCESSOS ANTIGOS EM QUE A CLASSIFICAÇÂO É DIFERENTE DO GRUPO 4785
            classf.classificacao_de_servico != '4785 - GES.PROC.JUD.TERCEIR' 
            OR classf.classificacao_de_servico IS NULL
        )
    )
    AND NOT ( --- REMOVEMOS AS LINHAS EM QUE SÂO PROCESSOS ADMINISTRATIVOS E >= QUE 02-09-2024
        carteira = 'PROCESSOS ADMINISTRATIVOS'
        AND data_cadastro >= '2024-09-02'
    ) -- FINALIZA FILTRO E PASTAS
    
    --- FILTROS REALIZADOS NO SCRIPT BRD02_Faturamento Bradesco Cível_v7.R
    AND 
    prazo_final >= '2024-09-01'
    AND 
    numero_subpasta = '0'
    AND 
    tarefas.situacao = 'FINALIZADA'
    AND
    tarefas.tarefa_id IN ('8041062', '8307695', '8041274', '8097789', '8208419', '8158499', '8208422', '8121640', '8110032', '8123174')
    {filtro}
    """
    return query


def query_regras_anorarios():
    query = """
    -- Essa tabela vai retornar os anorarios que estão no script do R
    SELECT id, campo, valor FROM financeiro.bradesco_honorarios
    """
    return query

def query_rules():
    query = """
SELECT 
    r.id,
    r.name,
    r.description,
    r.contract,
    r.obs,
    r.verba,
    r.data_financeiro,
    r.valor_base,
    r.valor_liquido,
    r.descricao_extra,
    r.plano_de_contas,
    json_object_agg(
        rf.column_name,
        json_build_object('operator', rf.operator, 'value', rf.value)
    ) AS filtros
FROM financeiro."rule" r
LEFT JOIN financeiro.rule_filter rf ON rf.rule_id = r.id
GROUP BY r.id, r.name, r.description, r.contract, r.obs, r.verba, r.data_financeiro, r.valor_base, r.valor_liquido, r.descricao_extra, r.plano_de_contas;
 """
    return query

