create table if not exists user
(
    userId integer primary key,
    invites integer not null,
    timezone integer not null,
    invitePermission boolean,
    allowPing boolean,
    language text
);

create table if not exists invites
(
    id text primary key,
    createdAt datetime,
    expiresAt datetime,
    maxUses integer,
    url text,
    userId integer not null,
    foreign key (userId)
    references user (userId)
        on update restrict
        on delete restrict
);

create table if not exists pingRules (
    id integer primary key autoincrement,
    start datetime,
    end datetime,
    creationTime text,
    userId integer not null,
    foreign key (userId)
    references user (userId)
        on update restrict
        on delete restrict
);
