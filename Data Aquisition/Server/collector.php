<?php 	
require('class/database-connection.php');	
if($_POST['type'] == null){
	function nameToInt($name){
		return intval(substr(base_convert($name, 16,10),0,18));
	}

	$database = new DatabaseConnection();
	$uploaders = $database->getFullTable('UploadCounter');
	$uploader_numbers = array();
	foreach($uploaders as $index=>$uploader){
		array_push($uploader_numbers, nameToInt(hash("md5", $uploader['name'])));
	}
 
	//Head
	echo "<html><head>
	<script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.bundle.js'></script>
	<script src='scripts/origami.min.js?" . time() . "'></script>
	<script src='https://cdn.plot.ly/plotly-latest.min.js'></script>
	<script src='https://code.jquery.com/jquery-3.2.1.slim.min.js' integrity='sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN' crossorigin='anonymous'></script>
	<script src='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js' integrity='sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q' crossorigin='anonymous'></script>
	<script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js' integrity='sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl' crossorigin='anonymous'></script>
		
	<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css' integrity='sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm' crossorigin='anonymous'></head><body>";
	
	//Jumbotron
	echo "<div class='jumbotron pt-3'>
		<h3 class='display-4'>Data Statstics</h3>
		<a href='captcha-acquisition.user.js?" . time() ."'>From the captcha logging script</a><br/>
		<a href='retrieve'>Download Files</a>
	</div>";
	
	//Data distribution - plot.ly
	$top_dir = scandir("data");
	$data_stats = array();
	foreach($top_dir as $dir){
		if($dir != "." && $dir != ".." && $dir != "test" && gettype(strpos($dir, "error")) == 'boolean'){
			$sub_dir = scandir("data/$dir");
			array_push($data_stats, ["category"=>$dir, "count"=>(sizeof($sub_dir) - 2)]);
		}
	}
	echo '
	  <div id="directory-item-pie" class="w-75"></div>
		  <script>
			var data = [{
		  values: [';
		  
		foreach($data_stats as $index=>$data_stat){
			$data_stat_count = $data_stat['count'];
			if($index == 0) echo "'$data_stat_count'";
			else echo ",'$data_stat_count'";
		}

		  echo '],
		  labels: [';
		  
		foreach($data_stats as $index=>$data_stat){
			$data_stat_type = $data_stat['category'];
			if($index == 0) echo "'$data_stat_type'";
			else echo ",'$data_stat_type'";
		}
		  
		  echo'],
		  type: "pie"
		}];

		Plotly.newPlot("directory-item-pie", data);
  </script>';
	
	//Count Canvas(chart Js)
	echo "<div style='width:50%'>
		<canvas id='count-canvas' width='400' height='400'></canvas>
		<script>
		var ctx = document.getElementById('count-canvas').getContext('2d');
		var count = new Chart(ctx, {
			type: 'bar',
			data: {
				labels: [";
				foreach($uploaders as $index=>$uploader){
					$uploader_name = $uploader['name'];
					if($index == 0) echo "'$uploader_name'";
					else echo ",'$uploader_name'";
				}
				
			echo "],
				datasets: [{
					label: '# of Uploads',
					data: [";
					
				foreach($uploaders as $index=>$uploader){
					$uploader_count = $uploader['count'];
					if($index == 0) echo "'$uploader_count'";
					else echo ",'$uploader_count'";
				}
					
				echo	"],
					backgroundColor: [";
					
				foreach($uploader_numbers as $index=>$uploader_number){
					$uploader_rgba = "rgba(" . $uploader_number % 255 . "," . ($uploader_number / 10) % 255 . "," . ($uploader_number / 100) % 255  .",0.2)";
					if($index == 0) echo "'$uploader_rgba '";
					else echo ",'$uploader_rgba'";
				}
						
				   echo "],
					borderColor: [";
					foreach($uploader_numbers as $index=>$uploader_number){
						$uploader_rgba = "rgba(" . ($uploader_number / 1000) % 255 . "," . ($uploader_number / 10000) % 255 . "," . ($uploader_number / 100000) % 255  .",0.2)";
						if($index == 0) echo "'$uploader_rgba '";
						else echo ",'$uploader_rgba'";
					}
				   echo "],
					hoverBackgroundColor: [" ;
					foreach($uploader_numbers as $index=>$uploader_number){
						$uploader_rgba = "rgba(" . ($uploader_number / 1000000) % 255 . "," . ($uploader_number / 10000000) % 255 . "," . ($uploader_number / 1000000000) % 255  .",0.2)";
						if($index == 0) echo "'$uploader_rgba '";
						else echo ",'$uploader_rgba'";
					}
				echo "],
					borderWidth: 1
				}]
			},
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero:true
						}
					}]
				}
			}
		});
		</script>";
	//toal count
	$total = 0;
	foreach($uploaders as $uploader){
		$total += intval($uploader["count"]);
	}
	echo "<p> Total: $total</p></div>";
	
	//daily count history graph - origami js
	$dates = $database->getFullTable('UploadByDate');
	echo '<div class="w-700">
		<canvas width="1000" height="1000" id="history-canvas" class="img-fluid"></canvas>
		<script>
origami("#history-canvas")
  .chartLine({
    labels: [';
	
	foreach($dates as $index=>$daily){
		$date = $daily['date'];
		if($index == 0) echo "'$date'";
		else echo ",'$date'";
	}
	
	echo '],
    fill: true,
	animation: "---fade",
    datasets: [
      {
        data: [';
		
	foreach($dates as $index=>$daily){
		$date_count = $daily['count'];
		if($index == 0) echo "'$date_count'";
		else echo ",'$date_count'";
	}	
	
	echo '],
        points: true,
        pointsColor: "purple",
        line: "4px dotted purple",
      }
    ]
  }).draw();
		</script></div>';
	echo date('Y-m-d');
	
	echo "</body></html>";
		
	}
	
	
	
	
	
	else{
		
		foreach($_POST as &$field){
			$field = rawurldecode($field);
		}
		
		$upload_count = 0;
		
		if($_POST['type'] == 'full'){
			$filename = hash('sha256', $_POST['package']) . '-' . time() . ';' . $_POST['hits']; 
			$img_file = fopen('data/' . $_POST['challenge'] . "/$filename.jpg", 'w');
			if(!$img_file){
				$err_file = fopen('error_log', 'a+');
				fwrite($err_file, time() . " : Couldn't add " . 'data/' . $_POST['challenge'] . "/$filename.jpg --- F\n");
				fclose($err_file);
				$img_file = fopen('data/errorF' . "/$filename.jpg", 'w');
			} 
			fwrite($img_file, base64_decode($_POST['package']));		
			fclose($img_file);			
			$upload_count++;
		}
		else if($_POST['type'] == 'partial'){
			$_POST['package'] = explode(",", $_POST['package']);
			foreach($_POST['package'] as $package){
				$filename = hash('sha256', $package) . '-' . time(); 
				$img_file = fopen('data/' . $_POST['challenge'] . "/$filename.jpg", 'w');
				if(!$img_file){
					$err_file = fopen('error_log', 'a+');
					fwrite($err_file, time() . " : Couldn't add " . 'data/' . $_POST['challenge'] . "/$filename.jpg --- P\n");
					fclose($err_file);
					$img_file = fopen('data/errorP' . "/$filename.jpg", 'w');
				} 
				fwrite($img_file, base64_decode($package));
				fclose($img_file);
				$upload_count++;
			}
		}

		$database = new DatabaseConnection();
		//update per person
		$uploader = $database->getPostDetails('UploadCounter', 'name', $_POST['name'])[0];
		if($uploader != null){
			$database->updatePost('UploadCounter','name', $_POST['name'], ['count'=> ($uploader['count'] + $upload_count)]);
		}
		else{
			$database->addToTable('UploadCounter', ['name'=>$_POST['name'], 'count'=> $upload_count]);
		//update per date
		}	
		$the_date = date('Y-m-d');
		$daily = $database->getPostDetails('UploadByDate', 'date',$the_date)[0];
		if($daily != null){
			$database->updatePost('UploadByDate','date', $the_date, ['count'=> ($daily['count'] + $upload_count)]);
		}
		else{
			$database->addToTable('UploadByDate', ['date'=>$the_date, 'count'=> $upload_count]);
		}	
		$database = null;
}
	
?>