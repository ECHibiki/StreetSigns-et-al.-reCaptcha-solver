<html>
<head>
<?php
	echo "<script>
	function activateData(element){
			var data_inputs = document.getElementById('data-inputs').getElementsByTagName('INPUT');
			for (var box = 0 ; box <  data_inputs.length ; box++){
				data_inputs[box].checked = element.checked;
		}
	}</script>"
?>
</head>
<body>
<?php echo "<pre>";
	if(sizeof($_POST) == 0){
		echo "<form method='POST' target='_self'>";
		echo "<label><input onclick='activateData(this)' type='checkbox' name='all'>Select All</label>";
		echo "<hr/>";
		echo "<div id='data-inputs'>";
		$data_dir = scandir("data");
		foreach($data_dir as $index=>$dir){
			if($index > 1 && $dir != "test" && gettype(strpos($dir, 'error')) == 'boolean'){ //skip junk paths
				echo "<label><input type='checkbox' name='$dir'>$dir</label><br/>";
			}
		}
		echo "</div>";
		echo "<hr/>";
		echo "<label><input type='checkbox' name='small'>Small Images</label><br/>";
		echo "<label><input type='checkbox' name='large'>Large Images</label><br/>";
		echo "<hr/>";
		echo "Training Percentage: <span id='trainperc'>80%</span><br/>0<input type='range' style='width:15%' name='train' id='train' max='100' min='0' value='80'>100<br/>";
		echo "Valid Percentage: <span id='validperc'>10%</span><br/>0<input type='range' style='width:15%' name='valid' id='valid' max='100' min='0' value='10'>100<br/>";
		echo "Test Percentage: <span id='testperc'>10%</span><br/>0<input type='range' style='width:15%' name='test' id='test' max='100' min='0' value='10'>100<br/>";
		echo "<hr/>";
		echo "<input type='submit'></input>";
		echo "</form>";
		echo "<script>
		document.getElementById('train').addEventListener('change', function(elem){
			document.getElementById('trainperc').textContent = elem.target.value + '%';
		});
		document.getElementById('valid').addEventListener('change', function(elem){
			document.getElementById('validperc').textContent = elem.target.value + '%';
		});
		document.getElementById('test').addEventListener('change', function(elem){
			document.getElementById('testperc').textContent = elem.target.value + '%';
		});
		</script>";
	}
	else{
		// var_dump($_POST);
		if(intval($_POST['train']) + intval($_POST['valid']) + intval($_POST['test']) > 100){
			exit("Data percentages don't add up to 100%");
		}
		$train_files = array();
		$valid_files = array();
		$test_files = array();
		foreach($_POST as $directory=>$active){
			if($directory == 'all' || $directory == 'small' || $directory == 'large' || $directory == 'train' || $directory == 'valid' || $directory == 'test' ) continue;
			$directory = str_replace("_", " ", $directory);
			$file_dir = scandir("data/$directory");
			$added_count = 0;
			$train_qnt = (int)(sizeof($file_dir) * (intval($_POST['train']) / 100));			
			$valid_qnt = (int)(sizeof($file_dir) * (intval($_POST['valid']) / 100));	
			$test_qnt = (int)(sizeof($file_dir) * (intval($_POST['test']) / 100));
			shuffle($file_dir);		
			foreach($file_dir  as $index=>$file){
				if(!($file == "." || $file == "..")){ //skip junk paths
					$add = false;
					if(!isset($_POST["large"]) && !$_POST["small"]){
						$add = true;
					}
					else if($_POST["large"] == "on" && gettype(strpos($file, ';')) != 'boolean'){
						$add = true;
					}	
					else if($_POST["small"] == "on" && gettype(strpos($file, ';')) == 'boolean'){
						$add = true;
					}
					if($add){
						$added_count++;	
						if($added_count > $valid_qnt + $test_qnt) array_push($train_files,"data/$directory/$file");
						else if($added_count > $test_qnt) array_push($valid_files,"data/$directory/$file");
						else if($added_count > 0) array_push($test_files,"data/$directory/$file");
					}		
				}
			}
		}
		if(sizeof($train_files) + sizeof($valid_files) + sizeof($test_files) == 0){
			exit("Nothing found<br/>");
		}
		else{
			$image_zip = new ZipArchive();
			$zip_file="archives/CaptchaArchive.zip";
			if(file_exists($zip_file))
				unlink($zip_file);
				
			if ($image_zip->open($zip_file, ZipArchive::CREATE)!==TRUE) {
				exit("cannot open <$file>\n");
			}
			foreach($test_files as $file){
				$image_zip->addFile($file, "data/test/" . substr($file,5)); // take directory without data as path
			}
			foreach($valid_files as $file){
				$image_zip->addFile($file, "data/valid/" . substr($file,5));
			}
			foreach($train_files as $file){
				$image_zip->addFile($file, "data/train/" . substr($file,5));
			}
			$image_zip->close();
			echo "<a download='$zip_file' href='$zip_file' id='dl' style='display:none'>Download archive</a>";
			echo "<script>document.getElementById('dl').click();</script>";
			echo "<h4>File will autodownload</h4>";
		}
	}

?>
</body>
</html>