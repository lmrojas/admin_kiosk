--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actions (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    command character varying(50) NOT NULL,
    description character varying(200),
    icon_class character varying(50),
    requires_confirmation boolean,
    created_at timestamp without time zone,
    is_active boolean
);


ALTER TABLE public.actions OWNER TO postgres;

--
-- Name: actions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.actions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.actions_id_seq OWNER TO postgres;

--
-- Name: actions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.actions_id_seq OWNED BY public.actions.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: kiosk; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kiosk (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    serial_number character varying(50) NOT NULL,
    status character varying(20),
    ip_address character varying(45),
    location_id integer,
    current_latitude double precision,
    current_longitude double precision,
    location_mismatch boolean,
    state_id integer,
    last_connection timestamp without time zone,
    last_action_state character varying(100),
    sensors_data json,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.kiosk OWNER TO postgres;

--
-- Name: kiosk_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kiosk_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kiosk_id_seq OWNER TO postgres;

--
-- Name: kiosk_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kiosk_id_seq OWNED BY public.kiosk.id;


--
-- Name: kiosk_location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kiosk_location (
    id integer NOT NULL,
    kiosk_id integer NOT NULL,
    location_id integer NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone
);


ALTER TABLE public.kiosk_location OWNER TO postgres;

--
-- Name: kiosk_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kiosk_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kiosk_location_id_seq OWNER TO postgres;

--
-- Name: kiosk_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kiosk_location_id_seq OWNED BY public.kiosk_location.id;


--
-- Name: kiosk_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kiosk_logs (
    id integer NOT NULL,
    kiosk_id integer NOT NULL,
    event_type character varying(50) NOT NULL,
    message character varying(500) NOT NULL,
    details text,
    created_at timestamp without time zone NOT NULL,
    created_by character varying(100)
);


ALTER TABLE public.kiosk_logs OWNER TO postgres;

--
-- Name: kiosk_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kiosk_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kiosk_logs_id_seq OWNER TO postgres;

--
-- Name: kiosk_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kiosk_logs_id_seq OWNED BY public.kiosk_logs.id;


--
-- Name: location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    address character varying(255) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    description text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.location OWNER TO postgres;

--
-- Name: location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.location_id_seq OWNER TO postgres;

--
-- Name: location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.location_id_seq OWNED BY public.location.id;


--
-- Name: settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.settings (
    id integer NOT NULL,
    key character varying(50) NOT NULL,
    value character varying(200),
    description character varying(200)
);


ALTER TABLE public.settings OWNER TO postgres;

--
-- Name: settings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.settings_id_seq OWNER TO postgres;

--
-- Name: settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.settings_id_seq OWNED BY public.settings.id;


--
-- Name: states; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.states (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(200),
    color_class character varying(20) NOT NULL,
    created_at timestamp without time zone,
    is_active boolean
);


ALTER TABLE public.states OWNER TO postgres;

--
-- Name: states_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.states_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.states_id_seq OWNER TO postgres;

--
-- Name: states_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.states_id_seq OWNED BY public.states.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(64) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256),
    is_admin boolean,
    is_active boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: actions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions ALTER COLUMN id SET DEFAULT nextval('public.actions_id_seq'::regclass);


--
-- Name: kiosk id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk ALTER COLUMN id SET DEFAULT nextval('public.kiosk_id_seq'::regclass);


--
-- Name: kiosk_location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk_location ALTER COLUMN id SET DEFAULT nextval('public.kiosk_location_id_seq'::regclass);


--
-- Name: kiosk_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk_logs ALTER COLUMN id SET DEFAULT nextval('public.kiosk_logs_id_seq'::regclass);


--
-- Name: location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location ALTER COLUMN id SET DEFAULT nextval('public.location_id_seq'::regclass);


--
-- Name: settings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.settings ALTER COLUMN id SET DEFAULT nextval('public.settings_id_seq'::regclass);


