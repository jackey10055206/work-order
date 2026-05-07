-- v2 only: persist bottom summary fields shown in preview UI
-- Do NOT run this against legacy `work_order` database.

USE work_order_v2;

ALTER TABLE work_orders
  ADD COLUMN production_amount DECIMAL(12,2) NULL AFTER pack_transport_option_id,
  ADD COLUMN tax_amount DECIMAL(12,2) NULL AFTER production_amount,
  ADD COLUMN total_amount DECIMAL(12,2) NULL AFTER tax_amount;
