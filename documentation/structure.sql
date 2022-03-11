create table Role
(
    rid        serial
        constraint role_pk
            primary key,
    type       varchar(20) not null,
    created_at timestamptz not null,
    updated_at timestamptz not null
);

create unique index role_rid_uindex
    on Role (rid);

create unique index role_type_uindex
    on Role (type);



create table Organization
(
    oid        serial
        constraint organization_pk
            primary key,
    name       varchar(100) not null,
    created_at timestamptz  not null,
    updated_at timestamptz  not null
);

create unique index organization_oid_uindex
    on Organization (oid);

create unique index organization_name_uindex
    on Organization (oid);



create table Users
(
    uid        serial
        constraint user_pk
            primary key,
    first_name varchar(50)  not null,
    last_name  varchar(50)  not null,
    email      varchar(250) not null,
    created_at timestamptz  not null,
    updated_at timestamptz  not null,
    rid        int          not null
        constraint rid
            references role,
    oid        int          not null
        constraint oid
            references organization
);

create unique index user_email_uindex
    on Users (email);

create unique index user_uid_uindex
    on Users (uid);



create table Category
(
    cid        serial
        constraint category_pk
            primary key,
    name       varchar(50) not null,
    created_at timestamptz not null,
    updated_at timestamptz not null
);

create unique index category_cid_uindex
    on Category (cid);

create unique index category_name_uindex
    on Category (name);



create table Model
(
    mid         serial
        constraint model_pk
            primary key,
    name        varchar(100) not null,
    source      varchar(250) not null,
    uploaded_at timestamptz  not null,
    uid         int          not null
        constraint uid
            references users
);

create unique index model_mid_uindex
    on Model (mid);



create table Optimization_Details
(
    odid        serial
        constraint optimization_details_pk
            primary key,
    information varchar(250) not null,
    detail      varchar(250) not null,
    created_at  timestamptz  not null,
    mid         int          not null
        constraint mid
            references Model,
    cid         int          not null
        constraint cid
            references Category
);

create unique index optimization_details_odid_uindex
    on Optimization_Details (odid);



create table Benchmarking_Details
(
    bdid        serial
        constraint benchmarking_details_pk
            primary key,
    information varchar(250) not null,
    detail      varchar(250) not null,
    created_at  timestamptz  not null,
    mid         int          not null
        constraint mid
            references Model,
    cid         int          not null
        constraint cid
            references Category
);

create unique index benchmarking_details_bdid_uindex
    on Benchmarking_Details (bdid);