--
-- Name: states id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.states ALTER COLUMN id SET DEFAULT nextval('public.states_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: actions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actions (id, name, command, description, icon_class, requires_confirmation, created_at, is_active) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: kiosk; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kiosk (id, name, serial_number, status, ip_address, location_id, current_latitude, current_longitude, location_mismatch, state_id, last_connection, last_action_state, sensors_data, created_at, updated_at) FROM stdin;
7	Kiosk Test 007	SN67324693	offline	192.168.1.227	3	-31.4201	-64.1888	f	1	2025-01-13 15:29:07.221003	\N	{"cpu_usage": 40.19110928655748, "ram_usage": 54.27136810562875, "disk_usage": 71.43259898265278, "temperature": 30.540634905782397, "network": {"latency": 84.42666111030437, "download_speed": 50.77059709616208, "upload_speed": 32.716230338904715, "signal_strength": -46.29246313514465}, "ups": {"status": "bypass", "battery_level": 59.00579056423889, "estimated_runtime": 117}}	2025-01-13 18:16:46.265091	2025-01-13 18:29:07.221003
4	Kiosk Test 004	SN72066349	offline	192.168.1.60	1	-34.6037	-58.3816	f	1	2025-01-13 15:52:42.519215	\N	{"cpu_usage": 32.62888103030466, "ram_usage": 31.967361199485428, "disk_usage": 41.583652206719606, "temperature": 26.519355106765513, "network": {"latency": 77.16588497309073, "download_speed": 43.14630143987788, "upload_speed": 44.02705254911585, "signal_strength": -66.31711758633612}, "ups": {"status": "battery", "battery_level": 82.63895390630864, "estimated_runtime": 28}}	2025-01-13 18:16:46.265091	2025-01-13 18:52:42.519215
3	Kiosk Test 003	SN43571204	offline	192.168.1.13	5	-32.8908	-68.8272	f	1	2025-01-13 15:52:42.711534	\N	{"cpu_usage": 36.88024830444229, "ram_usage": 48.874059814074975, "disk_usage": 63.361225831807445, "temperature": 31.368557388425252, "network": {"latency": 192.64732525224284, "download_speed": 95.88310363116594, "upload_speed": 40.415259478198166, "signal_strength": -34.471844048199564}, "ups": {"status": "battery", "battery_level": 77.17082037589515, "estimated_runtime": 102}}	2025-01-13 18:16:46.265091	2025-01-13 18:52:42.711534
5	Kiosk Test 005	SN66029930	offline	192.168.1.86	3	-31.4201	-64.1888	f	1	2025-01-13 15:42:59.441284	\N	{"cpu_usage": 55.361971550048914, "ram_usage": 52.917388303957495, "disk_usage": 46.2641419669051, "temperature": 25.971972847521617, "network": {"latency": 160.1539388576416, "download_speed": 74.22065702542007, "upload_speed": 39.886408196476715, "signal_strength": -42.44240747068626}, "ups": {"status": "online", "battery_level": 82.70856729363183, "estimated_runtime": 95}}	2025-01-13 18:16:46.265091	2025-01-13 18:42:59.441284
1	Kiosk Test 001	SN72920616	offline	192.168.1.72	3	-31.4201	-64.1888	f	1	2025-01-13 15:46:31.743842	\N	{"cpu_usage": 75.80336788161397, "ram_usage": 92.49017030141366, "disk_usage": 90.68732568270654, "temperature": 40.151480254533794, "network": {"latency": 51.439586796261786, "download_speed": 50.148787620981395, "upload_speed": 44.62071411089767, "signal_strength": -51.715260662004376}, "ups": {"status": "battery", "battery_level": 23.517598138500784, "estimated_runtime": 81}}	2025-01-13 18:16:46.265091	2025-01-13 18:46:31.743842
6	Kiosk Test 006	SN97880399	offline	192.168.1.127	1	-34.6037	-58.3816	f	1	2025-01-13 15:46:31.95195	\N	{"cpu_usage": 76.12965330263224, "ram_usage": 80.86133260189024, "disk_usage": 85.82794049034757, "temperature": 36.465180803158916, "network": {"latency": 149.33120907849036, "download_speed": 74.23968039805288, "upload_speed": 36.52078181245976, "signal_strength": -61.54786509389943}, "ups": {"status": "online", "battery_level": 67.23523235906457, "estimated_runtime": 104}}	2025-01-13 18:16:46.265091	2025-01-13 18:46:31.95195
2	Kiosk Test 002	SN46573091	offline	192.168.1.148	1	-34.6037	-58.3816	f	1	2025-01-13 15:58:04.355686	\N	{"cpu_usage": 76.37494763236135, "ram_usage": 87.93939410981731, "disk_usage": 88.5745698241087, "temperature": 35.52976238087628, "network": {"latency": 129.31861441304125, "download_speed": 41.82391396190947, "upload_speed": 25.463803665691707, "signal_strength": -45.40458715981792}, "ups": {"status": "battery", "battery_level": 44.72987767031508, "estimated_runtime": 61}}	2025-01-13 18:16:46.265091	2025-01-13 18:58:04.355686
9	Kiosk Test 009	SN45084052	offline	192.168.1.215	1	-34.6037	-58.3816	f	1	2025-01-13 15:42:59.876303	\N	{"cpu_usage": 20.98143507139835, "ram_usage": 65.58854853253445, "disk_usage": 64.14073490581632, "temperature": 30.036096833671667, "network": {"latency": 105.25266812032235, "download_speed": 3.7870654530542884, "upload_speed": 28.91231609624799, "signal_strength": -60.040744253357374}, "ups": {"status": "online", "battery_level": 26.043557390064773, "estimated_runtime": 70}}	2025-01-13 18:16:46.265091	2025-01-13 18:42:59.876303
10	Kiosk Test 010	SN60899677	offline	192.168.1.88	5	-32.8908	-68.8272	f	1	2025-01-13 15:41:56.955952	\N	{"cpu_usage": 26.85712733151165, "ram_usage": 45.43659557685214, "disk_usage": 56.0441491488387, "temperature": 26.806303639770412, "network": {"latency": 66.15303327463364, "download_speed": 56.516201356975266, "upload_speed": 15.27151873846494, "signal_strength": -51.279702616836886}, "ups": {"status": "battery", "battery_level": 44.90060842710311, "estimated_runtime": 113}}	2025-01-13 18:16:46.265091	2025-01-13 18:41:56.955952
8	Kiosk Test 008	SN71908321	offline	192.168.1.30	2	-34.5891	-58.3738	f	1	2025-01-13 15:41:57.017014	\N	{"cpu_usage": 54.52436988887724, "ram_usage": 37.899838448860145, "disk_usage": 73.94441187981266, "temperature": 26.486591767392447, "network": {"latency": 152.32994443237538, "download_speed": 6.907555411254366, "upload_speed": 29.25779254642999, "signal_strength": -33.370899715902084}, "ups": {"status": "bypass", "battery_level": 99.44053071538953, "estimated_runtime": 55}}	2025-01-13 18:16:46.265091	2025-01-13 18:41:57.018045
\.


--
-- Data for Name: kiosk_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kiosk_location (id, kiosk_id, location_id, start_date, end_date) FROM stdin;
\.


--
-- Data for Name: kiosk_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.kiosk_logs (id, kiosk_id, event_type, message, details, created_at, created_by) FROM stdin;
\.


--
-- Data for Name: location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location (id, name, address, latitude, longitude, description, created_at, updated_at) FROM stdin;
1	Shopping Abasto	Av. Corrientes 3247, CABA	-34.6037	-58.3816	Centro comercial principal	2025-01-13 18:16:16.959159	2025-01-13 18:16:16.959159
2	Terminal Retiro	Av. Ant├írtida Argentina s/n, CABA	-34.5891	-58.3738	Terminal de buses principal	2025-01-13 18:16:16.973592	2025-01-13 18:16:16.973592
3	Patio Olmos	Av. V├®lez Sarsfield 361, C├│rdoba	-31.4201	-64.1888	Shopping center c├®ntrico	2025-01-13 18:16:16.975604	2025-01-13 18:16:16.975604
4	Alto Rosario	Jun├¡n 501, Rosario	-32.9468	-60.6393	Centro comercial principal	2025-01-13 18:16:16.977959	2025-01-13 18:16:16.977959
5	Mendoza Plaza	Av. Acceso Este 3280, Guaymall├®n	-32.8908	-68.8272	Shopping principal de Mendoza	2025-01-13 18:16:16.979962	2025-01-13 18:16:16.979962
\.


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.settings (id, key, value, description) FROM stdin;
1	system_name	Admin Kiosk	Nombre del sistema
2	refresh_interval	5	Intervalo de actualizaci├│n en segundos
3	max_logs	100	M├íximo n├║mero de logs a mostrar
4	cpu_warning	80	Umbral de advertencia de CPU (%)
5	cpu_critical	90	Umbral cr├¡tico de CPU (%)
6	ram_warning	85	Umbral de advertencia de RAM (%)
7	ram_critical	95	Umbral cr├¡tico de RAM (%)
8	disk_warning	85	Umbral de advertencia de disco (%)
9	disk_critical	95	Umbral cr├¡tico de disco (%)
\.


--
-- Data for Name: states; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.states (id, name, description, color_class, created_at, is_active) FROM stdin;
1	Normal	Funcionamiento normal	success	2025-01-13 18:16:16.938276	t
2	Warning	Advertencias activas	warning	2025-01-13 18:16:16.954123	t
3	Error	Errores cr├¡ticos	danger	2025-01-13 18:16:16.956145	t
4	Offline	Sin conexi├│n	secondary	2025-01-13 18:16:16.957156	t
5	Maintenance	En mantenimiento	info	2025-01-13 18:16:16.958156	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, is_admin, is_active, created_at, updated_at) FROM stdin;
\.


