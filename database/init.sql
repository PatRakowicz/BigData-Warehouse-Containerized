create table if not exists fred_data (
	id int auto_increment primary key,
	indicator varchar(20),
	date date,
	value decimal(15, 4),
	unique(indicator, date) -- Prevents dupe records of the indicator
);
