#ifndef __KTRAINING_H
#define __KTRAINING_H

#include <Arduino.h>

enum {open, ongoing, done, skipped};

struct kParam {
  char param[2];
  uint16_t value;
};

struct kExercise {
  char name[4];
  uint16_t weight;
  struct kParam params[4];
  uint8_t status;
  uint8_t reps;
};

struct kTraining {
  struct kExercise exercises[12];
  uint8_t currentExercise;
};

#endif

/*
struct student_college_detail
{
    int college_id;
    char college_name[50];
};

struct student_detail
{
    int id;
    char name[20];
    float percentage;
    // structure within structure
    struct student_college_detail clg_data;
}stu_data;
// */
