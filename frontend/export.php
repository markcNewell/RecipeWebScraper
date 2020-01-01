<?php

	$filename = "../websites.json"


	$jsonText = $_POST;
	$decodedText = html_entity_decode($jsonText);
	$posted_data = json_decode($decodedText);


	$data = json_decode(file_get_contents($filename), true);


	array_push($data, $posted_data);
	$return = file_put_contents($filename, $data);

	if ($return === False) {
		echo "Error writing to file";
	}
	else {
		echo "Success";
	}

?>