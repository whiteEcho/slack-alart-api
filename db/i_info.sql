create table i_info (
    id number generated always as identity,
    category varchar2(20) not null,
    summary varchar2(600) not null,
    org_file_name varchar(100) not null,
    report blob not null,
    create_at timestamp not null,
    update_at timestamp not null,
    primary key(id)
);
comment on table i_info is '事故報告の管理用テーブル';
comment on column i_info.id is '事故報告管理ID';
comment on column i_info.category is '事故種別';
comment on column i_info.summary is '概要';
comment on column i_info.org_file_name is 'ファイル名';
comment on column i_info.report is '報告ファイル';
comment on column i_info.create_at is '作成日';
comment on column i_info.update_at is '更新日';
