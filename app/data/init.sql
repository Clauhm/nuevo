-- Crear una base de datos llamada data_bank
CREATE DATABASE data_bank;

-- Conectar a la base de datos data_bank
\c data_bank;

-- Eliminar la tabla accounts si ya existe
DROP TABLE IF EXISTS accounts; 

-- Crear la tabla accounts con los siguientes campos
CREATE TABLE accounts(
    account_no TEXT,
    date DATE,
    transaction_details TEXT,
    withdrawal_amt FLOAT,
    deposit_amt FLOAT,
    balance_amt FLOAT
);

-- Ajustar el formato de fecha a día/mes/año
SET datestyle = 'DMY';

-- Cargar datos desde un archivo CSV a la tabla accounts
\copy accounts(account_no, date, transaction_details, withdrawal_amt, deposit_amt, balance_amt) FROM '/docker-entrypoint-initdb.d/datanueva.csv'  DELIMITER ','  CSV HEADER;