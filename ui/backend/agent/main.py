import json
from pathlib import Path

# from graph_state_dict import workflow
from .graph_state_dict import workflow
# from imports import langfuse_handler

DATA_DIR_PATH = (Path(__file__).resolve().parent.parent.parent.parent / "data").resolve()
EVALUATION_FILE_PATH = (Path(__file__).resolve().parent.parent.parent.parent / "data/exam_evaluation.json").resolve()


def evaluate():
    
    # graph = workflow.compile()
    with open(EVALUATION_FILE_PATH, 'r') as json_file:
        json_data = json.load(json_file)

    student_answer = """Random"""     # inputs that we'll be providing         
    relevant_theory = None            # inputs that we'll be providing          
    marking_scheme = None             # inputs that we'll be providing         
    total_score = None                # inputs that we'll be providing 
    question = None                   # inputs that we'll be providing
    sample_answer = None              # inputs that we'll be providing        
    student_answer_chunks = None      # outputs that we'll produce                   
    student_marks_chunkwise = None    # outputs that we'll produce                     
    total_score_gained = None         # outputs that we'll produce                
    teacher_reasoning = None          # outputs that we'll produce   

    
    """
    {
        "subject": "computer science",
        "number-of-questions": ,
        "questions-schema" : [
            {
                "question": str,
                "question": str: 
                "schema": List[Tuple(str, int/float)]
                "relevant-theory": str
            }
    }
    """

    num_questions = json_data['number-of-questions']
    course_name = json_data['subject']
    final_output_list = []
    for i in range(num_questions) : 
        question = json_data['questions-schema'][i]['question']    
        schema = json_data['questions-schema'][i]['schema']    
        relevant_theory = json_data['questions-schema'][i]['relevant-theory']
        total_score = json_data['questions-schema'][i]['total-score'] 
        sample_answer = """sample answer"""  
        student_answer = json_data['questions-schema'][i]['student-answer']     
        graph = workflow.compile()


        inputs_to_graph = {
            "marking_scheme" : schema,
            "question" : question,
            "total_score" : total_score,
            "relevant_theory" : relevant_theory,
            "student_answer" : student_answer,
            "course_name" : course_name,
            
            "student_answer_chunks" : [],
            "sample_answer" : sample_answer,
            "student_marks_chunkwise" : [],
            "total_score_gained" : 0.0,
            "teacher_reasoning" : [],
        }
        result = graph.invoke(input = inputs_to_graph) # , config={"callbacks": [langfuse_handler],"run_name":"parent-graph"})
        dump_results = {
                            "question" : question,
                            "total_score_question" : result['total_score'],
                            "total_score_gained" : result['total_score_gained'],
                            "student_answer" : result['student_answer'],
                            "student_answer_chunks" : result['student_answer_chunks'],
                            "student_marks_chunkwise": result["student_marks_chunkwise"],
                            "marking_scheme" : result['marking_scheme'],
                            "teacher_reasoning" : result['teacher_reasoning']
                       }
        final_output_list.append(dump_results)

    final_dict = {
        "subject" : course_name,
        "number-of-questions":num_questions,
        "results":final_output_list,
    }        
    
    with open(f"{DATA_DIR_PATH}/{course_name}_output.json",'w') as fptr : 
        json.dump(final_dict, fptr)

            
    """
    {
        subject  : 
        total-questions : 
        results : [
            {                
                "marks-gained" : 
                "feedback" : 
            },
            {                
                "marks-gained" : 
                "feedback" : 
            },
            {                
                "marks-gained" : 
                "feedback" : 
            },
        ]
  
        
    }
    """
                     

if __name__=="__main__":
    evaluate()






# Reuqired Inputs : 
# # 
# course_name
# student_answer
# relevant_theory
# marking_scheme
# total_score





# dict : 
#student_marks_chunkwise : key 
#total_score_gained : key 
#teacher_reasoning : key 
# Direct Json Dump 