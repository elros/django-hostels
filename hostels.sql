--
-- Create model Bed
--
CREATE TABLE "HOSTELS_BED" ("ID" NUMBER(11) NOT NULL PRIMARY KEY, "GENDER" NUMBER(11) NOT NULL);
--
-- Create model Charge
--
CREATE TABLE "HOSTELS_CHARGE" ("ID" NUMBER(11) NOT NULL PRIMARY KEY, "VALUE" DOUBLE PRECISION NOT NULL, "IS_INCOME" NUMBER(1) NOT NULL CHECK ("IS_INCOME" IN (0,1)), "DATE" TIMESTAMP NOT NULL, "REASON" NUMBER(11) NOT NULL);
--
-- Create model Hostel
--
CREATE TABLE "HOSTELS_HOSTEL" ("ID" NUMBER(11) NOT NULL PRIMARY KEY, "CITY" NVARCHAR2(50) NULL, "ADDRESS" NVARCHAR2(100) NULL, "PHONE_NUMBER" NVARCHAR2(50) NULL);
--
-- Create model Operator
--
CREATE TABLE "HOSTELS_OPERATOR" ("ID" NUMBER(11) NOT NULL PRIMARY KEY, "FULL_NAME" NVARCHAR2(50) NULL, "IDENTIFICATION" NVARCHAR2(150) NULL, "PHONE_NUMBER" NVARCHAR2(50) NULL, "IS_ADMIN" NUMBER(1) NOT NULL CHECK ("IS_ADMIN" IN (0,1)), "USER_ID" NUMBER(11) NOT NULL UNIQUE);
CREATE TABLE "HOSTELS_OPERATOR_HOSTELS" ("ID" NUMBER(11) NOT NULL PRIMARY KEY, "OPERATOR_ID" NUMBER(11) NOT NULL, "HOSTEL_ID" NUMBER(11) NOT NULL);
--
-- Create model Order
--
CREATE TABLE "HOSTELS_ORDER" ("ID" NUMBER(11) NOT NULL PRIMARY KEY, "START_DATE" DATE NOT NULL, "END_DATE" DATE NOT NULL, "VALUE" DOUBLE PRECISION NOT NULL, "GUEST_FULL_NAME" NVARCHAR2(100) NULL, "GUEST_IDENTIFICATION" NVARCHAR2(150) NULL, "GUEST_PHONE_NUMBER" NVARCHAR2(50) NULL, "STATUS" NUMBER(11) NOT NULL, "BED_ID" NUMBER(11) NOT NULL);
--
-- Create model Tax
--
CREATE TABLE "HOSTELS_TAX" ("ID" NUMBER(11) NOT NULL PRIMARY KEY, "NAME" NVARCHAR2(200) NULL);
--
-- Create model TaxGrade
--
CREATE TABLE "HOSTELS_TAXGRADE" ("ID" NUMBER(11) NOT NULL PRIMARY KEY, "THRESHOLD_DAYS" NUMBER(11) NOT NULL, "DAY_PRICE" DOUBLE PRECISION NOT NULL, "TAX_ID" NUMBER(11) NOT NULL);
--
-- Add field tax to hostel
--
ALTER TABLE "HOSTELS_HOSTEL" ADD "TAX_ID" NUMBER(11) NOT NULL;
ALTER TABLE "HOSTELS_HOSTEL" MODIFY "TAX_ID" DEFAULT NULL;
--
-- Add field order to charge
--
ALTER TABLE "HOSTELS_CHARGE" ADD "ORDER_ID" NUMBER(11) NOT NULL;
ALTER TABLE "HOSTELS_CHARGE" MODIFY "ORDER_ID" DEFAULT NULL;
--
-- Add field actual_order to bed
--
ALTER TABLE "HOSTELS_BED" ADD "ACTUAL_ORDER_ID" NUMBER(11) NULL UNIQUE;
ALTER TABLE "HOSTELS_BED" MODIFY "ACTUAL_ORDER_ID" DEFAULT NULL;
--
-- Add field hostel to bed
--
ALTER TABLE "HOSTELS_BED" ADD "HOSTEL_ID" NUMBER(11) NOT NULL;
ALTER TABLE "HOSTELS_BED" MODIFY "HOSTEL_ID" DEFAULT NULL;
--
-- Add field tax to bed
--
ALTER TABLE "HOSTELS_BED" ADD "TAX_ID" NUMBER(11) NOT NULL;
ALTER TABLE "HOSTELS_BED" MODIFY "TAX_ID" DEFAULT NULL;

DECLARE
    i INTEGER;
BEGIN
    SELECT COUNT(*) INTO i FROM USER_CATALOG
        WHERE TABLE_NAME = 'HOSTELS_BED_SQ' AND TABLE_TYPE = 'SEQUENCE';
    IF i = 0 THEN
        EXECUTE IMMEDIATE 'CREATE SEQUENCE "HOSTELS_BED_SQ"';
    END IF;
