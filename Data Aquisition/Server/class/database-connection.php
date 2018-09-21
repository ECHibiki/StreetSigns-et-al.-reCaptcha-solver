<?php

class DatabaseConnection{
	
	private $sql_data = array();
	protected $connection = null;
	
	public $delete_status = false;
	
	public $path_prefix="";
	
	public $alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p","q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
	
	function __construct($path_prefix = ""){
		$this->path_prefix = $path_prefix;
		$sql_ini = fopen($path_prefix . "settings/sql.ini", "r");
		if(!$sql_ini) $sql_ini = fopen($path_prefix . "$path_prefix/settings/sql.ini", "r");
		while(!feof($sql_ini)){
			$line = fgets($sql_ini);
			$key = substr($line, 0, strpos($line, "="));
			$value = trim(substr($line, strpos($line, "=")+1));
			$this->sql_data[$key] = $value;
		}
		$this->connectToDatabase();
	}
	
	function connectToDatabase(){	
		try {
            $this->connection = new PDO ("mysql:dbname=" . $this->sql_data["database"] . ";host=" . $this->sql_data["connection"],
												$this->sql_data["user"], 	$this->sql_data["pass"]);
			$this->connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        } catch (PDOException $e) {
            $this->logsys .= "Failed to get DB handle: " . $e->getMessage() . "\n";
			$err_file = fopen('error_log', 'a+');
			fwrite($err_file, time() . " : Failed to get DB handle: " . $e->getMessage() . "\n");
        }
	}
	
	function getConnection(){
		return $this->connection;
	}
	
	function addToTable($tablename, $paramaters){
		$param_len = sizeof($paramaters);
		$bind_string = "";
		$table_string= "";
		$first_comma = false;
		foreach($paramaters as $key => $param){
			if(!$first_comma){
			$bind_string = ":$key";
			$table_string = "`$key`";
			$first_comma = true;
			}
			else{
				$bind_string .= ",:$key";
				$table_string .= ",`$key`";
			} 
		}
		$statement = $this->connection->prepare("INSERT INTO `".$this->sql_data["database"] ."`.`$tablename`($table_string) VALUES(" . $bind_string . ")");
	
		$index = 0;
		foreach($paramaters as $key => $param){
			$success =	$statement->bindParam(":" . $key , $paramaters[$key]);
			$index++;
		}
		try{
			$statement->execute();
		}catch(Exception  $e){
		   echo "<strong>" . $e->getMessage() . "</strong><br/>";
			$err_file = fopen('error_log', 'a+');
			fwrite($err_file, time() . " :".  $e->getMessage() . "\n");
		}	
	}
	
	function deleteFromTable($table, $refining_paramater, $bind_val){
		$statement = $this->connection->prepare("DELETE FROM `$table` WHERE `$table`.`$refining_paramater` = :bindval");
		$statement->bindParam(":bindval", $bind_val);
		try{
			$response = $statement->execute();
		}catch(Exception  $e){
		   echo "<strong>" . $e->getMessage() . "</strong><br/>";
		}	
	}
	
	function getPostDetails($table, $refining_paramater, $bind_val){
		$statement = $this->connection->prepare("SELECT * FROM `$table` WHERE `$table`.`$refining_paramater` = :bindval");
		$statement->bindParam(":bindval", $bind_val);
		try{
			$response = $statement->execute();
			return $statement->fetchAll();
		}catch(Exception  $e){
		   echo "<strong>" . $e->getMessage() . "</strong><br/>";
		   			$err_file = fopen('error_log', 'a+');
			fwrite($err_file, time() . " :".  $e->getMessage() . "\n");
		}	
	}
	
	function updatePost($table, $table_search, $table_search_value, $keyed_params){
		$first_entry = true;
		$set_string = "";
		foreach($keyed_params as $key=>$value){
			if($first_entry){
				$set_string = "$key=:$key";
			}
			else $set_string .= ",$key=:$key";
		}
		
		$statement = $this->connection->prepare("UPDATE `$table` SET $set_string WHERE $table_search=:param_to_find");		
		$statement->bindParam(":param_to_find", $table_search_value);
		
		foreach($keyed_params as $key=>$value){
			$statement->bindParam(":$key", $value);
		}
		
		try{
			$response = $statement->execute();
		}catch(Exception  $e){
		   echo "<strong>" . $e->getMessage() . "</strong><br/>";
		   			$err_file = fopen('error_log', 'a+');
			fwrite($err_file, time() . " :".  $e->getMessage() . "\n");
		}	
	}
	
	function getFullTable($table){
		$statement = $this->connection->prepare("SELECT * FROM `$table`");
		try{
			$response = $statement->execute();
			return $statement->fetchAll();
		}catch(Exception  $e){
		   echo "<strong>" . $e->getMessage() . "</strong><br/>";
		}	
	}
}

?>