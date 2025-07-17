-- ==================================================
-- Filename : setup.sql
-- Author : CRESP Enguerran
-- Motor : SQLite
-- Rôle : setup all Tables needed for the app / Recycle them
-- Last Update : 06/07/2025
-- ==================================================

create table META_Fournisseurs(
    ID_Fournisseur integer primary key autoincrement,
    name varchar(255) not null,
    email varchar(255) not null,
    location varchar(512) not null
);

create table META_Mesures(
    ID_Mesure integer primary key autoincrement,
    unit_type varchar(10) unique not null
);

create table META_Mesures_Conversion(
    ID_Mesures_Conversion integer primary key autoincrement,
    unit_base number not null references META_Mesures(ID_Mesure),
    unit_dest number not null references META_Mesures(ID_Mesure),
    multiplier float not null
);


create table META_Ingredients (
    ID_Ingredient integer primary key autoincrement,
    name varchar(64) not null,
    primary_unit number not null references META_Mesures(ID_Mesure),
    secondary_unit number not null references META_Mesures(ID_Mesure),
    fournisseur number not null references META_Fournisseurs(ID_Fournisseur)
);