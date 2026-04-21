CREATE DATABASE IF NOT EXISTS work_order_v2
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE work_order_v2;

CREATE TABLE IF NOT EXISTS clients (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  short_name VARCHAR(100) NOT NULL,
  full_name VARCHAR(255) NULL,
  phone VARCHAR(100) NULL,
  address VARCHAR(255) NULL,
  tax_id VARCHAR(100) NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_clients_short_name (short_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS employees (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_employees_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS pack_transport_options (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  pack_name VARCHAR(100) NOT NULL,
  transport_name VARCHAR(100) NOT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_pack_transport_pair (pack_name, transport_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS option_items (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  option_group ENUM(
    'production_item',
    'material',
    'lamination',
    'board_type',
    'board_thickness',
    'extra_material'
  ) NOT NULL,
  item_name VARCHAR(100) NOT NULL,
  slug VARCHAR(140) NULL,
  sort_order INT NOT NULL DEFAULT 0,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  legacy_source_table VARCHAR(64) NULL,
  legacy_source_column VARCHAR(64) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_option_group_item_name (option_group, item_name),
  KEY idx_option_group_sort (option_group, sort_order, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS work_orders (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  work_number VARCHAR(50) NOT NULL,
  case_name VARCHAR(255) NULL,
  client_id BIGINT UNSIGNED NULL,
  company_phone VARCHAR(100) NULL,
  contact_name VARCHAR(100) NULL,
  work_time VARCHAR(100) NULL,
  cleanup_time VARCHAR(100) NULL,
  work_address VARCHAR(255) NULL,
  pack_transport_option_id BIGINT UNSIGNED NULL,
  remark TEXT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'draft',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_work_orders_work_number (work_number),
  KEY idx_work_orders_client_id (client_id),
  KEY idx_work_orders_pack_transport_option_id (pack_transport_option_id),
  CONSTRAINT fk_work_orders_client
    FOREIGN KEY (client_id) REFERENCES clients(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_work_orders_pack_transport_option
    FOREIGN KEY (pack_transport_option_id) REFERENCES pack_transport_options(id)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS work_order_lines (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  work_order_id BIGINT UNSIGNED NOT NULL,
  line_no INT NOT NULL,
  production_item_id BIGINT UNSIGNED NULL,
  material_id BIGINT UNSIGNED NULL,
  lamination_id BIGINT UNSIGNED NULL,
  board_type_id BIGINT UNSIGNED NULL,
  board_thickness_id BIGINT UNSIGNED NULL,
  extra_material_id BIGINT UNSIGNED NULL,
  width_mm DECIMAL(10,2) NULL,
  height_mm DECIMAL(10,2) NULL,
  quantity INT NULL,
  extra_material_quantity INT NULL,
  extra_material_total DECIMAL(12,2) NULL,
  cbm DECIMAL(10,2) NULL,
  cbm_unit_price DECIMAL(10,2) NULL,
  line_total DECIMAL(12,2) NULL,
  note VARCHAR(255) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_work_order_lines_order_line (work_order_id, line_no),
  KEY idx_work_order_lines_production_item_id (production_item_id),
  KEY idx_work_order_lines_material_id (material_id),
  KEY idx_work_order_lines_lamination_id (lamination_id),
  KEY idx_work_order_lines_board_type_id (board_type_id),
  KEY idx_work_order_lines_board_thickness_id (board_thickness_id),
  KEY idx_work_order_lines_extra_material_id (extra_material_id),
  CONSTRAINT fk_work_order_lines_work_order
    FOREIGN KEY (work_order_id) REFERENCES work_orders(id)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_work_order_lines_production_item
    FOREIGN KEY (production_item_id) REFERENCES option_items(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_work_order_lines_material
    FOREIGN KEY (material_id) REFERENCES option_items(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_work_order_lines_lamination
    FOREIGN KEY (lamination_id) REFERENCES option_items(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_work_order_lines_board_type
    FOREIGN KEY (board_type_id) REFERENCES option_items(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_work_order_lines_board_thickness
    FOREIGN KEY (board_thickness_id) REFERENCES option_items(id)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_work_order_lines_extra_material
    FOREIGN KEY (extra_material_id) REFERENCES option_items(id)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
