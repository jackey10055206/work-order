-- v2 only: add dedicated column for UI field 「備料計價」
-- Do NOT run this against legacy `work_order` database.

USE work_order_v2;

ALTER TABLE work_order_lines
  ADD COLUMN extra_material_total DECIMAL(12,2) NULL
  AFTER extra_material_quantity;
