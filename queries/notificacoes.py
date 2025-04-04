def import_notioficacoes_civel():
    query = r"""
SELECT 
    sub_query.pasta_id,
	sub_query.data,
	sub_query.prazo_final,
	sub_query.responsavel,
	sub_query.conteudo,
	sub_query.evento
FROM (
	SELECT 
		notif_email.id,
		gcpj,
		pasta_id,
		data,
		notif_email.tipo_de_anexo AS "email_tipo_anexo",
		regra_tipo_anexo.tipo_de_anexo AS "regra_tipo_anexo",
		pastas.responsavel AS "pasta_responsavel",
		regras_civel.responsavel_pasta AS "regra_responsavel",
		regras_civel.responsavel_tarefa,
		CASE 
			WHEN regra_tipo_anexo.tipo_de_anexo = 'INTIMACAO' THEN 'Guilherme claudino D`Alécio'
			WHEN pastas.responsavel = 'Fernando Augusto Ogura' THEN 'lorenzo Pedrotti Cadorin'
			WHEN (pastas.responsavel IS NULL) OR (pastas.responsavel = '') THEN 'lorenzo Pedrotti Cadorin'
			WHEN regra_tipo_anexo.tipo_de_anexo = 'REVISAR' THEN regras_civel.responsavel_tarefa
			ELSE regras_civel.responsavel_tarefa
		END AS "responsavel",
		regra_tipo_anexo.evento,
		CONCAT('NOTIFICAÇÃO DE INCLUSÃO DE ANEXO NO GCPJ, DO TIPO => ', regra_tipo_anexo.tipo_de_anexo, ' <= DO DIA ', notif_email.data) AS "conteudo",
		CURRENT_DATE AS "prazo_final",
		status_importacao,
		pastas.carteira,
		regras_civel.carteira
	FROM 
		civel_matriz.email_notificacoes_gcpj AS "notif_email"
	LEFT JOIN 
		autojur.pastas AS "pastas" ON notif_email.gcpj = pastas.localizador
	LEFT JOIN 
		civel_matriz.regra_notificacoes_civel AS "regras_civel" ON pastas.responsavel = regras_civel.responsavel_pasta AND pastas.carteira = regras_civel.carteira
	LEFT JOIN 
		civel_matriz.regra_notificacao_tipo_de_anexo AS "regra_tipo_anexo"  ON notif_email.tipo_de_anexo = regra_tipo_anexo.tipo_de_anexo
	WHERE 
		status_importacao IS NULL
		AND 
		pastas.tipo_de_pasta = 'JUDICIAL CíVEL'
		AND 
		pastas.numero_subpasta = '0'
		AND
		(NOT (LOWER(notif_email.assunto) LIKE '%reporte%') OR (notif_email.assunto IS NULL))
	) AS "sub_query"
	WHERE 
		sub_query.responsavel IS NOT NULL 
		AND 
		sub_query.evento IS NOT NULL 
    LIMIT 10

    """
    return query