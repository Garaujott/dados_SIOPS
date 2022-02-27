*import_receitas

foreach i in "2019"  {
	import delimited "data\\`i'\OutrosFormatos\csv\Receita\Estadual - Receitas de `i'.csv", case(preserve) clear
	
	do "do_files/labels_receitas.do"
	
	save "data\\`i'\OutrosFormatos\dta\Receita\Estadual - Receitas de `i'.dta", replace

}
