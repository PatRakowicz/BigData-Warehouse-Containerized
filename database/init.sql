create table fred_data (
	id int auto_increment primary key,
	indicator varchar(20),
	date date,
	value decimal(15, 4),
	unique(indicator, date)
);
