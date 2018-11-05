/* SCRIPT SQL PARA CREACION DE TABLA ALUMNO */
CREATE TABLE alumno
(
  nya character varying(70) NOT NULL,
  legajo integer NOT NULL,
  sexo character varying(7) NOT NULL,
  edad integer NOT NULL,
  password character varying(30) NOT NULL,
  CONSTRAINT pk_alum PRIMARY KEY (legajo),
  CONSTRAINT chk_edad CHECK (edad < 100 AND edad > 17),
  CONSTRAINT chk_sexo CHECK (sexo::text = ANY (ARRAY['hombre'::character varying, 'mujer'::character varying]::text[]))
)

--CONSEDO PERMISOS A USER jtatest
GRANT ALL ON TABLE alumno TO jtatest;
