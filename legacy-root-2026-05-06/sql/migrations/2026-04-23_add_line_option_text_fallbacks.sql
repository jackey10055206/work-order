USE work_order_v2;

ALTER TABLE work_order_lines
  ADD COLUMN production_item_text VARCHAR(100) NULL AFTER production_item_id,
  ADD COLUMN material_text VARCHAR(100) NULL AFTER material_id,
  ADD COLUMN lamination_text VARCHAR(100) NULL AFTER lamination_id,
  ADD COLUMN board_type_text VARCHAR(100) NULL AFTER board_type_id,
  ADD COLUMN board_thickness_text VARCHAR(100) NULL AFTER board_thickness_id,
  ADD COLUMN extra_material_text VARCHAR(100) NULL AFTER extra_material_id;
