create table if not exists user
(
    id integer primary key,
    invites integer,
    timezone integer,
    invite_permission boolean,
    allow_ping boolean,
    language text
);

create table if not exists invite
(
    id text primary key,
    created_at datetime,
    expires_at datetime,
    max_uses integer,
    url text,
    user_id integer not null,
    foreign key (user_id)
    references user (id)
        on update restrict
        on delete restrict
);

create table if not exists ping_rule (
    id integer primary key autoincrement,
    start datetime,
    end datetime,
    creation_time text,
    user_id integer not null,
    foreign key (user_id)
    references user (id)
        on update restrict
        on delete restrict
);
