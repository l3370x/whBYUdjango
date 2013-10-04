<?PHP
$mysqli = new mysqli("db492851746.db.1and1.com", "dbo492851746", "wafflepassword", "db492851746");

$mysqli->query('insert into teacher_teacher values(1,2,"Richard","Miller","rick@calmriver.com")');

$mysqli->close();
?>
