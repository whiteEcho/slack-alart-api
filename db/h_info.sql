CREATE TABLE h_info (
 id NUMBER GENERATED ALWAYS AS IDENTITY,
 reporter VARCHAR(20) NOT NULL,
 date_of_occurred DATE,
 date_of_discovered DATE NOT NULL,
 summary NVARCHAR2(600) NOT NULL,
 detail NVARCHAR2(2000),
 created_at TIMESTAMP NOT NULL,
 updated_at TIMESTAMP NOT NULL,
 PRIMARY KEY(id)
 )
;
COMMENT ON TABLE h_info IS 'ヒヤリハットの管理用テーブル';
COMMENT ON COLUMN h_info.id IS 'ヒヤリハット管理ID';
COMMENT ON COLUMN h_info.reporter IS '報告者';
COMMENT ON COLUMN h_info.date_of_occurred IS '発生日';
COMMENT ON COLUMN h_info.date_of_discovered IS '発覚日';
COMMENT ON COLUMN h_info.summary IS '概要';
COMMENT ON COLUMN h_info.detail IS '詳細';
COMMENT ON COLUMN h_info.created_at IS '作成日';
COMMENT ON COLUMN h_info.updated_at IS '更新日';
