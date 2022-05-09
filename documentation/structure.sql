create table Organization
(
    oid        serial
        constraint organization_pk
            primary key,
    name       varchar(100) not null,
    created_at timestamptz  not null,
    updated_at timestamptz  not null,
    owner_id         int          not null
    constraint uid
        references users
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
    updated_at timestamptz  not null
);

create unique index user_email_uindex
    on Users (email);

create unique index user_uid_uindex
    on Users (uid);



create table Model
(
    mid         serial
        constraint model_pk
            primary key,
    name        varchar(100) not null,
    source      varchar(250) not null,
    uploaded_at timestamptz  not null,
    type        varchar(15)  not null,
    uid         int          not null
        constraint uid
            references users,
    oid        int
        constraint oid
            references organization
);

create unique index model_mid_uindex
    on Model (mid);



create table Model_Results
(
    rid         serial
        constraint model_results_pk
            primary key,
    type        varchar(20)  not null,
    information varchar(250) not null,
    detail      TEXT         not null,
    created_at  timestamptz  not null,
    mid         int          not null
        constraint mid
            references Model
);

create unique index model_results_rid_uindex
    on Model_Results (rid);



create table Model_Task
(
    tid        varchar(155)
        constraint model_task_pk
            primary key,
    type       varchar(20) not null,
    queue      varchar(10) not null,
    created_at timestamptz not null,
    mid        int         not null
        constraint mid
            references Model
);

create unique index model_task_tid_uindex
    on Model_Task (tid);


create table user_organizations
(
    uoid       serial
        constraint user_organizations_pk
            primary key,
    oid        int                not null
        constraint user_organizations_organization_oid_fk
            references organization,
    email      varchar(250)       not null,
    accepted   bool default False not null,
    created_at timestamptz        not null,
    updated_at timestamptz        not null
);

create unique index user_organizations_uoid_uindex
    on user_organizations (uoid);