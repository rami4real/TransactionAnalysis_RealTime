CREATE EXTERNAL TABLE fraude (
      Unnamed_0 INT,
      trans_date_trans_time STRING,
      cc_num BIGINT,
      merchant STRING,
      category STRING,
      amt DOUBLE,
      first STRING,
      last STRING,
      gender STRING,
      street STRING,
      city STRING,
      state STRING,
      zip INT,
      lat DOUBLE,
      long DOUBLE,
      city_pop INT,
      job STRING,
      dob STRING,
      trans_num STRING,
      unix_time BIGINT,
      merch_lat DOUBLE,
      merch_long DOUBLE,
      is_fraud INT
  )
  ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ',' 
  LINES TERMINATED BY '\n' 
  LOCATION '/kafka_ingestion/csv_files'
  TBLPROPERTIES ("skip.header.line.count"="1");