END;
/;

CREATE OR REPLACE TRIGGER "HOSTELS_BED_TR"
BEFORE INSERT ON "HOSTELS_BED"
FOR EACH ROW
WHEN (new."ID" IS NULL)
    BEGIN
        SELECT "HOSTELS_BED_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
/;

DECLARE
    i INTEGER;
BEGIN
    SELECT COUNT(*) INTO i FROM USER_CATALOG
        WHERE TABLE_NAME = 'HOSTELS_CHARGE_SQ' AND TABLE_TYPE = 'SEQUENCE';
    IF i = 0 THEN
        EXECUTE IMMEDIATE 'CREATE SEQUENCE "HOSTELS_CHARGE_SQ"';
    END IF;
END;
/;

CREATE OR REPLACE TRIGGER "HOSTELS_CHARGE_TR"
BEFORE INSERT ON "HOSTELS_CHARGE"
FOR EACH ROW
WHEN (new."ID" IS NULL)
    BEGIN
        SELECT "HOSTELS_CHARGE_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
/;

DECLARE
    i INTEGER;
BEGIN
    SELECT COUNT(*) INTO i FROM USER_CATALOG
        WHERE TABLE_NAME = 'HOSTELS_HOSTEL_SQ' AND TABLE_TYPE = 'SEQUENCE';
    IF i = 0 THEN
        EXECUTE IMMEDIATE 'CREATE SEQUENCE "HOSTELS_HOSTEL_SQ"';
    END IF;
END;
/;

CREATE OR REPLACE TRIGGER "HOSTELS_HOSTEL_TR"
BEFORE INSERT ON "HOSTELS_HOSTEL"
FOR EACH ROW
WHEN (new."ID" IS NULL)
    BEGIN
        SELECT "HOSTELS_HOSTEL_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
/;

DECLARE
    i INTEGER;
BEGIN
    SELECT COUNT(*) INTO i FROM USER_CATALOG
        WHERE TABLE_NAME = 'HOSTELS_OPERATOR_SQ' AND TABLE_TYPE = 'SEQUENCE';
    IF i = 0 THEN
        EXECUTE IMMEDIATE 'CREATE SEQUENCE "HOSTELS_OPERATOR_SQ"';
    END IF;
END;
/;

CREATE OR REPLACE TRIGGER "HOSTELS_OPERATOR_TR"
BEFORE INSERT ON "HOSTELS_OPERATOR"
FOR EACH ROW
WHEN (new."ID" IS NULL)
    BEGIN
        SELECT "HOSTELS_OPERATOR_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
/;
ALTER TABLE "HOSTELS_OPERATOR" ADD CONSTRAINT "B5A3B4C86857E0DF336B7470BAA921" FOREIGN KEY ("USER_ID") REFERENCES "AUTH_USER" ("ID") DEFERRABLE INITIALLY DEFERRED;

DECLARE
    i INTEGER;
BEGIN
    SELECT COUNT(*) INTO i FROM USER_CATALOG
        WHERE TABLE_NAME = 'HOSTELS_OPERATOR_HOSTELS_SQ' AND TABLE_TYPE = 'SEQUENCE';
    IF i = 0 THEN
        EXECUTE IMMEDIATE 'CREATE SEQUENCE "HOSTELS_OPERATOR_HOSTELS_SQ"';
    END IF;
END;
/;

CREATE OR REPLACE TRIGGER "HOSTELS_OPERATOR_HOSTELS_TR"
BEFORE INSERT ON "HOSTELS_OPERATOR_HOSTELS"
FOR EACH ROW
WHEN (new."ID" IS NULL)
    BEGIN
        SELECT "HOSTELS_OPERATOR_HOSTELS_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
/;
ALTER TABLE "HOSTELS_OPERATOR_HOSTELS" ADD CONSTRAINT "D0DD854EFCAC12CEA80FEA245B053E" FOREIGN KEY ("OPERATOR_ID") REFERENCES "HOSTELS_OPERATOR" ("ID") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "HOSTELS_OPERATOR_HOSTELS" ADD CONSTRAINT "D618E89127C52D98031CC3779F3E4B" FOREIGN KEY ("HOSTEL_ID") REFERENCES "HOSTELS_HOSTEL" ("ID") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "HOSTELS_OPERATOR_HOSTELS" ADD CONSTRAINT "HOST_OPERATOR_ID_D0EF8337_UNIQ" UNIQUE ("OPERATOR_ID", "HOSTEL_ID");
CREATE INDEX "HOSTELS_OPERATOR_HOSTELS_4C280" ON "HOSTELS_OPERATOR_HOSTELS" ("OPERATOR_ID");
CREATE INDEX "HOSTELS_OPERATOR_HOSTELS_351AF" ON "HOSTELS_OPERATOR_HOSTELS" ("HOSTEL_ID");

