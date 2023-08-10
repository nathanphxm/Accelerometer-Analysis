#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

time_t get_timestamp(FILE *file, time_t *file_timestamp) {
    char line[256];
    while (fgets(line, sizeof(line), file)) {
        int x, y, z;
        double lat, lon;
        int month, day, year, hour, minute, second;

        if (line[0] == '*') {
            sscanf(line, "*%ld", file_timestamp);
        } else if (sscanf(line, "%d,%d,%d,%lf,%lf,%d,%d,%d,%d,%d,%d", &x, &y, &z, &lat, &lon, &day, &month, &year, &hour, &minute, &second) == 11) {
            struct tm timeinfo = {0};
            timeinfo.tm_year = year - 1900;
            timeinfo.tm_mon = month - 1;
            timeinfo.tm_mday = day;
            timeinfo.tm_hour = hour;
            timeinfo.tm_min = minute;
            timeinfo.tm_sec = second;

            time_t timestamp = mktime(&timeinfo);
            if (timestamp == -1) {
                fprintf(stderr, "Error converting date and time to timestamp\n");
                return -1;
            }
            return timestamp;
        }
    }
    return -1; // Return -1 if no GPS data found
}

void update_timestamps(const char *filename, time_t gps_timestamp, time_t file_timestamp) {
    FILE *input_file = fopen(filename, "r");
    if (input_file == NULL) {
        perror("Error opening input file");
        return;
    }

    char output_filename[256];
    char gps_filename[256];
    char *dot = strrchr(filename, '.');
    if (dot) {
        snprintf(output_filename, dot - filename + 1, "%s", filename);
        strcat(output_filename, "_clean");
        strcat(output_filename, dot);

        snprintf(gps_filename, dot - filename + 1, "%s", filename);
        strcat(gps_filename, "_gps");
        strcat(gps_filename, dot);
    } else {
        snprintf(output_filename, sizeof(output_filename), "%s_clean", filename);
        snprintf(gps_filename, sizeof(gps_filename), "%s_gps", filename);
    }

    FILE *output_file = fopen(output_filename, "w");
    FILE *gps_file = fopen(gps_filename, "w");
    if (output_file == NULL || gps_file == NULL) {
        perror("Error opening output file");
        fclose(input_file);
        return;
    }

    char line[256];
    time_t timestamp_diff = gps_timestamp - file_timestamp;
    time_t current_timestamp = 0;
    while (fgets(line, sizeof(line), input_file)) {
        if (line[0] == '*') {
            time_t original_timestamp;
            sscanf(line, "*%ld", &original_timestamp);
            current_timestamp = original_timestamp + timestamp_diff;
            fprintf(output_file, "*%ld\n", current_timestamp);
        } else {
            int x, y, z;
            double lat, lon;
            int day, month, year, hour, minute, second;
            if (sscanf(line, "%d,%d,%d,%lf,%lf,%d,%d,%d,%d,%d,%d", &x, &y, &z, &lat, &lon, &day, &month, &year, &hour, &minute, &second) == 11) {
                // Write GPS data to gps_file
                fprintf(gps_file, "%ld,%lf,%lf\n", current_timestamp, lat, lon);
            } else if (sscanf(line, "%d,%d,%d", &x, &y, &z) == 3 && (x != 0 || y != 0 || z != 0)) {
                fprintf(output_file, "%d,%d,%d\n", x, y, z);
            }
        }
    }

    fclose(input_file);
    fclose(output_file);
    fclose(gps_file);
    printf("Updated file written to %s\n", output_filename);
    printf("GPS data written to %s\n", gps_filename);
}


int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return EXIT_FAILURE;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL) {
        perror("Error opening file");
        return EXIT_FAILURE;
    }

    time_t file_timestamp = 0;
    time_t gps_timestamp = get_timestamp(file, &file_timestamp);
    fclose(file);

    if (gps_timestamp != -1) {
        update_timestamps(argv[1], gps_timestamp, file_timestamp);
    } else {
        printf("No GPS data found in the file.\n");
    }

    return EXIT_SUCCESS;
}
