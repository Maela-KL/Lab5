#Import the important libraries

from machine import Pin, I2C
import time

#Setup I2C for the DS3231 Real Time Clock
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
rtc_address = 0x68  # DS3231 address

#Function to convert BCD (RTC format) to normal numbers
def bcd_to_int(b):
    return (b >> 4) * 10 + (b & 0x0F)

# --- Function to read hours, minutes, and seconds from RTC ---
def read_rtc_time(): #reads time from the RTC and returns hours, minutes, seconds
    data = i2c.readfrom_mem(rtc_address, 0x00, 3)
    seconds = bcd_to_int(data[0])
    minutes = bcd_to_int(data[1])
    hours = bcd_to_int(data[2] & 0x3F)  # mask 24-hour mode bits
    return hours, minutes, seconds

# --- Function to convert hours/minutes/seconds into total seconds ---
def total_seconds():
    hours, minutes, seconds = read_rtc_time()
    return hours * 3600 + minutes * 60 + seconds

# --- Main Game Loop ---
print("Welcome to the 15-Second Timing Game!")
print("When ready, press ENTER to start.")
print("Then press ENTER again after you think 15 seconds have passed.\n")

try:
    while True:
        input("Press ENTER to start...")
        start = total_seconds()
        print("Timer started! Count 15 seconds in your head...")

        input("Press ENTER again when you think 15 seconds have passed.")
        end = total_seconds()

        # If the time wrapped around midnight
        if end < start:
            end += 24 * 3600

        elapsed = end - start
        print("You counted:", elapsed, "seconds.")

        # Save result to log file
        log = open("log.txt", "a")
        log.write(str(elapsed) + "\n")
        log.flush()  # make sure data is saved

        print("Result saved to log.txt.\n")

except KeyboardInterrupt:
    print("\nProgram stopped early.")

finally:
    log.close()
    print("Log file closed. Goodbye!")