DECLARE
    i INTEGER;
BEGIN
    SELECT COUNT(*) INTO i FROM USER_CATALOG
        WHERE TABLE_NAME = 'HOSTELS_ORDER_SQ' AND TABLE_TYPE = 'SEQUENCE';
    IF i = 0 THEN
        EXECUTE IMMEDIATE 'CREATE SEQUENCE "HOSTELS_ORDER_SQ"';
    END IF;
END;
/;

CREATE OR REPLACE TRIGGER "HOSTELS_ORDER_TR"
BEFORE INSERT ON "HOSTELS_ORDER"
FOR EACH ROW
WHEN (new."ID" IS NULL)
    BEGIN
        SELECT "HOSTELS_ORDER_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
/;
ALTER TABLE "HOSTELS_ORDER" ADD CONSTRAINT "D2B76162B4D52934FAB7FCF1725764" FOREIGN KEY ("BED_ID") REFERENCES "HOSTELS_BED" ("ID") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "HOSTELS_ORDER_7CD27A4C" ON "HOSTELS_ORDER" ("BED_ID");

DECLARE
    i INTEGER;
BEGIN
    SELECT COUNT(*) INTO i FROM USER_CATALOG
        WHERE TABLE_NAME = 'HOSTELS_TAX_SQ' AND TABLE_TYPE = 'SEQUENCE';
    IF i = 0 THEN
        EXECUTE IMMEDIATE 'CREATE SEQUENCE "HOSTELS_TAX_SQ"';
    END IF;
END;
/;

CREATE OR REPLACE TRIGGER "HOSTELS_TAX_TR"
BEFORE INSERT ON "HOSTELS_TAX"
FOR EACH ROW
WHEN (new."ID" IS NULL)
    BEGIN
        SELECT "HOSTELS_TAX_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
/;

DECLARE
    i INTEGER;
BEGIN
    SELECT COUNT(*) INTO i FROM USER_CATALOG
        WHERE TABLE_NAME = 'HOSTELS_TAXGRADE_SQ' AND TABLE_TYPE = 'SEQUENCE';
    IF i = 0 THEN
        EXECUTE IMMEDIATE 'CREATE SEQUENCE "HOSTELS_TAXGRADE_SQ"';
    END IF;
END;
/;

CREATE OR REPLACE TRIGGER "HOSTELS_TAXGRADE_TR"
BEFORE INSERT ON "HOSTELS_TAXGRADE"
FOR EACH ROW
WHEN (new."ID" IS NULL)
    BEGIN
        SELECT "HOSTELS_TAXGRADE_SQ".nextval
        INTO :new."ID" FROM dual;
    END;
/;
ALTER TABLE "HOSTELS_TAXGRADE" ADD CONSTRAINT "D39427237584ECD4E165ADFA9A7315" FOREIGN KEY ("TAX_ID") REFERENCES "HOSTELS_TAX" ("ID") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "HOSTELS_TAXGRADE_59FC14E7" ON "HOSTELS_TAXGRADE" ("TAX_ID");
CREATE INDEX "HOSTELS_HOSTEL_59FC14E7" ON "HOSTELS_HOSTEL" ("TAX_ID");
ALTER TABLE "HOSTELS_HOSTEL" ADD CONSTRAINT "D9EF41AC9494710372989EA6EAE9FC" FOREIGN KEY ("TAX_ID") REFERENCES "HOSTELS_TAX" ("ID") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "HOSTELS_CHARGE_69DFCB07" ON "HOSTELS_CHARGE" ("ORDER_ID");
ALTER TABLE "HOSTELS_CHARGE" ADD CONSTRAINT "C14F51C39AEB2D086FB2EDE6E99DAA" FOREIGN KEY ("ORDER_ID") REFERENCES "HOSTELS_ORDER" ("ID") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "HOSTELS_BED" ADD CONSTRAINT "D0B12506BCAB42AF9E81F3169DD247" FOREIGN KEY ("ACTUAL_ORDER_ID") REFERENCES "HOSTELS_ORDER" ("ID") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "HOSTELS_BED_3AE5C04B" ON "HOSTELS_BED" ("HOSTEL_ID");
ALTER TABLE "HOSTELS_BED" ADD CONSTRAINT "D191BBF38CD5F5DA676A64416D3DC9" FOREIGN KEY ("HOSTEL_ID") REFERENCES "HOSTELS_HOSTEL" ("ID") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "HOSTELS_BED_59FC14E7" ON "HOSTELS_BED" ("TAX_ID");
ALTER TABLE "HOSTELS_BED" ADD CONSTRAINT "D693ECD50E8C392973EDF00A9A0267" FOREIGN KEY ("TAX_ID") REFERENCES "HOSTELS_TAX" ("ID") DEFERRABLE INITIALLY DEFERRED;

COMMIT;