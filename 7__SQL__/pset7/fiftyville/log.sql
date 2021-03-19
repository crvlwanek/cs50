-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Initial look at the crime scene report
SELECT * FROM crime_scene_reports WHERE year = 2020 AND month = 7 AND day = 28 AND street LIKE "%Chamberlin%";
-- Description: Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted 
-- today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.

-- Search for crime scene interviews
SELECT * FROM interviews WHERE year = 2020 AND month = 7 AND day = 28;
-- Ruth: Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive 
-- away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
SELECT * FROM courthouse_security_logs WHERE year = 2020 AND month = 7 AND day = 28;
-- Licence plates: 4328GD8, 5P2BI95, 6P58WS2, G412CB7
SELECT * FROM people WHERE license_plate = "G412CB7";
-- **Danielle | (389) 555-5198 | 8496433585 | 4328GD8
-- Patrick | (725) 555-4692 | 2963008352 | 5P2BI95
-- Amber | (301) 555-4174 | 7526138472 | 6P58WS2
-- Roger | (130) 555-0289 | 1695452385 | G412CB7

-- Eugene: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by 
-- the ATM on Fifer Street and saw the thief there withdrawing some money.
SELECT * FROM atm_transactions WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = "Fifer Street";
-- Bank accounts: 28500762, 28296815, 76054385, 49610011, 16153065, 25506511, 81061156, 26013199
SELECT * FROM bank_accounts JOIN people ON bank_accounts.person_id = people.id WHERE account_number = 25506511;
-- **Danielle | (389) 555-5198 | 8496433585 | 4328GD8
-- Bobby | (826) 555-1652 | 9878712108 | 30G67EN
-- *Madison | (286) 555-6063 | 1988161715 | 1106N58
-- **Ernest | (367) 555-5533 | 5773159633 | 94KL13X
-- Roy | (122) 555-4581 | 4408372428 | QX4YZN3
-- **Elizabeth | (829) 555-5269 | 7049073643 | L93JTIZ
-- Victoria | (338) 555-6650 | 9586786673 | 8X428L0
-- Russell | (770) 555-1861 | 3592750733 | 322W7JE

-- Raymond: As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say 
-- that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to 
-- purchase the flight ticket.
SELECT * FROM flights JOIN airports ON flights.origin_airport_id = airports.id WHERE year = 2020 AND month = 7 AND day = 29;
SELECT * FROM flights JOIN airports ON flights.destination_airport_id = airports.id WHERE year = 2020 AND month = 7 AND day = 29;
-- Earliest flight goes to Heathrow Airport in London
SELECT * FROM passengers JOIN people ON passengers.passport_number = people.passport_number WHERE flight_id = 36;
-- Find the phone call to know who the accomplice is
SELECT * FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND caller = "(389) 555-5198" OR receiver = "(389) 555-5198";
SELECT * FROM people WHERE phone_number = "(609) 555-5876";
SELECT * FROM phone_calls WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60;
SELECT hour, minute, activity, name FROM courthouse_security_logs JOIN people ON courthouse_security_logs.license_plate = people.license_plate 
WHERE year = 2020 AND month = 7 AND day = 28;
SELECT receiver, duration, name FROM phone_calls JOIN people 
ON phone_calls.caller = people.phone_number WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60;
-- 45 seconds Ernest
SELECT caller, duration, name FROM phone_calls JOIN people 
ON phone_calls.receiver = people.phone_number WHERE year = 2020 AND month = 7 AND day = 28 AND duration <= 60;
-- Berthold