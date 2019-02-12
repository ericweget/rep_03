import json
from flask import Flask, request, Response
from flask import render_template, flash, redirect
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

import sys
sys.path.append('/home/evaclickfsm/classes')

import hrqclasses
import dbclasses
import fsmclasses

@app.route('/')
@app.route('/index')
def index():

    sql = dbclasses.SQLighter()
    fsm = fsmclasses.HrqFsm()
    fsm.setStateLogTable(sql)

    return redirect('http://evaclickfsm.pythonanywhere.com/goto_state?event_code=v_00')

@app.route('/goto_state', methods=['GET', 'POST'])
def goto_state():

    event_code = request.args.get('event_code')
    sql = dbclasses.SQLighter()
    fsm = fsmclasses.HrqFsm()

    state_current = fsm.getCurrentState(sql)
    state_next = fsm.getNextState(sql, state_current, event_code)

#return 'event_code[' + event_code + '] state_current:[' + state_current + '] state_next:[' + state_next + ']';

#s_000_v__init_state
    if state_next == 's_000_v__init_state':
        return render_template('/s_000_v__init_state.html', title='s_000_v__init_state')

#s_010_v__promt_need_instruction
    if state_next == 's_010_v__promt_need_instruction':
        return render_template('/s_010_v__promt_need_instruction.html', title='s_010_v__promt_need_instruction')

#s_030_v__instruction
    if state_next == 's_030_v__instruction':
        return render_template('/s_030_v__instruction.html', title='Instrs_030_v__instructionuction')

#s_040_v__agreement
    if state_next == 's_040_v__agreement':
        return render_template('/s_040_v__agreement.html', title='s_040_v__agreement')

#s_050__start_questionnaire
    if state_next == 's_050__start_questionnaire':
        sql = dbclasses.SQLighter()
        sql.create_table('answer_01')

        return redirect('http://evaclickfsm.pythonanywhere.com/goto_state?event_code=v_10&question_code=Q_00')

#s_060_v__questions
    if state_next == 's_060_v__questions':
        full_name = '/home/evaclickfsm/data/hrq.json'
        hrq = hrqclasses.HrqDataFromFile(json, full_name)
        hrq_data = hrq.getAll()
        question_code = request.args.get('question_code')
        if 'current_question_code' in request.form :
            question_code = request.form['current_question_code']
            if 'answer_code' not in request.form :
                next_question_code = question_code

                return render_template('s_060_v__questions.html', title='s_060_v__questions', hrq_data = hrq_data, question_code = next_question_code, error = 'no answer selected')
            if 'answer_code' in request.form :
                answer_code = request.form['answer_code']
                sql = dbclasses.SQLighter()
                query = "INSERT INTO `answer_01` (`ANSW_QUESTION_CODE`, `ANSW_ANSWER_CODE`) VALUES ('" + question_code + "', '" + answer_code + "')"
                sql.insert(query)

        next_question_code = hrq.getNextQuestionCode(question_code)

        if next_question_code == 'Q_LAST_ONE':

            return redirect('/goto_state?event_code=v_20')

        return render_template('s_060_v__questions.html', title='s_060_v__questions', hrq_data = hrq_data, question_code = next_question_code, error = '')

#s_070_v__show_result
    if state_next == 's_070_v__show_result':
        full_name = '/home/evaclickfsm/data/hrq.json'
        hrq = hrqclasses.HrqDataFromFile(json, full_name)
        hrq_data = hrq.getAll()

        sql = dbclasses.SQLighter()

        question_all = 0
        question_with_correct_answer = 0
        for question_code in hrq_data:
            if question_code != 'Q_00':
                question_all += 1
                row = sql.getByQuestionCode(question_code)
                answer_code = row[2]
                if hrq_data[question_code]['answers'][answer_code]['is_right'] == 'true':
                    question_with_correct_answer += 1

        percentage_of_correct_answers = (question_with_correct_answer/question_all)*100

        return render_template('s_070_v__show_result.html', title='s_070_v__show_result', percentage_of_correct_answers = percentage_of_correct_answers)

#s_800_v__quit_questionnaire
    if state_next == 's_800_v__quit_questionnaire':
        return render_template('/s_800_v__quit_questionnaire.html', title='s_800_v__quit_questionnaire')






    return 'Error: unknown state_new:[' + state_next + ']'

