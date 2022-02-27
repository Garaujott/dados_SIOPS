*import_despesas_2018


foreach i in "2018" "2019" "2020" {

	foreach j in "1 - Recursos Ordinários - Fonte Livre" "2 - Receitas de Impostos e Transferencias de Impostos" "3 - Transferência Fundo a Fundo de Recursos do SUS Provenientes do Governo Federal" "4 -Transferência Fundo a Fundo de Recursos do SUS Provenientes do Governo Estadual" "5 - Transferência de Convênios ou de Contratos de Repasse Vinculados à Saúde" "6 - Operações de Crédito Vinculadas à Saúde" "7 - Royalties de Petróleo Vinculadas à Saúde" "8 - Outros Recursos Vinculados à Saúde" {
	
		foreach k in "301 - Atenção Basica" "302 - Assistência Hospitalar Ambulatorial" "303 - Suporte Profilático Terapêutico" "304 - Vigilância Sanitária" "305 - Vigilância Epidemiológica" "306 - Alimentação e Nutrição" "Administrativas" "Informações Complementares"{
			import delimited "data\\`i'\OutrosFormatos\csv\Despesa\\`j'\\`k'.csv", case(preserve) clear
	
			do "do_files/labels_despesas.do"
	
			save "data\\`i'\OutrosFormatos\dta\Despesa\\`j'\\`k'.dta", replace
		}
	}		
}