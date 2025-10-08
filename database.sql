CREATE TABLE student (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    nameclass VARCHAR(255) NOT NULL,
    note FLOAT
);
 
CREATE TABLE classroom (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nameclass VARCHAR(255) NOT NULL,
    course VARCHAR(255) NOT NULL
);


INSERT INTO classroom (nameclass, course)
VALUES ('SRI2015', '2015'),('SRI2016', '2016'),('SRI2017', '2017'),('SRI2018', '2018'),('SRI2019', '2019'),('SRI2020', '2020'),('SRI2021', '2021'),('SRI2022', '2022');

INSERT INTO student (name, surname, nameclass, note)
VALUES ('Javier',"Garcia","SRI2015", 2.5),('Javier',"Garcia","SRI2016", 5.5),('Jose',"Perez","SRI2017", 7.5),('Juan',"Gomez","SRI2018", 8.5),('Andrea',"Tubo","SRI2019", 9.5);
