$(document).ready(()=>{

	$("#submit").click(()=>{
		var list = $("li");
		var input_dict = {};
		var website = {};


		//Get the url
		var homepage = $($(list[0]).children("input")[0]).val();


		//Create the input_dictionary
		for (var i = 1; i < (list.length - 1); i++) {
			var id = $(list[i]).attr("id");
			var inputs = $(list[i]).children("input");
			var finder = $(inputs[1]).val();

			var dict = {};
			dict["element"] = $(inputs[0]).val();
			dict[$(inputs[1]).val()] = $(inputs[2]).val();


			input_dict[id] = [dict]
		}


		//Create the final object to export
		website["homepage"] = homepage;
		website["input_dict"] = input_dict;
		website["lastmod"] = "2000-01-01" //Just set to ages ago to get all the urls


		//Send to php page to write to file
		$.post("export.php",
			website,
			function(data, status){
				alert("Data: " + data + "\nStatus: " + status);
			}
		);
	});

});