#!/usr/bin/env python3

"""
Quiz creator with random ordered quistions and answers.
Save in files with .txt extension
"""

import random
import os

capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau',
            'Arizona': 'Phoenix', 'Arkansas': 'Little Rock',
            'California': 'Sacramento', 'Colorado': 'Denver',
            'Connecticut': 'Hartford', 'Delaware': 'Dover',
            'Florida': 'Tallahassee', 'Georgia': 'Atlanta',
            'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois': 'Springfield',
            'Indiana': 'Indianapolis', 'Iowa': 'Des Moines',
            'Kansas': 'Topeka', 'Kentucky': 'Frankfort',
            'Louisiana': 'Baton Rouge', 'Maine': 'Augusta',
            'Maryland': 'Annapolis', 'Massachusetts': 'Boston',
            'Michigan': 'Lansing', 'Minnesota': 'Saint Paul',
            'Mississippi': 'Jackson', 'Missouri': 'Jefferson City',
            'Montana': 'Helena', 'Nebraska': 'Lincoln',
            'Nevada': 'Carson City', 'New Hampshire': 'Concord',
            'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe',
            'New York': 'Albany', 'North Carolina': 'Raleigh',
            'North Dakota': 'Bismarck', 'Ohio': 'Columbus',
            'Oklahoma': 'Oklahoma City', 'Oregon': 'Salem',
            'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence',
            'South Carolina': 'Columbia', 'South Dakota': 'Pierre',
            'Tennessee': 'Nashville', 'Texas': 'Austin',
            'Utah': 'Salt Lake City', 'Vermont': 'Montpelier',
            'Virginia': 'Richmond', 'Washington': 'Olympia',
            'West Virginia': 'Charleston', 'Wisconsin': 'Madison',
            'Wyoming': 'Cheyenne'}

quizDir = os.path.join(os.getcwd(), "quiz_folder")


def randStates(d):
    states = list(d.keys())
    random.shuffle(states)
    return states


def openStreams(num, qDir):
    quiz = open(os.path.join(qDir, "quiz_{:d}.txt".format(num)), 'w')
    answer = open(os.path.join(qDir, "answer_{:d}.txt".format(num)), 'w')
    return quiz, answer


def randAnswers(states, num):
    correct = capitals[states[num]]
    wrong = list(capitals.values())
    wrong.remove(correct)
    options = random.sample(wrong, 3) + [correct]
    random.shuffle(options)
    return correct, options


def Q_A_fill(qFile, aFile, qNum, states):
    correct, option = randAnswers(states, qNum)

    qFile.write("\t{}. Capital of {}\n".format(qNum + 1, states[qNum]))
    for i in range(4):
        qFile.write("\t\t\t{}.{}\n".format("ABCD"[i], option[i]))
    qFile.write('\n')

    aFile.write("\t{}. {}\n".format(qNum + 1, correct))


def fillFiles(num, qDir):
    quizFile, answerFile = openStreams(num, qDir)
    quizFile.write("\n" + (" " * 20) + "Quiz #{:d}\n\n".format(num))
    answerFile.write("\n" + (" " * 20) + "Answers for quiz #{:d}\n\n".
                     format(num))
    states = randStates(capitals)

    for qNum in range(len(capitals.keys())):
        Q_A_fill(quizFile, answerFile, qNum, states)

    quizFile.close()
    answerFile.close()


def createFiles(amount, qDir):
    for quizNum in range(amount):
        fillFiles(quizNum + 1, qDir)


if __name__ == "__main__":
    createFiles(3, quizDir)