--
-- Name: actions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.actions_id_seq', 1, false);


--
-- Name: kiosk_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kiosk_id_seq', 10, true);


--
-- Name: kiosk_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kiosk_location_id_seq', 1, false);


--
-- Name: kiosk_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.kiosk_logs_id_seq', 1, false);


--
-- Name: location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.location_id_seq', 5, true);


--
-- Name: settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.settings_id_seq', 9, true);


--
-- Name: states_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.states_id_seq', 5, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: actions actions_command_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_command_key UNIQUE (command);


--
-- Name: actions actions_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_name_key UNIQUE (name);


--
-- Name: actions actions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: kiosk_location kiosk_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk_location
    ADD CONSTRAINT kiosk_location_pkey PRIMARY KEY (id);


--
-- Name: kiosk_logs kiosk_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk_logs
    ADD CONSTRAINT kiosk_logs_pkey PRIMARY KEY (id);


--
-- Name: kiosk kiosk_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk
    ADD CONSTRAINT kiosk_pkey PRIMARY KEY (id);


--
-- Name: kiosk kiosk_serial_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk
    ADD CONSTRAINT kiosk_serial_number_key UNIQUE (serial_number);


--
-- Name: location location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_pkey PRIMARY KEY (id);


--
-- Name: settings settings_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_key_key UNIQUE (key);


--
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);


--
-- Name: states states_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.states
    ADD CONSTRAINT states_name_key UNIQUE (name);


--
-- Name: states states_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.states
    ADD CONSTRAINT states_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: kiosk kiosk_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk
    ADD CONSTRAINT kiosk_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.location(id);


--
-- Name: kiosk_location kiosk_location_kiosk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk_location
    ADD CONSTRAINT kiosk_location_kiosk_id_fkey FOREIGN KEY (kiosk_id) REFERENCES public.kiosk(id);


--
-- Name: kiosk_location kiosk_location_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk_location
    ADD CONSTRAINT kiosk_location_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.location(id);


--
-- Name: kiosk_logs kiosk_logs_kiosk_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk_logs
    ADD CONSTRAINT kiosk_logs_kiosk_id_fkey FOREIGN KEY (kiosk_id) REFERENCES public.kiosk(id);


--
-- Name: kiosk kiosk_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kiosk
    ADD CONSTRAINT kiosk_state_id_fkey FOREIGN KEY (state_id) REFERENCES public.states(id);


--
-- PostgreSQL database dump complete
--

