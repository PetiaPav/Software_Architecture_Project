-- Clinics
INSERT INTO CLINICS (id, physical_address, name, start_time, end_time) VALUES (1, '111 Sherbrooke W.', 'Uber Hospital', 8, 20);

-- UBER_CLINICS
INSERT INTO UBER_CLINICS (id, physical_address, name, start_time, end_time) VALUES (1, '222 Maisonneuve Blvd. W.', 'Uber Children Hospital', '08:00', '20:00');
INSERT INTO UBER_CLINICS (id, physical_address, name, start_time, end_time) VALUES (2, '243 St-Catherine W.', 'Uber Hospital', '08:00', '20:00');
INSERT INTO UBER_CLINICS (id, physical_address, name, start_time, end_time) VALUES (3, '225 Rene-Levesque Blvd. W.', 'Uber Sante Hospital', '08:00', '20:00');

-- USERS (All passwords qwe123456)
INSERT INTO USERS (id, first_name, last_name, password) VALUES (1, 'Benny', 'Bombs', '$5$rounds=535000$9Hn.TKXfmLsr4Riy$IjnYzjlHIfBq4o7kL4kGGxROnTtlttfJ4WLVCqHvydB');
INSERT INTO USERS (id, first_name, last_name, password) VALUES (2, 'Michael', 'Henderson', '$5$rounds=535000$9Hn.TKXfmLsr4Riy$IjnYzjlHIfBq4o7kL4kGGxROnTtlttfJ4WLVCqHvydB');
INSERT INTO USERS (id, first_name, last_name, password) VALUES (3, 'John', 'Doe', '$5$rounds=535000$9Hn.TKXfmLsr4Riy$IjnYzjlHIfBq4o7kL4kGGxROnTtlttfJ4WLVCqHvydB');
INSERT INTO USERS (id, first_name, last_name, password) VALUES (4, 'Jane', 'Jameson', '$5$rounds=535000$9Hn.TKXfmLsr4Riy$IjnYzjlHIfBq4o7kL4kGGxROnTtlttfJ4WLVCqHvydB');
INSERT INTO USERS (id, first_name, last_name, password) VALUES (5, 'John', 'Doe', '$5$rounds=535000$9Hn.TKXfmLsr4Riy$IjnYzjlHIfBq4o7kL4kGGxROnTtlttfJ4WLVCqHvydB');
INSERT INTO USERS (id, first_name, last_name, password) VALUES (6, 'Jane', 'Jameson', '$5$rounds=535000$9Hn.TKXfmLsr4Riy$IjnYzjlHIfBq4o7kL4kGGxROnTtlttfJ4WLVCqHvydB');
INSERT INTO USERS (id, first_name, last_name, password) VALUES (7, 'Amanda', 'Nunes', '$5$rounds=535000$9Hn.TKXfmLsr4Riy$IjnYzjlHIfBq4o7kL4kGGxROnTtlttfJ4WLVCqHvydB');
INSERT INTO USERS (id, first_name, last_name, password) VALUES (8, 'Peter', 'Parker', '$5$rounds=535000$9Hn.TKXfmLsr4Riy$IjnYzjlHIfBq4o7kL4kGGxROnTtlttfJ4WLVCqHvydB');

-- Patients
INSERT INTO PATIENTS (id, user_fk, email, health_card, phone_number, birthday, gender, physical_address) VALUES (1, 1, 'benny@gmail.com', 'BBOM 5424 5242', '(514)723-3635', '1985-04-01', 'M', '123 jogno drive');
INSERT INTO PATIENTS (id, user_fk, email, health_card, phone_number, birthday, gender, physical_address) VALUES (2, 2, 'michael@gmail.com', 'MGGN 5444 1234', '(514)555-1234', '1997-03-01', 'M', '1211 1st Avenue');

-- Doctors
INSERT INTO DOCTORS (id, user_fk, permit_number, specialty, city) VALUES (1, 3, 265345, 'Family Doctor', 'Montreal');
INSERT INTO DOCTORS (id, user_fk, permit_number, specialty, city) VALUES (2, 4, 555666, 'Eyes', 'Laval');

-- Doctor_Clinic_Assignment
INSERT INTO DOCTOR_CLINIC_ASSIGNMENT (id, clinic_id, doctor_id) VALUES (1, 1, 1);
INSERT INTO DOCTOR_CLINIC_ASSIGNMENT (id, clinic_id, doctor_id) VALUES (2, 1, 2);

-- Doctor Availability
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (1, 1, 1, 27, 1);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (2, 1, 1, 28, 1);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (3, 1, 1, 29, 1);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (4, 1, 1, 45, 0);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (5, 1, 1, 46, 0);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (6, 1, 1, 47, 0);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (7, 1, 3, 27, 0);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (8, 1, 3, 28, 0);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (9, 1, 3, 29, 0);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (10, 1, 3, 45, 1);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (11, 1, 3, 46, 1);
INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (12, 1, 3, 47, 1);

-- Nurses
INSERT INTO NURSES (id, user_fk, access_id) VALUES (1, 7, 'ABC12345');
INSERT INTO NURSES (id, user_fk, access_id) VALUES (2, 8, 'RET66777');

-- ROOMS
INSERT INTO ROOMS (id, name, clinic_id) VALUES (1, '303', 1);
INSERT INTO ROOMS (id, name, clinic_id) VALUES (2, '305', 1);
INSERT INTO ROOMS (id, name, clinic_id) VALUES (3, '306', 1);
INSERT INTO ROOMS (id, name, clinic_id) VALUES (4, '101', 2);
INSERT INTO ROOMS (id, name, clinic_id) VALUES (5, '102', 2);
INSERT INTO ROOMS (id, name, clinic_id) VALUES (6, '560', 3);

-- DOCTOR_GENERIC_AVAILABILITIES
INSERT INTO DOCTOR_GENERIC_AVAILABILITIES (id, doctor_id, date_time, walk_in) VALUES (1, 1, '2019-12-31 12:00:00', 0);
INSERT INTO DOCTOR_GENERIC_AVAILABILITIES (id, doctor_id, date_time, walk_in) VALUES (2, 1, '2019-11-31 13:00:00', 1);

-- DOCTOR_ADJUSTMENTS
INSERT INTO DOCTOR_ADJUSTMENTS (id, doctor_id, date_time, opp_type_add, walk_in) VALUES (1, 1, '2019-12-31 14:00:00', 1, 1);
INSERT INTO DOCTOR_ADJUSTMENTS (id, doctor_id, date_time, opp_type_add, walk_in) VALUES (2, 2, '2019-11-31 15:00:00', 2, 0);
INSERT INTO DOCTOR_ADJUSTMENTS (id, doctor_id, date_time, opp_type_add, walk_in) VALUES (3, 2, '2019-11-22 16:00:00', 1, 0);

-- APPOINTMENTS
INSERT INTO APPOINTMENTS (id, clinic_id, room_id, doctor_id, patient_id, date_time, walk_in) VALUES (1, 1, 1, 1, 1, '2019-11-22 10:00:00', 0);
INSERT INTO APPOINTMENTS (id, clinic_id, room_id, doctor_id, patient_id, date_time, walk_in) VALUES (2, 2, 2, 2, 2, '2019-10-11 08:00:00', 1);
INSERT INTO APPOINTMENTS (id, clinic_id, room_id, doctor_id, patient_id, date_time, walk_in) VALUES (3, 3, 1, 3, 1, '2019-05-24 17:00:00', 0);
