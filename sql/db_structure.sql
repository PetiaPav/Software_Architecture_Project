-- ROOM SLOTS
CREATE TABLE ROOM_SLOTS (
  id int(11) NOT NULL AUTO_INCREMENT,
  clinic_id int(11) DEFAULT NULL,
  room_id int(11) DEFAULT NULL,
  week_index int(11) DEFAULT NULL,
  day_index int(11) DEFAULT NULL,
  slot_index int(11) DEFAULT NULL,
  walk_in tinyint(4) DEFAULT '0',
  doctor_id int(11) DEFAULT NULL,
  patient_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY fk_patient_id_idx (patient_id),
  KEY fk_doctor_id_idx (doctor_id),
  CONSTRAINT fk_doctor_id_idx FOREIGN KEY (doctor_id) REFERENCES DOCTORS (id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT fk_patient_id_idx FOREIGN KEY (patient_id) REFERENCES PATIENTS (id) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- DOCTOR CLINIC ASSIGNMENTS
CREATE TABLE DOCTOR_CLINIC_ASSIGNMENT (
  id int(11) NOT NULL AUTO_INCREMENT,
  clinic_id int(11) DEFAULT NULL,
  doctor_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (doctor_id) REFERENCES DOCTORS (id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY (clinic_id) REFERENCES CLINICS (id) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- CLINICS 
CREATE TABLE CLINICS (
  id int(11) NOT NULL AUTO_INCREMENT,
  physical_address varchar(100) DEFAULT NULL,
  name varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- USERS
CREATE TABLE USERS (
  id int(11) NOT NULL AUTO_INCREMENT,
  first_name varchar(100) NOT NULL,
  last_name varchar(100) NOT NULL,
  password varchar(100) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- PATIENTS
CREATE TABLE PATIENTS (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_fk int(11) NOT NULL,
  email varchar(100) NOT NULL,
  health_card varchar(14) NOT NULL,
  phone_number varchar(15) NOT NULL,
  birthday date NOT NULL,
  gender varchar(15) NOT NULL,
  physical_address varchar(100) NOT NULL,
  PRIMARY KEY (id),
  KEY PATIENTS_USERS_FK (user_fk),
  CONSTRAINT PATIENTS_USERS_FK FOREIGN KEY (user_fk) REFERENCES USERS (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- NURSES
CREATE TABLE NURSES (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_fk int(11) NOT NULL,
  access_id varchar(8) NOT NULL,
  PRIMARY KEY (id),
  KEY NURSES_USERS_FK (user_fk),
  CONSTRAINT NURSES_USERS_FK FOREIGN KEY (user_fk) REFERENCES USERS (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- DOCTORS
CREATE TABLE DOCTORS (
  id int(11) NOT NULL AUTO_INCREMENT,
  user_fk int(11) NOT NULL,
  permit_number int(7) NOT NULL,
  specialty varchar(100) NOT NULL,
  city varchar(100) NOT NULL,
  PRIMARY KEY (id),
  KEY DOCTORS_USERS_FK (user_fk),
  CONSTRAINT DOCTORS_USERS_FK FOREIGN KEY (user_fk) REFERENCES USERS (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- DOCTOR AVAILIBILITIES
CREATE TABLE DOCTOR_AVAILABILITIES (
  id int(11) NOT NULL AUTO_INCREMENT,
  doctor_id int(11) NOT NULL,
  day_index int(11) NOT NULL,
  slot_index int(11) NOT NULL,
  walk_in tinyint(4) NOT NULL,
  PRIMARY KEY (id),
  KEY DOCTORS_FK (doctor_id),
  CONSTRAINT DOCTORS_FK FOREIGN KEY (doctor_id) REFERENCES DOCTORS (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

-- DOCTOR AVAILABILITIES WEEKLY
CREATE TABLE DOCTOR_AVAILABILITIES_SPECIAL (
  id int(11) NOT NULL AUTO_INCREMENT,
  doctor_id int(11) NOT NULL,
  week_index int(11) NOT NULL,
  day_index int(11) NOT NULL,
  slot_index int(11) NOT NULL,
  walk_in tinyint(4) NOT NULL,
  available varchar(15) NOT NULL,
  PRIMARY KEY (id),
  KEY DOCTORS_SPECIAL_FK (doctor_id),
  CONSTRAINT DOCTORS_SPECIAL_FK FOREIGN KEY (doctor_id) REFERENCES DOCTORS (id) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
