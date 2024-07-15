
drop materialized view if exists prod.mv_shelve_count cascade;
CREATE MATERIALIZED VIEW prod.mv_shelve_count AS
SELECT c.name AS category_name, SUM(pos.product_count) AS shelves_count
FROM products_on_shelves pos
         JOIN product_categories pc ON pos.product_id = pc.product_id
         JOIN categories c ON pc.category_id = c.category_id
GROUP BY c.name;

drop materialized view if exists prod.mv_external_supplies cascade;
CREATE MATERIALIZED VIEW prod.mv_external_supplies AS
SELECT
    es.finish_date AS date,
    c.name AS category_name,
    SUM(esp.product_count) AS sum_products_finish_date
FROM
    external_supplies es
    LEFT JOIN external_supplies_products esp ON esp.ext_supply_id = es.ext_supply_id
    LEFT JOIN product_categories pc ON esp.product_id = pc.product_id
    LEFT JOIN categories c ON pc.category_id = c.category_id
GROUP BY
    es.finish_date, c.name, esp.product_count
ORDER BY
    es.finish_date, c.name ASC;


drop materialized view if exists prod.mv_product_summary cascade;
CREATE MATERIALIZED VIEW prod.mv_product_summary AS
SELECT
    c.issue_date AS date,
     cat.name AS category_name,
     SUM(pcp.product_count) AS sum_products_issue_date
FROM
    checks c
    LEFT JOIN product_check_positions pcp ON pcp.check_id = c.check_id
    LEFT JOIN product_categories pc ON pcp.product_id = pc.product_id
    LEFT JOIN categories cat ON pc.category_id = cat.category_id
GROUP BY
    c.issue_date, cat.name;


CREATE OR REPLACE FUNCTION refresh_materialized_views()
                RETURNS TRIGGER AS $$
BEGIN
                REFRESH MATERIALIZED VIEW mv_shelve_count;
                REFRESH MATERIALIZED VIEW mv_external_supplies;
                REFRESH MATERIALIZED VIEW mv_product_summary;
RETURN NEW;
END;
            $$ LANGUAGE plpgsql


CREATE TRIGGER update_materialized_views_trigger
    AFTER INSERT OR UPDATE OR DELETE
                    ON checks
                        FOR EACH STATEMENT
                        EXECUTE FUNCTION refresh_materialized_views()

CREATE TRIGGER update_materialized_views_trigger
    AFTER INSERT OR UPDATE OR DELETE
                    ON product_check_positions
                        FOR EACH STATEMENT
                        EXECUTE FUNCTION refresh_materialized_views()

CREATE TRIGGER update_materialized_views_trigger
    AFTER INSERT OR UPDATE OR DELETE
                    ON product_categories
                        FOR EACH STATEMENT
                        EXECUTE FUNCTION refresh_materialized_views()

CREATE TRIGGER update_materialized_views_trigger
    AFTER INSERT OR UPDATE OR DELETE
                    ON categories
                        FOR EACH STATEMENT
                        EXECUTE FUNCTION refresh_materialized_views()

CREATE TRIGGER update_materialized_views_trigger
    AFTER INSERT OR UPDATE OR DELETE
                    ON external_supplies
                        FOR EACH STATEMENT
                        EXECUTE FUNCTION refresh_materialized_views()

CREATE TRIGGER update_materialized_views_trigger
    AFTER INSERT OR UPDATE OR DELETE
                    ON external_supplies_products
                        FOR EACH STATEMENT
                        EXECUTE FUNCTION refresh_materialized_views()

CREATE TRIGGER update_materialized_views_trigger
    AFTER INSERT OR UPDATE OR DELETE
                    ON products_on_shelves
                        FOR EACH STATEMENT
                        EXECUTE FUNCTION refresh_materialized_views()
