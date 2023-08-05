$("input[name='select_all']").on("click", sellect_all);
$("input[name*='date']").datepicker({dateFormat:'yy-mm-dd',});
function sellect_all(){
  var to_select = this.checked;
  documentos = $("input[type='checkbox'][name='venta']");
  documentos.each(function(){
    this.checked = to_select;
  });
}

$("#btn_generar_factura").on("click", function(){
	var documentos_selecionados = $("input[type='checkbox'][name='venta']:checked").map(function() {return this.value;}).get();
	if (documentos_selecionados.length > 0) {
		$("#btn_generar_factura").attr("disabled","disabled");
		// debugger;
		$.ajax({
			url:'/factura_global_app/generar_factura_global', 
			type : 'get', 
			data:{
				'documentos':documentos_selecionados,
			}, 
			success: function(data){ 
				if (data.error == '') {
					$.ajax({
						url:'/factura_global_app/generar_venta_factura', 
						type : 'get', 
						data:{
							'factura_id':data.factura_id,
							'reporte_id':data.reporte_id,
						}, 
						success: function(data){

							if (data.error != '') {
								location.reload(true);							
							}
							else{
								alert(data.error);
							};
						},
						error: function() {
							$("#btn_generar_factura").attr("disabled",false);
							location.reload(true);
					  	},
					});
					
				}
				else{
					alert(data.error);
					$("#btn_generar_factura").attr("disabled",false);
				};
			},
			error: function() {
				// alert("fallo algo");
				// $("#btn_generar_factura").attr("disabled",false);
				location.reload(true);
		  	},
		});

	}else{
		alert("Seleciona almenos un documento");
	}
});
